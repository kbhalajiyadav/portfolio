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
`docs/content-taxonomy.md`.

## Build and validation

The validated local sequence is:

```bash
python3 -m pip install PyYAML==6.0.3 websocket-client==1.9.0
bash scripts/build_browser_icons.sh
python3 scripts/build_cv.py --no-compile
python3 scripts/audit_source.py
python3 scripts/audit_styles.py
python3 scripts/audit_templates.py
python3 scripts/check_workflows.py
node --check assets/js/site.js
hugo --gc --minify --printPathWarnings --baseURL https://bhalaji.com/
python3 scripts/check_site.py public
python3 scripts/check_external_links.py public --site-origin https://bhalaji.com/
```

GitHub Actions also runs accessibility, responsive-layout, laptop-frame, and
mobile and desktop Lighthouse checks before deployment. CV compilation is
handled by the dedicated XeLaTeX workflow.

## Rights

Copyright © 2026 Bhalaji Yadav Kantepalle. All rights reserved. The repository
is publicly viewable but is not released under an open-source license. Files
that state a separate license remain governed by that license. See `LICENSE`
for the applicable terms.
