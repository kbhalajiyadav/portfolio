# Portfolio design governance

This document records the design, information-architecture, scientific-communication, and release lessons that should carry forward into every portfolio change. It is a decision framework, not a visual-style checklist. New work should preserve these principles unless there is a documented reason to depart from them.

## 1. Primary objective

The portfolio should behave like a well-designed scientific instrument: restrained, legible, purposeful, evidence-driven, and easy to inspect. Changes should improve scientific communication, trust, orientation, or usability rather than add decoration for its own sake.

The default priority order is:

1. factual accuracy and provenance;
2. hierarchy and wayfinding;
3. scientific communication;
4. accessibility and responsive behavior;
5. visual rhythm and consistency;
6. performance and maintainability;
7. decorative polish.

## 2. Information hierarchy and wayfinding

Primary destinations are `About`, `Research`, `Outputs`, `Experience`, `Engagement`, and `Contact`. The persistent header is the main wayfinding system for these pages.

Rules:

- Primary destination pages do not show a redundant `Portfolio home` back link.
- Detail pages do show one contextual parent link when it helps users recover the information hierarchy.
- Publication and thesis records return to `Research outputs`.
- Intellectual-property and research-software records return to `Research outputs`.
- Research-project records return to `Research`.
- Industry case studies return to `Experience`.
- Utility pages that are not primary destinations may still use a home link when helpful.
- A back-link label should name the parent destination, not the implementation concept of a home page.

## 3. Evidence-link contract

A link that names specific evidence must land on that specific evidence, not merely the containing section.

Examples:

- `article` -> article record;
- `software` -> software record;
- `patent-pending technology` -> intellectual-property record;
- `adhesion presentations` -> the adhesion presentation series;
- `computer-vision presentations` -> the computer-vision presentation series.

For hash-linked expandable evidence:

- the target has a stable explicit ID;
- the browser scroll position reserves the sticky-header offset;
- the target automatically opens when addressed by the hash;
- the target receives a restrained persistent target state so the visitor can identify what the link referenced;
- target emphasis must not depend on animation or color alone.

## 4. Scientific visual integrity

Visuals are either empirical evidence or explanatory schematics. They must never blur that distinction.

Rules:

- Do not publish synthetic CSV traces, fabricated axes, or simulated measurements as if they were observed data.
- Synthetic data may be used privately to test plotting layouts, but not as public evidence unless clearly and prominently labelled as simulated.
- Conceptual diagrams should be explicitly schematic and should avoid quantitative axes or numerical claims.
- Prefer original SVG/HTML/CSS scientific schematics over generic stock imagery or decorative AI imagery.
- Use real experimental plots only when the underlying data and interpretation are defensible and appropriately attributable.
- Scientific visuals should reuse the portfolio visual language: restrained linework, teal/rust accents, serif/sans hierarchy, and the existing trace/rings/grid motifs.

The portfolio signature sequence is:

`Stimulus -> Structure -> Response -> Measurement -> Translation`

It is explanatory, not a claim of quantitative data.

## 5. Content architecture and public language

Public copy should communicate research rather than expose internal project-management language.

Rules:

- Labels should add orientation instead of repeating the adjacent heading.
- Use method-level terms on program pages (`computer vision`) and implementation-specific tools (`OpenCV`) where technical detail is appropriate.
- Avoid governance, audit, release, benchmark, package, or staging language in visitor-facing prose unless the subject itself requires it.
- Homepage copy argues the research identity; destination pages carry the fuller evidence.
- Repetition across Home, About, Research, Outputs, Experience, and Engagement should be intentional and role-specific.

## 6. Counts, dates, and derived claims

Do not manually duplicate numerical claims when they can be derived or checked against canonical records.

Rules:

- Presentation counts must agree with `data/portfolio.yaml` canonical presentation records.
- Publication, software, student-project, and intellectual-property counts must be traceable to canonical structured data.
- Dates and role chronology must agree across `data/portfolio.yaml`, `data/cv.yaml`, rendered pages, and the generated CV.
- If a count cannot be made deterministic, prefer a non-numeric phrase over an unverified number.

