# Research Notes tooling and integration decision record

This document records the tooling architecture for the Research Notes system. The objective is not to maximize the number of tools. Each tool must have one clear responsibility, preserve the private/public boundary, and reduce more maintenance than it adds.

## 1. Final architecture

Use a deliberately hybrid but minimal stack:

1. **Obsidian** — private capture, literature notes, concept development, and research thinking.
2. **Quartz 5, local only** — optional private graph/search/backlink/transclusion layer.
3. **Native Hugo Markdown** — default canonical source for ordinary Research Notes.
4. **Hugo** — sole production renderer and owner of navigation, typography, metadata, structured data, accessibility, page layout, and the public `bhalaji.com` visual system.
5. **GitHub** — public-source version control, CI, review, deployment evidence, and post-clearance publication history only.
6. **Zotero + Better BibTeX** — optional local reference-management path for curated public bibliographies; the master library remains private.
7. **Quarto** — optional, feature-triggered compiler only when a note genuinely needs capabilities that native Hugo Markdown does not provide efficiently.

Do **not** replace Hugo with Quartz, Quarto, MyST/Jupyter Book, Astro/Starlight, Material for MkDocs, Docusaurus, or Obsidian Publish unless a future requirement cannot be met cleanly within the current architecture.

## 2. Private research layer

### Obsidian

Best role: private research engine.

Use for embryo ideas, literature notes, private reflections, source annotations, research questions, candidate outlines, and conceptual relationships.

Privacy is determined by the storage/data-classification decision, not by Obsidian itself. Remote sync is used only when the service is permitted for the data class involved.

Official reference: <https://obsidian.md/help/sync/security>

### Quartz 5

Best role: private/local knowledge-navigation layer.

Useful capabilities include backlinks, graph navigation, local search, transclusions, configurable filters, and static local preview.

Filtering a draft from generated Quartz output does **not** make the source private. Quartz is therefore not the confidentiality boundary and is not part of the canonical public deployment.

Official references:

- <https://quartz.jzhao.xyz/>
- <https://quartz.jzhao.xyz/advanced/making-plugins>

## 3. Default Research Note authoring

**Default canonical source: native Hugo Markdown.**

This keeps one directly reviewable, directly publishable source and avoids generated-source drift.

The Note 001 private comparison confirmed that for a prose-led note with a modest bibliography and a small number of figures, Quarto would add `.qmd` source, bibliography/compiler management, and generated Markdown without removing enough authoring work to justify the extra transformation layer.

The detailed decision is recorded in `docs/research-note-authoring-decision.md`; issue #79 is closed as completed.

## 4. Quarto — conditional, not standard infrastructure

Quarto remains useful because it supports Pandoc/citeproc citations, CSL styles, numbered figures/tables/equations, cross-references, executable Python/R/Jupyter content, reproducible plot generation, and `hugo-md` output.

Official references:

- <https://quarto.org/docs/output-formats/hugo.html>
- <https://quarto.org/docs/authoring/footnotes-and-citations>
- <https://quarto.org/docs/authoring/cross-references>

Re-evaluate Quarto only when a future note genuinely needs one or more of:

- executable Python/R/Jupyter output;
- dense numbered cross-references across figures, tables, or equations;
- equation-heavy technical authoring;
- citation-heavy synthesis where BibTeX/CSL materially reduces maintenance risk;
- multi-format scientific output from one canonical source.

A future Quarto pilot must still preserve Hugo as the final renderer, produce deterministic/reviewable Markdown, keep private `.qmd`/notebooks/data outside public Git until repository-safe, and pass the same disclosure/provenance/accessibility controls as hand-authored assets.

Quarto is **not** added to portfolio CI for Note 001.

## 5. Reference management

Recommended optional path:

`private Zotero collection -> Better BibTeX deterministic citekeys/export -> curated public bibliography -> Hugo or Quarto when justified`

Rules:

- keep the master Zotero library private;
- export only public bibliographic metadata used by the note;
- do not export private notes, annotations, attachments, unpublished manuscripts, or restricted metadata;
- citation existence is not enough: claim-to-source fit and source-status review remain mandatory.

