# Bhalaji Yadav Kantepalle — Research Portfolio

Source for [bhalaji.com](https://bhalaji.com), an academic portfolio documenting
public research outputs, research software, presentations, teaching, service,
and selected professional experience.

The site is intentionally a professional research portfolio—not a laboratory
notebook or a repository for unpublished results. Experimental formulations,
restricted datasets, unpublished figures, and future experimental schedules are
kept outside this repository.

## Information architecture

- `data/portfolio.yaml` — curated homepage content and chronology
- `content/publication/` — public publication and thesis records
- `content/project/` — selected public research-software and professional work
- `data/cv.yaml` — single source for the generated curriculum vitae
- `scripts/build_cv.py` — YAML-to-LaTeX CV generator
- `data/publication_sync.json` — public journal-article metadata synchronized
  from ORCID
- `scripts/sync_orcid.py` — deterministic ORCID metadata synchronizer
- `layouts/`, `static/css/`, and `static/js/` — portfolio presentation and
  interaction layer

## Publication synchronization

The weekly GitHub workflow reads the public works record for
[ORCID 0000-0003-0551-6172](https://orcid.org/0000-0003-0551-6172), counts
items classified by ORCID as `journal-article`, and updates
`data/publication_sync.json` only when the public record changes.

```bash
python3 scripts/sync_orcid.py
```

The homepage count follows this generated file. Selected publication cards
remain curated so a metadata change cannot automatically expose incomplete or
unreviewed site content.

Google Scholar remains linked as a discovery and citation profile. It is not
scraped during builds because Scholar does not provide a supported public
profile API for this use.

## Curriculum vitae

Edit `data/cv.yaml`, then regenerate both the reviewable LaTeX source and the
public PDF:

```bash
python3 -m pip install PyYAML
python3 scripts/build_cv.py
```

The generator requires `latexmk` and XeLaTeX. The deployment workflow rebuilds
the CV before every production build.

## Local development

Requirements:

- Hugo Extended 0.124.1
- Go, for Hugo modules
- Python 3

```bash
hugo server
```

The production site is built and deployed to GitHub Pages from `main` through
`.github/workflows/hugo.yaml`.

## Content policy

- Only public or explicitly approved research information belongs here.
- Publication and software claims should resolve to a DOI, repository, or
  institutional record whenever possible.
- Quantitative claims should remain traceable to a public source.
- Personal documents and images may not be reused without permission.

See [Contributing](.github/CONTRIBUTING.md), [Security](.github/SECURITY.md),
and the [repository license](LICENSE).
