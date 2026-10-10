#!/usr/bin/env python3
"""Static governance checks for portfolio hierarchy, evidence links, and design rules."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    required_docs = ["docs/design-governance.md", "docs/content-taxonomy.md"]
    for path in required_docs:
        if not (ROOT / path).is_file():
            errors.append(f"missing governance document: {path}")

    readme = read("README.md")
    for path in required_docs:
        if path not in readme:
            errors.append(f"README must link {path}")

    top_level_templates = [
        "layouts/about/single.html",
        "layouts/outputs/list.html",
        "layouts/experience/list.html",
        "layouts/engagement/list.html",
        "layouts/contact/list.html",
    ]
    for path in top_level_templates:
        text = read(path)
        if 'class="back-link' in text or "Portfolio home" in text:
            errors.append(f"primary destination must rely on persistent header, not home back-link: {path}")

    default_single = read("layouts/_default/single.html")
    for marker in ("$isPrimaryDestination", 'slice "/research/"', "if not $isPrimaryDestination"):
        if marker not in default_single:
            errors.append(f"Research primary-destination back-link guard missing marker {marker!r}")

    project_single = read("layouts/project/single.html")
    for marker in ('"/experience/"', '"/outputs/"', '"/research/"', '"Research Software"'):
        if marker not in project_single:
            errors.append(f"contextual project parent rule missing {marker!r}")
    for forbidden in ('"/#experience"', '"/#research"'):
        if forbidden in project_single:
            errors.append(f"project detail pages must not back-link to homepage sections: {forbidden}")

    portfolio = yaml.safe_load(read("data/portfolio.yaml"))
    research = portfolio.get("research", [])
    if not research:
        errors.append("portfolio research program is empty")
    else:
        top_tags = research[0].get("tags", [])
        if "Computer vision" not in top_tags:
            errors.append("high-level measurement program must use method term 'Computer vision'")
        if "OpenCV" in top_tags:
            errors.append("high-level measurement program must not expose implementation-specific OpenCV tag")

    series = portfolio.get("presentation_series", [])
    presentations = portfolio.get("presentations", [])
    ids = [str(item.get("id", "")).strip() for item in series]
    if not ids or any(not value for value in ids):
        errors.append("every presentation series needs a stable explicit id")
    if len(ids) != len(set(ids)):
        errors.append("presentation-series ids must be unique")
    for value in ids:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
            errors.append(f"presentation-series id is not a stable slug: {value!r}")

    number_words = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
    }
    for item in series:
        titles = set(item.get("presentation_titles", []))
        if not titles:
            errors.append(f"presentation series {item.get('id')!r} lacks canonical presentation_titles")
            continue
        posters = [
            record for record in presentations
            if record.get("title") in titles and str(record.get("kind", "")).lower() == "poster"
        ]
        count = len(posters)
        word = number_words.get(count, str(count))
        summary = str(item.get("summary", ""))
        if not re.search(rf"\b{re.escape(word)}\b.*\bposter presentations\b", summary, flags=re.IGNORECASE):
            errors.append(
                f"presentation-series summary count is not synchronized for {item.get('id')!r}: "
                f"expected {word} poster presentations from canonical records"
            )

    research_content = read("content/research/index.md")
    if "/#presentations" in research_content:
        errors.append("Research must not use a generic homepage presentation anchor for specific evidence")
    for value in ids:
        expected = f"/engagement/#{value}"
        if expected not in research_content:
            errors.append(f"Research is missing exact engagement evidence link {expected}")

    for path in ("layouts/landing/list.html", "layouts/engagement/list.html"):
        text = read(path)
        if 'id="{{ .id }}"' not in text:
            errors.append(f"presentation-series template must emit stable ids: {path}")

    runtime = read("assets/js/site.js")
    for marker in ("openDeepLinkedDetails", "hashchange", "details.open = true"):
        if marker not in runtime:
            errors.append(f"deep-linked expandable evidence runtime missing {marker!r}")

    polish = read("static/css/final-polish.css")
    for marker in (
        ".trajectory-grid h3 + p",
        ".series:target",
        "@media(max-width:820px)",
        ".research-signature",
    ):
        if marker not in polish:
            errors.append(f"final polish layer missing governance style marker {marker!r}")

    base = read("layouts/_default/baseof.html")
    if "final-polish.css" not in base:
        errors.append("base template does not load final-polish.css")

    signature = read("layouts/partials/research_signature.html")
    for marker in (
        "Stimulus to translation research framework",
        "Schematic; no quantitative data are implied.",
        "research-signature__mobile",
    ):
        if marker not in signature:
            errors.append(f"research signature is missing integrity/accessibility marker {marker!r}")

    if errors:
        print("Design-governance audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Design-governance audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
