# Research Notes tooling and integration decision record

This document records the tooling architecture for the Research Notes system. The objective is not to maximize the number of tools. It is to give each tool one clear responsibility, keep the public site coherent with `bhalaji.com`, avoid introducing a second publishing stack when an existing component already solves the problem, and avoid making paid-only services part of the required workflow.

## 1. Decision summary

Use a deliberately hybrid stack:

1. **Obsidian** — private note capture, literature notes, concept development, and graph-based research thinking.
2. **Quartz 5, local only** — optional private preview/navigation layer for backlinks, graph exploration, search, transclusions, and digital-garden behavior.
3. **Quarto, optional per-note compiler** — pilot for notes that genuinely need scholarly mechanics such as citations, bibliographies, numbered figures/tables/equations, cross-references, or reproducible Python/R/Jupyter output.
4. **Hugo** — remain the only production website renderer and owner of navigation, typography, metadata, structured data, accessibility, page layout, and the public `bhalaji.com` visual system.
5. **GitHub** — public-source version control, CI, review, deployment evidence, and post-clearance publication history only.
6. **Zotero + Better BibTeX (local toolchain, recommended)** — canonical personal reference management and deterministic BibTeX/BibLaTeX export for public-note citations.

Do **not** replace Hugo with Quartz, Quarto, MyST/Jupyter Book, Astro/Starlight, Material for MkDocs, Docusaurus, or Obsidian Publish unless a future requirement cannot be met cleanly within the current architecture.

## 2. Cost/access rule

Required infrastructure must be free/open-source or already included in the repository/hosting stack. Optional ChatGPT/external integrations may be recommended only when they have a genuine free tier or a verifiable academic/student-access route. Paid-only services must not become a dependency of publication, governance, discoverability measurement, or citation verification.

A student discount alone does not make a tool part of the default stack if a free/open alternative already handles the requirement adequately.

## 3. Tool responsibility boundaries

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

Privacy is determined by the storage/data-classification decision, not by Obsidian itself. If remote sync is used, the service must be permitted for the data class involved. Institutional/storage rules still control whether a particular research dataset or confidential material may be stored there.

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

Quarto is unusually compatible with the existing architecture because it has a first-class `hugo-md` output format. In this mode Quarto can execute code and generate Markdown while Hugo remains responsible for theming, navigation, page layout, and final HTML. Quarto itself is free and open-source.

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
- <https://quarto.org/license.html>

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

Decision: **watchlist, not current integration**. It becomes attractive if the project later needs a multi-chapter computational book, course, extended methods manual, or notebook-heavy research monograph. For individual portfolio notes, adding MyST alongside Hugo and Quartz would currently duplicate more infrastructure than it removes.

### Astro Starlight / Material for MkDocs / Docusaurus

All are capable documentation systems, but none solves a Research Notes requirement that justifies replacing the mature Hugo portfolio and its validation stack. Keep them as reference implementations, not dependencies.

### Obsidian Publish

Do not use it as the canonical publication path. It would duplicate Hugo hosting/branding and does not replace the institutional data-classification requirement for private research material.

## 4. Reference-management architecture

### Zotero + Better BibTeX

Recommended local reference-management path:

`Zotero collection -> Better BibTeX deterministic citekeys -> curated public-note bibliography -> Quarto/Hugo rendering`

Zotero is free to use locally with unlimited local items/files; its optional hosted attachment storage has a free quota. Better BibTeX is a Zotero extension used for deterministic citation keys and exports.

Official references:

- <https://www.zotero.org/support/storage_faq>
- <https://retorque.re/zotero-better-bibtex/citing/>
- <https://retorque.re/zotero-better-bibtex/exporting/auto/>

Rules:

- keep the master Zotero library private;
- export only a curated collection containing public sources used by Research Notes;
- do not export private notes, attachments, annotations, unpublished manuscripts, or restricted metadata into this public repository;
- citation existence is not enough: source status/retraction/correction review remains required before publication.

## 5. Citation verification support

Use free/open infrastructure as the baseline:

- **Crossref/Crossmark** — canonical metadata and update/correction/retraction signals where available;
- **Consensus** — optional literature discovery/triangulation through its genuine free tier; academic email may also qualify for discounted paid access, but paid access is not required by this workflow;
- installed scholarly/reference-auditing connectors may be used when their current free allowance is sufficient;
- manual inspection of the actual paper/source remains the final authority for the claim being made.

**Scite is not part of the default recommendation.** Its current ChatGPT/MCP access requires a paid plan or an active trial; an academic discount may exist, but that does not satisfy this project's free-by-default rule.

No plugin, AI tool, or citation graph substitutes for reading the underlying source relevant to the claim.

## 6. Discoverability support

Primary free measurement plane:

- Google Search Console for indexing, queries, impressions, and clicks;
- Bing Webmaster Tools where useful;
- existing site analytics/privacy controls where appropriate;
- repository-native measurements and link checks.

Do not make paid SEO suites such as Ahrefs a project dependency or default recommendation. If a university later supplies access through an institutional/student program, it can be used opportunistically, but the workflow must remain fully functional without it.

Do not let SEO tools determine scientific claims or publication topics. They may identify discoverability gaps only after a topic has passed governance, evidence, and strategic-fit gates.

## 7. GitHub operational support

Keep:

- Dependabot for GitHub Actions and npm dependency updates;
- pinned action SHAs;
- local pre-commit/pre-push disclosure checks;
- Research Notes governance CI;
- full Hugo/accessibility/performance CI;
- monthly integrity checks;
- GitHub Dependency Graph;
- official pinned dependency-review action on pull requests.

Administrative additions:

- main-branch ruleset requiring `governance` and `build` status checks;
- after successful validation on PR #77, require `dependency-review` as well;
- expected source app set to GitHub Actions where possible;
- no bypass except deliberate emergency/admin use.

GitHub documents that required status checks can be bound to an expected GitHub App source and must pass before merge when enabled in a ruleset:
<https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>

## 8. Tool-adoption test

A new tool is adopted only if it passes all six tests:

1. **Unique value** — solves a requirement not already handled adequately.
2. **Boundary safety** — does not blur private/public or evidence/disclosure boundaries.
3. **Interoperability** — plain files and durable formats remain available; avoid proprietary lock-in for the canonical record.
4. **Maintenance ratio** — recurring value exceeds dependency/configuration burden.
5. **Exit path** — content remains usable if the tool disappears.
6. **Access economics** — free/open or verifiably student-accessible; no paid-only dependency for a core function.

## 9. Current recommendation

Adopt now:

- Hugo production;
- Obsidian private authoring;
- local-only Quartz preview;
- existing governance/build CI;
- local disclosure hooks;
- GitHub Dependency Graph + dependency review;
- explicit GitHub ruleset required checks (manual repository-admin action);
- Zotero + Better BibTeX for the bibliography pilot.

Pilot next:

- Quarto `hugo-md` for one private/local methods-note prototype.

Eligible optional ChatGPT integration:

- **Consensus** — installed; genuine free tier, with academic-email discount available for optional upgrades.

Not recommended under the free/student-access rule:

- Scite as a default connector because current MCP/ChatGPT access is paid after trial;
- Ahrefs as a default integration because it is a paid SEO suite and not necessary for core discoverability work.

Watchlist:

- MyST/Jupyter Book 2 for future multi-page computational narratives.

Do not add now:

- second public site generator;
- public Quartz deployment;
- Obsidian Publish as canonical site;
- automatic bidirectional vault/public-repository synchronization;
- paid-only analytics/research connectors as core dependencies;
- generic prose/SEO plugins that duplicate existing governance checks without clear signal.
