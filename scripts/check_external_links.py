#!/usr/bin/env python3
"""Check external links without confusing provider bot-blocking with broken records."""
from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
import json
from pathlib import Path
import socket
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (compatible; BhalajiPortfolioLinkAudit/1.0; +https://bhalaji.com/)"
PERMANENT_FAILURES = {404, 410}
SOFT_STATUSES = {401, 403, 405, 406, 409, 418, 425, 429, 451}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def request(url: str, method: str, timeout: float) -> tuple[int | None, str]:
    req = Request(
        url,
        method=method,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        },
    )
    try:
        with urlopen(req, timeout=timeout, context=ssl.create_default_context()) as response:
            return int(response.status), response.geturl()
    except HTTPError as exc:
        return int(exc.code), exc.geturl() or url
    except (URLError, TimeoutError, socket.timeout, ssl.SSLError) as exc:
        return None, str(exc)


def check(url: str, timeout: float) -> dict[str, object]:
    status, detail = request(url, "HEAD", timeout)
    if status in {None, 400, 405, 501}:
        status, detail = request(url, "GET", timeout)
    elif status and status >= 400 and status not in PERMANENT_FAILURES:
        # Many scholarly/profile providers reject HEAD while allowing a browser-style GET.
        get_status, get_detail = request(url, "GET", timeout)
        if get_status is not None and (status is None or get_status < status):
            status, detail = get_status, get_detail
    if status is None:
        outcome = "warning"
    elif 200 <= status < 400:
        outcome = "ok"
    elif status in SOFT_STATUSES or 500 <= status < 600:
        outcome = "warning"
    elif status in PERMANENT_FAILURES:
        outcome = "error"
    else:
        outcome = "warning"
    return {"url": url, "status": status, "outcome": outcome, "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default="public")
    parser.add_argument("--report", default="artifacts/external-links.json")
    parser.add_argument("--strict-network", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=12.0)
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: generated site directory does not exist: {root}")
        return 1

    sources: dict[str, set[str]] = defaultdict(set)
    for html in root.rglob("*.html"):
        parsed = LinkParser()
        parsed.feed(html.read_text(encoding="utf-8", errors="replace"))
        for raw in parsed.links:
            url, _ = urldefrag(raw.strip())
            if urlparse(url).scheme in {"http", "https"}:
                sources[url].add(str(html.relative_to(root)))

    ordered_urls = sorted(sources)
    results_by_url: dict[str, dict[str, object]] = {}
    workers = max(1, min(args.workers, 16))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check, url, args.timeout): url for url in ordered_urls}
        completed = 0
        for future in as_completed(futures):
            url = futures[future]
            completed += 1
            try:
                result = future.result()
            except Exception as exc:  # Defensive: one provider must not abort the report.
                result = {"url": url, "status": None, "outcome": "warning", "detail": repr(exc)}
            result["sources"] = sorted(sources[url])
            results_by_url[url] = result
            print(f"[{completed}/{len(ordered_urls)}] {str(result['outcome']).upper():7} {result['status'] or '-':>3} {url}")

    results = [results_by_url[url] for url in ordered_urls]
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"checked": len(results), "results": results}, indent=2) + "\n")

    hard = [result for result in results if result["outcome"] == "error"]
    warnings = [result for result in results if result["outcome"] == "warning"]
    if hard or (args.strict_network and warnings):
        print(f"External-link audit failed: {len(hard)} permanent failures; {len(warnings)} warnings.")
        return 1
    print(f"External-link audit passed: {len(results)} URLs; {len(warnings)} provider/network warnings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
