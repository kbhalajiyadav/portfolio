#!/usr/bin/env python3
"""Build the public CV from data/cv.yaml using XeLaTeX."""

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
DEFAULT_TEMPLATE = ROOT / "cv" / "template.tex"
DEFAULT_TEX = ROOT / "cv" / "generated" / "bhalaji_cv.tex"
DEFAULT_PDF = ROOT / "static" / "uploads" / "resume.pdf"


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


def render(data: dict) -> str:
    p = data["profile"]
    output: list[str] = []

    output.append(
        section(
            "Research Profile",
            [rf"\color{{Ink}} {esc(p['summary'])}\color{{black}}"],
        )
    )

    education: list[str] = []
    for item in data["education"]:
        education.append(
            rf"\entry{{{esc(item['degree'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(item['institution'])}}}{{{esc(item['location'])}}}"
        )
        education.append(bullets(item.get("details", [])))
    output.append(section("Education", education))

    research: list[str] = []
    for item in data["research_experience"]:
        subtitle = item["organization"]
        if item.get("advisor"):
            subtitle += f" | Advisor: {item['advisor']}"
        research.append(
            rf"\entry{{{esc(item['role'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(subtitle)}}}{{{esc(item['location'])}}}"
        )
        research.append(bullets(item.get("bullets", [])))
    output.append(section("Research and Teaching Experience", research))

    pubs = [
        "\\begin{enumerate}\n"
        + "\n".join(rf"  \item {esc(item)}" for item in data["publications"])
        + "\n\\end{enumerate}"
    ]
    output.append(section("Peer-Reviewed Publications", pubs))

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
    output.append(section("Research Software", software))

    presentations = [
        "\\begin{enumerate}\n"
        + "\n".join(
            rf"  \item \dateditem{{\textbf{{{esc(item['type'])}.}} "
            rf"{esc(item['citation'])}}}{{{esc(item['date'])}}}"
            for item in data["presentations"]
        )
        + "\n\\end{enumerate}"
    ]
    output.append(section("Presentations, Seminar, and Defense", presentations))

    engagement: list[str] = []
    for item in data["engagement"]:
        engagement.append(
            rf"\smallentry{{{esc(item['role'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(item['organization'])}}}"
        )
    output.append(section("Teaching, Review, and Applied Innovation", engagement))

    industry: list[str] = []
    for item in data["industry_experience"]:
        industry.append(
            rf"\entry{{{esc(item['role'])}}}{{{esc(item['period'])}}}"
            rf"{{{esc(item['organization'])}}}{{{esc(item['location'])}}}"
        )
        industry.append(bullets(item.get("bullets", [])))
    output.append(section("Industry Experience", industry))

    honors = [honors_bullets(data["honors_development"])]
    output.append(section("Honors and Professional Development", honors))

    skills = []
    for index, item in enumerate(data["technical_skills"]):
        suffix = r"\\[2pt]" if index < len(data["technical_skills"]) - 1 else ""
        skills.append(
            rf"\textbf{{{esc(item['category'])}:}} {esc(item['items'])}{suffix}"
        )
    output.append(section("Technical Skills", [r"{\small " + "\n".join(skills) + "}"]))

    return "\n".join(output)


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--tex", type=Path, default=DEFAULT_TEX)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--no-compile", action="store_true")
    args = parser.parse_args()

    data = yaml.safe_load(args.data.read_text(encoding="utf-8"))
    template = args.template.read_text(encoding="utf-8")
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

    tex = (
        template.replace("@@PDF_AUTHOR@@", esc(profile["name"]))
        .replace("@@UPDATED@@", esc(updated))
        .replace("@@NAME@@", esc(profile["name"]))
        .replace("@@HEADLINE@@", esc(profile["headline"]))
        .replace("@@CONTACT_LINE_ONE@@", contact_one)
        .replace("@@CONTACT_LINE_TWO@@", contact_two)
        .replace("@@BODY@@", render(data))
    )
    args.tex.parent.mkdir(parents=True, exist_ok=True)
    args.tex.write_text(tex, encoding="utf-8")

    if not args.no_compile:
        compile_pdf(args.tex, args.pdf)
    print(f"Generated {args.tex.relative_to(ROOT)}")
    if not args.no_compile:
        print(f"Generated {args.pdf.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError, yaml.YAMLError) as error:
        print(f"CV build failed: {error}", file=sys.stderr)
        raise SystemExit(1)
