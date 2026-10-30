#!/usr/bin/env python3
"""Verify that the deployed portfolio is serving the intended release."""
from __future__ import annotations

import argparse
import hashlib
import re
import struct
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

EXPECTED_TEXT = {
    "": [
        "Making material response measurable and interpretable.",
        "Soft matter",
        "Current question",
        "Recent research, at a glance.",
        "Substrate Enhanced Mechanochromic Sensitivity in Stimuli Response Textiles",
        "Current doctoral research",
        "Liquid crystals as a model system for how processing shapes structure.",
        "What a peel trace can reveal.",
        "Comparing strength, stability, and deformation tolerance",
        "Research questions",
        "Research statement",
        "Ph.D. student",
        "Browse all research outputs",
        'href="/favicon.svg"',
        'href="/favicon-48.png"',
        'href="/favicon.ico"',
        'href="/apple-touch-icon.png"',
        'href="/site.webmanifest"',
        "data-site-runtime",
        "Privacy choices",
        "Rights",
        "All rights reserved",
    ],
    "about/": [
        "About Bhalaji Yadav Kantepalle",
        "Research built around measurable response",
        "From chemical engineering to doctoral research",
        "VCU Soft Functional Materials Lab",
        "Christina Tang, Ph.D.",
        "Research profiles and institutional links",
        "Research questions open to collaboration",
    ],
    "research/": [
        "Resolve structure under stimuli",
        "Translate reproducibly",
        "Connected research outputs",
        "Open research questions",
        "Small-molecule cholesteric mixtures",
        "application-specific validation before performance claims.",
    ],
    "research-statement/": [
        "Research Statement",
        "Small-molecule cholesteric mixtures",
        "Computational infrared thermography",
    ],
    "outputs/": [
        "Research Outputs",
        "Peer-reviewed article",
        "Research software",
        "Intellectual property record",
    ],
    "experience/": [
        "Experience & Education",
        "Professional and research experience",
        "Education",
        "Research training",
    ],
    "engagement/": [
        "Engagement",
        "Presentations and research events",
        "Teaching and research guidance",
        "Service and review",
    ],
    "contact/": [
        "Collaboration and methods exchange",
        "contact@bhalaji.com",
        "VCU Soft Functional Materials Lab",
    ],
    "privacy/": [
        "Privacy and analytics notice",
        "Microsoft Clarity",
        "The Microsoft Clarity script is not loaded before",
        "advertising storage denied",
    ],
    "brand-use/": [
        "Copyright and trademark notice",
        "does not place its contents in the public domain",
        "BK monogram",
    ],
    "project/peel-trace-evaluation/": [
        "https://doi.org/10.5281/zenodo.20301242",
        "Recommended citation",
        "Example analysis output",
    ],
    "publication/masters-thesis/": [
        "https://doi.org/10.25772/f6wc-rh09",
        "Manuscript availability",
    ],
    "project/optical-metrology/": [
        "Optical Metrology for Mechanochromic Textiles",
        "Measurement workflow",
        "Presentations and outputs",
        "VCU Engineering Graduate",
        "29th VCU Graduate Student Research",
    ],
    "project/quantitative-thermal-imaging/": [
        "Intellectual-property status",
        "Patent pending",
        "Technology overview",
        "VCU Tech # TAN-26-099",
        "What patent pending means",
    ],
    "robots.txt": ["OAI-SearchBot", "Claude-SearchBot", "Microsoft Clarity project xuo3lvzchr"],
    "sitemap.xml": ["<urlset", "/about/", "/research/", "/outputs/", "/experience/", "/engagement/", "/contact/"],
    "site.webmanifest": ["/icon-192.png", "/icon-512.png", "/favicon.svg"],
}

EXPECTED_RUNTIME_TEXT = [
    "https://www.clarity.ms/tag/",
    "xuo3lvzchr",
    "consentv2",
    "analytics_Storage",
    "bhalaji.analyticsConsent.v1",
    "copied to clipboard",
]

MASTODON_PROFILE = "https://infosec.exchange/@bhalaji"

