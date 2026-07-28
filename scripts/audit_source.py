#!/usr/bin/env python3
"""Fail on known regression patterns in the portfolio source."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json
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

if (ROOT / 'content' / 'authors').exists():
    errors.append('legacy content/authors archive must not be published')
config_text = (ROOT / 'config/_default/config.yaml').read_text(encoding='utf-8')
if 'author: authors' in config_text or 'publication_type: publication_types' in config_text or 'category: categories' in config_text:
    errors.append('unused legacy taxonomies must remain disabled')

# The public site is now a self-contained Hugo build; obsolete framework layers must not return.
for obsolete in ('go.mod', 'go.sum', 'config/_default/module.yaml'):
    if (ROOT / obsolete).exists():
        errors.append(f'{obsolete}: obsolete HugoBlox module dependency must remain removed')
if 'HugoBlox' in config_text or 'blox-bootstrap' in config_text or 'WebAppManifest' in config_text:
    errors.append('config/_default/config.yaml: obsolete module-defined output or HugoBlox import')
params_text = texts[ROOT / 'config/_default/params.yaml']
for obsolete_marker in ('wowchemy', 'academicons', 'isotope', 'theme_day', 'google_analytics'):
    if obsolete_marker in params_text:
        errors.append(f'config/_default/params.yaml: obsolete inherited configuration marker {obsolete_marker!r}')
if '/research/#resolve-structure\n' in texts[ROOT / 'data/portfolio.yaml']:
    errors.append('data/portfolio.yaml: stale research fragment; use #resolve-structure-under-stimuli')

security_text = (ROOT / 'static/.well-known/security.txt').read_text(encoding='utf-8')
expiry_match = re.search(r'^Expires:\s*(.+)$', security_text, re.MULTILINE)
if not expiry_match:
    errors.append('static/.well-known/security.txt: missing Expires field')
else:
    try:
        expiry = datetime.fromisoformat(expiry_match.group(1).replace('Z', '+00:00'))
        if expiry < datetime.now(timezone.utc) + timedelta(days=180):
            errors.append('static/.well-known/security.txt: expiry must remain at least 180 days ahead')
    except ValueError:
        errors.append('static/.well-known/security.txt: invalid Expires timestamp')

header_text = texts[ROOT / 'layouts/partials/site_header.html']
if 'class="u-photo indieweb-photo"' not in header_text or 'alt="Portrait of {{ $p.profile.name }}"' not in header_text:
    errors.append('layouts/partials/site_header.html: hidden IndieWeb photo requires a durable non-empty alt value')

# Browser-audit tools must use exact direct versions rather than floating ranges.
package = json.loads((ROOT / 'package.json').read_text(encoding='utf-8'))
expected_tools = {'@lhci/cli': '0.15.1', 'pa11y-ci': '4.1.1'}
if package.get('devDependencies') != expected_tools:
    errors.append(f"package.json: expected exact audit-tool versions {expected_tools}")
if package.get('engines', {}).get('node') != '>=24':
    errors.append('package.json: Node.js 24 or newer must be required')

for required in (
    'package.json', '.pa11yci.cjs', '.lighthouserc.cjs',
    'scripts/check_external_links.py', 'scripts/check_workflows.py',
    'scripts/check_live_site.py', 'scripts/check_responsive.py',
    'scripts/check_laptop_landing.py',
):
    if not (ROOT / required).exists():
        errors.append(f'{required}: missing production hardening file')

# The network checker must never test unreleased bhalaji.com routes against production.
external_checker = (ROOT / "scripts" / "check_external_links.py").read_text(encoding="utf-8")
required_external_checker_tokens = [
    "skipped_same_site",
    "site_hosts",
    "same_site_urls_validated_locally",
]
for token in required_external_checker_tokens:
    if token not in external_checker:
        errors.append(f"external-link checker lost same-site exclusion invariant: {token}")

site_checker = (ROOT / "scripts" / "check_site.py").read_text(encoding="utf-8")
for token in ("site_hosts", "Absolute links back to the canonical site are internal", "target_for(root, html, ref, site_hosts)"):
    if token not in site_checker:
        errors.append(f"generated-site checker lost absolute same-site validation invariant: {token}")

laptop_checker = (ROOT / 'scripts' / 'check_laptop_landing.py').read_text(encoding='utf-8')
for token in ('WIDTH = 1366', 'HEIGHT = 768', 'eyebrowLines', 'extends below the landing frame'):
    if token not in laptop_checker:
        errors.append(f'laptop landing audit lost required invariant: {token}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors), file=sys.stderr)
    raise SystemExit(1)

print(f'Source audit passed across {len(files)} text files.')
