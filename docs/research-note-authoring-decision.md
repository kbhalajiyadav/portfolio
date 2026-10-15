# Research Note authoring decision

This record captures the outcome of the private Note 001 authoring comparison without placing the private candidate itself in public Git.

## Decision

**Native Hugo Markdown is the default Research Notes authoring format. Quarto remains an optional, feature-triggered compiler rather than a standard dependency.**

For Research Note 001, use native Hugo Markdown when the note is eventually cleared for public-source staging.

## Why

Note 001 is primarily a prose-and-figure methods note. It uses two original SVG schematics and a modest bibliography, but it does not require executable analysis, numbered equations, a dense cross-reference network, or multi-format scientific output.

A native Hugo source can express the complete public artifact directly using the existing Research Notes front matter, Hugo figure handling, related-work metadata, transparency metadata, and the portfolio's Notes presentation layer. This leaves one authoritative publishable source plus figure assets.

The private Quarto candidate demonstrated a real advantage for citation authoring: citekeys and a curated BibTeX file are cleaner than repeating explicit DOI links. However, adopting Quarto for this note would also introduce an additional source format, bibliography input, compiler/version dependency, and generated Hugo Markdown. That requires a source-of-truth rule and creates another place for drift without enough compensating value for this note.

The local comparison also exercised the Quarto candidate's bibliography through Pandoc/citeproc successfully. The Quarto CLI itself was **not** executed in the current environment because the binary could not be retrieved, so Quarto-specific filters and final `hugo-md` cross-reference behavior are not treated as validated.

## Default authoring rule

Use native Hugo Markdown unless a note materially benefits from Quarto-specific scientific-authoring capabilities.

Quarto becomes a candidate when one or more of the following are genuinely required:

- executable Python, R, or Jupyter output that should be regenerated from source;
- numbered cross-references across several figures, tables, equations, theorems, or sections;
- mathematically dense content where equation numbering/cross-referencing improves maintainability;
- citation-heavy synthesis where a curated BibTeX/CSL workflow substantially reduces citation-maintenance risk;
- multi-format scientific output generated from the same canonical source.

If those triggers are absent, the additional compiler layer is not justified.

## Source-of-truth rule if Quarto is used later

If a future note adopts Quarto:

1. the private `.qmd` is the authoritative authoring source during incubation;
2. generated Hugo Markdown is treated as a build product and is never hand-edited;
3. source `.qmd`, notebooks, code, data, and bibliography material remain outside public Git until each item is independently repository-safe;
4. the generated public-source candidate must pass the same governance, provenance, accessibility, presentation, dependency, and full-site checks as native Markdown;
5. Quarto version/checksum and deterministic-output expectations must be documented before CI adoption.

## Bibliography decision

Zotero + Better BibTeX remains useful independently of Quarto. A curated public-source collection can provide stable citation metadata for verification and drafting even when the final Hugo note contains explicit human-reviewable citations and references.

The master Zotero library, private annotations, attachments, unpublished records, and restricted material remain outside the public repository.

## Note 001 promotion state

The private candidate has been mapped to the Research Notes schema, including:

- `summary` and first-class `in_brief`;
- `note_type: method`;
- `status: stable` as the intended release state, subject to final review;
- related public article, thesis record, and software links;
- funding provenance for the underlying published study;
- verified public-source identifiers;
- original non-experimental SVG figures.

The private candidate remains fail-closed. `repository_safe`, final source-status review, and author release remain publication-boundary decisions; this document does not authorize publication or commit the private note source.

## Re-evaluation

Do not periodically add Quarto merely because it exists. Re-evaluate it when a future Research Note crosses one of the feature triggers above. At that point run a dedicated local pilot against the current stable Quarto release before changing production CI.