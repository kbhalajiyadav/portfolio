#!/usr/bin/env python3
"""Update reviewable portfolio display controls from GitHub Actions inputs."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLS = ROOT / "data" / "site_controls.yaml"


def as_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected true or false, received {value!r}")


def bounded_int(value: str, *, minimum: int = 1, maximum: int = 12) -> int:
    number = int(value)
    if not minimum <= number <= maximum:
        raise argparse.ArgumentTypeError(f"Value must be between {minimum} and {maximum}")
    return number


def load_controls() -> dict[str, Any]:
    data = yaml.safe_load(CONTROLS.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit("data/site_controls.yaml must contain a mapping")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--presentation-series", required=True, type=bounded_int)
    parser.add_argument("--teaching-records", required=True, type=bounded_int)
    parser.add_argument("--service-records", required=True, type=bounded_int)
    parser.add_argument("--notes", required=True, type=as_bool)
    parser.add_argument("--presentations-archive", required=True, type=as_bool)
    parser.add_argument("--webmentions", required=True, type=as_bool)
    args = parser.parse_args()

    data = load_controls()
    homepage = data.setdefault("homepage", {})
    limits = homepage.setdefault("limits", {})
    features = data.setdefault("features", {})

    limits.update(
        {
            "presentation_series": args.presentation_series,
            "teaching_records": args.teaching_records,
            "service_records": args.service_records,
        }
    )
    features.update(
        {
            "notes": args.notes,
            "presentations_archive": args.presentations_archive,
            "webmentions": args.webmentions,
            "search": False,
            "latest_updates": False,
        }
    )

    CONTROLS.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(CONTROLS.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