## 7. Rhythm and spacing

Visual consistency means shared hierarchy and rhythm, not forcing every content type into the same card.

Rules:

- Related heading/body pairs must have visible breathing room; headings should not visually collide with body text.
- Section spacing should communicate hierarchy: page shell -> section -> subsection -> heading/body -> record.
- Equal-height cards are used only when content and comparison benefit from equal height.
- Intrinsic-height editorial structures are preferred for education, timelines, records, and asymmetric content.
- Large unused white zones require a content or hierarchy reason; they are not a substitute for spacing.
- Repeated cards, borders, shadows, or callouts should be removed when they do not add semantic structure.

## 8. Responsive composition

Passing overflow checks is necessary but not sufficient. Each major width band should look intentionally composed.

Rules:

- Desktop can use two-column editorial compositions when both columns retain readable measures.
- The hero should stack before the text column becomes visibly squeezed by the portrait.
- Tablet is a first-class layout state, not merely compressed desktop.
- Mobile ordering prioritizes orientation and action: context -> heading -> explanation -> actions/status -> visual.
- The sticky header, menu, target offsets, and TOC must remain synchronized at every breakpoint.
- Responsive QA includes at least 320, 390, 680, 768, 820, 980, 1180, 1440, and a wide desktop state when relevant.

## 9. Interaction states

Every interactive state must explain itself.

Rules:

- Hover, focus, active, current-page, expanded, and hash-target states must be distinguishable.
- Keyboard and pointer behavior must remain equivalent.
- Focus should never be removed without a visible replacement.
- Expandable records retain native `details/summary` semantics unless a stronger accessible pattern is required.
- Reduced-motion preference is respected.

## 10. Card and component discipline

The site should use the smallest set of component patterns that accurately fit the information.

- Research programs may use the numbered three-part system.
- Education and chronology use editorial/timeline structures.
- Presentation series use expandable records.
- Detail pages use article/case-study layouts.
- Do not introduce a new card style when an existing semantic pattern fits.
- Visual variation is acceptable when structural hierarchy remains predictable.

## 11. Provenance, SEO, and external records

- Claims should link to authoritative records when reasonable.
- Structured data, canonical URLs, OpenGraph/Twitter metadata, ORCID, Scholar, GitHub, institutional records, and DOI links must remain synchronized.
- External institutional pages can support a claim only to the extent that their current text supports it; stale external pages must not override newer canonical records.
- Search/indexing lag must not be mistaken for deployment state. Verify the live response directly.

## 12. Deployment and test workflow

Substantial design/content changes are developed on a branch and reviewed through a pull request.

Required sequence:

`branch -> source audits -> production build -> generated-site audit -> browser accessibility/responsive/interaction audits -> Lighthouse -> PR review -> merge -> Pages deployment -> live smoke test -> exact release-marker verification`

A successful build is not equivalent to a successful deployment, and a successful Pages deployment is not equivalent to a successful live smoke test. Treat them as independent gates.

## 13. Change-review questions

Before merging any change, ask:

- Is the fact supported and canonical?
- Is this the correct information level and parent destination?
- Does a link land on the exact evidence named by its text?
- Is the wording public-facing rather than internal?
- Does the layout still make sense at tablet widths, not only desktop/mobile?
- Is whitespace carrying hierarchy rather than accidental emptiness?
- Is a new visual clearly schematic or clearly empirical?
- Are all interaction states keyboard-accessible and understandable?
- Did we create a one-off exception that should instead become a reusable rule?
- Did source, rendered, and live-release checks all pass?

## 14. Exceptions

Rules can be overridden when a specific scientific, accessibility, or communication need justifies it. The exception should be documented in the relevant template/content change or pull-request rationale so future work does not accidentally normalize a one-off choice.
