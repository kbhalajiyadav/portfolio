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
        "A material that changes color is easy to make",
        "Ph.D. student",
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
        "Chemical engineering, regulated practice, and research metrology",
        "Profiles and records",
        "Collaboration and methods exchange",
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
    "project/optical-metrology/": [
        "Optical Metrology for Mechanochromic Textiles",
        "Measurement workflow",
        "Evidence boundary",
    ],
    "research/": ["Resolve structure under stimuli", "Translate reproducibly"],
    "robots.txt": ["OAI-SearchBot", "Claude-SearchBot", "Microsoft Clarity project xuo3lvzchr"],
    "sitemap.xml": ["<urlset", "/about/"],
    "site.webmanifest": ["/icon-192.png", "/icon-512.png", "/favicon.svg"],
}

EXPECTED_RUNTIME_TEXT = [
    "https://www.clarity.ms/tag/",
    "xuo3lvzchr",
    "consentv2",
    "analytics_Storage",
    "bhalaji.analyticsConsent.v1",
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

# These paths are expected to disappear eventually, but CDN or browser-edge caches
# may continue serving them after a successful Pages deployment. They are therefore
# reported as cleanup warnings, not used as release-blocking evidence.
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
            "User-Agent": "BhalajiPortfolioDeployCheck/2.1",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urlopen(request, timeout=25) as response:
        return int(response.status), response.headers.get_content_type(), response.read()


def normalize_optional_attribute_quotes(body: str) -> str:
    """Normalize standards-valid unquoted href/src values for stable marker checks."""
    return re.sub(
        r"\b(href|src)=([^\s\"'=<>`]+)",
        r'\1="\2"',
        body,
        flags=re.IGNORECASE,
    )


def extract_attribute(tag: str, name: str) -> str | None:
    """Return a quoted or unquoted HTML attribute value from one start tag."""
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
        for tag in re.findall(r"<a\b[^>]*>", body, flags=re.IGNORECASE):
            if extract_attribute(tag, "href") != MASTODON_PROFILE:
                continue
            rel = (extract_attribute(tag, "rel") or "").split()
            if "me" in rel:
                matched = True
                break
        if not matched:
            errors.append(f"{home_url}: missing Mastodon rel=me link to {MASTODON_PROFILE}")
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
                errors.append(f"{runtime_url}: missing deferred analytics marker {needle!r}")
    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        errors.append(f"{home_url}: {exc}")
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
