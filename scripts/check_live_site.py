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
        "/media/bk-safari-tab-20260730-1.png",
        "/media/bk-safari-touch-20260730-1.png",
    ],
    "research/": ["Resolve structure under stimuli", "Translate reproducibly"],
    "robots.txt": ["OAI-SearchBot", "Claude-SearchBot"],
    "sitemap.xml": ["<urlset"],
}

EXPECTED_BINARY = {
    "media/bk-safari-tab-20260730-1.png": {
        "content_type": "image/png",
        "sha256": "4d0110c27d45cbe48418b8a84d5871de971b6839ebddf8da552e27c74b343b3d",
    },
    "media/bk-safari-touch-20260730-1.png": {
        "content_type": "image/png",
        "sha256": "9208d9b32b7774b87ce7da8d00cebaf09a600f7a6cb3a59af14ca5ea75119233",
    },
}


def fetch(url: str) -> tuple[int, str, bytes]:
    req = Request(
        url,
        headers={
            "User-Agent": "BhalajiPortfolioDeployCheck/1.1",
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
