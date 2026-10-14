#!/usr/bin/env python3
"""Fail closed on Research Notes disclosure, repository, and publication boundaries."""
from __future__ import annotations

from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
NOTES_ROOT = ROOT / "content" / "notes"

# These names are reserved for local/private incubation and must never be tracked
# inside this public repository. The preferred private vault lives outside ROOT.
FORBIDDEN_PRIVATE_ROOTS = (
    ROOT / ".research-incubator",
    ROOT / "embryo",
    ROOT / "private-research",
)

ALLOWED_NOTE_TYPES = {"method", "concept", "reflection"}
ALLOWED_STATUSES = {"stable", "evolving", "corrected", "retired", "withdrawn"}
ALLOWED_DISCLOSURE_BASES = {
    "public_literature",
    "published_own_work",
    "authorized_public_disclosure",
}
ALLOWED_COI = {"none_declared", "disclosed", "managed"}
ALLOWED_REVIEW = {"not_applicable", "cleared"}
ALLOWED_VENUE = {"not_applicable", "cleared"}

UNSAFE_TRUE_FLAGS = (
    "contains_unpublished_research",
    "contains_unpublished_collaborator_material",
    "contains_confidential_or_sponsor_material",
)

COMPLETE_REVIEW_FIELDS = (
    "ownership_review",
    "contributor_review",
    "funding_review",
    "privacy_review",
    "external_tool_review",
    "copyright_review",
)

REQUIRED_GOVERNANCE_FIELDS = (
    "repository_safe",
    "disclosure_basis",
    "contains_unpublished_research",
    "contains_unpublished_collaborator_material",
    "contains_confidential_or_sponsor_material",
    "potentially_patent_sensitive",
    "ip_clearance",
    "venue_policy_review",
    "embargo_status",
    "regulated_research_material",
    "ethics_review",
    "export_control_review",
    "dual_use_review",
    "ownership_review",
    "contributor_review",
    "funding_review",
    "privacy_review",
    "external_tool_review",
    "coi_status",
    "coi_statement",
    "copyright_review",
    "source_status_review",
    "author_release_decision",
)


def parse_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("malformed YAML front matter")
    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        raise ValueError("front matter must be a mapping")
    return metadata, parts[2].strip()


def require_nonempty(errors: list[str], path: Path, metadata: dict, field: str) -> None:
    value = metadata.get(field)
    if value is None or (isinstance(value, str) and not value.strip()):
        errors.append(f"{path}: required field {field!r} is empty")


def review_value(governance: dict, field: str) -> str:
    return str(governance.get(field, "")).strip()


