#!/usr/bin/env python3
"""Audit visual-system invariants without freezing one screenshot or copy length."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "static/css/site.css").read_text(encoding="utf-8")
REF = (ROOT / "static/css/refinements.css").read_text(encoding="utf-8")
ABOUT = (ROOT / "static/css/about.css").read_text(encoding="utf-8")
POLISH = (ROOT / "static/css/final-polish.css").read_text(encoding="utf-8")
ALL = SITE + "\n" + REF + "\n" + ABOUT + "\n" + POLISH


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value)


def rule_has(css: str, selector: str, declaration: str) -> bool:
    pattern = re.compile(rf"{re.escape(selector)}\s*\{{([^}}]+)\}}", re.MULTILINE)
    wanted = compact(declaration)
    return any(wanted in compact(match.group(1)) for match in pattern.finditer(css))


def luminance(value: str) -> float:
    channels = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
    return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + .05) / (low + .05)


def main() -> int:
    errors: list[str] = []
    all_compact = compact(ALL)
    ref_compact = compact(REF)
    polish_compact = compact(POLISH)

    # Brand colors must remain readable on every site surface.
    tokens = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", ALL))
    required_tokens = ("paper", "surface", "surface-soft", "ink", "ink-soft", "teal", "cyan", "rust", "control-line")
    for name in required_tokens:
        if name not in tokens:
            errors.append(f"missing color token --{name}")
    if all(name in tokens for name in required_tokens):
        for foreground in ("ink", "ink-soft", "teal", "cyan", "rust"):
            for background in ("paper", "surface", "surface-soft"):
                ratio = contrast(tokens[foreground], tokens[background])
                if ratio < 4.5:
                    errors.append(f"--{foreground} contrast on --{background} is {ratio:.2f}:1; requires 4.5:1")
        for background in ("paper", "surface", "surface-soft"):
            ratio = contrast(tokens["control-line"], tokens[background])
            if ratio < 3:
                errors.append(f"--control-line contrast on --{background} is {ratio:.2f}:1; requires 3:1")

    for marker in (
        ".visually-hidden", ".indieweb-photo", ".lnk", ":focus-visible",
        "@media(max-width:1180px)", "@media(max-width:980px)",
        "@media(max-width:680px)", "@media(prefers-reduced-motion:reduce)",
    ):
        if marker not in SITE:
            errors.append(f"missing required base style marker {marker}")

    for rule in (
        ".series-grid{align-items:start}",
        ".series{align-self:start}",
        ".series summary{min-height:0}",
        ".menu-button,.copy-button{border-color:var(--control-line)}",
        ".toc-disclosure summary{display:flex;align-items:center;min-height:24px}",
        ".site-footer nav a,.site-footer nav .privacy-choice-link{display:inline-flex;align-items:center;min-height:24px;line-height:1.4}",
    ):
        if compact(rule) not in ref_compact:
            errors.append(f"interactive/accessibility invariant missing {rule!r}")

    # Homepage research outputs: a two-column pair must not inherit the old
    # 1fr/1fr two-row sidebar, which silently allocates an empty grid track.
    if not rule_has(SITE, ".package-artifacts", "grid-template-rows:auto"):
        errors.append("base related-output grid must not reserve two equal-height rows")
    if not rule_has(REF, ".package-artifacts", "grid-template-rows:auto"):
        errors.append("editorial related-output grid must explicitly declare intrinsic rows")
    for css, name in ((SITE, "base"), (REF, "refinement"), (ABOUT, "about"), (POLISH, "polish")):
        for match in re.finditer(r"\.package-artifacts\s*\{([^}]+)\}", css):
            declaration = re.search(r"grid-template-rows\s*:\s*([^;}]+)", match.group(1))
            if declaration and ("fr" in declaration.group(1) or "repeat(" in declaration.group(1)):
                errors.append(f"{name} CSS reintroduces fixed/fractional related-output grid rows")

    # Research figures remain borderless and carry visible, readable provenance.
    for selector, declaration in (
        (".research-figure__media", "border:0"),
        (".research-figure__open", "border:0"),
        (".research-figure figcaption small", "display:block"),
        (".research-figure figcaption small", "max-width:70ch"),
        (".package-lead>.research-figure--featured", "margin-top:1.6rem"),
    ):
        if not rule_has(REF, selector, declaration):
            errors.append(f"research figure presentation invariant missing {selector} {declaration}")
    if re.search(r"\.research-figure\{margin:0\}\s*\.package-lead>\.research-figure--featured\s*\{", REF):
        errors.append("featured figure spacing must not be re-overridden after its canonical layout rule")

    # Native homepage disclosures must stay legible, keyboard-focusable, and unboxed.
    for selector, declaration in (
        (".home-disclosure", "border-block:1px solid var(--line-strong)"),
        (".home-disclosure>summary", "min-height:48px"),
        (".home-disclosure>summary", "list-style:none"),
        (".home-disclosure>summary:focus-visible", "outline:2px solid var(--teal)"),
        (".home-disclosure:not([open])>.home-disclosure__body", "display:none"),
        (".research-extension__details .trajectory-grid", "border-top:0"),
    ):
        if not rule_has(REF, selector, declaration):
            errors.append(f"missing disclosure visual invariant {selector}: {declaration}")
    mobile_privacy = re.search(r"@media\(max-width:680px\)\s*\{(.*?)\}\s*@media\(prefers-reduced-motion", REF, re.DOTALL)
    if not mobile_privacy or mobile_privacy.group(1).count(".privacy-banner__actions{") != 1:
        errors.append("mobile privacy action styling must have only one declaration block")
    compact_schematic = re.search(r"@media\(max-width:820px\)\s*\{(.*?)\}\s*@media\(prefers-reduced-motion", POLISH, re.DOTALL)
    if not compact_schematic or any(
        f".{selector}{{" in compact_schematic.group(1)
        for selector in ("hero", "hero__copy", "hero__visual", "identity-note")
    ):
        errors.append("820px schematic CSS must not repeat the 980px compact hero")

    # Content-flow guardrails: real copy controls height; fixed text slots are forbidden.
    if not rule_has(REF, ".pillar", "min-height:0"):
        errors.append("research-program cards must remain intrinsically height-safe")
    if not (rule_has(REF, ".pillar", "display:flex") or rule_has(REF, ".pillar", "display:grid")):
        errors.append("research-program cards require an explicit intrinsic layout model")
    if not rule_has(REF, ".pillar>.lnk", "margin-top:auto"):
        errors.append("research-program action must follow flexible content flow")
    if re.search(r"\.pillar(?:\s+h3|\s*>\s*p)?\s*\{[^}]*\b(?:height|min-height):\s*[0-9.]+(?:em|rem|px)", REF):
        errors.append("research-program title/body text must not use fixed heights")
    if re.search(r"\.pillar\s*\{[^}]*grid-template-rows:[^;}]*[0-9.]+(?:em|rem|px)", REF):
        errors.append("research-program cards must not use fixed text-row heights")

    if not rule_has(REF, ".two-col", "align-items:start"):
        errors.append("experience/education columns must align to content start")
    if not rule_has(REF, ".education-panel", "align-self:start"):
        errors.append("education panel must remain intrinsic")
    if not rule_has(REF, ".trajectory-grid", "align-items:start"):
        errors.append("doctoral application/automation columns must remain intrinsic")
    if not rule_has(REF, ".trajectory-grid", "border-block:1px solid var(--line)"):
        errors.append("doctoral direction must retain the editorial ruled-band treatment")
    if re.search(r"\.(?:education-panel|trajectory-grid)(?:\s+article)?\s*\{[^}]*\b(?:height|min-height):\s*[0-9.]+(?:em|rem|px)", REF):
        errors.append("education/doctoral editorial content must not use fixed heights")

    if ".about-program-grid" in ABOUT:
        errors.append("About must not duplicate the homepage research-program card grid")
    if not rule_has(ABOUT, ".about-method-grid", "border-block:1px solid var(--line)"):
        errors.append("About methods must use the lighter editorial-band treatment")
    if not rule_has(ABOUT, ".about-profile-links", "border-block:1px solid var(--line)"):
        errors.append("About profile links must use the editorial ruled-list treatment")

    # The mobile hero needs an explicit composition; inherited desktop widths caused the 390px collapse.
    mobile_match = re.search(r"@media\(max-width:680px\)\s*\{(.*)\}\s*@media\(prefers-reduced-motion", REF, re.DOTALL)
    if not mobile_match:
        errors.append("missing mobile refinement block")
    else:
        mobile = mobile_match.group(1)
        for selector, declaration in (
            (".hero", "grid-template-columns:1fr"),
            (".hero__copy", "width:100%"),
            (".hero .eyebrow", "max-width:none"),
            (".hero h1", "max-width:100%"),
            (".hero h1", "text-wrap:balance"),
        ):
            if not rule_has(mobile, selector, declaration):
                errors.append(f"mobile hero invariant missing {selector} {declaration}")

    # Tablet composition, evidence targeting, and explanatory scientific visual are governed in the final polish layer.
    for rule in (
        ".trajectory-grid h3 + p{margin-top:.55rem}",
        ".series[id]{scroll-margin-top:calc(var(--header-h) + 38px)}",
        ".series:target{border-left:2px solid var(--teal);",
        "@media(max-width:820px)",
        ".research-signature__desktop",
        ".research-signature__mobile",
    ):
        if compact(rule) not in polish_compact:
            errors.append(f"final governed visual invariant missing {rule!r}")
    # Compact hero rules belong to the 980px breakpoint; repeating them at
    # 820px makes later responsive revisions unnecessarily fragile.
    compact_match = re.search(r"@media\(max-width:980px\)\s*\{(.*?)\}\s*@media\(max-width:820px", POLISH, re.DOTALL)
    if not compact_match:
        errors.append("missing governed compact hero composition block")
    else:
        compact_hero = compact_match.group(1)
        for selector, declaration in (
            (".hero", "grid-template-columns:1fr"),
            (".hero__copy", "width:100%"),
            (".hero h1", "max-width:100%"),
            (".identity-note", "position:static"),
        ):
            if not rule_has(compact_hero, selector, declaration):
                errors.append(f"compact hero invariant missing {selector} {declaration}")
    tablet_match = re.search(r"@media\(max-width:820px\)\s*\{(.*?)\}\s*@media\(prefers-reduced-motion", POLISH, re.DOTALL)
    if not tablet_match or not rule_has(tablet_match.group(1), ".research-signature__desktop", "display:none"):
        errors.append("820px scientific schematic must switch to its mobile treatment")

    motif = re.search(r"--motif-opacity:([0-9.]+)", REF)
    if not motif:
        errors.append("missing decorative motif opacity token")
    elif not .25 <= float(motif.group(1)) <= .5:
        errors.append(f"research motif opacity outside restrained range: {motif.group(1)}")
    if compact(".pillar--grid .motif::after{border-width:1px}") not in ref_compact:
        errors.append("grid motif accent must remain a soft 1px stroke")

    for rule in (
        "@view-transition{navigation:auto}",
        ".site-head{view-transition-name:site-header}",
        "::view-transition-old(site-header),::view-transition-new(site-header){animation:none}",
        "::view-transition-old(root),::view-transition-new(root),::view-transition-old(site-header),::view-transition-new(site-header){animation:none!important}",
        ".privacy-banner{position:relative;z-index:90;",
        'html[data-analytics-consent="granted"] .privacy-banner,html[data-analytics-consent="denied"] .privacy-banner{display:none}',
        ".section{padding-block:var(--refined-section-space)}",
        ".section[id],.contact-section[id]{scroll-margin-top:calc(var(--header-h) + 38px)}",
        ".page-shell{padding-block:clamp(3rem,6vw,5.25rem)}",
    ):
        if compact(rule) not in ref_compact:
            errors.append(f"system invariant missing {rule!r}")
    for rule in (
        ".research-package{display:block;border:0;border-top:1px solid var(--line-strong);",
        ".secondary-output{border:0;border-top:1px solid var(--line);background:transparent;",
        ".hero+.privacy-banner{margin-top:0;",
    ):
        if compact(rule) not in ref_compact:
            errors.append(f"research hierarchy or below-introduction privacy styling missing {rule}")
    if ".privacy-banner+main .hero" in REF:
        errors.append("privacy notice must not displace the homepage hero")
    if ".privacy-banner{position:fixed" in ref_compact:
        errors.append("privacy controls must remain in document flow")
    if "text-align:justify" in all_compact:
        errors.append("body copy must not use full justification")

    durations = [int(value) for value in re.findall(r"::view-transition-(?:old|new)\(root\)\{animation:(\d+)ms", ref_compact)]
    if len(durations) != 2 or max(durations, default=999) > 220:
        errors.append(f"root page transitions must remain two short durations <=220ms: {durations}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Style audit passed: contrast, interaction, intrinsic content flow, mobile/tablet composition, editorial restraint, evidence targeting, scientific schematic integrity, motion, privacy, and spacing guardrails verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
