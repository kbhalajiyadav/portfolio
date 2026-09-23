#!/usr/bin/env python3
"""Check canonical facts shared across portfolio, CV, and publication metadata."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm_doi(value: str) -> str:
    match = DOI_RE.search(str(value))
    return match.group(0).lower().rstrip(".,;)") if match else ""


def norm_text(value: object) -> str:
    return " ".join(str(value).split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orcid-snapshot",
        type=Path,
        default=ROOT / "data" / "publication_sync.json",
        help="ORCID JSON snapshot to reconcile against the canonical portfolio.",
    )
    args = parser.parse_args()

    portfolio = load_yaml(ROOT / "data" / "portfolio.yaml")
    cv = load_yaml(ROOT / "data" / "cv.yaml")
    orcid = load_json(args.orcid_snapshot)
    errors: list[str] = []

    p_profile = portfolio["profile"]
    c_profile = cv["profile"]
    shared_profile = {
        "name": "name",
        "location": "location",
        "email": "email",
        "linkedin": "linkedin",
        "github": "github",
        "orcid": "orcid",
        "scholar": "scholar",
    }
    for p_key, c_key in shared_profile.items():
        if norm_text(p_profile.get(p_key)) != norm_text(c_profile.get(c_key)):
            errors.append(
                f"profile drift: portfolio.{p_key}={p_profile.get(p_key)!r} "
                f"!= cv.{c_key}={c_profile.get(c_key)!r}"
            )

    if "cv_version" in p_profile:
        errors.append("portfolio.profile.cv_version must not be manually maintained; PDF hash is the cache key")

    metric_by_label = {item["label"]: item for item in portfolio.get("metrics", [])}
    posters = metric_by_label.get("Research posters", {})
    if posters.get("source") != "presentations":
        errors.append("Research posters metric must be derived from presentations")
    actual_posters = sum(1 for item in portfolio.get("presentations", []) if item.get("kind") == "Poster")
    if actual_posters < 1:
        errors.append("no Poster records found for derived poster metric")

    stale_phrases = ("ongoing Summer 2026", "two ongoing student projects", "summer researchers on ongoing projects")
    serialized = (
        (ROOT / "data" / "portfolio.yaml").read_text(encoding="utf-8")
        + "\n"
        + (ROOT / "data" / "cv.yaml").read_text(encoding="utf-8")
    )
    for phrase in stale_phrases:
        if phrase.lower() in serialized.lower():
            errors.append(f"stale Summer 2026 status remains: {phrase!r}")

    portfolio_industry = {
        item["period"]: (norm_text(item["role"]), norm_text(item["organization"]))
        for item in portfolio.get("experience", [])
        if item.get("period") in {"May 2023–May 2024", "Oct 2022–Apr 2023"}
    }
    cv_industry = {
        item["period"]: (norm_text(item["role"]), norm_text(item["organization"]))
        for item in cv.get("industry_experience", [])
    }
    for period in ("May 2023–May 2024", "Oct 2022–Apr 2023"):
        if portfolio_industry.get(period) != cv_industry.get(period):
            errors.append(
                f"industry identity drift for {period}: "
                f"portfolio={portfolio_industry.get(period)!r}, cv={cv_industry.get(period)!r}"
            )

    p_software = portfolio.get("software", {})
    cv_software = (cv.get("research_software") or [{}])[0]
    if norm_text(p_software.get("version")) != norm_text(cv_software.get("version")):
        errors.append("research software version differs between portfolio and CV")
    if norm_doi(p_software.get("version_doi", "")) != norm_doi(cv_software.get("archive", "")):
        errors.append("research software archived DOI differs between portfolio and CV")

    portfolio_pubs = {
        norm_doi(item.get("doi", "")): norm_text(item.get("title", ""))
        for item in portfolio.get("publications", [])
    }
    if "" in portfolio_pubs:
        errors.append("portfolio publication missing DOI")
        portfolio_pubs.pop("", None)

    orcid_pubs = {
        norm_doi(item.get("doi", "")): norm_text(item.get("title", ""))
        for item in orcid.get("works", [])
        if item.get("type") == "journal-article"
    }
    if portfolio_pubs != orcid_pubs:
        missing = sorted(set(portfolio_pubs) - set(orcid_pubs))
        extra = sorted(set(orcid_pubs) - set(portfolio_pubs))
        mismatched = sorted(
            doi for doi in set(portfolio_pubs) & set(orcid_pubs)
            if portfolio_pubs[doi].casefold() != orcid_pubs[doi].casefold()
        )
        errors.append(
            "publication drift versus ORCID snapshot: "
            f"missing_from_orcid={missing}, extra_in_orcid={extra}, title_mismatch={mismatched}"
        )

    cv_dois = {norm_doi(item) for item in cv.get("publications", [])}
    cv_dois.discard("")
    if cv_dois != set(portfolio_pubs):
        errors.append(
            f"CV publication DOI set differs from portfolio: "
            f"cv={sorted(cv_dois)}, portfolio={sorted(portfolio_pubs)}"
        )

    if int(orcid.get("journal_article_count", -1)) != len(orcid_pubs):
        errors.append("ORCID journal_article_count does not equal the number of synchronized journal articles")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(
        "Cross-source consistency passed: "
        f"{len(portfolio_pubs)} publications, {actual_posters} posters, "
        f"{len(portfolio_industry)} industry roles, shared identity fields aligned."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