def main() -> int:
    errors: list[str] = []
    checked = 0
    staged = 0
    published = 0

    for path in FORBIDDEN_PRIVATE_ROOTS:
        if path.exists():
            errors.append(
                f"{path.relative_to(ROOT)}: private incubation material must not exist in this public repository; "
                "keep the private vault outside the portfolio repository"
            )

    if not NOTES_ROOT.exists():
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
            return 1
        print("Research Notes governance guardrail passed: no content/notes directory exists yet.")
        return 0

    note_files = [
        path
        for path in sorted(NOTES_ROOT.rglob("*.md"))
        if not (path.parent == NOTES_ROOT and path.name in {"_index.md", "index.md"})
    ]

    for path in note_files:
        checked += 1
        rel = path.relative_to(ROOT)
        try:
            metadata, body = parse_markdown(path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        # Public-repository source must have enough structure to audit even when
        # the website page is still a Hugo draft.
        for field in ("title", "date", "lastmod", "note_type", "status"):
            require_nonempty(errors, rel, metadata, field)

        note_type = str(metadata.get("note_type", "")).strip()
        status = str(metadata.get("status", "")).strip()
        if note_type and note_type not in ALLOWED_NOTE_TYPES:
            errors.append(f"{rel}: note_type must be one of {sorted(ALLOWED_NOTE_TYPES)}")
        if status and status not in ALLOWED_STATUSES:
            errors.append(f"{rel}: status must be one of {sorted(ALLOWED_STATUSES)}")

        governance = metadata.get("governance")
        if not isinstance(governance, dict):
            errors.append(f"{rel}: governance mapping is required before a note enters the public repository")
            continue

        for field in REQUIRED_GOVERNANCE_FIELDS:
            if field not in governance:
                errors.append(f"{rel}: governance.{field} is required")

        sources = metadata.get("sources")
        if sources is None:
            errors.append(f"{rel}: sources list is required")
        elif not isinstance(sources, list):
            errors.append(f"{rel}: sources must be a YAML list")

        # ---- Public-repository boundary: applies to drafts and published notes. ----
        if governance.get("repository_safe") is not True:
            errors.append(
                f"{rel}: governance.repository_safe must be explicitly true before the file is committed; "
                "draft:true is not private in a public repository"
            )
        else:
            staged += 1

        disclosure_basis = review_value(governance, "disclosure_basis")
        if disclosure_basis not in ALLOWED_DISCLOSURE_BASES:
            errors.append(
                f"{rel}: governance.disclosure_basis must be one of {sorted(ALLOWED_DISCLOSURE_BASES)}"
            )

        for field in UNSAFE_TRUE_FLAGS:
            value = governance.get(field)
            if value is True:
                errors.append(f"{rel}: public repository cannot contain governance.{field}=true")
            elif value is not False:
                errors.append(f"{rel}: governance.{field} must be explicitly false before repository entry")

        patent_sensitive = governance.get("potentially_patent_sensitive")
        ip_clearance = review_value(governance, "ip_clearance")
        if patent_sensitive not in (True, False):
            errors.append(f"{rel}: governance.potentially_patent_sensitive must be true or false")
        if ip_clearance not in ALLOWED_REVIEW:
            errors.append(f"{rel}: governance.ip_clearance must be one of {sorted(ALLOWED_REVIEW)}")
        if patent_sensitive is True and ip_clearance != "cleared":
            errors.append(f"{rel}: patent-sensitive material requires governance.ip_clearance=cleared before repository entry")
        if patent_sensitive is False and ip_clearance != "not_applicable":
            errors.append(f"{rel}: non-patent-sensitive material should use governance.ip_clearance=not_applicable")

        venue_review = review_value(governance, "venue_policy_review")
        if venue_review not in ALLOWED_VENUE:
            errors.append(f"{rel}: governance.venue_policy_review must be one of {sorted(ALLOWED_VENUE)}")
        if review_value(governance, "embargo_status") != "none":
            errors.append(f"{rel}: governance.embargo_status must be 'none' before material enters this public repository")

        regulated = governance.get("regulated_research_material")
        ethics_review = review_value(governance, "ethics_review")
        if regulated not in (True, False):
            errors.append(f"{rel}: governance.regulated_research_material must be true or false")
        if ethics_review not in ALLOWED_REVIEW:
            errors.append(f"{rel}: governance.ethics_review must be one of {sorted(ALLOWED_REVIEW)}")
        if regulated is True and ethics_review != "cleared":
            errors.append(f"{rel}: regulated-research material requires governance.ethics_review=cleared")
        if regulated is False and ethics_review != "not_applicable":
            errors.append(f"{rel}: non-regulated material should use governance.ethics_review=not_applicable")

        for field in ("export_control_review", "dual_use_review"):
            value = review_value(governance, field)
            if value not in ALLOWED_REVIEW:
                errors.append(f"{rel}: governance.{field} must be one of {sorted(ALLOWED_REVIEW)}")

        for field in COMPLETE_REVIEW_FIELDS:
            if review_value(governance, field) != "complete":
                errors.append(f"{rel}: governance.{field} must be complete before repository entry")

        coi_status = review_value(governance, "coi_status")
        coi_statement = review_value(governance, "coi_statement")
        if coi_status not in ALLOWED_COI:
            errors.append(f"{rel}: governance.coi_status must be one of {sorted(ALLOWED_COI)}")
        if coi_status in {"disclosed", "managed"} and not coi_statement:
            errors.append(f"{rel}: disclosed/managed COI requires governance.coi_statement")

        is_draft = bool(metadata.get("draft", True))
        if is_draft:
            # At this point the source may be public on GitHub but intentionally
            # absent from the rendered site while editorial/web QA continues.
            continue

        # ---- Website publication boundary. ----
        published += 1
        require_nonempty(errors, rel, metadata, "summary")
        if not body:
            errors.append(f"{rel}: published note body must not be empty")

        if review_value(governance, "source_status_review") != "complete":
            errors.append(f"{rel}: governance.source_status_review must be complete before website publication")
        if review_value(governance, "author_release_decision") != "approved":
            errors.append(f"{rel}: governance.author_release_decision must be approved before website publication")

        if not isinstance(sources, list) or not any(str(item).strip() for item in sources):
            errors.append(f"{rel}: published note requires at least one independently verified source")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(
        "Research Notes governance guardrail passed: "
        f"checked {checked} note source file(s), {staged} repository-safe candidate(s), "
        f"including {published} website-published note(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
