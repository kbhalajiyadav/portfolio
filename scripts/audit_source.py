#!/usr/bin/env python3
"""Fail on known regression patterns in the portfolio source."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {'.html', '.css', '.js', '.yaml', '.yml', '.md', '.txt', '.py'}

scan_roots = [ROOT / name for name in ('config', 'content', 'data', 'layouts', 'static', 'cv')]
files = [p for base in scan_roots for p in base.rglob('*') if p.is_file() and p.suffix.lower() in TEXT_EXTENSIONS]
texts = {p: p.read_text(encoding='utf-8', errors='replace') for p in files}

forbidden = {
    'Incoming Ph.D.': 'stale doctoral status',
    'reading-progress': 'removed homepage progress bar',
    'http://example.org': 'sample URL',
    'See the evidence workflow': 'misdirected homepage link',
    '>Archive ↗<': 'ambiguous software label',
    '>Repository ↗<': 'ambiguous thesis/source label',
}
errors: list[str] = []
for needle, reason in forbidden.items():
    for path, text in texts.items():
        if needle in text:
            errors.append(f'{path.relative_to(ROOT)}: {reason}: {needle!r}')

# The public identity must remain consistent across the main data sources.
for required in ('Ph.D. student', 'Stimuli-responsive'):
    if required.lower() not in texts[ROOT / 'data/portfolio.yaml'].lower():
        errors.append(f'data/portfolio.yaml: missing {required!r}')

# All externally displayed arrow labels should use the unbreakable link atom.
for path in [ROOT / 'layouts/landing/list.html', ROOT / 'layouts/publication/single.html']:
    for match in re.finditer(r'<a\b[^>]*>[^<\n]*(?:↗|↓)', texts[path]):
        snippet = match.group(0)
        if 'class="lnk"' not in snippet and 'class="button' not in snippet:
            errors.append(f'{path.relative_to(ROOT)}: arrow link is not a link atom: {snippet[:100]}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Source audit passed across {len(files)} text files.')
