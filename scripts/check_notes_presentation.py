#!/usr/bin/env python3
"""Validate the non-publishing Research Notes presentation fixtures."""
from __future__ import annotations

from pathlib import Path
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
    ):
        require(index, needle, "notes index", errors)

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
    ):
        require(method, needle, "method fixture", errors)

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
    ):
        require(withdrawn, needle, "withdrawn fixture", errors)
    forbid(withdrawn, "WITHDRAWN_FIXTURE_BODY_SHOULD_NOT_APPEAR", "withdrawn fixture", errors)
    forbid(withdrawn, 'class="article-content', "withdrawn fixture", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research Notes presentation fixtures passed: index, metadata, schema, TOC, correction, retirement, and withdrawal states verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
