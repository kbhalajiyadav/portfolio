# Research Notes design and publication standard

This document defines **how** a Research Note should read, look, behave, and remain maintainable after it has passed the governance and strategic publication gates.

It complements:

- `docs/research-notes-governance.md` — **can** this material enter public disclosure?
- `docs/research-publishing-visibility-strategy.md` — **should** this topic be published and how does it create long-term value?
- `docs/research-notes-lifecycle.md` — **where** does the note live through embryo, incubation, staging, publication, correction, and retirement?

The design standard answers: **how should the public artifact work?**

## 1. Design objective

A Research Note is not a conventional blog post and not a simulated journal paper. It is a curated explanatory layer connecting scientific questions, methods, evidence, interpretation, and the author's public scholarly record.

The section may introduce an editorial reading layout, but it may not introduce a second visual identity.

Reuse the portfolio's existing:

- typography;
- palette/tokens;
- spacing scale;
- navigation and footer;
- link language;
- border/radius conventions;
- responsive breakpoints where appropriate;
- accessibility conventions;
- restrained motion principles.

## 2. Note classes

Use only three authoring classes initially:

- `method` — measurement, analysis, reproducibility, workflow, or experimental reasoning;
- `concept` — scientific concepts interpreted through the author's research perspective;
- `reflection` — evidence-grounded methodological or intellectual reflection.

The public status is independent of type:

- `evolving`;
- `stable`;
- `corrected`;
- `retired`;
- `withdrawn`.

Do not create new categories until a real corpus makes them necessary. Subject granularity belongs primarily in tags/topics.

## 3. Reading hierarchy

A normal note should support three depths of use:

### Five-second layer

The first viewport should communicate:

- note class;
- descriptive title;
- one- or two-sentence standfirst/summary;
- publication/revision status;
- central question or conclusion.

### Thirty-second layer

A scanning reader should find:

- `In brief` or equivalent concise synthesis;
- meaningful section headings;
- the first explanatory figure when one materially helps;
- key limitations/conditions;
- clear route to related public evidence.

### Deep-reading layer

The full note may contain:

- scientific argument;
- figures/tables/equations;
- evidence and citations;
- failure modes;
- interpretation;
- limitations;
- related research/software;
- references;
- revision/correction information when applicable.

## 4. Default article anatomy

Use this as the normal sequence, not a rigid template:

1. kicker: `Research Note · Method|Concept|Reflection`;
2. title;
3. standfirst;
4. metadata: author, publication date, substantive update date, status;
5. `In brief`;
6. primary explanatory figure when useful;
7. problem/context;
8. main explanation or method;
9. interpretation/failure modes;
10. practical or scientific implications;
11. limitations/uncertainty;
12. related public work;
13. references;
14. correction/revision notice when required;
15. related notes / next navigation.

Do not force a hero image.

## 5. Length and text density

Length follows the scientific problem, not an SEO target.

Typical ranges:

- short technical note: about 600–1,000 words;
- standard research note: about 1,000–1,800 words;
- substantial method/concept note: occasionally up to about 2,500 words.

If substantially longer, test whether the content should become two linked notes or a larger scholarly artifact.

Body typography should target a readable line length of roughly 65–72 characters where practical.

Avoid:

- large uninterrupted prose blocks;
- one-sentence paragraphs used only for visual rhythm;
- artificial heading proliferation;
- listicle formatting where continuous scientific explanation is clearer.

## 6. Headings and navigation

Headings must describe the scientific function of the section.

Prefer:

- `What the trace actually contains`;
- `Where interpretation can fail`;
- `Why timing becomes part of the measurement`.

Avoid generic headings such as `Discussion` when a more informative heading exists.

Table of contents rule:

- short note with fewer than about four substantial sections: no TOC;
- longer technical note: compact TOC;
- mobile: collapsed/disclosure UI;
- desktop: inline or restrained side treatment.

No permanent large digital-garden sidebar is required on public notes.

## 7. Scientific visual grammar

Every visual must reduce cognitive work, demonstrate evidence, or make a relationship easier to understand. Decorative laboratory imagery is not a reason to add a figure.

Choose visual form by reader question:

| Reader question | Preferred form |
| --- | --- |
| What is happening? | conceptual schematic |
| In what sequence? | process diagram |
| How are elements related? | relationship map |
| How does a quantity change? | plot |
| Which region matters? | annotated trace |
| How is the experiment arranged? | geometry/setup diagram |
| What should be selected? | decision matrix |
| What are the trade-offs? | comparison table |

