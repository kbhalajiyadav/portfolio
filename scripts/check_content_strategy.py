#!/usr/bin/env python3
"""Protect complementary content roles, tone, and derived proof metrics.

This check is intentionally semantic rather than pixel- or sentence-exact. It
keeps shared facts synchronized while preventing the homepage, About, Research,
Outputs, and CV from collapsing into repeated copies of the same narrative.
"""
from __future__ import annotations

from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]

HYPE_TERMS = (
    "groundbreaking",
    "cutting-edge",
    "world-class",
    "revolutionary",
    "game-changing",
    "best-in-class",
    "unparalleled",
)
INTERNAL_PROCESS_TERMS = (
    "evidence boundary",
    "canonical facts",
    "public-safe",
    "quarantine",
)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    _, front, body = text.split("---", 2)
    return yaml.safe_load(front) or {}, body.strip()


def norm(value: object) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"\[[^\]]+\]\([^\)]+\)", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def words(value: object) -> list[str]:
    return norm(value).split()


def sentences(value: object) -> list[str]:
    text = " ".join(str(value or "").split())
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(words(part)) >= 9]


def similarity(a: str, b: str) -> tuple[float, float]:
    na, nb = norm(a), norm(b)
    seq = SequenceMatcher(None, na, nb).ratio()
    sa, sb = set(na.split()), set(nb.split())
    jaccard = len(sa & sb) / len(sa | sb) if sa and sb else 0.0
    return seq, jaccard


