#!/usr/bin/env python3
"""Validate the non-publishing Research Notes presentation fixtures."""
from __future__ import annotations

from pathlib import Path
import re
import sys


def require(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"{label}: missing {needle!r}")


def forbid(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle in text:
        errors.append(f"{label}: unexpected {needle!r}")


def read_page(root: Path, relative: str, errors: list[str]) -> str:
    path = root / relative
    if not path.exists():
        errors.append(f"missing rendered fixture: {relative}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_notes_presentation.py <rendered-site-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    errors: list[str] = []

    index = read_page(root, "notes/index.html", errors)
    for needle in (
        "Research Notes",
        "Featured",
        "Methods",
        "Concepts",
        "Reflections",
        "Presentation Fixture: Method",
        "Presentation Fixture: Corrected Concept",
        "Presentation Fixture: Retired Reflection",
        "Presentation Fixture: Withdrawn Concept",
        "This note has been withdrawn and should not be relied upon.",
    ):
        require(index, needle, "notes index", errors)
    forbid(index, "Synthetic withdrawn note used only to validate tombstone rendering.", "notes index", errors)

    method = read_page(root, "notes/presentation-method/index.html", errors)
    for needle in (
        "Research Note",
        "Method",
        "Evolving note.",
        "On this page",
        "synthetic fixture content",
        '"@type":"Article"',
        '"@type":"BreadcrumbList"',
        "article:published_time",
        'property="og:type" content="article"',
        '/social/research.png',
        'name=robots content="noindex,follow"',
        '/css/site-notes.min.',
    ):
        require(method, needle, "method fixture", errors)

    css_match = re.search(r'href=([^ >]*?/css/site-notes\.min\.[^ >]+?\.css)', method)
    if not css_match:
        errors.append("method fixture: could not resolve the Notes-specific stylesheet")
    else:
        css_name = css_match.group(1).split("/css/", 1)[-1]
        css_path = root / "css" / css_name
        if not css_path.exists():
            errors.append(f"method fixture: missing Notes stylesheet asset {css_name!r}")
        else:
            css = css_path.read_text(encoding="utf-8")
            for needle in (".note-status-banner", ".note-reading-grid", ".notes-index__section"):
                require(css, needle, "Notes stylesheet", errors)

    corrected = read_page(root, "notes/presentation-corrected/index.html", errors)
    for needle in (
        "Corrected.",
        "A synthetic factual statement was corrected for presentation testing.",
        "Reviewed October 14, 2026",
        "This body exists only to test the corrected state",
    ):
        require(corrected, needle, "corrected fixture", errors)

    retired = read_page(root, "notes/presentation-retired/index.html", errors)
    for needle in (
        "Retired.",
        "This synthetic note has been superseded for presentation testing.",
        "Current replacement",
        "This body remains visible",
    ):
        require(retired, needle, "retired fixture", errors)

    withdrawn = read_page(root, "notes/presentation-withdrawn/index.html", errors)
    for needle in (
        "Withdrawn — do not rely on this note.",
        "This synthetic note must not be relied upon",
        "See current material",
        "This Research Note has been withdrawn and should not be relied upon.",
        '"creativeWorkStatus":"withdrawn"',
    ):
        require(withdrawn, needle, "withdrawn fixture", errors)
    for needle in (
        "WITHDRAWN_FIXTURE_BODY_SHOULD_NOT_APPEAR",
        'class="article-content',
        "Synthetic withdrawn note used only to validate tombstone rendering.",
    ):
        forbid(withdrawn, needle, "withdrawn fixture", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research Notes presentation fixtures passed: dedicated stylesheet, index, metadata, Open Graph, schema, TOC, correction, retirement, withdrawal, and tombstone leakage controls verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
