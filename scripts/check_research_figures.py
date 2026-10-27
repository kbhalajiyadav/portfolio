#!/usr/bin/env python3
"""Check provenance metadata and actual PNG dimensions for published portfolio figures.

Source of truth: publication front matter. Below-target resolution is reported
as an advisory; source-quality exports are retained without invented upscaling.
"""
from __future__ import annotations

from pathlib import Path
import struct
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_IMAGES = (ROOT / "static" / "media" / "research").resolve()
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)
    if len(header) < 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError("invalid PNG signature or IHDR")
    return struct.unpack(">II", header[16:24])


def check() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    count = 0
    for page in sorted((ROOT / "content" / "publication").glob("*/index.md")):
        raw = page.read_text(encoding="utf-8")
        if not raw.startswith("---\n"):
            continue
        parts = raw.split("---", 2)
        if len(parts) < 3:
            errors.append(f"{page}: incomplete front matter")
            continue
        front = yaml.safe_load(parts[1]) or {}
        for entry in front.get("figures", []) or []:
            count += 1
            src = entry.get("src", "")
            label = f"{page.relative_to(ROOT)}: {src or '(missing src)'}"
            required = ("src", "width", "height", "alt", "caption", "credit", "evidence", "license", "license_url")
            for key in required:
                if not entry.get(key):
                    errors.append(f"{label}: missing {key}")
            if not src or not src.startswith("media/research/") or not src.endswith(".png"):
                errors.append(f"{label}: figure path must be a PNG under static/media/research/")
                continue
            if src in seen:
                errors.append(f"{label}: duplicate image path in publication records")
            seen.add(src)
            img = (ROOT / "static" / src).resolve()
            if not img.is_relative_to(RESEARCH_IMAGES) or not img.is_file():
                errors.append(f"{label}: missing image or unsafe path")
                continue
            if entry.get("license") != "CC BY 4.0" or entry.get("license_url") != "https://creativecommons.org/licenses/by/4.0/":
                errors.append(f"{label}: journal-figure license metadata differs from verified CC BY 4.0")
            if len(str(entry.get("alt", "")).strip()) < 30:
                errors.append(f"{label}: descriptive alt text is absent/too brief")
            if not any(term in str(entry.get("credit", "")).lower() for term in ("resiz", "native", "cropp", "lossless", "re-encod", "reassembl")):
                warnings.append(f"{label}: review whether resizing should be disclosed in credit")
            try:
                actual = png_dimensions(img)
                declared = (int(entry["width"]), int(entry["height"]))
            except (ValueError, TypeError, KeyError) as exc:
                errors.append(f"{label}: cannot determine PNG dimensions ({exc})")
                continue
            if actual != declared:
                errors.append(f"{label}: image metadata {declared} does not match PNG {actual}")
            if actual[0] < 1000:
                warnings.append(f"{label}: only {actual[0]} px wide; replace with authentic source export, not upscaling")
    for item in warnings:
        print("FIGURE WARNING:", item)
    for item in errors:
        print("FIGURE ERROR:", item, file=sys.stderr)
    print(f"Research figure provenance audit: {count} figures; {len(errors)} errors; {len(warnings)} advisories")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(check())
