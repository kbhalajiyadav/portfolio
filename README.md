# Bhalaji Yadav Kantepalle — Research Portfolio

Source for [bhalaji.com](https://bhalaji.com), an academic portfolio focused on
stimuli-responsive soft and liquid-crystalline materials, quantitative metrology,
rheology, neutron scattering, and reproducible processing.

The site is a public research record rather than a laboratory notebook. It excludes
unpublished formulations, restricted datasets, detailed experimental schedules,
confidential employer information, and unsupported claims.

## Edit content

- `data/portfolio.yaml` — homepage content, chronology, and public evidence
- `data/site_controls.yaml` — homepage limits and future feature controls
- `content/research/index.md` — stable research-program page
- `content/publication/` and `content/project/` — detailed public records
- `data/cv.yaml` — source for the generated two-page CV

The owner-only **Propose portfolio display controls** workflow can change homepage
limits and future feature switches through a draft pull request. Search and Latest
Updates are intentionally disabled.

## Local validation

```bash
python3 -m pip install PyYAML==6.0.3 websocket-client==1.9.0
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

GitHub Actions also runs responsive, accessibility, Lighthouse, external-link, and
post-deployment checks. The CV compiles in a separate path-filtered workflow using the
proven XeLaTeX dependency set.

## Discovery and ownership

The site includes canonical metadata, structured scholarly data, RSS, sitemap,
`rel="me"`, IndieWeb microformats, crawler policy, `llms.txt`, and IndexNow support.
Google Search Console, Bing Webmaster Tools, and optional IndieWeb endpoints still
require account-issued values in `config/_default/params.yaml`.

## License

See `LICENSE`. Security contact information is published at
`static/.well-known/security.txt`.
