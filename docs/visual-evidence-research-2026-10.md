# Visual evidence and research presentation — discovery brief

**Status:** research inventory and design hypotheses only; not approved for production.  
**Prepared:** 2026-10-26.  
**Scope:** bhalaji.com and its Hugo repository. No site templates, public copy, brand assets, deployment settings, or production data are changed by this brief.

## Decision in brief

Favor **authentic, attributable scientific evidence** over decoration. Keep the existing BK monogram, paper/ink/teal/rust palette, portrait, editorial hierarchy, research-signature sequence, and source-of-truth model. Enrich published work with genuine figures; use clearly labeled original SVG schematics for conceptual/process explanation. Add no scientific-looking synthetic measurements.

The target is a visitor being able to answer, in seconds: What is the research question? What was measured? What was learned? Where can I inspect the supporting paper, data, or software?

## Baseline inventory (source repository, main, inspected 2026-10-26)

- **Hugo data/template model:** landing page at `layouts/landing/list.html`, generated from `data/portfolio.yaml`. It currently renders the hero, portrait, proof, five-stage research signature, three research pillars, primary article/thesis/software research package, intellectual property, chronology, engagement, and contact.
- **Publication presentation:** `layouts/publication/single.html` contains abstract, source links, citation/BibTeX and related-record links; there is no dedicated scientific figure component yet.
- **Research overview:** `content/research/index.md` already links empirical work and makes a useful distinction between measured work and doctoral directions.
- **Checked-in visual assets:** `static/uploads/avatar-portrait.jpg`, `static/media/shelfie-feedback-friday-2026.jpg`, `static/media/bk-monogram-canonical-20260730.svg`, `static/favicon.svg`. The two SVGs implement a shared identity, not two independent research images.
- **Generated preview graphics:** `scripts/build_social_cards.py` generates deterministic social cards at build time; these are not checked-in research photographs or plots.
- **Design governance:** `docs/design-governance.md` requires schematic/empirical separation, provenance, accessibility, responsive QA, and restrained existing visual language. `docs/content-taxonomy.md` makes canonical destinations and evidence links explicit.
- **CI:** `.github/workflows/hugo.yaml` runs publication/research site audits, responsiveness, accessibility, Lighthouse, and Pages deployment; push deployment is limited to main. A research-branch documentation commit alone does not deploy.
- **Current editorial opportunity:** real scientific figures are missing from the homepage and publication/project detail pages despite rich text and evidence links. Avoid reflexively making new top-level navigation routes or duplicating the whole CV on the homepage.

## External precedent: what to learn from Bo Tang, not copy

Reference: https://botang.org/ and https://botang.org/research/

1. Research topics start with a meaningful question and an immediately understandable figure.
2. Related papers, source code, and data sit adjacent to the research account, not several clicks apart.
3. Graphics are labeled and credited. On his research page, illustrative photo/motion is explicitly distinguished from real computational data; source and license are named.
4. His design suits an optimization/software body of work. Neither his imagery nor layout needs to be reproduced, and his teaching/software IA is not automatically appropriate for the current size of this portfolio.

## Candidate visual assets — source-first shortlist

All **candidates**, not files cleared/committed for public deployment. Verify the original figure at full resolution, figure-level credits, and scientific context before promotion.

