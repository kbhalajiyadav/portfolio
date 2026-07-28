#!/usr/bin/env python3
"""Verify that the newly deployed portfolio is serving the intended release."""
from __future__ import annotations
import argparse, time
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

EXPECTED = {
    "": ["A material that changes color is easy to make", "Ph.D. student"],
    "research/": ["Resolve structure under stimuli", "Translate reproducibly"],
    "robots.txt": ["OAI-SearchBot", "Claude-SearchBot"],
    "sitemap.xml": ["<urlset"],
}

def fetch(url: str) -> tuple[int, str]:
    req = Request(url, headers={"User-Agent": "BhalajiPortfolioDeployCheck/1.0"})
    with urlopen(req, timeout=20) as response:
        return int(response.status), response.read().decode('utf-8', errors='replace')

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('base_url')
    parser.add_argument('--attempts', type=int, default=12)
    parser.add_argument('--delay', type=float, default=10.0)
    args = parser.parse_args()
    base = args.base_url.rstrip('/') + '/'
    last_error = ''
    for attempt in range(1, args.attempts + 1):
        errors = []
        for path, needles in EXPECTED.items():
            url = urljoin(base, path)
            try:
                status, body = fetch(url)
                if status != 200:
                    errors.append(f'{url}: HTTP {status}')
                for needle in needles:
                    if needle not in body:
                        errors.append(f'{url}: missing release marker {needle!r}')
            except (URLError, HTTPError, TimeoutError) as exc:
                errors.append(f'{url}: {exc}')
        if not errors:
            print(f'Live deployment smoke test passed for {base}')
            return 0
        last_error = '; '.join(errors)
        print(f'Attempt {attempt}/{args.attempts} not ready: {last_error}')
        if attempt < args.attempts:
            time.sleep(args.delay)
    print(f'Live deployment smoke test failed: {last_error}')
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
