#!/usr/bin/env python3
"""Alert when the portfolio's research-software version drifts from its public GitHub release."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    portfolio = yaml.safe_load((ROOT / "data" / "portfolio.yaml").read_text(encoding="utf-8"))
    software = portfolio["software"]
    expected = str(software["version"]).strip()
    repository = str(software["repository"]).rstrip("/")

    parsed = urlparse(repository)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.hostname != "github.com" or len(parts) != 2:
        print(f"ERROR: unsupported research software repository URL: {repository}", file=sys.stderr)
        return 1

    api = f"https://api.github.com/repos/{parts[0]}/{parts[1]}/releases?per_page=10"
    request = urllib.request.Request(
        api,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "bhalaji-portfolio-integrity/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            releases = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"ERROR: unable to check public research-software releases: {exc}", file=sys.stderr)
        return 1

    published = [item for item in releases if not item.get("draft")]
    if not published:
        print("ERROR: no public research-software release found", file=sys.stderr)
        return 1

    current = str(published[0].get("tag_name", "")).strip()
    if current != expected:
        print(
            "ERROR: research-software release drift detected: "
            f"portfolio={expected!r}, newest_public_release={current!r}. "
            "Review before changing the public portfolio.",
            file=sys.stderr,
        )
        return 1

    print(f"Research-software release is current: {expected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
