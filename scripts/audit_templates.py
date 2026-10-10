#!/usr/bin/env python3
"""Static checks for the custom Hugo layout system before rendering."""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "layouts"


def main() -> int:
    errors: list[str] = []
    templates = sorted(LAYOUTS.rglob("*.html"))
    if not templates:
        errors.append("no Hugo templates found")
    for path in templates:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if text.count("{{") != text.count("}}"):
            errors.append(f"{relative}: unbalanced Hugo template delimiters")
        if "partials" not in path.parts and path.name != "baseof.html":
            if '{{ define "main" }}' not in text:
                errors.append(f"{relative}: missing main template definition")
        for image in re.findall(r"<img\b[^>]*>", text, flags=re.IGNORECASE):
            for attribute in ("src=", "alt=", "width=", "height="):
                if attribute not in image:
                    errors.append(f"{relative}: image missing {attribute[:-1]}: {image[:140]}")

    base = (LAYOUTS / "_default/baseof.html").read_text(encoding="utf-8")
    for marker in ('partial "seo_head.html"', 'partial "site_header.html"', 'block "main"', 'partial "site_footer.html"'):
        if marker not in base:
            errors.append(f"layouts/_default/baseof.html: missing {marker}")
    for marker in ('data-analytics-consent="unknown"', 'data-consent-bootstrap', 'bhalaji.analyticsConsent.v1', 'dataset.analyticsConsent'):
        if marker not in base:
            errors.append(f"layouts/_default/baseof.html: missing prepaint consent marker {marker}")
    for marker in ('resources.FromString "css/core.css"', 'resources.Concat "css/site.css"', 'fingerprint "sha384"'):
        if marker not in base:
            errors.append(f"layouts/_default/baseof.html: missing bundled CSS marker {marker}")

    seo_head = (LAYOUTS / "partials/seo_head.html").read_text(encoding="utf-8")
    mastodon_head_marker = '<link rel="me" href="https://infosec.exchange/@bhalaji">'
    if mastodon_head_marker not in seo_head:
        errors.append("SEO head must retain the Mastodon rel=me verification link")
    if '"https://infosec.exchange/@bhalaji"' not in seo_head:
        errors.append("Person structured data must retain Mastodon in sameAs")

    header = (LAYOUTS / "partials/site_header.html").read_text(encoding="utf-8")
    for marker in ('class="brand__monogram"', 'viewBox="0 0 40 40"', 'fill="currentColor"'):
        if marker not in header:
            errors.append(f"shared header must retain the canonical vector BK monogram marker {marker}")
    if "https://infosec.exchange/@bhalaji" in header:
        errors.append("shared header must not contain a redundant Mastodon verification backlink")

    # Primary navigation is intentionally canonical and stable across pages; do not
    # restore the old mix of homepage fragments and standalone destinations.
    canonical_url_markers = (
        '{{ $aboutURL := "about/" | relURL }}',
        '{{ $researchURL := "research/" | relURL }}',
        '{{ $outputsURL := "outputs/" | relURL }}',
        '{{ $experienceURL := "experience/" | relURL }}',
        '{{ $engagementURL := "engagement/" | relURL }}',
        '{{ $contactURL := "contact/" | relURL }}',
    )
    for marker in canonical_url_markers:
        if marker not in header:
            errors.append(f"shared header lost canonical primary destination marker {marker!r}")
    nav_markers = (
        '>About</a>',
        '>Research</a>',
        '>Outputs</a>',
        '>Experience</a>',
        '>Engagement</a>',
        '>Contact</a>',
    )
    nav_positions = [header.find(marker) for marker in nav_markers]
    if any(position < 0 for position in nav_positions):
        errors.append("shared header must retain About, Research, Outputs, Experience, Engagement, and Contact navigation")
    elif nav_positions != sorted(nav_positions):
        errors.append("shared header navigation must keep the primary information architecture in order")
    for obsolete in ('#research', '#outputs', '#experience', '#presentations', '#contact'):
        if obsolete in header:
            errors.append(f"shared header must not mix canonical navigation with homepage fragment {obsolete!r}")
    if 'href="{{ $root }}#trajectory"' in header:
        errors.append("shared header must keep doctoral trajectory within Research rather than primary navigation")
    if 'aria-current="page"' not in header:
        errors.append("shared header must expose current standalone pages to assistive technology")

    trajectory = (LAYOUTS / "partials/home_trajectory.html").read_text(encoding="utf-8")
    if ">Open research questions</h3>" not in trajectory:
        errors.append("doctoral collaboration block must use the reader-facing 'Open research questions' heading")
    if "Questions worth combining methods around" in trajectory:
        errors.append("doctoral collaboration block must not restore process-oriented collaboration wording")

    footer = (LAYOUTS / "partials/site_footer.html").read_text(encoding="utf-8")
    if "https://infosec.exchange/@bhalaji" in footer:
        errors.append("shared footer must not expose Mastodon after verification is established")

    about_layout = (LAYOUTS / "about/single.html").read_text(encoding="utf-8")
    for marker in ('class="about-fact-strip"', 'class="about-section__intro"', 'class="about-path__marker"', 'Professional path in chronological order'):
        if marker not in about_layout:
            errors.append(f"About template lost structural marker {marker!r}")
    if 'about-portrait__caption' in about_layout:
        errors.append("About portrait must not repeat name, role, and location already present in the page hierarchy")
    if 'about-program-grid' in about_layout:
        errors.append("About must not duplicate the homepage research-program card grid")
    about_content = (ROOT / "content/about.md").read_text(encoding="utf-8")
    if "bio:\n  - >-" not in about_content:
        errors.append("content/about.md: biography entries must remain explicit YAML block scalars")

    for required in (
        LAYOUTS / "outputs/list.html",
        LAYOUTS / "experience/list.html",
        LAYOUTS / "engagement/list.html",
        LAYOUTS / "contact/list.html",
    ):
        if not required.exists():
            errors.append(f"{required.relative_to(ROOT)}: primary destination template missing")

    outputs_layout = LAYOUTS / "outputs/list.html"
    if outputs_layout.exists():
        outputs = outputs_layout.read_text(encoding="utf-8")
        for marker in ('Research software', 'Intellectual property record', 'Peer-reviewed article'):
            if marker not in outputs:
                errors.append(f"outputs hub lost record type {marker!r}")
        if 'role="group" aria-label="Filter research outputs by type"' not in outputs:
            errors.append("outputs filter must retain a concise accessible group label")
        if outputs.count('data-output-filter=') != 5:
            errors.append("outputs filter must retain exactly five type choices")
        if "output-filter__label" in outputs or re.search(r">\s*Show\s*<", outputs, flags=re.IGNORECASE):
            errors.append("outputs filter must not reintroduce a redundant visible Show label")

    privacy = (LAYOUTS / "partials/privacy_controls.html").read_text(encoding="utf-8")
    banner = re.search(r'<section\b[^>]*data-privacy-banner[^>]*>', privacy)
    if not banner:
        errors.append("privacy notice must retain the shared data-privacy-banner element")
    elif re.search(r'\bhidden\b', banner.group(0)):
        errors.append("privacy notice must render from the prepaint consent state, not reveal later from deferred JavaScript")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Template audit passed: {len(templates)} Hugo templates checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
