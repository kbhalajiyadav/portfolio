#!/usr/bin/env python3
"""Verify that the newly deployed portfolio is serving the intended release."""
from __future__ import annotations

import argparse
import hashlib
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

EXPECTED_TEXT = {
    "": [
        "A material that changes color is easy to make",
        "Ph.D. student",
        "/media/bk-monogram-unified-20260730-2.svg",
        "/media/bk-tab-64-20260730-2.png",
        "/media/bk-touch-180-20260730-2.png",
    ],
    "research/": ["Resolve structure under stimuli", "Translate reproducibly"],
    "robots.txt": ["OAI-SearchBot", "Claude-SearchBot"],
    "sitemap.xml": ["<urlset"],
}

EXPECTED_BINARY = {
    "media/bk-monogram-unified-20260730-2.svg": {
        "content_type": "image/svg+xml",
        "sha256": "be81e244ac7c634d5a2707290f859af8965f712843f724852097390788d0d090",
    },
    "media/bk-tab-64-20260730-2.png": {
        "content_type": "image/png",
        "sha256": "21a108bc2c1175fa304e70b92c706176cdd0084936e47a0f2a3ab48baf463223",
    },
    "media/bk-touch-180-20260730-2.png": {
        "content_type": "image/png",
        "sha256": "0f8cd19f18d87a9d3d90f16c758f289ac1021aaa6a1d1bb1342d27d9c3f51fc4",
    },
    "media/bk-favicon-20260730-2.ico": {
        "content_type": "image/vnd.microsoft.icon",
        "sha256": "e5762c12fe0acaa781905df645dc420d2d63fc19b878f0ca5a68215d5931069d",
    },
}


def fetch(url: str) -> tuple[int, str, bytes]:
    req = Request(
        url,
        headers={
            "User-Agent": "BhalajiPortfolioDeployCheck/1.2",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urlopen(req, timeout=20) as response:
        content_type = response.headers.get_content_type()
        return int(response.status), content_type, response.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay", type=float, default=10.0)
    args = parser.parse_args()
    base = args.base_url.rstrip("/") + "/"
    last_error = ""

    for attempt in range(1, args.attempts + 1):
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

        for path, expected in EXPECTED_BINARY.items():
            url = urljoin(base, path)
            try:
                status, content_type, raw = fetch(url)
                if status != 200:
                    errors.append(f"{url}: HTTP {status}")
                if content_type != expected["content_type"]:
                    errors.append(
                        f"{url}: content type {content_type!r}, expected {expected['content_type']!r}"
                    )
                digest = hashlib.sha256(raw).hexdigest()
                if digest != expected["sha256"]:
                    errors.append(
                        f"{url}: SHA-256 {digest}, expected {expected['sha256']}"
                    )
            except (URLError, HTTPError, TimeoutError) as exc:
                errors.append(f"{url}: {exc}")

        if not errors:
            print(f"Live deployment smoke test passed for {base}")
            return 0

        last_error = "; ".join(errors)
        print(f"Attempt {attempt}/{args.attempts} not ready: {last_error}")
        if attempt < args.attempts:
            time.sleep(args.delay)

    print(f"Live deployment smoke test failed: {last_error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
