#!/usr/bin/env python3
"""Require immutable action pins and hardened GitHub Actions conventions."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
workflows = sorted((ROOT / '.github/workflows').glob('*.y*ml'))

# These workflows intentionally create commits or branches. All other workflows
# must use read-only contents permissions and must not retain checkout credentials.
PUBLISHING_WORKFLOWS = {
    'sync-publications.yaml',
    'manage-site-controls.yaml',
}

for workflow in workflows:
    text = workflow.read_text(encoding='utf-8')
    lines = text.splitlines()
    is_publishing = workflow.name in PUBLISHING_WORKFLOWS

    for index, line in enumerate(lines):
        match = re.search(r'\buses:\s*([^\s#]+)', line)
        if not match:
            continue
        ref = match.group(1)
        if not ref.startswith(('./', 'docker://')) and (
            '@' not in ref or not re.search(r'@[0-9a-f]{40}$', ref)
        ):
            errors.append(
                f'{workflow.relative_to(ROOT)}:{index + 1}: action is not pinned '
                f'to a 40-character commit SHA: {ref}'
            )
        if ref.startswith('actions/checkout@') and not is_publishing:
            following = '\n'.join(lines[index + 1:index + 7])
            if 'persist-credentials: false' not in following:
                errors.append(
                    f'{workflow.relative_to(ROOT)}:{index + 1}: non-publishing checkout '
                    'must disable persisted credentials'
                )

    if 'timeout-minutes:' not in text:
        errors.append(f'{workflow.relative_to(ROOT)}: every job must define timeout-minutes')

    if not is_publishing and re.search(r'^\s*contents:\s*write\s*$', text, re.MULTILINE):
        errors.append(f'{workflow.relative_to(ROOT)}: unnecessary contents: write permission')

    if is_publishing:
        if not re.search(r'^\s*contents:\s*write\s*$', text, re.MULTILINE):
            errors.append(f'{workflow.relative_to(ROOT)}: publishing workflow requires contents: write')
        if workflow.name == 'manage-site-controls.yaml' and not re.search(
            r'^\s*pull-requests:\s*write\s*$', text, re.MULTILINE
        ):
            errors.append(
                f'{workflow.relative_to(ROOT)}: site-control publisher requires pull-requests: write'
            )

hugo = (ROOT / '.github/workflows/hugo.yaml').read_text(encoding='utf-8')
for marker in (
    'sha256sum --check --strict',
    'python3 scripts/check_site.py public',
    'python3 scripts/check_external_links.py public',
    'npx pa11y-ci',
    'npx lhci autorun',
    'python3 scripts/check_responsive.py',
    'python3 scripts/check_live_site.py',
    'Upload diagnostics on failure',
):
    if marker not in hugo:
        errors.append(f'.github/workflows/hugo.yaml: missing release gate {marker!r}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Workflow security audit passed: {len(workflows)} workflows.')
