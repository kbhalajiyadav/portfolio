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
    nav_markers = (
        'class="nav-about',
        'href="{{ $root }}#research"',
        'href="{{ $root }}#outputs"',
        'href="{{ $root }}#trajectory"',
        'href="{{ $root }}#experience"',
        'href="{{ $root }}#presentations">Engagement',
        'class="nav-contact" href="{{ $root }}#contact"',
    )
    nav_positions = [header.find(marker) for marker in nav_markers]
    if any(position < 0 for position in nav_positions):
        errors.append("shared header must retain About plus the complete homepage section navigation")
    elif nav_positions != sorted(nav_positions):
        errors.append("shared header navigation must keep About separate and homepage anchors in scroll order")
    if 'aria-current="page"' not in header:
        errors.append("shared header must expose the current About page to assistive technology")
    footer = (LAYOUTS / "partials/site_footer.html").read_text(encoding="utf-8")
    if "https://infosec.exchange/@bhalaji" in footer:
        errors.append("shared footer must not expose Mastodon after verification is established")
    about_layout = (LAYOUTS / "about/single.html").read_text(encoding="utf-8")
    for marker in ('class="about-fact-strip"', 'class="about-section__intro"', 'class="about-path__marker"', 'Professional path in chronological order'):
        if marker not in about_layout:
            errors.append(f"About template lost structural marker {marker!r}")
    if 'about-portrait__caption' in about_layout:
        errors.append("About portrait must not repeat name, role, and location already present in the page hierarchy")
    about_content = (ROOT / "content/about.md").read_text(encoding="utf-8")
    if "bio:\n  - >-" not in about_content:
        errors.append("content/about.md: biography entries must remain explicit YAML block scalars")
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
