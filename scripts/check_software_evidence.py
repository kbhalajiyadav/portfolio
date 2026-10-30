#!/usr/bin/env python3
"""Verify the unchanged Peel Trace reference image and its scientific boundary."""
from pathlib import Path
import hashlib
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / "static/media/research/peel-trace-reference-qc.png"
PAGE = ROOT / "content/project/peel-trace-evaluation/index.md"
SHORTCODE = ROOT / "layouts/shortcodes/source-figure.html"
EXPECTED_GIT_BLOB = "5b7a02b4030853e7f34af63bd650d65d861f2ce1"
EXPECTED_SIZE = 271863
EXPECTED_DIMENSIONS = (3993, 1350)


def main() -> int:
    errors = []
    if not IMAGE.is_file():
        errors.append("software reference QC image missing")
    else:
        raw = IMAGE.read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if len(raw) != EXPECTED_SIZE or git_blob != EXPECTED_GIT_BLOB:
            errors.append("software reference image no longer matches canonical upstream PNG")
        if not raw.startswith(b"\x89PNG\r\n\x1a\n") or len(raw) < 24 or struct.unpack(">II", raw[16:24]) != EXPECTED_DIMENSIONS:
            errors.append("software reference PNG has unexpected dimensions or format")
    source = PAGE.read_text(encoding="utf-8")
    for marker in (
        "peel-trace-reference-qc.png",
        "bundled Scotch Tape reference example",
        "not experimental data from the wearable-textile adhesion article",
        "source-figure",
    ):
        if marker not in source:
            errors.append(f"software page missing evidence provenance marker {marker!r}")
    template = SHORTCODE.read_text(encoding="utf-8")
    for marker in ('loading="lazy"', 'decoding="async"', 'alt="{{ $alt }}"', 'figcaption', 'reproduced unchanged'):
        if marker not in template:
            errors.append(f"software source-image shortcode missing {marker!r}")
    if errors:
        print("\n".join("ERROR: " + error for error in errors), file=sys.stderr)
        return 1
    print("Peel Trace QC source pixels, provenance, alt text, loading and scope verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
