#!/usr/bin/env python3
"""Verify that the deployed portfolio is serving the intended release."""
from __future__ import annotations

import argparse
import hashlib
import struct
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

EXPECTED_TEXT = {
    "": [
        "A material that changes color is easy to make",
        "Ph.D. student",
        "/favicon.svg?v=20260730-6",
        "/media/bk-browser-32-20260730-v6.png",
        "/media/bk-browser-20260730-v6.ico",
        "/media/bk-apple-touch-20260730-v6.png",
        "Rights",
        "All rights reserved",
    ],
    "brand-use/": [
        "Rights and permitted use",
        "No license is granted",
        "BK monogram",
    ],
    "research/": ["Resolve structure under stimuli", "Translate reproducibly"],
    "robots.txt": ["OAI-SearchBot", "Claude-SearchBot"],
    "sitemap.xml": ["<urlset"],
    "site.webmanifest": [
        "/media/bk-app-192-20260730-v6.png",
        "/media/bk-app-512-20260730-v6.png",
        "/media/bk-monogram-canonical-20260730.svg",
    ],
}

SVG_HASHES = {
    "media/bk-monogram-canonical-20260730.svg": "fa01ced619c53e23288298bbda048f4685452b86e0e72b6b25f9e695190893c9",
    "favicon.svg": "fa01ced619c53e23288298bbda048f4685452b86e0e72b6b25f9e695190893c9",
}

PNG_SIZES = {
    "media/bk-browser-32-20260730-v6.png": (32, 32),
    "media/bk-apple-touch-20260730-v6.png": (180, 180),
    "media/bk-app-192-20260730-v6.png": (192, 192),
    "media/bk-app-512-20260730-v6.png": (512, 512),
}

ICO_PATH = "media/bk-browser-20260730-v6.ico"

REMOVED_PATHS = [
    "favicon.ico",
    "media/bk-safari-tab-20260730-1.png",
    "media/bk-safari-touch-20260730-1.png",
    "media/bk-monogram.svg",
    "media/bk-monogram-192.png",
    "media/bk-monogram-512.png",
    "media/bk-favicon-20260729-3.ico",
    "media/og-card.png",
]


def fetch(url: str) -> tuple[int, str, bytes]:
    request = Request(
        url,
        headers={
            "User-Agent": "BhalajiPortfolioDeployCheck/1.5",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urlopen(request, timeout=20) as response:
        return int(response.status), response.headers.get_content_type(), response.read()


def validate_release(base: str) -> list[str]:
    errors: list[str] = []

    for path, needles in EXPECTED_TEXT.items():
        url = urljoin(base, path)
        try:
            status, _content_type, raw = fetch(url)
            body = raw.decode("utf-8", errors="replace")
            if status != 200:
                errors.append(f"{url}: HTTP {status}")
            for needle in needles:
                if needle not in body:
                    errors.append(f"{url}: missing release marker {needle!r}")
        except (URLError, HTTPError, TimeoutError) as exc:
            errors.append(f"{url}: {exc}")

    for path, expected_hash in SVG_HASHES.items():
        url = urljoin(base, path)
        try:
            status, content_type, raw = fetch(url)
            if status != 200:
                errors.append(f"{url}: HTTP {status}")
            if content_type != "image/svg+xml":
                errors.append(f"{url}: content type {content_type!r}, expected 'image/svg+xml'")
            digest = hashlib.sha256(raw).hexdigest()
            if digest != expected_hash:
                errors.append(f"{url}: SHA-256 {digest}, expected {expected_hash}")
        except (URLError, HTTPError, TimeoutError) as exc:
            errors.append(f"{url}: {exc}")

    for path, expected_size in PNG_SIZES.items():
        url = urljoin(base, path)
        try:
            status, content_type, raw = fetch(url)
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
        except (URLError, HTTPError, TimeoutError) as exc:
            errors.append(f"{url}: {exc}")

    ico_url = urljoin(base, ICO_PATH)
    try:
        status, content_type, raw = fetch(ico_url)
        if status != 200:
            errors.append(f"{ico_url}: HTTP {status}")
        if content_type not in {"image/vnd.microsoft.icon", "image/x-icon", "application/octet-stream"}:
            errors.append(f"{ico_url}: unexpected content type {content_type!r}")
        if len(raw) < 6:
            errors.append(f"{ico_url}: truncated ICO")
        else:
            reserved, kind, count = struct.unpack("<HHH", raw[:6])
            if (reserved, kind) != (0, 1) or count < 4:
                errors.append(f"{ico_url}: invalid ICO directory")
    except (URLError, HTTPError, TimeoutError) as exc:
        errors.append(f"{ico_url}: {exc}")

    for path in REMOVED_PATHS:
        url = urljoin(base, path)
        try:
            status, _content_type, _raw = fetch(url)
            if status != 404:
                errors.append(f"{url}: obsolete asset still served with HTTP {status}")
        except HTTPError as exc:
            if exc.code != 404:
                errors.append(f"{url}: unexpected HTTP {exc.code}")
        except (URLError, TimeoutError) as exc:
            errors.append(f"{url}: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay", type=float, default=10.0)
    args = parser.parse_args()

    base = args.base_url.rstrip("/") + "/"
    last_errors: list[str] = []
    for attempt in range(1, args.attempts + 1):
        last_errors = validate_release(base)
        if not last_errors:
            print(f"Live deployment smoke test passed for {base}")
            return 0
        print(f"Attempt {attempt}/{args.attempts} not ready: {'; '.join(last_errors)}")
        if attempt < args.attempts:
            time.sleep(args.delay)

    print(f"Live deployment smoke test failed: {'; '.join(last_errors)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
