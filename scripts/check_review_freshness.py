#!/usr/bin/env python3
"""Alert when human-authored substantive review dates become stale."""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TODAY = dt.datetime.now(dt.timezone.utc).date()


def parse_frontmatter_date(path: Path, field: str) -> dt.date:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        raise ValueError(f"{path}: missing YAML front matter")
    data = yaml.safe_load(match.group(1))
    value = data.get(field)
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value))


def main() -> int:
    portfolio = yaml.safe_load((ROOT / "data" / "portfolio.yaml").read_text(encoding="utf-8"))
    checks = [
        ("portfolio profile", dt.date.fromisoformat(str(portfolio["profile"]["last_updated_iso"])), 180),
        ("privacy notice", parse_frontmatter_date(ROOT / "content" / "privacy.md", "lastmod"), 365),
        ("rights notice", parse_frontmatter_date(ROOT / "content" / "brand-use.md", "lastmod"), 365),
    ]

    errors: list[str] = []
    for label, reviewed, max_age in checks:
        age = (TODAY - reviewed).days
        if age < 0:
            errors.append(f"{label}: review date is in the future ({reviewed.isoformat()})")
        elif age > max_age:
            errors.append(
                f"{label}: human review is {age} days old; threshold is {max_age} days. "
                "Review the content before advancing the date."
            )
        else:
            print(f"{label}: reviewed {reviewed.isoformat()} ({age} days ago; threshold {max_age})")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
