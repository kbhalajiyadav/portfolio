#!/usr/bin/env python3
"""Fail on portfolio style regressions that affect accessibility or responsive behavior."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "static/css/site.css"
REFINEMENTS = ROOT / "static/css/refinements.css"


def luminance(value: str) -> float:
    channels = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def main() -> int:
    text = CSS.read_text(encoding="utf-8")
    refinements = REFINEMENTS.read_text(encoding="utf-8")
    errors: list[str] = []
    tokens = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", text))
    for name in ("paper", "surface", "ink", "ink-soft", "teal", "cyan", "rust"):
        if name not in tokens:
            errors.append(f"missing color token --{name}")
    if not errors:
        for foreground in ("ink", "ink-soft", "teal", "cyan", "rust"):
            for background in ("paper", "surface"):
                ratio = contrast(tokens[foreground], tokens[background])
                if ratio < 4.5:
                    errors.append(f"--{foreground} contrast on --{background} is {ratio:.2f}:1; requires 4.5:1")
    required = (
        ".visually-hidden", ".indieweb-photo", ".lnk", ":focus-visible",
        "@media(max-width:1180px)", "@media(max-width:980px)",
        "@media(max-width:680px)", "@media(prefers-reduced-motion:reduce)",
    )
    for marker in required:
        if marker not in text:
            errors.append(f"missing required style marker {marker}")
    footer_control_rule = (
        ".site-footer nav .privacy-choice-link{color:var(--ink-soft);"
        "font-family:var(--sans);font-size:.76rem;font-weight:400;"
        "text-decoration:none}"
    )
    if footer_control_rule not in refinements:
        errors.append("footer privacy control must match the adjacent footer-link typography")
    footer_layout_rules = (
        ".site-footer nav{align-items:baseline;justify-content:flex-end}",
        ".site-footer nav a,.site-footer nav .privacy-choice-link{line-height:1.4}",
        ".site-footer nav{flex-wrap:nowrap;column-gap:.875rem;white-space:nowrap}",
        ".site-footer nav{justify-content:flex-start}",
    )
    for rule in footer_layout_rules:
        if rule not in refinements:
            errors.append(f"footer alignment invariant missing {rule!r}")
    pillar_alignment_rules = (
        ".pillar{display:flex;flex-direction:column}",
        ".pillar h3{min-height:3.24em}",
        ".pillar>p{min-height:8.1em}",
        ".pillar>p{min-height:9.72em}",
        ".pillar>.lnk{align-self:flex-start;margin-top:auto}",
    )
    for rule in pillar_alignment_rules:
        if rule not in refinements:
            errors.append(f"research-program alignment invariant missing {rule!r}")
    if "text-align:justify" in text.replace(" ", ""):
        errors.append("body copy must not use full justification")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Style audit passed: contrast, hidden microformats, focus, breakpoints, footer alignment, and research-card alignment verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
