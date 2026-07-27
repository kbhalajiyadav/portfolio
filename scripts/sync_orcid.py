#!/usr/bin/env python3
"""Synchronize public journal-article metadata from an ORCID record."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_ORCID = "0000-0003-0551-6172"
DEFAULT_OUTPUT = Path("data/publication_sync.json")
ORCID_PATTERN = re.compile(r"^\d{4}-\d{4}-\d{4}-[\dX]{4}$")
PAPER_TYPES = {"journal-article"}


def nested_value(mapping: dict[str, Any] | None, *keys: str) -> Any:
    value: Any = mapping
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    doi = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix) :]
    return doi or None


def fetch_works(orcid: str) -> dict[str, Any]:
    url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.orcid+json",
            "User-Agent": "bhalaji-portfolio-publication-sync/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unable to retrieve the public ORCID works record: {exc}") from exc


def extract_doi(group: dict[str, Any]) -> str | None:
    external_ids = nested_value(group, "external-ids", "external-id") or []
    for external_id in external_ids:
        if str(external_id.get("external-id-type", "")).lower() == "doi":
            normalized = nested_value(external_id, "external-id-normalized", "value")
            return normalize_doi(normalized or external_id.get("external-id-value"))
    return None


def choose_summary(group: dict[str, Any]) -> dict[str, Any]:
    summaries = group.get("work-summary") or []
    if not summaries:
        return {}
    return max(
        summaries,
        key=lambda item: int(item.get("display-index") or 0),
    )


def transform(record: dict[str, Any], orcid: str) -> list[dict[str, str]]:
    works: list[dict[str, str]] = []
    for group in record.get("group") or []:
        summary = choose_summary(group)
        if summary.get("type") not in PAPER_TYPES:
            continue

        title = nested_value(summary, "title", "title", "value")
        if not title:
            continue

        doi = extract_doi(group)
        year = nested_value(summary, "publication-date", "year", "value")
        journal = nested_value(summary, "journal-title", "value")
        source_url = nested_value(summary, "url", "value")

        item: dict[str, str] = {
            "title": str(title).strip(),
            "type": str(summary.get("type")),
        }
        if year:
            item["year"] = str(year)
        if journal:
            item["journal"] = str(journal).strip()
        if doi:
            item["doi"] = doi
            item["url"] = f"https://doi.org/{doi}"
        elif source_url:
            item["url"] = str(source_url)

        works.append(item)

    works.sort(key=lambda item: (item.get("year", ""), item["title"]), reverse=True)
    return works


def load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def synchronize(orcid: str, output: Path) -> bool:
    record = fetch_works(orcid)
    works = transform(record, orcid)
    existing = load_existing(output)

    stable_payload = {
        "orcid": orcid,
        "profile_url": f"https://orcid.org/{orcid}",
        "source": "ORCID Anonymous API v3.0",
        "journal_article_count": len(works),
        "works": works,
    }
    existing_stable = (
        {key: existing.get(key) for key in stable_payload}
        if isinstance(existing, dict)
        else None
    )

    if existing_stable == stable_payload:
        print(f"ORCID publication metadata is already current ({len(works)} journal articles).")
        return False

    payload = {
        **stable_payload,
        "last_synced": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {output} with {len(works)} public journal articles.")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--orcid", default=DEFAULT_ORCID, help="ORCID iD to synchronize")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Generated Hugo data file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not ORCID_PATTERN.fullmatch(args.orcid):
        print(f"Invalid ORCID iD: {args.orcid}", file=sys.stderr)
        return 2
    try:
        synchronize(args.orcid, args.output)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
