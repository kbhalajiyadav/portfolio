#!/usr/bin/env python3
"""Build the public academic CV and compact industry resume from data/cv.yaml."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "cv.yaml"
CV_TEMPLATE = ROOT / "cv" / "template.tex"
RESUME_TEMPLATE = ROOT / "cv" / "resume_template.tex"
CV_TEX = ROOT / "cv" / "generated" / "bhalaji_cv.tex"
RESUME_TEX = ROOT / "cv" / "generated" / "bhalaji_resume.tex"
CV_PDF = ROOT / "static" / "uploads" / "cv.pdf"
RESUME_PDF = ROOT / "static" / "uploads" / "resume.pdf"


LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def esc(value: object) -> str:
    text = str(value)
    return "".join(LATEX_REPLACEMENTS.get(char, char) for char in text)


def href(url: str, label: str) -> str:
    safe_url = (
        url.replace("\\", "/")
        .replace("%", r"\%")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("&", r"\&")
    )
    return rf"\cvlink{{{safe_url}}}{{{esc(label)}}}"


def bullets(items: list[str]) -> str:
    if not items:
        return ""
    body = "\n".join(rf"  \item {esc(item)}" for item in items)
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}\n"


def honors_bullets(items: list[object]) -> str:
    """Render compact honor and credential entries with optional verified links."""
    if not items:
        return ""

    rendered: list[str] = []
    for item in items:
        if isinstance(item, str):
            rendered.append(esc(item))
            continue

        label = str(item.get("label", "")).strip()
        url = str(item.get("url", "")).strip()
        links = item.get("links", [])
        details = str(item.get("details", "")).strip()

        if links:
            linked_labels = r" \contactsep ".join(
                href(str(link["url"]), str(link["label"])) for link in links
            )
            text = f"{esc(label)}: {linked_labels}" if label else linked_labels
        elif url:
            text = href(url, label)
        else:
            text = esc(label)

        if details:
            text += f", {esc(details)}"
        rendered.append(text)

    body = "\n".join(rf"  \item {item}" for item in rendered)
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}\n"


def section(title: str, content: list[str]) -> str:
    return rf"\section{{{esc(title)}}}" + "\n" + "\n".join(content) + "\n"


def render_education(data: dict) -> str:
    education: list[str] = []
    for item in data["education"]:
        education.append(
            rf"\entry{{{esc(item['degree'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(item['institution'])}}}{{{esc(item['location'])}}}"
        )
        education.append(bullets(item.get("details", [])))
    return section("Education", education)


def render_research_experience(data: dict, compact: bool = False) -> str:
    research: list[str] = []
    for item in data["research_experience"]:
        subtitle = item["organization"]
        if item.get("advisor"):
            subtitle += f" | Advisor: {item['advisor']}"
        research.append(
            rf"\entry{{{esc(item['role'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(subtitle)}}}{{{esc(item['location'])}}}"
        )
        item_bullets = item.get("bullets", [])
        if compact and len(item_bullets) > 3:
            item_bullets = item_bullets[:3]
        research.append(bullets(item_bullets))
    return section("Research and Teaching Experience", research)


def render_publications(data: dict, title: str = "Peer-Reviewed Publications") -> str:
    pubs = [
        "\\begin{enumerate}\n"
        + "\n".join(rf"  \item {esc(item)}" for item in data["publications"])
        + "\n\\end{enumerate}"
    ]
    return section(title, pubs)


def render_intellectual_property(data: dict) -> str:
    intellectual_property: list[str] = []
    for item in data.get("intellectual_property", []):
        intellectual_property.append(
            rf"\smallentry{{{esc(item['title'])}}}"
            rf"{{{esc(item['status'])} · {esc(item['year'])}}}"
            rf"{{{esc(item['inventors'])}}}"
        )
        intellectual_property.append(
            r"{\small "
            + esc(item["description"])
            + " "
            + esc(item["organization"])
            + r" \contactsep "
            + esc(f"VCU Tech # {item['tech_id']}")
            + "}"
        )
    return section("Intellectual Property", intellectual_property) if intellectual_property else ""


def render_software(data: dict) -> str:
    software: list[str] = []
    for item in data["research_software"]:
        software.append(
            rf"\smallentry{{{esc(item['title'])}}}{{{esc(item['version'])}}}"
            rf"{{{esc(item['authors'])}}}"
        )
        software.append(
            rf"{{\small {esc(item['description'])} "
            + href(item["repository"], "Repository")
            + r" \contactsep "
            + href(item["archive"], "Archived release")
            + "}"
        )
    return section("Research Software", software)


def render_presentations(data: dict) -> str:
    presentations = [
        "\\begin{enumerate}\n"
        + "\n".join(
            rf"  \item \dateditem{{\textbf{{{esc(item['type'])}.}} "
            rf"{esc(item['citation'])}}}{{{esc(item['date'])}}}"
            for item in data["presentations"]
        )
        + "\n\\end{enumerate}"
    ]
    return section("Presentations, Seminar, and Defense", presentations)


def render_engagement(data: dict) -> str:
    engagement: list[str] = []
    for item in data["engagement"]:
        engagement.append(
            rf"\smallentry{{{esc(item['role'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(item['organization'])}}}"
        )
    return section("Teaching, Review, and Applied Innovation", engagement)


def render_industry(data: dict, compact: bool = False) -> str:
    industry: list[str] = []
    for item in data["industry_experience"]:
        industry.append(
            rf"\entry{{{esc(item['role'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(item['organization'])}}}{{{esc(item['location'])}}}"
        )
        item_bullets = item.get("bullets", [])
        if compact and len(item_bullets) > 3:
            item_bullets = item_bullets[:3]
        industry.append(bullets(item_bullets))
    return section("Industry Experience", industry)


def render_honors(data: dict) -> str:
    return section("Honors and Professional Development", [honors_bullets(data["honors_development"])])


def render_skills(data: dict) -> str:
    skills = []
    for index, item in enumerate(data["technical_skills"]):
        suffix = r"\\[2pt]" if index < len(data["technical_skills"]) - 1 else ""
        skills.append(
            rf"\textbf{{{esc(item['category'])}:}} {esc(item['items'])}{suffix}"
        )
    return section("Technical Skills", [r"{\small " + "\n".join(skills) + "}"])


def render_cv(data: dict) -> str:
    p = data["profile"]
    output = [
        section("Research Profile", [rf"\color{{Ink}} {esc(p['summary'])}\color{{black}}"]),
        render_education(data),
        render_research_experience(data),
        render_publications(data),
        render_intellectual_property(data),
        render_software(data),
        render_presentations(data),
        render_engagement(data),
        render_industry(data),
        render_honors(data),
        render_skills(data),
    ]
    return "\n".join(part for part in output if part)


def render_resume(data: dict) -> str:
    p = data["profile"]
    output = [
        section("Profile", [rf"\color{{Ink}} {esc(p['summary'])}\color{{black}}"]),
        render_education(data),
        render_research_experience(data, compact=True),
        render_industry(data, compact=True),
        render_publications(data, title="Selected Peer-Reviewed Publications"),
        render_intellectual_property(data),
        render_software(data),
        render_honors(data),
        render_skills(data),
    ]
    return "\n".join(part for part in output if part)


def compile_pdf(tex_path: Path, pdf_path: Path) -> None:
    if not shutil.which("latexmk"):
        raise RuntimeError("latexmk is required to compile the CV")
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1735689600")
    subprocess.run(
        [
            "latexmk",
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={tex_path.parent}",
            str(tex_path),
        ],
        check=True,
        cwd=ROOT,
        env=env,
    )
    built_pdf = tex_path.with_suffix(".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(built_pdf, pdf_path)
    for suffix in (".aux", ".fdb_latexmk", ".fls", ".log", ".out", ".pdf", ".xdv"):
        artifact = tex_path.with_suffix(suffix)
        if artifact.exists():
            artifact.unlink()


def render_template(data: dict, template_path: Path, body: str) -> str:
    template = template_path.read_text(encoding="utf-8")
    profile = data["profile"]
    updated = str(profile["updated"])

    contact_parts = [
        esc(profile["location"]),
        href(f"mailto:{profile['email']}", profile["email"]),
    ]
    if profile.get("phone"):
        contact_parts.append(esc(profile["phone"]))
    contact_one = r" \contactsep ".join(contact_parts)

    contact_two = (
        href(profile["portfolio"], "bhalaji.com")
        + r" \contactsep "
        + href(profile["linkedin"], "LinkedIn")
        + r" \contactsep "
        + href(profile["scholar"], "Google Scholar")
        + r" \contactsep "
        + href(profile["orcid"], "ORCID")
        + r" \contactsep "
        + href(profile["github"], "GitHub")
    )

    return (
        template.replace("@@PDF_AUTHOR@@", esc(profile["name"]))
        .replace("@@UPDATED@@", esc(updated))
        .replace("@@NAME@@", esc(profile["name"]))
        .replace("@@HEADLINE@@", esc(profile["headline"]))
        .replace("@@CONTACT_LINE_ONE@@", contact_one)
        .replace("@@CONTACT_LINE_TWO@@", contact_two)
        .replace("@@BODY@@", body)
    )


def build_document(data: dict, template_path: Path, tex_path: Path, pdf_path: Path, body: str, compile_output: bool) -> None:
    tex = render_template(data, template_path, body)
    tex_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path.write_text(tex, encoding="utf-8")
    if compile_output:
        compile_pdf(tex_path, pdf_path)
    print(f"Generated {tex_path.relative_to(ROOT)}")
    if compile_output:
        print(f"Generated {pdf_path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--document", choices=("all", "cv", "resume"), default="all")
    parser.add_argument("--no-compile", action="store_true")
    args = parser.parse_args()

    data = yaml.safe_load(args.data.read_text(encoding="utf-8"))
    compile_output = not args.no_compile

    if args.document in ("all", "cv"):
        build_document(data, CV_TEMPLATE, CV_TEX, CV_PDF, render_cv(data), compile_output)
    if args.document in ("all", "resume"):
        build_document(data, RESUME_TEMPLATE, RESUME_TEX, RESUME_PDF, render_resume(data), compile_output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError, yaml.YAMLError) as error:
        print(f"CV build failed: {error}", file=sys.stderr)
        raise SystemExit(1)
