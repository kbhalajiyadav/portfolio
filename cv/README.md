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

## Privacy rule

Include only public or approved professional information. Do not add
unpublished formulations, datasets, figures, experimental schedules, or
detailed thesis results while the manuscript remains under embargo.
