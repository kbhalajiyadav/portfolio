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
    'Beginning Aug 2026': 'stale future-tense appointment status',
    'Completion expected August 2026': 'stale degree-completion language',
    'From July 2026': 'stale doctoral start date',
    'Metrology Lead': 'unverified formal role title',
    '+1 (804) 310-4169': 'public phone number',
    '804 310-4169': 'public phone number',
    'reading-progress': 'removed homepage progress bar',
    'http://example.org': 'sample URL',
    'See the evidence workflow': 'misdirected homepage link',
    '>Archive ↗<': 'ambiguous software label',
    '>Repository ↗<': 'ambiguous thesis/source label',
    'Applied innovation & professional development': 'duplicated engagement taxonomy',
    'Netroschooltraining': 'incorrect name for the National Neutron Scattering School',
    'The Situation: Beyond the Human Eye': 'legacy case-study framing',
    'Ground Truth Pipeline': 'unverified optical-metrology overclaim',
    'true material reflectance': 'unsupported optical-metrology claim',
    'Reduced data processing time by >90%': 'unsupported performance claim',
    'primary validation tool': 'unverified deployment claim',
    'injury monitoring': 'unsupported clinical application',
}
errors: list[str] = []
for needle, reason in forbidden.items():
    for path, text in texts.items():
        if needle in text:
            errors.append(f'{path.relative_to(ROOT)}: {reason}: {needle!r}')

portfolio_text = texts[ROOT / 'data/portfolio.yaml']
for required in (
    'Ph.D. student',
    'Stimuli-responsive',
    'Aug 2026–present',
    'M.S. degree',
    'professional_development:',
    '1st National Neutron Scattering School',
    'Oak Ridge National Laboratory',
    'applied_innovation:',
    'Prototype Demonstrator · Shelfie Program',
    'VCU da Vinci Center · Feedback Friday',
    'Graduate Researcher · Quantitative Metrology',
):
    if required.lower() not in portfolio_text.lower():
        errors.append(f'data/portfolio.yaml: missing {required!r}')

landing_text = texts[ROOT / 'layouts/landing/list.html']
for required in (
    '<h3>Research training</h3>',
    '<h3 class="subhead">Applied innovation</h3>',
    'range $p.professional_development',
    'range $p.applied_innovation',
):
    if required not in landing_text:
        errors.append(f'layouts/landing/list.html: missing taxonomy invariant {required!r}')

cv_text = texts[ROOT / 'data/cv.yaml']
build_cv_text = (ROOT / 'scripts/build_cv.py').read_text(encoding='utf-8')
for required in (
    'Aug 2026–Present',
    'Graduate Researcher, Quantitative Metrology',
    'Teaching, Review, and Applied Innovation',
    'Presentation of Research--Foundational',
    'https://www.credly.com/badges/a2c228cc-13df-4153-b22b-741275119646',
    'https://www.credly.com/badges/e6785521-d537-4ea8-983f-3e1b123f01c7/public_url',
    'https://www.credly.com/badges/ad98e65e-5b4e-4910-9dff-fa54960fdeca/public_url',
    'https://www.credly.com/badges/8caba56a-a526-4891-9408-55e68ee2b0cf/public_url',
    'honors_bullets',
):
    if required.lower() not in (cv_text + build_cv_text).lower():
        errors.append(f'CV source: missing {required!r}')

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

for obsolete in ('go.mod', 'go.sum', 'config/_default/module.yaml'):
    if (ROOT / obsolete).exists():
        errors.append(f'{obsolete}: obsolete HugoBlox module dependency must remain removed')
if 'HugoBlox' in config_text or 'blox-bootstrap' in config_text or 'WebAppManifest' in config_text:
    errors.append('config/_default/config.yaml: obsolete module-defined output or HugoBlox import')
params_text = texts[ROOT / 'config/_default/params.yaml']
for obsolete_marker in ('wowchemy', 'academicons', 'isotope', 'theme_day', 'google_analytics'):
    if obsolete_marker in params_text:
        errors.append(f'config/_default/params.yaml: obsolete inherited configuration marker {obsolete_marker!r}')
if '/research/#resolve-structure\n' in portfolio_text:
    errors.append('data/portfolio.yaml: stale research fragment; use #resolve-structure-under-stimuli')

rights_text = texts[ROOT / 'content/brand-use.md']
for required in (
    'Copyright and trademark notice',
    'Uses permitted by applicable law',
    'unregistered trademarks',
    'does not place its contents in the public domain',
    'separate license',
):
    if required not in rights_text:
        errors.append(f'content/brand-use.md: missing rights clarification {required!r}')

optical_text = texts[ROOT / 'content/project/optical-metrology/index.md']
for required in (
    'Presented research',
    'CIE L\\*a\\*b\\*',
    'clinical validation',
    'public release of the underlying experimental data',
):
    if required not in optical_text:
        errors.append(f'content/project/optical-metrology/index.md: missing evidence boundary {required!r}')

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

for path in (
    ROOT / 'content/project/peel-trace-evaluation/index.md',
    ROOT / 'content/project/optical-metrology/index.md',
    ROOT / 'content/project/fda-project/index.md',
    ROOT / 'content/project/supply-chain-automation/index.md',
):
    if re.search(r'^toc:\s*true\s*$', texts[path], re.MULTILINE):
        errors.append(f'{path.relative_to(ROOT)}: short page must not enable a table of contents')
for path in (ROOT / 'layouts/_default/single.html', ROOT / 'layouts/project/single.html'):
    text = texts[path]
    if 'data-responsive-toc' not in text or '<details class="toc-disclosure" open' in text:
        errors.append(f'{path.relative_to(ROOT)}: responsive TOC must not be hard-coded open')
site_js = (ROOT / 'assets/js/site.js').read_text(encoding='utf-8')
for token in ("data-responsive-toc", "matchMedia('(min-width: 981px)')", "responsiveToc.open = desktopToc.matches"):
    if token not in site_js:
        errors.append(f'assets/js/site.js: responsive TOC invariant missing {token!r}')
if (ROOT / 'static/js/site.js').exists():
    errors.append('static/js/site.js: unused duplicate runtime script must remain removed')

workflow_text = (ROOT / '.github/workflows/hugo.yaml').read_text(encoding='utf-8')
if 'node --check assets/js/site.js' not in workflow_text:
    errors.append('.github/workflows/hugo.yaml: JavaScript syntax check must target the bundled asset')

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

laptop_checker = (ROOT / 'scripts/check_laptop_landing.py').read_text(encoding='utf-8')
for token in ('WIDTH = 1366', 'HEIGHT = 768', 'eyebrowLines', 'extends below the landing frame'):
    if token not in laptop_checker:
        errors.append(f'laptop landing audit lost required invariant {token!r}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors), file=sys.stderr)
    raise SystemExit(1)

print(f'Source audit passed across {len(files)} text files.')
