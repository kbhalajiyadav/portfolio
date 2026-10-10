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
    '99% reduction in data entry errors': 'quarantined historical metric with conflicting denominator',
    '99% of compliance gaps': 'quarantined historical metric with conflicting denominator',
    '90% increase in data accuracy': 'quarantined trade-normalization metric pending definition',
    '96% reduction in system downtime': 'quarantined cutover metric pending baseline verification',
    'zero production downtime': 'unsupported cutover claim',
    'ensuring GMP compliance': 'overstated compliance guarantee',
    'primary validation tool': 'unverified deployment claim',
    'injury monitoring': 'unsupported clinical application',
    'ongoing Summer 2026': 'stale completed student-project status',
    'two ongoing student projects': 'stale completed student-project status',
    '## Evidence boundary': 'internal audit wording exposed in public content',
    '## Public scope': 'internal disclosure framing exposed in public content',
    '## Current public scope': 'internal disclosure framing exposed in public content',
    '## Public technical scope': 'internal disclosure framing exposed in public content',
    '## Verification scope': 'internal disclosure framing exposed in public content',
    'IP project details': 'intellectual-property output mislabeled as a generic project',
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
    'M.S. · Chemical & Life Science Engineering',
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

if not (ROOT / 'data/current_affiliation.yaml').exists():
    errors.append('data/current_affiliation.yaml: canonical current lab/advisor context must remain present')

landing_text = texts[ROOT / 'layouts/landing/list.html']
for required in (
    '<h3>Research training</h3>',
    '<h3 class="subhead">Applied innovation</h3>',
    'range $p.professional_development',
    'range $p.applied_innovation',
    'Browse all research outputs',
    '/project/quantitative-thermal-imaging/',
    '{{ $ip.status }}',
    'VCU Tech # {{ $ip.tech_id }}',
):
    if required not in landing_text:
        errors.append(f'layouts/landing/list.html: missing homepage invariant {required!r}')

outputs_content = ROOT / 'content/outputs/_index.md'
outputs_layout = ROOT / 'layouts/outputs/list.html'
if not outputs_content.exists() or not outputs_layout.exists():
    errors.append('first-class /outputs/ hub must remain present')
else:
    outputs_text = outputs_layout.read_text(encoding='utf-8')
    for required in (
        'data-output-type="intellectual-property"',
        'data-output-type="thesis"',
        'data-output-type="software"',
        'Peer-reviewed article',
        'Technology details',
    ):
        if required not in outputs_text:
            errors.append(f'layouts/outputs/list.html: missing output fact {required!r}')

if 'cv_version:' in portfolio_text:
    errors.append('data/portfolio.yaml: manual cv_version must remain removed; templates hash the PDF')

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

for path in [ROOT / 'layouts/landing/list.html', ROOT / 'layouts/publication/single.html', ROOT / 'layouts/outputs/list.html']:
    for match in re.finditer(r'<a\b[^>]*>[^<\n]*(?:↗|↓)', path.read_text(encoding='utf-8')):
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
optical_flat = ' '.join(optical_text.split())
for required in (
    'Presented research',
    'CIE L\\*a\\*b\\*',
    '## Presentations',
    'VCU Engineering Graduate',
    '29th VCU Graduate Student Research Symposium',
):
    if required not in optical_flat:
        errors.append(f'content/project/optical-metrology/index.md: missing optical-metrology fact {required!r}')

ip_text = texts[ROOT / 'content/project/quantitative-thermal-imaging/index.md']
for required in (
    'record_type: "intellectual-property"',
    'Patent pending',
    'VCU Tech # TAN-26-099',
    'Bhalaji Yadav Kantepalle and Christina Tang',
    '## Technology overview',
    '## Status',
):
    if required not in ip_text:
        errors.append(f'content/project/quantitative-thermal-imaging/index.md: missing IP fact {required!r}')

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
for required in ('About</a>', 'Research</a>', 'Outputs</a>', 'Experience</a>', 'Engagement</a>', 'Contact</a>'):
    if required not in header_text:
        errors.append(f'layouts/partials/site_header.html: missing primary-navigation item {required!r}')
if '>Trajectory</a>' in header_text:
    errors.append('layouts/partials/site_header.html: doctoral direction belongs within Research, not primary navigation')

for path in (
    ROOT / 'content/project/peel-trace-evaluation/index.md',
    ROOT / 'content/project/optical-metrology/index.md',
    ROOT / 'content/project/fda-project/index.md',
    ROOT / 'content/project/supply-chain-automation/index.md',
    ROOT / 'content/project/quantitative-thermal-imaging/index.md',
):
    if re.search(r'^toc:\s*true\s*$', texts[path], re.MULTILINE):
        errors.append(f'{path.relative_to(ROOT)}: short page must not enable a table of contents')
for path in (ROOT / 'layouts/_default/single.html', ROOT / 'layouts/project/single.html'):
    text = texts[path]
    if 'data-responsive-toc' not in text or '<details class="toc-disclosure" open' in text:
        errors.append(f'{path.relative_to(ROOT)}: responsive TOC must not be hard-coded open')

base_template = (ROOT / 'layouts/_default/baseof.html').read_text(encoding='utf-8')
for token in (
    'resources.FromString "css/core.css"',
    'resources.FromString "css/refinements.css"',
    'resources.FromString "css/about.css"',
    'resources.Concat "css/site.css"',
    'fingerprint "sha384"',
):
    if token not in base_template:
        errors.append(f'layouts/_default/baseof.html: bundled fingerprinted CSS invariant missing {token!r}')
if (ROOT / 'assets/css/site.css').exists():
    errors.append('assets/css/site.css: obsolete manual @import wrapper must remain removed')

site_js = (ROOT / 'assets/js/site.js').read_text(encoding='utf-8')
for token in (
    "data-responsive-toc",
    "matchMedia('(min-width: 981px)')",
    "responsiveToc.open = desktopToc.matches",
    "data-copy-status",
    "copied to clipboard",
):
    if token not in site_js:
        errors.append(f'assets/js/site.js: interaction/accessibility invariant missing {token!r}')
if (ROOT / 'static/js/site.js').exists():
    errors.append('static/js/site.js: unused duplicate runtime script must remain removed')

publication_template = texts[ROOT / 'layouts/publication/single.html']
for token in ('role="status"', 'aria-live="polite"', 'data-copy-status', 'data-copy-label="Citation"'):
    if token not in publication_template:
        errors.append(f'layouts/publication/single.html: copy-feedback accessibility marker missing {token!r}')

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
    'scripts/check_accessibility_interactions.py',
    'scripts/check_laptop_landing.py', 'scripts/check_component_integrity.py',
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