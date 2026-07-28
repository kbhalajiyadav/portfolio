# Bhalaji Yadav Kantepalle — Research Portfolio

Source for [bhalaji.com](https://bhalaji.com), a professional academic portfolio for a Ph.D. student working on stimuli-responsive soft and liquid-crystalline materials, quantitative metrology, rheology, neutron scattering, and reproducible processing.

The site is a public research record, not a laboratory notebook. It excludes unpublished formulations, restricted datasets, detailed experimental schedules, confidential employer information, and claims that are not supported by a public source.

## Information architecture

- `data/portfolio.yaml` — curated homepage content and chronology
- `content/research/index.md` — stable, citable research-program page
- `content/publication/` — public article and thesis records
- `content/project/` — research software and selected professional case studies
- `data/cv.yaml` — source for the generated curriculum vitae
- `scripts/build_cv.py` — YAML-to-LaTeX CV generator
- `layouts/` — unified homepage and internal-page templates
- `static/css/site.css` and `static/js/site.js` — one token, component, and interaction system
- `static/llms.txt` and `static/llms-full.txt` — concise public context for AI retrieval systems

## Search and identity discovery

The build includes:

- canonical URLs, descriptive titles, metadata, Open Graph, and Twitter cards;
- `ProfilePage`, `Person`, `WebSite`, `ScholarlyArticle`, `Thesis`, and `SoftwareSourceCode` JSON-LD where appropriate;
- `<link rel="me">` identity links to ORCID, Google Scholar, LinkedIn, and GitHub;
- an explicit `robots.txt` policy that permits conventional indexing plus OpenAI/Anthropic search and user-directed retrieval, while blocking their separate model-development crawlers;
- a Hugo sitemap;
- `llms.txt` and `llms-full.txt` as complementary machine-readable summaries; and
- IndexNow submission after a successful deployment.

`rel="me"` links identity profiles to the site. They do not replace ownership verification in Google Search Console or Bing Webmaster Tools. Add the issued verification values to `config/_default/params.yaml`:

```yaml
marketing:
  verification:
    google: ""
    bing: ""
```

Keep the fields empty until the corresponding service provides a code.

## Build and validation

The GitHub Actions workflow:

1. installs Hugo Extended 0.124.1;
2. regenerates the YAML-driven CV;
3. runs source regression checks;
4. builds the Hugo site;
5. checks generated pages for missing metadata, duplicate IDs, broken local links, and missing fragments;
6. deploys GitHub Pages; and
7. sends a non-blocking IndexNow notification.

Local validation:

```bash
python3 -m pip install PyYAML
python3 scripts/build_cv.py
python3 scripts/audit_source.py
hugo --gc --minify --printPathWarnings --baseURL https://bhalaji.com/
python3 scripts/check_site.py public
```

## Publication synchronization

The weekly workflow reads public ORCID journal-article metadata for ORCID `0000-0003-0551-6172` and updates `data/publication_sync.json` only when the public record changes.

## Visual and interaction policy

- Ivory is the page field; white is the content surface.
- Ink is primary text; teal is structural and navigational.
- Cyan is reserved for hover and keyboard focus.
- Rust is reserved for current status and dates.
- Link arrows are part of an unbreakable link atom.
- Body text is left aligned with a 68-character measure.
- Scattering rings appear only in the structure-under-stimuli context.
- There is no reading-progress bar, custom cursor, universal popup, or decorative 3D scene.

## Content updates

Update `data/portfolio.yaml` for homepage facts, then update `data/cv.yaml` when the same fact belongs in the CV. Run the full validation sequence before publishing.

## IndieWeb and owned publishing

The shared templates include `rel="me"`, microformats2 identity/content markup, RSS discovery, and conditional endpoint discovery. Future POSSE notes are scaffolded but intentionally absent from the public navigation until durable content exists. See [`INDIEWEB-POSSE.md`](INDIEWEB-POSSE.md).

## License and disclosure

Source-code permissions and reserved portfolio-content terms are defined in `LICENSE`. Security reporting instructions are in `.github/SECURITY.md` and `static/.well-known/security.txt`.
