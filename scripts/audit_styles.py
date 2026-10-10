#!/usr/bin/env python3
"""Fail on style regressions that affect accessibility, responsive behavior, or editorial flow."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "static/css/site.css"
REFINEMENTS = ROOT / "static/css/refinements.css"
ABOUT = ROOT / "static/css/about.css"


def luminance(value: str) -> float:
    channels = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def contains_declaration(css: str, selector: str, declaration: str) -> bool:
    pattern = re.compile(rf"{re.escape(selector)}\s*\{{([^}}]+)\}}", re.MULTILINE)
    wanted = compact(declaration)
    return any(wanted in compact(match.group(1)) for match in pattern.finditer(css))


def main() -> int:
    text = CSS.read_text(encoding="utf-8")
    refinements = REFINEMENTS.read_text(encoding="utf-8")
    about = ABOUT.read_text(encoding="utf-8")
    combined = text + "\n" + refinements + "\n" + about
    errors: list[str] = []

    # Later declarations intentionally win, matching the browser cascade.
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
                    errors.append(f"--{foreground} contrast on --{background} is {ratio:.2f}:1; requires 4.5:1")
        for background in ("paper", "surface", "surface-soft"):
            ratio = contrast(tokens["control-line"], tokens[background])
            if ratio < 3.0:
                errors.append(f"--control-line contrast on --{background} is {ratio:.2f}:1; requires 3:1")

    for marker in (
        ".visually-hidden", ".indieweb-photo", ".lnk", ":focus-visible",
        "@media(max-width:1180px)", "@media(max-width:980px)",
        "@media(max-width:680px)", "@media(prefers-reduced-motion:reduce)",
    ):
        if marker not in text:
            errors.append(f"missing required style marker {marker}")

    for rule in (
        ".series-grid{align-items:start}",
        ".series{align-self:start}",
        ".series summary{min-height:0}",
        ".menu-button,.copy-button{border-color:var(--control-line)}",
        ".toc-disclosure summary{display:flex;align-items:center;min-height:24px}",
        ".site-footer nav a,.site-footer nav .privacy-choice-link{display:inline-flex;align-items:center;min-height:24px;line-height:1.4}",
    ):
        if rule not in compact(refinements):
            errors.append(f"interactive-layout/accessibility invariant missing {rule!r}")

    # Card copy must remain in normal flow. Alignment may use flex/grid, but no fixed text rows.
    if not contains_declaration(refinements, ".pillar", "min-height:0"):
        errors.append("research-program cards must remain intrinsically height-safe")
    if not (
        contains_declaration(refinements, ".pillar", "display:flex")
        or contains_declaration(refinements, ".pillar", "display:grid")
    ):
        errors.append("research-program cards require an explicit intrinsic layout model")
    if re.search(r"\.pillar(?:\s+h3|\s*>\s*p)?\s*\{[^}]*\b(?:height|min-height):\s*[0-9.]+(?:em|rem|px)", refinements):
        errors.append("research-program title/body text must not use fixed heights")
    if re.search(r"\.pillar\s*\{[^}]*grid-template-rows:[^;}]*[0-9.]+(?:em|rem|px)", refinements):
        errors.append("research-program cards must not use fixed text-row heights")
    if not contains_declaration(refinements, ".pillar>.lnk", "margin-top:auto"):
        errors.append("research-program action should align through flexible space after content")

    # Editorial side-by-side blocks should align at their content start instead of stretching.
    if not contains_declaration(refinements, ".two-col", "align-items:start"):
        errors.append("experience/education columns must align to content start")
    if not contains_declaration(refinements, ".education-panel", "align-self:start"):
        errors.append("education panel must stay intrinsic rather than stretch to its neighbor")
    if re.search(r"\.education-panel(?:\s+article)?\s*\{[^}]*\b(?:height|min-height):\s*[0-9.]+(?:em|rem|px)", refinements):
        errors.append("education content must not use fixed heights")
    if not contains_declaration(refinements, ".trajectory-grid", "align-items:start"):
        errors.append("doctoral application/automation columns must align to content start")
    if not contains_declaration(refinements, ".trajectory-grid", "border-block:1px solid var(--line)"):
        errors.append("doctoral direction should retain the editorial ruled-band treatment")
    if re.search(r"\.trajectory-grid(?:\s+article)?\s*\{[^}]*\b(?:height|min-height):\s*[0-9.]+(?:em|rem|px)", refinements):
        errors.append("doctoral direction content must not use fixed heights")

    # About should not restore the duplicated research-card grid or fixed-height supporting blocks.
    if ".about-program-grid" in about:
        errors.append("About must not duplicate the homepage research-program card grid")
    if re.search(r"\.about-(?:method|profile)-[^,{]*\s*\{[^}]*\b(?:height|min-height):\s*[0-9.]+(?:em|rem|px)", about):
        errors.append("About supporting content must remain intrinsic")
    if not contains_declaration(about, ".about-method-grid", "border-block:1px solid var(--line)"):
        errors.append("About methods must retain the lighter editorial-band treatment")
    if not contains_declaration(about, ".about-profile-links", "border-block:1px solid var(--line)"):
        errors.append("About profile links must retain the editorial ruled-list treatment")

    # Mobile hero requires its own composition; inherited desktop widths caused the 390px collapse.
    mobile_block = re.search(r"@media\(max-width:680px\)\s*\{(.*)\}\s*@media\(prefers-reduced-motion", refinements, re.DOTALL)
    if not mobile_block:
        errors.append("missing mobile refinement block")
    else:
        mobile = mobile_block.group(1)
        for selector, declaration in (
            (".hero", "grid-template-columns:1fr"),
            (".hero__copy", "width:100%"),
            (".hero .eyebrow", "max-width:none"),
            (".hero h1", "max-width:100%"),
            (".hero h1", "text-wrap:balance"),
        ):
            if not contains_declaration(mobile, selector, declaration):
                errors.append(f"mobile hero invariant missing {selector} {declaration}")

    motif_match = re.search(r"--motif-opacity:([0-9.]+)", refinements)
    if not motif_match:
        errors.append("missing decorative motif opacity token")
    else:
        motif_opacity = float(motif_match.group(1))
        if motif_opacity > 0.5:
            errors.append(f"research motifs are too visually dominant: opacity={motif_opacity}")
        if motif_opacity < 0.25:
            errors.append(f"research motifs are too faint to retain their intended cue: opacity={motif_opacity}")
    if ".pillar--grid .motif::after{border-width:1px}" not in compact(refinements):
        errors.append("grid motif accent must remain a soft 1px decorative stroke")

    for rule in (
        "@view-transition{navigation:auto}",
        ".site-head{view-transition-name:site-header}",
        "::view-transition-old(site-header),::view-transition-new(site-header){animation:none}",
        "::view-transition-old(root),::view-transition-new(root),::view-transition-old(site-header),::view-transition-new(site-header){animation:none!important}",
    ):
        if rule not in compact(refinements):
            errors.append(f"navigation-continuity/motion invariant missing {rule!r}")
    transition_durations = [int(value) for value in re.findall(r"::view-transition-(?:old|new)\(root\)\{animation:(\d+)ms", compact(refinements))]
    if len(transition_durations) != 2:
        errors.append("cross-page transition must define exactly two short root transition durations")
    elif max(transition_durations) > 220:
        errors.append(f"cross-page motion exceeds 220ms attention budget: {transition_durations}")

    for rule in (
        ".privacy-banner{position:relative;z-index:90;",
        'html[data-analytics-consent="granted"] .privacy-banner,html[data-analytics-consent="denied"] .privacy-banner{display:none}',
        'html[data-analytics-consent="unknown"] .privacy-banner+main .hero{padding-top:clamp(2.75rem,5vw,4.5rem)}',
        'html[data-analytics-consent="unknown"] .privacy-banner+main .page-shell{padding-top:clamp(2.5rem,4vw,3.75rem)}',
    ):
        if compact(rule) not in compact(refinements):
            errors.append(f"privacy-layout invariant missing {rule!r}")
    if ".privacy-banner{position:fixed" in compact(refinements):
        errors.append("privacy controls must remain in document flow and must not obscure page content")

    for rule in (
        "--refined-section-space:clamp(4.5rem,7vw,6.5rem)",
        ".section{padding-block:var(--refined-section-space)}",
        ".section[id],.contact-section[id]{scroll-margin-top:calc(var(--header-h) + 38px)}",
        ".page-shell{padding-block:clamp(3rem,6vw,5.25rem)}",
        ".back-link{margin-bottom:2.1rem}",
        ".page-header{margin-bottom:2.55rem}",
        ".article-layout{gap:clamp(2.5rem,4vw,4rem)}",
    ):
        if compact(rule) not in compact(refinements):
            errors.append(f"page-spacing invariant missing {rule!r}")

    if "text-align:justify" in compact(combined):
        errors.append("body copy must not use full justification")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "Style audit passed: branded contrast, interactive boundaries, focus/breakpoints, intrinsic editorial flow, "
        "mobile hero composition, decorative restraint, reduced-motion page continuity, privacy controls, and page spacing verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