| ID | Proposed placement | Candidate / primary source | Class | Evidence and permission status | Decision |
| --- | --- | --- | --- | --- | --- |
| A1 | Homepage selected first-author output; article detail | 2026 *Polymers* article, **Figure 2A**: representative textile T-peel force/displacement behavior (verify full panel and legibility) | Empirical published figure | https://doi.org/10.3390/polym18121504 ; journal CC BY 4.0 subject to third-party exceptions | **P1**, consider contextual crop or high-quality thumbnail; never strip axes |
| A2 | Article detail, possibly overview thumbnail | Same paper **Figure 4**: multi-criteria radar comparison | Empirical published figure | Same publication and license | **P1** on detail; may be unreadable as a small homepage card |
| A3 | Article detail / wearable interface outcome | Same paper **Figure 5**: conductive trace preparation and strain-to-electrical-failure assessment | Empirical published figure and photographs | Same publication; inspect panels, coauthor/third-party credits | **P2**, do not present as validated consumer device |
| A4 | Methods note or article detail | Same paper **supplementary Figure S1**: specimen setup and peel-test arrangement | Empirical/experimental setup | Publication supplement; verify independent component rights | **P2**, potentially better to link publisher supplement than duplicate |
| B1 | Coauthored electrospinning article detail | 2025 *Polymers* article **Figure 1**: SEM images of TPU, nylon, and layered fibers, preserving scale bars | Empirical microscopy | https://doi.org/10.3390/polym17131777 ; journal CC BY 4.0 subject to third-party exceptions | **P1**, excellent material-characterization image |
| B2 | Coauthored article detail | Same paper **Figure 5**: Young's modulus comparison across fiber mats/layered variants | Empirical statistical figure | Same publication and license | **P2**, pair with accurate text on variability/conditions |
| S1 | Peel Trace Evaluation software detail | `docs/peel_trace_workflow_overview.png` in public lab repository | Published workflow diagram | https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates ; repository declares Apache-2.0; check image-specific notices | **P1**, review readability; ideal as software process figure |
| S2 | Software detail only | `docs/example_outputs/scotch_tape_qc_trace.png` from the same repository | Real example of software output | Same repository; README identifies a Scotch Tape reference/example | **P2**, explicitly label validation/demo example; NOT evidence from the published textile adhesive comparison |
| C1 | Research program / future doctoral direction | Original, text-first **stimulus → material structure → observable response → measurement** diagram | Conceptual SVG, not empirical | Can create independently from public research narrative | **P1**; preserve the five-stage signature; avoid inventing microscopy/scattering patterns or instrument results |
| C2 | Optical metrology project detail | Original flow diagram: synchronized imaging + deformation tracking → region selection → CIE L*a*b* metrics → comparative analysis | Conceptual method diagram | https://bhalaji.com/project/optical-metrology/ ; design must not reveal non-public project data | **P2**, schematic and labeled, no simulated color-to-strain result |
| P1 | Engagement / applied innovation | Existing `shelfie-feedback-friday-2026.jpg` | Existing event photograph | Already hosted; separate consent/release and recognizable third-party review required before prominent reuse | **Conditional**, do not make a homepage research hero |
| IP1 | Patent-pending Quantitative Thermal Imaging page | **No unpublished experimental imagery**. At most a non-enabling descriptive icon if university approves | Conceptual / intellectual property | https://bhalaji.com/project/quantitative-thermal-imaging/ and VCU public listing | **Hold**; no invention drawings, calibration values, unpublished details or unreleased prototypes |

The published adhesive paper's open dataset (https://doi.org/10.5281/zenodo.20278428) and version-specific software release (https://doi.org/10.5281/zenodo.20301242) provide reproducibility anchors. Replotting any figure from data would require protocol/units/selection checks, explicit version and transformation metadata, and agreement with the published interpretation. Reuse an authoritative paper figure first; do not casually regenerate apparent empirical results.

## Rights and provenance rules

- MDPI's *Polymers* publication policy states its articles are CC BY and its figures/tables may be reused with clear credit; check each selected figure for separately credited third-party components. https://www.mdpi.com/journal/polymers/about and https://www.mdpi.com/openaccess
- CC BY 4.0 attribution includes creators, source, link to license, and an indication of changes. https://creativecommons.org/licenses/by/4.0/
- Preserve a per-asset record: `id`, `source URL/DOI`, `article figure/panel`, `authors/credit`, `license`, `modifications`, `empirical|schematic|photo`, `public-release status`, `alt text`, `scientific caveat`, `intended placement`, `reviewed date`. Do not assume all assets in an Apache-2.0 repo are author-owned if an image contains independently licensed material.
- Reusable figures remain under their stated CC BY or Apache terms; do not relabel them as portfolio all-rights-reserved originals. The site's default rights notice needs an appropriate explicit exception/attribution at each figure, with links.
- No unauthorized image scraping from Bo Tang's site; it is inspiration only.
- Do not stage original data, confidential lab files, patent disclosure materials, third-party student work, private people photos, or thesis-under-embargo material.

## Three editorial layout hypotheses to test (not implementation decisions)

**Option A — Minimal evidence augmentation (preferred starting point):** retain section order, add one high-quality authentic figure into the primary research package, a small set of figures on the two article pages, and a workflow image on the software page. Lowest disruption and easiest controlled comparison.

**Option B — Evidence nearer the fold:** retain hero/portrait but introduce a compact selected-research-evidence strip immediately after proof; reposition existing editorial blocks rather than duplicate. Must prove it reduces discovery time without crowding tablet/mobile.

**Option C — Research-topic figure panels:** each of the three research pillars gets one visual, mixing empirical and schematic material only with unmistakable labels. Risk: implies equal maturity/availability of results in all three pillars; likely premature, particularly for doctoral work and IP.

