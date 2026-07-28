# YAML-to-LaTeX CV

The public CV is generated from one editable source:

```text
data/cv.yaml
```

Do not edit `static/uploads/resume.pdf` or
`cv/generated/bhalaji_cv.tex` manually.

## Build

Install Python's `PyYAML` package plus XeLaTeX and `latexmk`, then run:

```bash
python3 scripts/build_cv.py
```

This generates:

- `cv/generated/bhalaji_cv.tex`
- `static/uploads/resume.pdf`

The GitHub Pages workflow regenerates the CV before every site build. Updating
`data/cv.yaml` is therefore sufficient for future CV changes.

## Linked credentials

Entries under `honors_development` may be plain text or structured credential
records. Use a single `url` when one badge verifies the entry, or a `links` list
when an activity produced several separately verifiable badges. Keep the
credential's official title, issuing organization, issue date, and public URL in
`data/cv.yaml`; `scripts/build_cv.py` renders the badge names as clickable PDF
links.

The current linked records are:

- Design Thinking, Prototyping, and Pitching & Storytelling — VCU da Vinci
  Center, March 2026; and
- Presentation of Research--Foundational — Virginia Commonwealth University,
  April 23, 2025, associated with the 28th VCU Graduate Student Research
  Symposium presentation already listed in the CV.

## Privacy rule

Include only public or approved professional information. Do not add
unpublished formulations, datasets, figures, experimental schedules, or
detailed thesis results while the manuscript remains under embargo.