SVG_HASHES = {
    "media/bk-monogram-canonical-20260730.svg": "fa01ced619c53e23288298bbda048f4685452b86e0e72b6b25f9e695190893c9",
    "favicon.svg": "fa01ced619c53e23288298bbda048f4685452b86e0e72b6b25f9e695190893c9",
}

PNG_SIZES = {
    "favicon-48.png": (48, 48),
    "apple-touch-icon.png": (180, 180),
    "icon-192.png": (192, 192),
    "icon-512.png": (512, 512),
    "media/bk-browser-32-20260730-v6.png": (32, 32),
    "media/bk-apple-touch-20260730-v6.png": (180, 180),
    "media/bk-app-192-20260730-v6.png": (192, 192),
    "media/bk-app-512-20260730-v6.png": (512, 512),
}

ICO_PATHS = ["favicon.ico", "media/bk-browser-20260730-v6.ico"]
OBSOLETE_CACHE_PATHS = [
    "media/bk-safari-tab-20260730-1.png",
    "media/bk-safari-touch-20260730-1.png",
    "media/bk-monogram.svg",
    "media/bk-monogram-192.png",
    "media/bk-monogram-512.png",
    "media/bk-favicon-20260729-3.ico",
    "media/og-card.png",
]


def cache_busted(url: str, nonce: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["deploy_check"] = nonce
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def fetch(url: str, nonce: str) -> tuple[int, str, bytes]:
    request = Request(
        cache_busted(url, nonce),
        headers={
            "User-Agent": "BhalajiPortfolioDeployCheck/2.4",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urlopen(request, timeout=25) as response:
        return int(response.status), response.headers.get_content_type(), response.read()


def normalize_optional_attribute_quotes(body: str) -> str:
    return re.sub(
        r"\b(href|src)=([^\s\"'=<>`]+)",
        r'\1="\2"',
        body,
        flags=re.IGNORECASE,
    )


def extract_attribute(tag: str, name: str) -> str | None:
    match = re.search(
        rf"\b{re.escape(name)}=(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
        tag,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return next((value for value in match.groups() if value is not None), None)


def validate_mastodon_rel_me(base: str, nonce: str) -> list[str]:
    errors: list[str] = []
    home_url = urljoin(base, "")
    try:
        status, _content_type, raw = fetch(home_url, nonce)
        if status != 200:
            return [f"{home_url}: HTTP {status}"]
        body = raw.decode("utf-8", errors="replace")
        matched = False
        for tag in re.findall(r"<(?:a|link)\b[^>]*>", body, flags=re.IGNORECASE):
            if extract_attribute(tag, "href") != MASTODON_PROFILE:
                continue
            rel = (extract_attribute(tag, "rel") or "").split()
            if "me" in rel:
                matched = True
                break
        if not matched:
            errors.append(f"{home_url}: missing Mastodon rel=me verification link to {MASTODON_PROFILE}")
    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        errors.append(f"{home_url}: {exc}")
    return errors


def validate_runtime(base: str, nonce: str) -> list[str]:
    errors: list[str] = []
    home_url = urljoin(base, "")
    try:
        status, _content_type, raw = fetch(home_url, nonce)
        body = raw.decode("utf-8", errors="replace")
        if status != 200:
            return [f"{home_url}: HTTP {status}"]
        if "https://www.clarity.ms/tag/" in body:
            errors.append(f"{home_url}: Clarity must not load in initial HTML before consent")
        tags = re.findall(r"<script\b[^>]*data-site-runtime[^>]*>", body, re.IGNORECASE)
        if len(tags) != 1:
            errors.append(f"{home_url}: expected one data-site-runtime script, found {len(tags)}")
            return errors
        source = extract_attribute(tags[0], "src")
        if not source:
            errors.append(f"{home_url}: data-site-runtime script has no src")
            return errors
        runtime_url = urljoin(base, source)
        runtime_status, runtime_type, runtime_raw = fetch(runtime_url, nonce)
        runtime = runtime_raw.decode("utf-8", errors="replace")
        if runtime_status != 200:
            errors.append(f"{runtime_url}: HTTP {runtime_status}")
        if runtime_type not in {"application/javascript", "text/javascript", "text/plain"}:
            errors.append(f"{runtime_url}: unexpected content type {runtime_type!r}")
        for needle in EXPECTED_RUNTIME_TEXT:
            if needle not in runtime:
                errors.append(f"{runtime_url}: missing deferred runtime marker {needle!r}")
    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        errors.append(f"{home_url}: {exc}")
    return errors


def validate_homepage_styles(base: str, body: str, nonce: str) -> list[str]:
    """Verify the stylesheet actually served with the homepage contains the mobile-gap fix."""
    errors: list[str] = []
    stylesheet_links = []
    for tag in re.findall(r"<link\b[^>]*>", body, flags=re.IGNORECASE):
        if "stylesheet" not in (extract_attribute(tag, "rel") or "").split():
            continue
        href = extract_attribute(tag, "href")
        if href:
            stylesheet_links.append(urljoin(base, href))
    if len(stylesheet_links) != 1:
        return [f"homepage must reference one versioned stylesheet, found {len(stylesheet_links)}"]
    url = stylesheet_links[0]
    try:
        status, _content_type, raw = fetch(url, nonce)
        if status != 200:
            return [f"homepage stylesheet {url} returned HTTP {status}"]
        css = raw.decode("utf-8", errors="replace")
        required = (
            (r"#research\s*>\s*\.section-head\s*\{[^}]*margin-bottom\s*:\s*(?:0?\.7)rem", "compact homepage research heading gap"),
            (r"#research\s*>\s*\.research-signature\s*\{[^}]*margin-top\s*:\s*0(?:[;}])", "zero schematic top gap"),
        )
        for pattern, label in required:
            if not re.search(pattern, css):
                errors.append(f"homepage stylesheet {url} is missing {label}")
    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        errors.append(f"homepage stylesheet {url}: {exc}")
    return errors


def validate_release(base: str, nonce: str) -> list[str]:
    errors: list[str] = []

    for path, needles in EXPECTED_TEXT.items():
        url = urljoin(base, path)
        try:
            status, _content_type, raw = fetch(url, nonce)
            body = normalize_optional_attribute_quotes(raw.decode("utf-8", errors="replace"))
            if status != 200:
                errors.append(f"{url}: HTTP {status}")
            for needle in needles:
                if needle not in body:
                    errors.append(f"{url}: missing release marker {needle!r}")
            if not path:
                for obsolete in ("From stimulus to structure to measurement.", "Schematic; no quantitative data are implied."):
                    if obsolete in body:
                        errors.append(f"{url}: stale homepage copy remains visible: {obsolete!r}")
                errors.extend(validate_homepage_styles(base, body, nonce))
        except (URLError, HTTPError, TimeoutError, OSError) as exc:
            errors.append(f"{url}: {exc}")

    errors.extend(validate_mastodon_rel_me(base, nonce))
    errors.extend(validate_runtime(base, nonce))

    for path, expected_hash in SVG_HASHES.items():
        url = urljoin(base, path)
        try:
            status, content_type, raw = fetch(url, nonce)
            if status != 200:
                errors.append(f"{url}: HTTP {status}")
            if content_type not in {"image/svg+xml", "text/plain", "application/octet-stream"}:
                errors.append(f"{url}: unexpected SVG content type {content_type!r}")
            digest = hashlib.sha256(raw).hexdigest()
            if digest != expected_hash:
                errors.append(f"{url}: SHA-256 {digest}, expected {expected_hash}")
        except (URLError, HTTPError, TimeoutError, OSError) as exc:
            errors.append(f"{url}: {exc}")

    for path, expected_size in PNG_SIZES.items():
        url = urljoin(base, path)
        try:
            status, content_type, raw = fetch(url, nonce)
            if status != 200:
                errors.append(f"{url}: HTTP {status}")
            if content_type != "image/png":
                errors.append(f"{url}: content type {content_type!r}, expected 'image/png'")
            if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 24:
                errors.append(f"{url}: invalid PNG signature")
            else:
                size = struct.unpack(">II", raw[16:24])
                if size != expected_size:
                    errors.append(f"{url}: dimensions {size}, expected {expected_size}")
        except (URLError, HTTPError, TimeoutError, OSError) as exc:
            errors.append(f"{url}: {exc}")

    # Browser requests typically use the plain URL, not our cache-busted probe.
    # Verify the root icon both ways to catch a stale CDN 404 that a query might mask.
    touch_url = urljoin(base, "apple-touch-icon.png")
    try:
        with urlopen(Request(touch_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25) as response:
            if response.status != 200:
                errors.append(f"{touch_url}: direct browser request returned HTTP {response.status}")
            else:
                png = response.read()
                if len(png) < 24 or png[:8] != bytes.fromhex("89504e470d0a1a0a") or struct.unpack(">II", png[16:24]) != (180, 180):
                    errors.append(f"{touch_url}: direct browser request returned an invalid 180px icon")
    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        errors.append(f"{touch_url}: direct browser request failed: {exc}")

    direct_icon_url = urljoin(base, "favicon.ico")
    try:
        with urlopen(Request(direct_icon_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25) as response:
            if response.status != 200:
                errors.append(f"{direct_icon_url}: direct browser request returned HTTP {response.status}")
            else:
                raw_icon = response.read()
                if len(raw_icon) < 6 or struct.unpack("<HHH", raw_icon[:6])[:2] != (0, 1):
                    errors.append(f"{direct_icon_url}: direct browser request returned invalid ICO bytes")
    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        errors.append(f"{direct_icon_url}: direct browser request failed: {exc}")

    for path in ICO_PATHS:
        url = urljoin(base, path)
        try:
            status, content_type, raw = fetch(url, nonce)
            if status != 200:
                errors.append(f"{url}: HTTP {status}")
            if content_type not in {"image/vnd.microsoft.icon", "image/x-icon", "application/octet-stream"}:
                errors.append(f"{url}: unexpected content type {content_type!r}")
            if len(raw) < 6:
                errors.append(f"{url}: truncated ICO")
            else:
                reserved, kind, count = struct.unpack("<HHH", raw[:6])
                if (reserved, kind) != (0, 1) or count < 4:
                    errors.append(f"{url}: invalid ICO directory")
        except (URLError, HTTPError, TimeoutError, OSError) as exc:
            errors.append(f"{url}: {exc}")

    return errors


def report_obsolete_cache_paths(base: str, nonce: str) -> None:
    warnings: list[str] = []
    for path in OBSOLETE_CACHE_PATHS:
        url = urljoin(base, path)
        try:
            status, _content_type, _raw = fetch(url, nonce)
            if status != 404:
                warnings.append(f"{url}: obsolete asset remains cached with HTTP {status}")
        except HTTPError as exc:
            if exc.code != 404:
                warnings.append(f"{url}: unexpected HTTP {exc.code}")
        except (URLError, TimeoutError, OSError) as exc:
            warnings.append(f"{url}: cleanup check unavailable: {exc}")
    for warning in warnings:
        print(f"WARNING: {warning}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--attempts", type=int, default=18)
    parser.add_argument("--delay", type=float, default=10.0)
    args = parser.parse_args()

    base = args.base_url.rstrip("/") + "/"
    last_errors: list[str] = []
    for attempt in range(1, args.attempts + 1):
        nonce = f"{int(time.time())}-{attempt}"
        last_errors = validate_release(base, nonce)
        if not last_errors:
            report_obsolete_cache_paths(base, nonce)
            print(f"Live deployment smoke test passed for {base}")
            return 0
        print(f"Attempt {attempt}/{args.attempts} not ready: {'; '.join(last_errors)}")
        if attempt < args.attempts:
            time.sleep(args.delay)

    print(f"Live deployment smoke test failed: {'; '.join(last_errors)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