Start with A. Make B contingent on user testing/navigation evidence. Defer C unless adequate genuinely released material exists.

## Suggested illustration direction

- Use existing restrained motifs: trace (force history), rings (scale/structure), grid (registration and repeatability). Treat these as navigational/graphic motifs rather than representative experimental traces.
- Scientific diagrams should use accessible HTML/SVG with descriptive captions; no pseudo-measurement axes, numerical values, or photorealistic invented lab results.
- For published microscope images, preserve scale bar and labels. For plots, maintain complete axes, unit labels, legend, resolution, error representation, and provenance. Avoid cosmetic recoloring that changes interpretation.
- Actual lab photos should only be used if releasable, accurately captioned, consented where needed, and meaningful to the science. Stock microscopy or AI-generated experimental-looking photographs are inappropriate as evidence.

## Hugo and performance implementation constraints (future, not done)

1. Prefer co-located page resources under the relevant publication/project leaf bundle or a curated `static/media/research/` folder; choose one stable convention.
2. Render responsive images using Hugo image processing where feasible, with appropriate fallback, `srcset`/`sizes`, explicit dimensions, and native lazy loading for below-the-fold figures. Preserve the current eager/fetch-priority treatment for the portrait, and re-evaluate LCP before introducing any other high-priority images.
3. Define one reusable *research figure* component with image, source, evidence-type label, credit/license, alt, optional long description, optional publication link. Avoid one-off HTML variants.
4. Prefer accessible captions and links over hover-only figure labels, autoplay animation, data-heavy sliders, or decorative carousels.
5. Export/crop with reproducible file provenance; do not silently overwrite canonical figures or change visual scientific units.

Performance reference: https://web.dev/learn/design/responsive-images

## Verification and acceptance criteria before a visual PR

**Factual/provenance:** Every plotted or photographic visual must name its original source, evidence class, authors/license, scientific context, and any edit. Reviewer checks figure numbers/panels against the published PDF and confirms the caption does not overstate outcomes.

**Information architecture:** Source article, dataset, and software are one click from the related figure when public. Existing About / Research / Outputs / Experience / Engagement / Contact paths stay canonical. No duplication of CV facts.

**Accessibility:** Informative alt text conveys substance (not `image of plot`); full-size zoom isn't keyboard-trapping; color isn't the only encoding; figure text/scales remain readable; tab order and reduced motion pass.

**Responsive:** test 320, 390, 680, 768, 820, 980, 1180, 1440 widths plus laptop 1366×768 and wide desktop. Compare first-fold hierarchy, text measures, loading shifts and crop behavior.

**Performance:** compare baseline to branch for mobile/desktop LCP, CLS, total transferred image bytes, Lighthouse, loading on slower network, and generated social-preview integrity. No visual may materially regress quality without a documented tradeoff.

**Release:** branch → audits → PR review → merge only after explicit approval → independent Pages deployment → live smoke check. There is no approval to deploy visuals under this research brief.

## Outstanding checks / decision gates

1. Download and visually inspect full-resolution candidate figures (especially 2026 Figures 2, 4, and 5; 2025 Figures 1 and 5); verify panel labeling, legibility, and third-party credits.
2. Confirm source image rights at panel level and whether attribution can be accommodated in the current Hugo article template without ambiguity.
3. Determine whether the lab-repository workflow screenshot is legible as a responsive web asset and whether it should be served in its existing version or re-exported from source.
4. Decide if the existing event image contains people or labels requiring consent/brand approval; exclude until checked.
5. Review any proposed patent-associated visual with the institution's technology-transfer disclosure limits; no unpublished images in public draft.
6. Capture baseline screenshots/performance metrics at the site breakpoints before changes. No claim of tested improvement until this happens.
7. After full inspection, make a small **draft visual PR** containing only approved originals/reproductions and revised captions. Do not conflate research approval with production approval.

## Source references

- Existing site and architecture: https://bhalaji.com/ ; https://bhalaji.com/research/ ; https://bhalaji.com/outputs/ ; `docs/design-governance.md` ; `docs/content-taxonomy.md`
- Precedent: https://botang.org/ ; https://botang.org/research/
- Adhesion paper: https://doi.org/10.3390/polym18121504
- Electrospun fiber paper: https://doi.org/10.3390/polym17131777
- Reproducible dataset: https://doi.org/10.5281/zenodo.20278428
- Software and published documentation: https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates
- Source policy / attribution: https://www.mdpi.com/openaccess ; https://www.mdpi.com/journal/polymers/about ; https://creativecommons.org/licenses/by/4.0/