def section_after_heading(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<section>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group("section").strip() if match else ""


def main() -> int:
    portfolio = load_yaml(ROOT / "data" / "portfolio.yaml")
    cv = load_yaml(ROOT / "data" / "cv.yaml")
    about, _ = parse_markdown(ROOT / "content" / "about.md")
    research, research_body = parse_markdown(ROOT / "content" / "research" / "index.md")
    outputs, outputs_body = parse_markdown(ROOT / "content" / "outputs" / "_index.md")
    home_proof = (ROOT / "layouts" / "partials" / "home_proof.html").read_text(encoding="utf-8")
    errors: list[str] = []

    profile = portfolio.get("profile", {})
    cv_profile = cv.get("profile", {})

    # Current identity is structured once, while the hero status remains a concise display string.
    for field in ("role", "program", "institution"):
        if not norm(profile.get(field)):
            errors.append(f"portfolio.profile.{field} is required for structured current identity")
    status = norm(profile.get("status"))
    for field in ("role", "program", "institution"):
        value = norm(profile.get(field))
        if value and value not in status:
            errors.append(f"profile.status must include structured {field}: {profile.get(field)!r}")

    current_education = (cv.get("education") or [{}])[0]
    if norm(profile.get("institution")) != norm(current_education.get("institution")):
        errors.append("current institution differs between portfolio identity and first CV education record")
    if norm(profile.get("program")) not in norm(current_education.get("degree")):
        errors.append("current program differs between portfolio identity and first CV education record")

    # Surface roles: concise orientation -> biography -> scientific argument -> evidence index -> exhaustive CV.
    home_summary = str(profile.get("summary", ""))
    about_bio_items = [str(item) for item in about.get("bio", [])]
    about_bio = " ".join(about_bio_items)
    cv_summary = str(cv_profile.get("summary", ""))
    research_focus = section_after_heading(research_body, "Research focus")
    outputs_summary = str(outputs.get("summary", ""))

    if not (18 <= len(words(home_summary)) <= 38):
        errors.append("homepage summary should remain a concise 18–38 word research proposition")
    if len(about_bio_items) != 2 or not (55 <= len(words(about_bio)) <= 150):
        errors.append("About biography should remain two complementary paragraphs totaling 55–150 words")
    if not (25 <= len(words(cv_summary)) <= 65):
        errors.append("CV summary should remain a compact 25–65 word technical summary")
    if not research_focus or len(words(research_focus)) > 110:
        errors.append("Research focus should exist and stay within 110 words before deeper sections")
    if len(words(outputs_summary)) > 32:
        errors.append("Outputs summary should stay evidence-oriented and at or below 32 words")
    if re.search(r"\b(?:I|my|me)\b", f"{outputs_summary} {outputs_body}", re.I):
        errors.append("Outputs should use objective record language rather than first-person biography")

    # Guard against copy-paste drift. Shared terminology is expected; near-identical sentences are not.
    surfaces = {
        "home": home_summary,
        "about": about_bio,
        "cv": cv_summary,
        "research": f"{research.get('summary', '')} {research_focus}",
        "outputs": f"{outputs_summary} {outputs_body}",
    }
    for (name_a, text_a), (name_b, text_b) in combinations(surfaces.items(), 2):
        seq, jaccard = similarity(text_a, text_b)
        if seq >= 0.82 and jaccard >= 0.72:
            errors.append(
                f"surface narratives are too similar ({name_a} vs {name_b}: sequence={seq:.2f}, token={jaccard:.2f})"
            )
        for sentence_a in sentences(text_a):
            for sentence_b in sentences(text_b):
                sseq, sj = similarity(sentence_a, sentence_b)
                if sseq >= 0.93 and sj >= 0.82:
                    errors.append(
                        f"near-duplicate public sentence across {name_a}/{name_b}: {sentence_a!r}"
                    )

    # Public tone remains evidence-led and avoids internal governance vocabulary.
    public_files = [
        ROOT / "content" / "about.md",
        ROOT / "content" / "research" / "index.md",
        ROOT / "content" / "outputs" / "_index.md",
    ]
    public_files.extend(sorted((ROOT / "content" / "project").glob("**/*.md")))
    public_files.extend(sorted((ROOT / "content" / "publication").glob("**/*.md")))
    public_text = "\n".join(path.read_text(encoding="utf-8") for path in public_files).casefold()
    for phrase in HYPE_TERMS:
        if phrase in public_text:
            errors.append(f"unsupported promotional language found in public content: {phrase!r}")
    for phrase in INTERNAL_PROCESS_TERMS:
        if phrase in public_text:
            errors.append(f"internal governance wording leaked into public content: {phrase!r}")

    # Distinct page jobs remain explicit.
    for heading in ("Research focus", "Measure response", "Resolve structure under stimuli", "Translate reproducibly", "Collaboration questions"):
        if f"## {heading}" not in research_body:
            errors.append(f"Research page missing role-defining section: {heading}")
    for phrase in ("peer-reviewed articles", "M.S. thesis", "citable research software", "patent-pending intellectual property"):
        if norm(phrase) not in norm(outputs_summary):
            errors.append(f"Outputs summary no longer names record class: {phrase}")
    if "newest first" not in outputs_body.casefold():
        errors.append("Outputs page must explain reverse-chronological ordering")

    # Shared high-stakes facts should appear where context requires them, not everywhere.
    ip = (cv.get("intellectual_property") or [{}])[0]
    about_serialized = (ROOT / "content" / "about.md").read_text(encoding="utf-8")
    for value, label in ((ip.get("title"), "IP title"), (ip.get("tech_id"), "VCU Tech ID")):
        if value and str(value) not in about_serialized:
            errors.append(f"About professional path is missing synchronized {label}: {value!r}")
        if value and str(value) not in research_body:
            errors.append(f"Research page is missing synchronized {label}: {value!r}")

    p_software = portfolio.get("software", {})
    cv_software = (cv.get("research_software") or [{}])[0]
    if norm(p_software.get("title")) != norm(cv_software.get("title")):
        errors.append("software title differs between portfolio and CV")

    # Homepage proof numbers must be derived from canonical collections, not presentation-layer magic values.
    guided_count = sum(int(item.get("project_count", 0) or 0) for item in portfolio.get("teaching", []))
    if guided_count <= 0:
        errors.append("student-project proof metric must derive from structured teaching.project_count values")
    if len(cv.get("research_software", [])) <= 0:
        errors.append("citable-software proof metric has no canonical CV software record")
    if "metrics" in portfolio:
        errors.append("legacy presentation metrics must not be manually duplicated in portfolio.yaml")
    for required in ("len $cv.research_software", ".project_count", "len $cv.intellectual_property"):
        if required not in home_proof:
            errors.append(f"home proof strip must derive metric using {required!r}")
    if re.search(r"<strong>\s*1\s*</strong>\s*<span>Citable software release", home_proof):
        errors.append("software proof count is hard-coded in presentation markup")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(
        "Content strategy guardrail passed: complementary page roles, restrained tone, "
        f"structured current identity, and derived proof metrics ({guided_count} guided projects)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
