#!/usr/bin/env python3
"""Confirm that the canonical domain serves the exact deployed Git commit."""
from __future__ import annotations

import argparse
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


def cache_busted(url: str, nonce: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["release_check"] = nonce
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def fetch_text(url: str, nonce: str) -> str:
    request = Request(
        cache_busted(url, nonce),
        headers={
            "User-Agent": "BhalajiPortfolioReleaseCheck/1.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urlopen(request, timeout=25) as response:
        if int(response.status) != 200:
            raise RuntimeError(f"HTTP {response.status}")
        return response.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("expected_sha")
    parser.add_argument("--attempts", type=int, default=18)
    parser.add_argument("--delay", type=float, default=10.0)
    args = parser.parse_args()

    url = urljoin(args.base_url.rstrip("/") + "/", "robots.txt")
    marker = f"# Release commit: {args.expected_sha}"
    last_error = "marker not observed"

    for attempt in range(1, args.attempts + 1):
        nonce = f"{int(time.time())}-{attempt}"
        try:
            body = fetch_text(url, nonce)
            if marker in body:
                print(f"Exact release marker verified for {args.expected_sha}")
                return 0
            last_error = f"expected marker {marker!r} not present"
        except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
            last_error = str(exc)
        print(f"Attempt {attempt}/{args.attempts} not ready: {last_error}")
        if attempt < args.attempts:
            time.sleep(args.delay)

    print(f"Exact release marker verification failed: {last_error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