### Figure classes

Permitted figure classes:

- original conceptual schematic;
- original public/cleared scientific data;
- openly licensed/public data with attribution;
- adapted/reproduced figure with appropriate rights;
- clearly labelled illustrative/simulated figure;
- photograph with rights and disclosure clearance.

Illustrative/simulated curves must never be visually or verbally represented as measured data.

## 8. Figure design

Prefer SVG for:

- conceptual schematics;
- diagrams;
- line illustrations;
- many charts where browser/print behavior remains reliable.

Prefer optimized AVIF/WebP (with appropriate fallback when needed) for photographs/raster imagery.

Scientific plots require:

- labelled axes;
- units;
- readable labels at mobile widths;
- caption;
- legend only where useful;
- source/provenance classification;
- non-color redundancy when categories must be distinguished.

Meaning must not rely on color alone. Use line style, markers, labels, shape, or direct annotation as appropriate.

Photographs require both visible-content review and metadata/EXIF sanitization before publication.

## 9. Captions and alternative text

Use three separate layers when useful:

- `alt` — concise purpose/content needed to understand the image;
- caption — interpretation/provenance/context;
- surrounding prose — full scientific reasoning.

Do not stuff complete technical explanations into `alt` when the adjacent prose already provides them.

Purely decorative images, if ever used, receive empty alternative text.

## 10. Citations and references

Technical factual claims should be supported where a knowledgeable reader would reasonably ask for evidence.

Prefer:

- peer-reviewed primary literature;
- standards;
- authoritative technical sources;
- the author's relevant public paper/thesis/software/dataset/record.

A citation must support the specific nearby claim. Citation existence alone is not sufficient.

The references section should provide durable identifiers such as DOI where available.

Quarto/Pandoc citeproc may be used for notes that benefit from bibliography automation. Plain Markdown notes may use the site's native reference component once implemented.

Do not visually imitate a journal article unless the scholarly function genuinely requires it.

## 11. Evidence and uncertainty language

The text should make epistemic status legible.

Useful levels:

1. established/public scientific evidence;
2. author's already-public result;
3. supported interpretation;
4. methodological perspective;
5. hypothesis/open question.

Language must change accordingly. Avoid presenting interpretation as established fact.

## 12. Equations, code, and computational output

Equations should be rendered semantically and accessibly rather than embedded as raster images.

Executable code is included only when it materially improves reproducibility or understanding.

For computational notes:

- preserve source/code provenance;
- pin or record relevant environments when reproducibility depends on versions;
- do not publish sensitive input data;
- distinguish generated illustrative output from research data;
- prefer static accessible output over unnecessary interactive JavaScript.

Quarto is the preferred pilot for this class of note because it can generate Hugo Markdown while preserving Hugo as the final renderer.

## 13. Performance and Core Web Vitals

Research Notes should remain lighter than typical marketing/blog pages.

Public target thresholds:

- LCP: ≤ 2.5 s;
- INP: ≤ 200 ms;
- CLS: ≤ 0.1;

Internal Lighthouse goal for the static note template where practical:

- Performance: ≥ 95;
- Accessibility: 100;
- Best Practices: 100;
- SEO: 100.

These are engineering quality targets, not ranking guarantees.

Rules:

- no mandatory hero image;
- reserve image dimensions to prevent layout shift;
- responsive raster sources;
- lazy-load below-the-fold media;
- avoid client JavaScript for primary reading functionality;
- do not ship a graph/search framework until corpus size justifies it.

Authoritative references:

- <https://web.dev/articles/vitals>
- <https://developer.chrome.com/docs/lighthouse/overview>

## 14. Accessibility

Target WCAG 2.2 AA at minimum, with automated and manual checks.

Require:

- semantic heading order;
- keyboard accessibility;
- visible focus;
- sufficient contrast;
- descriptive link text;
- accessible figures/equations;
- adequate target sizes;
- no information encoded only through color;
- tables represented as real HTML tables, not screenshots;
- reduced-motion support for any animation.

Animation must be scientifically useful and must not be required to understand the content.

Authoritative reference: <https://www.w3.org/WAI/WCAG22/>

## 15. Metadata and machine readability

Published notes should expose:

- unique page title;
- meta description;
- canonical URL;
- Open Graph metadata;
- social preview image where appropriate;
- `Article` structured data;
- author linkage;
- `datePublished`;
- substantive `dateModified`;
- representative image where useful;
- breadcrumb structured data;
- related-publication/software links.

