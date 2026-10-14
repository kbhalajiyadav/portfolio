# Research Notes tooling and integration decision record

This document records the tooling architecture for the Research Notes system. The objective is not to maximize the number of tools. It is to give each tool one clear responsibility, keep the public site coherent with `bhalaji.com`, and avoid introducing a second publishing stack when an existing component already solves the problem.

## 1. Decision summary

Use a deliberately hybrid stack:

1. **Obsidian** — private note capture, literature notes, concept development, and graph-based research thinking.
2. **Quartz 5, local only** — optional private preview/navigation layer for backlinks, graph exploration, search, transclusions, and digital-garden behavior.
3. **Quarto, optional per-note compiler** — pilot for notes that genuinely need scholarly mechanics such as citations, bibliographies, numbered figures/tables/equations, cross-references, or reproducible Python/R/Jupyter output.
4. **Hugo** — remain the only production website renderer and owner of navigation, typography, metadata, structured data, accessibility, page layout, and the public `bhalaji.com` visual system.
5. **GitHub** — public-source version control, CI, review, deployment evidence, and post-clearance publication history only.
6. **Zotero + Better BibTeX (local toolchain, optional but recommended)** — canonical personal reference management and deterministic BibTeX/BibLaTeX export for public-note citations.

Do **not** replace Hugo with Quartz, Quarto, MyST/Jupyter Book, Astro/Starlight, Material for MkDocs, Docusaurus, or Obsidian Publish unless a future requirement cannot be met cleanly within the current architecture.

## 2. Tool responsibility boundaries

### Obsidian

Best role: private research engine.

Use for:

- embryo ideas and fragments;
- literature notes;
- backlinks and conceptual relationships;
- private reflections;
- candidate outlines;
- source annotations;
- research questions and future-note seeds.

Privacy is determined by the storage/data-classification decision, not by Obsidian itself. If remote sync is used, the service must be permitted for the data class involved. Obsidian Sync supports end-to-end encryption, but institutional/storage rules still control whether a particular research dataset or confidential material may be stored there.

Official reference: <https://obsidian.md/help/sync/security>

### Quartz 5

Best role: private digital-garden preview.

Strengths:

- native Obsidian-style Markdown workflow;
- backlinks and graph navigation;
- local search;
- transclusions;
- configurable filters and plugins;
- static output.

Limit: filtering a draft from generated output does **not** make its source private. Quartz is not the confidentiality boundary.

Official references:

- <https://quartz.jzhao.xyz/>
- <https://quartz.jzhao.xyz/advanced/making-plugins>

Decision: keep Quartz local/private and decoupled from the production deployment.

### Quarto

Best role: optional scientific-authoring/compiler layer.

Quarto is unusually compatible with the existing architecture because it has a first-class `hugo-md` output format. In this mode Quarto can execute code and generate Markdown while Hugo remains responsible for theming, navigation, page layout, and final HTML.

Useful capabilities:

- Pandoc/citeproc citations and bibliographies;
- CSL citation styles;
- numbered figures, tables, equations, sections, theorems, and proofs;
- cross-references;
- executable Python/R/Jupyter content;
- reproducible plot generation;
- Hugo Markdown output.

Official references:

- <https://quarto.org/docs/output-formats/hugo.html>
- <https://quarto.org/docs/authoring/footnotes-and-citations>
- <https://quarto.org/docs/authoring/cross-references>

Decision: **pilot, do not make mandatory yet**. A normal prose Research Note should remain plain Hugo Markdown. Adopt Quarto only when it removes real manual scientific-authoring work.

A Quarto pilot must satisfy all of the following before becoming part of CI:

- no change to the public visual identity;
- generated Markdown is deterministic enough for review;
- source `.qmd`, notebooks, code, and data remain outside public Git until repository-safe;
- raw HTML requirements do not weaken the site's security or integrity controls;
- generated assets pass the same disclosure and provenance checks as hand-authored assets;
- build time and dependency burden remain proportionate.

### MyST / Jupyter Book 2

MyST is a strong scientific-document system with citations, equations, cross-references, figures, directives, executable content, and publication-quality output. Jupyter Book 2 is now a distribution of the MyST Document Engine.

Official references:

- <https://mystmd.org/guide/quickstart-myst-markdown>
- <https://mystmd.org/guide/citations>
- <https://jupyterbook.org/stable>

Decision: **watchlist, not current integration**. MyST/Jupyter Book becomes attractive if the project later needs a multi-chapter computational book, course, extended methods manual, or notebook-heavy research monograph. For individual portfolio notes, adding MyST alongside Hugo and Quartz would currently duplicate more infrastructure than it removes.

### Astro Starlight

Starlight provides accessible documentation defaults, search, SEO, Markdown/MDX, frontmatter validation, and a plugin ecosystem.

Official reference: <https://starlight.astro.build/>

Decision: no migration. It would be a strong choice for a new documentation product, but `bhalaji.com` already has a mature Hugo design system and validation stack. Migrating would create large regression and maintenance cost without solving a unique Research Notes requirement.

