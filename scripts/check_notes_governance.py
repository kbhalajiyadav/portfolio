#!/usr/bin/env python3
"""Fail closed when Research Note publication-governance metadata is incomplete or unsafe."""
from __future__ import annotations

from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
NOTES_ROOT = ROOT / "content" / "notes"

ALLOWED_NOTE_TYPES = {"method", "concept", "reflection"}
ALLOWED_STATUSES = {"stable", "evolving"}
ALLOWED_DISCLOSURE_BASES = {
    "public_literature",
    "published_own_work",
    "authorized_public_disclosure",
}
ALLOWED_COI = {"none_declared", "disclosed", "managed"}
ALLOWED_ETHICS = {"not_applicable", "cleared"}
ALLOWED_IP = {"not_applicable", "cleared"}

UNSAFE_TRUE_FLAGS = (
    "contains_unpublished_research",
    "contains_unpublished_collaborator_material",
    "contains_confidential_or_sponsor_material",
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


def is_true(value: object) -> bool:
    return value is True


def require_nonempty(errors: list[str], path: Path, metadata: dict, field: str) -> None:
    value = metadata.get(field)
    if value is None or (isinstance(value, str) and not value.strip()):
        errors.append(f"{path}: required field {field!r} is empty")


def main() -> int:
    errors: list[str] = []
    checked = 0
    published = 0

    if not NOTES_ROOT.exists():
        print("Research Notes governance guardrail passed: no content/notes directory exists yet.")
        return 0

    note_files = [
        path
        for path in sorted(NOTES_ROOT.rglob("*.md"))
        if path.name not in {"_index.md", "index.md"} or path.parent != NOTES_ROOT
    ]

    for path in note_files:
        checked += 1
        rel = path.relative_to(ROOT)
        try:
            metadata, body = parse_markdown(path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        for field in ("title", "date", "lastmod", "summary", "note_type", "status"):
            require_nonempty(errors, rel, metadata, field)

        note_type = str(metadata.get("note_type", "")).strip()
        status = str(metadata.get("status", "")).strip()
        if note_type and note_type not in ALLOWED_NOTE_TYPES:
            errors.append(f"{rel}: note_type must be one of {sorted(ALLOWED_NOTE_TYPES)}")
        if status and status not in ALLOWED_STATUSES:
            errors.append(f"{rel}: status must be one of {sorted(ALLOWED_STATUSES)}")

        governance = metadata.get("governance")
        if not isinstance(governance, dict):
            errors.append(f"{rel}: governance mapping is required from the first draft")
            continue

        required_governance_fields = (
            "disclosure_basis",
            "contains_unpublished_research",
            "contains_unpublished_collaborator_material",
            "contains_confidential_or_sponsor_material",
            "potentially_patent_sensitive",
            "ip_clearance",
            "regulated_research_material",
            "ethics_review",
            "ownership_review",
            "coi_status",
            "coi_statement",
            "copyright_review",
            "publication_approval",
        )
        for field in required_governance_fields:
            if field not in governance:
                errors.append(f"{rel}: governance.{field} is required")

        sources = metadata.get("sources")
        if sources is None:
            errors.append(f"{rel}: sources list is required from the first draft")
        elif not isinstance(sources, list):
            errors.append(f"{rel}: sources must be a YAML list")

        if bool(metadata.get("draft", True)):
            continue

        published += 1

        if not body:
            errors.append(f"{rel}: published note body must not be empty")

        disclosure_basis = str(governance.get("disclosure_basis", "")).strip()
        if disclosure_basis not in ALLOWED_DISCLOSURE_BASES:
            errors.append(
                f"{rel}: published governance.disclosure_basis must be one of "
                f"{sorted(ALLOWED_DISCLOSURE_BASES)}"
            )

        for field in UNSAFE_TRUE_FLAGS:
            if is_true(governance.get(field)):
                errors.append(f"{rel}: cannot publish while governance.{field}=true")
            elif governance.get(field) is not False:
                errors.append(f"{rel}: governance.{field} must be explicitly false before publication")

        patent_sensitive = governance.get("potentially_patent_sensitive")
        ip_clearance = str(governance.get("ip_clearance", "")).strip()
        if patent_sensitive not in (True, False):
            errors.append(f"{rel}: governance.potentially_patent_sensitive must be true or false")
        if ip_clearance not in ALLOWED_IP:
            errors.append(f"{rel}: governance.ip_clearance must be one of {sorted(ALLOWED_IP)}")
        if patent_sensitive is True and ip_clearance != "cleared":
            errors.append(f"{rel}: patent-sensitive notes require governance.ip_clearance=cleared")
        if patent_sensitive is False and ip_clearance != "not_applicable":
            errors.append(f"{rel}: non-patent-sensitive notes should use governance.ip_clearance=not_applicable")

        regulated = governance.get("regulated_research_material")
        ethics_review = str(governance.get("ethics_review", "")).strip()
        if regulated not in (True, False):
            errors.append(f"{rel}: governance.regulated_research_material must be true or false")
        if ethics_review not in ALLOWED_ETHICS:
            errors.append(f"{rel}: governance.ethics_review must be one of {sorted(ALLOWED_ETHICS)}")
        if regulated is True and ethics_review != "cleared":
            errors.append(f"{rel}: regulated-research material requires governance.ethics_review=cleared")
        if regulated is False and ethics_review != "not_applicable":
            errors.append(f"{rel}: non-regulated notes should use governance.ethics_review=not_applicable")

        if str(governance.get("ownership_review", "")).strip() != "complete":
            errors.append(f"{rel}: governance.ownership_review must be complete")
        if str(governance.get("copyright_review", "")).strip() != "complete":
            errors.append(f"{rel}: governance.copyright_review must be complete")
        if str(governance.get("publication_approval", "")).strip() != "approved":
            errors.append(f"{rel}: governance.publication_approval must be approved")

        coi_status = str(governance.get("coi_status", "")).strip()
        coi_statement = str(governance.get("coi_statement", "")).strip()
        if coi_status not in ALLOWED_COI:
            errors.append(f"{rel}: governance.coi_status must be one of {sorted(ALLOWED_COI)}")
        if coi_status in {"disclosed", "managed"} and not coi_statement:
            errors.append(f"{rel}: disclosed/managed COI requires governance.coi_statement")

        if not isinstance(sources, list) or not any(str(item).strip() for item in sources):
            errors.append(f"{rel}: published note requires at least one verified source")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(
        "Research Notes governance guardrail passed: "
        f"checked {checked} note source file(s), including {published} published note(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
