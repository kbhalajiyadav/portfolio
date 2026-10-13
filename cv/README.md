# YAML-to-LaTeX CV and Resume

The public academic CV and compact professional resume are generated from one editable source:

```text
data/cv.yaml
```

Do not edit generated TeX or PDF files manually. They are build artifacts and are intentionally excluded from version control.

## Build

Install Python's `PyYAML` package plus XeLaTeX and `latexmk`, then run:

```bash
python3 scripts/build_cv.py
```

This generates:

- `cv/generated/bhalaji_cv.tex`
- `static/uploads/cv.pdf` — the academic/research CV; and
- `cv/generated/bhalaji_resume.tex`
- `static/uploads/resume.pdf` — the compact two-page professional resume.

The GitHub Pages workflow regenerates both documents before every site build. Updating `data/cv.yaml` is therefore sufficient for future content changes. The academic CV and resume use separate LaTeX templates so page density can be tuned independently without duplicating factual source data.

## Linked credentials

Entries under `honors_development` may be plain text or structured credential records. Use a single `url` when one badge verifies the entry, or a `links` list when an activity produced several separately verifiable badges. Keep the credential's official title, issuing organization, issue date, and public URL in `data/cv.yaml`; `scripts/build_cv.py` renders the badge names as clickable PDF links.

The current linked records are:

- Design Thinking, Prototyping, and Pitching & Storytelling — VCU da Vinci Center, March 2026; and
- Presentation of Research--Foundational — Virginia Commonwealth University, April 23, 2025, associated with the 28th VCU Graduate Student Research Symposium presentation already listed in the CV.

## Privacy rule

Include only public or approved professional information. Do not add unpublished formulations, datasets, figures, experimental schedules, internal validation documents, or detailed thesis results while the manuscript remains under embargo.
