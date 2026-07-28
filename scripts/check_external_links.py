#!/usr/bin/env python3
"""Check genuinely external links without testing unreleased same-site URLs.

Absolute links whose host matches the generated site's canonical host are internal.
They are validated by scripts/check_site.py against the freshly rendered ``public``
tree. This checker only contacts third-party domains, so a new same-site route does
not fail a pre-deployment build merely because the previous production release does
not contain it yet.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
import json
from pathlib import Path
import socket
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (compatible; BhalajiPortfolioLinkAudit/1.1; +https://bhalaji.com/)"
PERMANENT_FAILURES = {404, 410}
SOFT_STATUSES = {401, 403, 405, 406, 409, 418, 425, 429, 451, 999}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.canonicals: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            href = values.get("href")
            if href:
                self.links.append(href)
        elif tag == "link":
            rel = {part.lower() for part in str(values.get("rel", "")).split()}
            href = values.get("href")
            if "canonical" in rel and href:
                self.canonicals.append(href)


def normalized_origin(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None
    host = parsed.hostname.lower().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    port = parsed.port
    default_port = (parsed.scheme == "http" and port == 80) or (parsed.scheme == "https" and port == 443)
    port_text = "" if port is None or default_port else f":{port}"
    return f"{parsed.scheme.lower()}://{host}{port_text}"


def normalized_host(url: str) -> str | None:
    parsed = urlparse(url)
    if not parsed.hostname:
        return None
    host = parsed.hostname.lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


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
    parser.add_argument(
        "--site-origin",
        action="append",
        default=[],
        help="Origin treated as the generated site. May be repeated; otherwise inferred from canonical links.",
    )
    parser.add_argument("--strict-network", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=12.0)
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: generated site directory does not exist: {root}")
        return 1

    parsed_pages: list[tuple[Path, LinkParser]] = []
    canonical_origins: Counter[str] = Counter()
    for html in root.rglob("*.html"):
        parsed = LinkParser()
        parsed.feed(html.read_text(encoding="utf-8", errors="replace"))
        parsed_pages.append((html, parsed))
        for canonical in parsed.canonicals:
            origin = normalized_origin(canonical)
            if origin:
                canonical_origins[origin] += 1

    explicit_origins = {origin for value in args.site_origin if (origin := normalized_origin(value))}
    if explicit_origins:
        site_origins = explicit_origins
    elif canonical_origins:
        # A valid Hugo build should use one canonical origin. Accept every canonical
        # origin seen so diagnostics remain useful if a configuration error introduces two.
        site_origins = set(canonical_origins)
    else:
        site_origins = set()
        print("WARNING: no canonical site origin was found; all absolute HTTP links will be treated as external.")

    site_hosts = {host for origin in site_origins if (host := normalized_host(origin))}
    sources: dict[str, set[str]] = defaultdict(set)
    skipped_same_site: dict[str, set[str]] = defaultdict(set)

    for html, parsed in parsed_pages:
        relative_source = str(html.relative_to(root))
        for raw in parsed.links:
            url, _ = urldefrag(raw.strip())
            parsed_url = urlparse(url)
            if parsed_url.scheme not in {"http", "https"}:
                continue
            host = normalized_host(url)
            if host and host in site_hosts:
                skipped_same_site[url].add(relative_source)
                continue
            sources[url].add(relative_source)

    if site_origins:
        print("Same-site origins validated locally and excluded from network checks: " + ", ".join(sorted(site_origins)))
    print(f"Same-site absolute URLs skipped: {len(skipped_same_site)}")

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
    report.write_text(
        json.dumps(
            {
                "site_origins": sorted(site_origins),
                "same_site_urls_validated_locally": [
                    {"url": url, "sources": sorted(skipped_same_site[url])}
                    for url in sorted(skipped_same_site)
                ],
                "checked_external": len(results),
                "results": results,
            },
            indent=2,
        )
        + "\n"
    )

    hard = [result for result in results if result["outcome"] == "error"]
    warnings = [result for result in results if result["outcome"] == "warning"]
    if hard or (args.strict_network and warnings):
        print(f"External-link audit failed: {len(hard)} permanent failures; {len(warnings)} warnings.")
        return 1
    print(
        "External-link audit passed: "
        f"{len(results)} third-party URLs; {len(warnings)} provider/network warnings; "
        f"{len(skipped_same_site)} same-site URLs already validated locally."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