Official Better BibTeX references:

- <https://retorque.re/zotero-better-bibtex/citing/>
- <https://retorque.re/zotero-better-bibtex/exporting/auto/>

## 6. Citation verification support

Use layered verification rather than relying on one tool:

- Crossref/Crossmark where available for metadata/update signals;
- Consensus free tier for optional literature discovery/triangulation;
- installed citation-audit tools when their current access is free/eligible and useful;
- direct inspection of the underlying paper/source for the claim being made.

No plugin, AI system, or citation graph substitutes for reading the relevant source.

Do not make Scite or paid-only research/SEO products default dependencies unless a future verified academic/student entitlement makes them genuinely no-cost and they solve a measured gap.

## 7. Discoverability support

Use the existing first-party/free measurement plane first:

- Google Search Console;
- Bing Webmaster Tools / IndexNow where already integrated;
- repository-native integrity and performance audits;
- existing privacy-compatible analytics where appropriate.

SEO tooling may identify discoverability gaps only after a topic has passed governance, evidence, and strategic-fit gates. It must never determine scientific claims or force content production.

## 8. GitHub operational support

Keep:

- Dependabot for GitHub Actions/npm updates;
- GitHub Dependency Graph;
- pinned action SHAs;
- official dependency review on pull requests;
- local pre-commit/pre-push disclosure checks;
- Research Notes governance CI;
- Research Notes presentation CI with synthetic fixtures;
- full Hugo/accessibility/performance CI;
- monthly integrity checks.

Administrative control still required in repository settings:

- require `build` from GitHub Actions;
- require `governance` from GitHub Actions;
- require `dependency-review` from GitHub Actions;
- use GitHub Actions as expected source where available;
- avoid broad bypasses.

Issue #78 tracks that remaining ruleset configuration.

## 9. Alternatives reviewed

### MyST / Jupyter Book 2

Watchlist only. Reconsider for a future multi-chapter computational book, course, extended methods manual, or notebook-heavy research monograph.

### Astro/Starlight, Material for MkDocs, Docusaurus

No migration. They are strong documentation frameworks but would duplicate or replace mature Hugo infrastructure without solving a unique Research Notes requirement.

### Obsidian Publish

Not part of the canonical path. It would duplicate Hugo hosting/branding and does not replace institutionally appropriate private storage.

## 10. Cost/access rule

Required infrastructure must be one of:

1. free/open-source;
2. already included in an approved existing service/account; or
3. available at no cost through a verified student/academic entitlement.

A trial alone does not qualify as free access for long-term architecture.

If a tool changes its pricing/access model, re-evaluate it before relying on it.

## 11. Tool-adoption test

A new tool is adopted only if it passes all six tests:

1. **Unique value** — solves a requirement not already handled adequately.
2. **Boundary safety** — preserves research-disclosure and private/public boundaries.
3. **Interoperability** — canonical content remains in durable/open formats.
4. **Maintenance ratio** — recurring value exceeds dependency/configuration burden.
5. **Exit path** — content remains usable if the tool disappears.
6. **Cost/access** — meets the free/open-source/existing-entitlement/student-access rule.

## 12. Current recommendation

Adopt/retain now:

- Hugo production;
- native Hugo Markdown as default Research Note source;
- Obsidian private authoring;
- local-only Quartz preview/navigation;
- Zotero + Better BibTeX when bibliography management warrants it;
- GitHub Dependency Graph + dependency review;
- local disclosure hooks;
- governance, presentation, build, accessibility, and performance CI.

Feature-triggered only:

- Quarto for computation/cross-reference/equation/multi-format-heavy notes.

Watchlist:

- MyST/Jupyter Book 2 for future larger computational narratives.

Do not add now:

- a second public site generator;
- public Quartz deployment;
- Obsidian Publish as canonical site;
- automatic bidirectional vault/public-repository synchronization;
- paid-only SEO/research tooling as required infrastructure;
- generic prose/SEO plugins that duplicate existing checks without clear signal.