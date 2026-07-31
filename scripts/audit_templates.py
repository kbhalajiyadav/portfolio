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
    consent_markers = (
        'class="no-js" data-analytics-consent="unset"',
        "<script data-consent-bootstrap>",
        "window.localStorage.getItem(key)",
        "root.dataset.analyticsConsent = state",
        "root.classList.replace('no-js', 'js')",
    )
    for marker in consent_markers:
        if marker not in base:
            errors.append(f"shared template must retain pre-paint consent marker {marker!r}")
    if base.find("<script data-consent-bootstrap>") > base.find('rel="stylesheet"'):
        errors.append("consent-state bootstrap must run before the stylesheet can paint")
    privacy = (LAYOUTS / "partials/privacy_controls.html").read_text(encoding="utf-8")
    if "data-privacy-banner hidden" in privacy:
        errors.append("privacy notice must not rely on delayed JavaScript insertion for first-time visitors")
    for marker in ("<noscript>", "Analytics remains disabled because JavaScript is unavailable."):
        if marker not in privacy:
            errors.append(f"privacy controls must retain no-JavaScript fallback marker {marker!r}")
    header = (LAYOUTS / "partials/site_header.html").read_text(encoding="utf-8")
    for marker in ('class="brand__monogram"', 'viewBox="0 0 40 40"', 'fill="currentColor"'):
        if marker not in header:
            errors.append(f"shared header must retain the canonical vector BK monogram marker {marker}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Template audit passed: {len(templates)} Hugo templates checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