### Material for MkDocs

Material for MkDocs provides excellent built-in search, tags, blogging, media optimization, privacy/offline capabilities, and documentation navigation.

Official references:

- <https://squidfunk.github.io/mkdocs-material/plugins/>
- <https://squidfunk.github.io/mkdocs-material/plugins/search/>

Decision: no migration. It is optimized for documentation and knowledge bases; reproducing the current portfolio identity and evidence architecture would cost more than the gains.

### Docusaurus

Docusaurus is strong for large versioned technical-documentation products.

Official reference: <https://docusaurus.io/docs/versioning>

Decision: no migration. Its own documentation cautions that versioning increases contributor/build complexity and should be used only when the use case warrants it. Research Notes need corrections and status history, not multiple complete documentation versions.

### Obsidian Publish

Obsidian Publish can provide public or password-protected sites and integrates tightly with Obsidian.

Official references:

- <https://obsidian.md/help/publish/security>
- <https://obsidian.md/help/teams/publish>

Decision: not part of the canonical publishing path. It would duplicate Hugo hosting and branding, while site-password protection is site-wide rather than individual-note access control. A private authoring vault should remain private rather than rely on an unlisted or password-protected publishing surface unless institutional storage/hosting review explicitly allows it.

## 3. Reference-management architecture

### Zotero + Better BibTeX

Recommended local reference-management path:

`Zotero collection -> Better BibTeX deterministic citekeys -> curated public-note bibliography -> Quarto/Hugo rendering`

Better BibTeX provides stable/configurable citation keys and automatic exports suitable for text-based/version-controlled authoring.

Official references:

- <https://retorque.re/zotero-better-bibtex/citing/>
- <https://retorque.re/zotero-better-bibtex/exporting/auto/>

Rules:

- keep the master Zotero library private;
- export only a curated collection containing public sources used by Research Notes;
- do not export private notes, attachments, annotations, unpublished manuscripts, or restricted metadata into this public repository;
- citation existence is not enough: source status/retraction/correction review remains required before publication.

## 4. Citation verification support

The publication process should combine different tools rather than ask one system to prove everything:

- **Crossref/Crossmark** — canonical metadata and update/correction/retraction signals where available;
- **Scite** — optional citation-context and citation-graph review;
- **Consensus / scholarly-search connectors** — literature discovery and triangulation;
- **Scholar Sidekick / reference auditing tools** — fabrication/retraction checks where appropriate;
- manual inspection of the actual paper/source — final authority for the claim being made.

No plugin, AI tool, or citation graph substitutes for reading the underlying source relevant to the claim.

## 5. Discoverability support

Primary measurement plane:

- Google Search Console for indexing, queries, impressions, and clicks;
- existing site analytics/privacy controls where appropriate;
- Ahrefs only if deeper backlink, keyword, competitor, or AI-visibility analysis justifies the subscription and complexity.

Do not let SEO tools determine scientific claims or publication topics. They can identify discoverability gaps after a topic has already passed governance/evidence/strategic-fit gates.

## 6. GitHub operational support

Keep:

- Dependabot for GitHub Actions and npm dependency updates;
- pinned action SHAs;
- local pre-commit/pre-push disclosure checks;
- Research Notes governance CI;
- full Hugo/accessibility/performance CI;
- monthly integrity checks.

Add/require administratively:

- main-branch ruleset requiring `governance` and `build` status checks;
- expected source app set to GitHub Actions where possible;
- no bypass except deliberate emergency/admin use;
- consider requiring the dependency-review check after it proves stable.

GitHub documents that required status checks can be bound to an expected GitHub App source and must pass before merge when enabled in a ruleset:
<https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>

## 7. Tool-adoption test

A new tool is adopted only if it passes all five tests:

1. **Unique value** — solves a requirement not already handled adequately.
2. **Boundary safety** — does not blur private/public or evidence/disclosure boundaries.
3. **Interoperability** — plain files and durable formats remain available; avoid proprietary lock-in for the canonical record.
4. **Maintenance ratio** — recurring value exceeds dependency/configuration burden.
5. **Exit path** — content remains usable if the tool disappears.

This prevents the system from becoming a collection of overlapping plugins.

## 8. Current recommendation

Adopt now:

- Hugo production;
- Obsidian private authoring;
- local-only Quartz preview;
- existing governance/build CI;
- local disclosure hooks;
- dependency review (after CI validation);
- explicit GitHub ruleset required checks (manual repository-admin action).

Pilot next:

- Quarto `hugo-md` for one private/local methods-note prototype;
- Zotero + Better BibTeX curated bibliography export.

Optional external integrations:

- Scite for citation-context review;
- Ahrefs only when deeper SEO/backlink intelligence is useful.

Watchlist:

- MyST/Jupyter Book 2 for future multi-page computational narratives.

Do not add now:

- second public site generator;
- public Quartz deployment;
- Obsidian Publish as canonical site;
- automatic bidirectional vault/public-repository synchronization;
- generic prose/SEO plugins that duplicate existing governance checks without clear signal.