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
    combined = text + "\n" + refinements
    errors: list[str] = []

    # Later declarations intentionally win, matching the browser cascade for
    # the root-level brand tokens overridden in refinements.css.
    tokens = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", combined))
    for name in (
        "paper", "surface", "surface-soft", "ink", "ink-soft",
        "teal", "cyan", "rust", "control-line",
    ):
        if name not in tokens:
            errors.append(f"missing color token --{name}")

    if not errors:
        for foreground in ("ink", "ink-soft", "teal", "cyan", "rust"):
            for background in ("paper", "surface", "surface-soft"):
                ratio = contrast(tokens[foreground], tokens[background])
                if ratio < 4.5:
                    errors.append(
                        f"--{foreground} contrast on --{background} is {ratio:.2f}:1; requires 4.5:1"
                    )
        for background in ("paper", "surface", "surface-soft"):
            ratio = contrast(tokens["control-line"], tokens[background])
            if ratio < 3.0:
                errors.append(
                    f"--control-line contrast on --{background} is {ratio:.2f}:1; requires 3:1"
                )

    required = (
        ".visually-hidden", ".indieweb-photo", ".lnk", ":focus-visible",
        "@media(max-width:1180px)", "@media(max-width:980px)",
        "@media(max-width:680px)", "@media(prefers-reduced-motion:reduce)",
    )
    for marker in required:
        if marker not in text:
            errors.append(f"missing required style marker {marker}")

    interaction_rules = (
        ".series-grid{align-items:start}",
        ".series{align-self:start}",
        ".menu-button,.copy-button{border-color:var(--control-line)}",
        ".toc-disclosure summary{display:flex;align-items:center;min-height:24px}",
        ".site-footer nav a,.site-footer nav .privacy-choice-link{display:inline-flex;align-items:center;min-height:24px;line-height:1.4}",
    )
    for rule in interaction_rules:
        if rule not in refinements:
            errors.append(f"interactive-layout/accessibility invariant missing {rule!r}")

    footer_typography_markers = (
        ".site-footer nav .privacy-choice-link{",
        "color:var(--ink-soft)",
        "font-family:var(--sans)",
        "font-size:.76rem",
        "font-weight:400",
        "text-decoration:none",
    )
    for marker in footer_typography_markers:
        if marker not in refinements:
            errors.append(f"footer privacy control typography marker missing {marker!r}")

    footer_layout_rules = (
        ".site-footer nav{align-items:baseline;justify-content:flex-end}",
        ".site-footer nav{flex-wrap:nowrap;column-gap:.875rem;white-space:nowrap}",
        ".site-footer nav{justify-content:flex-start}",
    )
    for rule in footer_layout_rules:
        if rule not in refinements:
            errors.append(f"footer alignment invariant missing {rule!r}")

    # Card alignment must remain content-driven. Fixed text-row heights previously
    # let long copy collide with tags even though the card tops appeared aligned.
    pillar_alignment_rules = (
        "@supports (grid-template-rows:subgrid)",
        ".pillar{display:grid;grid-row:span 5;grid-template-rows:subgrid;min-height:0;align-items:start}",
        ".pillar .card-number{margin-bottom:2.5rem}",
        ".pillar h3{margin-top:0}",
        ".pillar>.lnk{align-self:end}",
        "@supports not (grid-template-rows:subgrid)",
        ".pillar{display:flex;flex-direction:column;min-height:430px}",
        ".pillar>.lnk{margin-top:auto}",
    )
    for rule in pillar_alignment_rules:
        if rule not in refinements:
            errors.append(f"research-program content-flow invariant missing {rule!r}")
    if re.search(r"\.pillar\{grid-template-rows:auto\s+[0-9.]+em\s+[0-9.]+em", refinements):
        errors.append("research-program cards must not restore fixed text-row heights that can cause content collisions")

    motif_match = re.search(r"--motif-opacity:([0-9.]+)", refinements)
    if not motif_match:
        errors.append("missing decorative motif opacity token")
    else:
        motif_opacity = float(motif_match.group(1))
        if motif_opacity > 0.5:
            errors.append(f"research motifs are too visually dominant: opacity={motif_opacity}")
        if motif_opacity < 0.25:
            errors.append(f"research motifs are too faint to retain their intended cue: opacity={motif_opacity}")
    if ".pillar--grid .motif::after{border-width:1px}" not in refinements:
        errors.append("grid motif accent must remain a soft 1px decorative stroke")

    transition_rules = (
        "@view-transition{navigation:auto}",
        ".site-head{view-transition-name:site-header}",
        "::view-transition-old(site-header),::view-transition-new(site-header){animation:none}",
        "::view-transition-old(root),::view-transition-new(root),::view-transition-old(site-header),::view-transition-new(site-header){animation:none!important}",
    )
    for rule in transition_rules:
        if rule not in refinements:
            errors.append(f"navigation-continuity/motion invariant missing {rule!r}")
    transition_durations = [int(value) for value in re.findall(r"::view-transition-(?:old|new)\(root\)\{animation:(\d+)ms", refinements)]
    if len(transition_durations) != 2:
        errors.append("cross-page transition must define exactly two short root transition durations")
    elif max(transition_durations) > 220:
        errors.append(f"cross-page motion exceeds 220ms attention budget: {transition_durations}")

    privacy_layout_rules = (
        ".privacy-banner{position:relative;z-index:90;",
        'html[data-analytics-consent="granted"] .privacy-banner,html[data-analytics-consent="denied"] .privacy-banner{display:none}',
        'html[data-analytics-consent="unknown"] .privacy-banner+main .hero{padding-top:clamp(2.75rem,5vw,4.5rem)}',
        'html[data-analytics-consent="unknown"] .privacy-banner+main .page-shell{padding-top:clamp(2.5rem,4vw,3.75rem)}',
        ".privacy-banner{align-items:stretch;flex-direction:column;gap:.9rem;width:calc(100% - 2rem);padding:1rem}",
    )
    for rule in privacy_layout_rules:
        if rule not in refinements:
            errors.append(f"privacy-layout invariant missing {rule!r}")
    if ".privacy-banner{position:fixed" in refinements:
        errors.append("privacy controls must remain in document flow and must not obscure page content")

    spacing_rules = (
        "--refined-section-space:clamp(4.5rem,7vw,6.5rem)",
        ".section{padding-block:var(--refined-section-space)}",
        ".page-shell{padding-block:clamp(3rem,6vw,5.25rem)}",
        ".back-link{margin-bottom:2.1rem}",
        ".page-header{margin-bottom:2.55rem}",
        ".article-layout{gap:clamp(2.5rem,4vw,4rem)}",
    )
    for rule in spacing_rules:
        if rule not in refinements:
            errors.append(f"page-spacing invariant missing {rule!r}")

    if "text-align:justify" in combined.replace(" ", ""):
        errors.append("body copy must not use full justification")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "Style audit passed: AA text contrast across all branded surfaces, "
        "3:1 interactive boundaries, 24px controls, focus, breakpoints, content-driven card flow, "
        "decorative restraint, reduced-motion-safe page continuity, privacy controls, and page spacing verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