`dateModified` must represent a substantive intellectual/content update, not a CSS or build-system change.

Use `Article`, not `BlogPosting`, unless the content model materially changes.

Google reference: <https://developers.google.com/search/docs/appearance/structured-data/article>

## 16. Social preview system

Generate social cards from the same visual system as the portfolio.

Default composition:

- note type/status;
- article title;
- author identity/monogram as appropriate;
- `bhalaji.com` provenance;
- portfolio palette and typography.

Do not use unrelated stock photographs simply to fill the social card.

## 17. Public note landing page

`/notes/` should be relevance/topic oriented, not primarily a reverse-chronological blog feed.

Initial sections may include:

- featured notes;
- Methods;
- Concepts;
- Reflections;
- topics/tags.

Dates remain visible metadata but should not dominate discovery.

Full-text search is deferred until the corpus is large enough to justify it; topic/tag filtering and strong internal linking are sufficient initially.

## 18. Internal-link architecture

Every note should be evaluated for meaningful links to:

- related notes;
- relevant research pages;
- publications;
- software;
- thesis/public scholarly records;
- external authoritative sources.

Anchor text should describe the destination/question rather than use generic `read more` language where context permits.

The public site may borrow Quartz's knowledge-graph principles without exposing a large graph visualization.

## 19. Revision, correction, retirement, and withdrawal rendering

### Minor edit

Spelling, formatting, or non-substantive link repair:

- correct silently;
- do not update substantive review date solely for this change.

### Substantive revision

Scientific clarification or meaningful new public evidence:

- update substantive modification date;
- add a compact revision note when reader interpretation could change.

### Corrected

Material factual/scientific error that does not invalidate the whole note:

- retain canonical URL;
- show visible correction notice;
- explain what changed without obscuring the record.

### Retired

Superseded/no longer maintained:

- keep a minimal page;
- explain status;
- link to replacement/current material when available.

### Withdrawn

Content should not be relied upon:

- retain a minimal status/tombstone page unless legal/safety circumstances require otherwise;
- avoid repeating problematic material unnecessarily;
- preserve enough provenance to prevent silent historical rewriting.

## 20. Print and archival behavior

A note should remain intelligible when printed or saved as PDF:

- remove unnecessary navigation/chrome;
- preserve figure captions and references;
- avoid orphaned headings where CSS can prevent them;
- preserve URLs/DOIs legibly where practical;
- interactive-only content must have a static fallback.

## 21. Mobile behavior

Mobile is a first-class reading surface.

Test at minimum:

- 320 px reflow width;
- 390 px mobile;
- common laptop viewport;
- wide desktop.

Plots/tables may scroll horizontally only when reflow would destroy scientific meaning; when scrolling is necessary, communicate it accessibly and avoid clipping labels.

## 22. Search/discovery quality

Search-facing title/description text must describe the real scientific question and expected reader value.

Avoid:

- clickbait;
- keyword stuffing;
- generic introductory pages created solely to capture traffic;
- duplicate articles differing only by wording;
- automatic content expansion based on search-volume opportunities.

Discovery optimization occurs after scientific/gov/strategic eligibility.

## 23. Release QA

Before `draft: false`, a note must pass:

### Scientific

- claims reviewed;
- citations verified;
- source-status/retraction check complete;
- interpretation/uncertainty appropriately labelled.

### Governance

- repository-safe;
- disclosure/ownership/IP/ethics/venue/COI/funding/privacy/copyright controls resolved.

### Editorial

- primary reader job is clear;
- title/standfirst/In Brief work at scan depth;
- limitations included where needed;
- related evidence linked.

### Visual

- figures have a reason to exist;
- figure provenance recorded;
- mobile/readability checked;
- alt/captions checked;
- no accidental disclosure in images/metadata.

### Web

- canonical/meta/social/schema valid;
- internal/external links pass;
- accessibility automation/manual checks pass;
- responsive checks pass;
- Lighthouse/performance gates pass;
- print output is acceptable for technical notes where relevant.

## 24. Anti-complexity rule

Do not add a component, plugin, animation, framework, search engine, CMS, or publishing service because it is fashionable or because another research site uses it.

Add it only when it removes more operational or reader complexity than it introduces.

The intended result is a durable scholarly surface whose sophistication is visible in the evidence architecture and clarity—not in the number of technologies used.