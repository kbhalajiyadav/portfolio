# Bhalaji Yadav Kantepalle — Research Portfolio

Official source for [bhalaji.com](https://bhalaji.com), a Hugo-based academic
portfolio and generated curriculum vitae.

## Repository structure

- `data/portfolio.yaml` — profile, chronology, and public records
- `data/cv.yaml` — structured source for the two-page CV
- `data/site_controls.yaml` — presentation limits and feature controls
- `content/` — research and portfolio pages
- `layouts/` — Hugo templates
- `assets/` and `static/` — styles, scripts, and published assets
- `scripts/` — deterministic build and validation utilities

Content classification decisions are recorded in
`docs/content-taxonomy.md`. Sitewide hierarchy, scientific-visual integrity,
responsive composition, evidence-link behavior, spacing, social-preview
behavior, and release lessons are recorded in `docs/design-governance.md`.
Research Note disclosure, ownership, IP, ethics/COI, citation, copyright, and
publication-release rules are recorded in `docs/research-notes-governance.md`.
These documents are intended to carry forward into future changes rather than
be rediscovered case by case.

## Research Notes publication gate

Research Notes are fail-closed by default. `archetypes/notes.md` creates drafts
with conservative governance flags, and `scripts/check_notes_governance.py`
rejects a public note when required publication metadata is incomplete or an
unsafe disclosure flag remains set. The dedicated GitHub Actions workflow runs
on relevant pull requests, main-branch changes, a monthly schedule, and manual
dispatch.

A passing automated check is necessary but not sufficient: scientific,
disclosure, ownership/collaboration, IP, ethics/COI, and copyright judgments
still require appropriate human review under the governing institutional,
sponsor, journal, and collaboration requirements.

## Build and validation

The validated local sequence is:

```bash
python3 -m pip install PyYAML==6.0.3 websocket-client==1.9.0
bash scripts/build_browser_icons.sh
python3 scripts/build_social_cards.py
python3 scripts/build_cv.py --no-compile
python3 scripts/audit_source.py
python3 scripts/audit_styles.py
python3 scripts/audit_templates.py
python3 scripts/check_design_governance.py
python3 scripts/check_notes_governance.py
python3 scripts/check_workflows.py
node --check assets/js/site.js
node --check assets/js/evidence-target.js
hugo --gc --minify --printPathWarnings --baseURL https://bhalaji.com/
python3 scripts/check_site.py public
python3 scripts/check_social_previews.py public
python3 scripts/check_external_links.py public --site-origin https://bhalaji.com/
```

GitHub Actions also runs accessibility, responsive-layout, contextual-navigation,
deep-link and dismissal-state, spacing, component-integrity, laptop-frame, and
mobile/desktop Lighthouse checks before deployment. Research Notes have an
additional publication-governance workflow. CV compilation is handled by the
dedicated XeLaTeX workflow.

## Rights

Copyright © 2026 Bhalaji Yadav Kantepalle. All rights reserved. The repository
is publicly viewable but is not released under an open-source license. Files
that state a separate license remain governed by that license. See `LICENSE`
for the applicable terms.