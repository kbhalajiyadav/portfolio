# Research Note 001 — public-source boundary map

Working title: **What a Peel Trace Tells You That a Single Force Value Cannot**

This file records the evidence boundary for the first Research Notes pilot. It is intentionally conservative: only already-public material may support the note, and the embargoed M.S. thesis manuscript is not treated as a technical source.

## Approved public sources

### Peer-reviewed article

Kantepalle, B. Y.; Epitawala Arachchige, U.; Joung, D.; Tang, C. **Multi-Criteria Selection of Adhesives for Wearable Textiles.** *Polymers* 2026, 18(12), 1504. DOI: `10.3390/polym18121504`.

Safe uses:

- published motivation and T-peel context;
- published definitions/interpretation of the multi-criteria framework;
- published discussion of peel-trace shape, stability, stick–slip, deformation tolerance, and repeatability;
- published numerical results where they are genuinely useful to the note;
- published authorship, funding, and data-availability statements.

### Public research software

**Peel Trace Evaluation for Soft Substrates**, manuscript-baseline release `v1.4.0-rc15`.

- GitHub: <https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates>
- Release DOI: `10.5281/zenodo.20301242`
- All-version DOI: `10.5281/zenodo.20278327`
- Repository license: Apache-2.0

Safe uses:

- public workflow logic and terminology;
- QC-first interpretation;
- protocol-defined force/stability descriptors;
- analysis-window, diagnostics, validation, and provenance concepts;
- public example/validation outputs where rights/provenance are clear;
- current public software behavior.

### Public source-data record

The published article states that the original T-peel source data are publicly archived at Zenodo DOI `10.5281/zenodo.20278428`.

Use only after the archive metadata/data needed for a claim have been independently checked. Do not infer unverified metadata from the DOI alone.

### Public thesis repository record

VCU Scholars Compass record: <https://scholarscompass.vcu.edu/etd/8456/>

Safe uses:

- bibliographic/degree relationship;
- public repository metadata;
- the fact that the manuscript remains under embargo until July 20, 2031.

The repository record is **not** permission to reconstruct, paraphrase, or disclose thesis-only technical material.

## General peel-mechanics sources

The pilot uses a deliberately small set of primary sources for general boundary claims rather than turning the note into a broad literature review.

- Kendall, K. **Thin-film peeling—the elastic term.** *Journal of Physics D: Applied Physics* 1975, 8, 1449–1452. DOI: `10.1088/0022-3727/8/13/005`.
  - Use: classical point that peel force reflects geometry and elastic deformation as well as interfacial work.
- Villey, R. et al. **Rate-dependent elastic hysteresis during the peeling of pressure sensitive adhesives.** *Soft Matter* 2015, 11, 3480–3491. DOI: `10.1039/C5SM00260E`.
  - Use: rate/rheology/dissipation sensitivity in pressure-sensitive adhesive peeling.
- Perrin, H. et al. **Peeling an elastic film from a soft viscoelastic adhesive: experiments and scaling laws.** *Soft Matter* 2019, 15, 770–778. DOI: `10.1039/C8SM01946K`.
  - Use: coupling among peel force, velocity, geometry, and viscoelastic dissipation in a soft adhesive system.
- Dalbe, M.-J. et al. **Inertial and stick-slip regimes of unstable adhesive tape peeling.** *Soft Matter* 2016, 12, 4537–4548. DOI: `10.1039/C6SM00119J`.
  - Use: oscillatory stick–slip/inertial peeling as a real instability rather than generic measurement noise.

The note must not imply that pressure-sensitive tape, polymer-gel, and textile-interface systems are mechanically identical. These references support general mechanics boundaries only.

The four general references above and the 2026 *Polymers* article were independently DOI/title matched and screened for retraction/expression-of-concern signals on October 14, 2026. All five matched their identifiers and none were flagged as retracted.

## Explicitly excluded

Do not use in Note 001:

- the embargoed thesis manuscript or thesis-only results/details;
- ongoing Ph.D. data, interpretations, figures, methods, or conclusions that are not already public;
- lab-internal discussion or internal documents;
- private reviewer or editorial correspondence;
- unpublished collaborator material;
- sponsor-confidential information;
- patent-sensitive or invention-enabling details not already publicly disclosed;
- figures, photographs, datasets, or attachments whose public rights/provenance are unclear.

## Core claim envelope

The note may explain that a force–displacement peel history can contain decision-relevant information beyond one scalar force summary, including:

- initiation/restart behavior;
- continuing force level;
- oscillation/stick–slip;
- stability;
- drift/analysis-window quality;
- displacement/break behavior; and
- repeatability across specimens.

The note must also preserve the public software's interpretation boundary: these are **protocol-defined descriptors of the measured peel response**, not universal intrinsic adhesive material constants.

## Proposed reader job

Primary reader job:

> Help a technically literate reader understand why inspecting and characterizing the force–displacement trace can be more informative than ranking soft-interface candidates by one peel-force value alone.

The note should explain the measurement logic, not act as a replacement for the peer-reviewed paper or the software documentation.

## Figure plan and current status

### Figure 1 — built privately

An **original conceptual schematic** showing two illustrative force–displacement traces with similar central force level but different stability/oscillation behavior.

Required label/caption language: **Illustrative schematic; not experimental data.**

Purpose: make the information-loss problem visible without reproducing a journal figure.

### Figure 2 — built privately

An original workflow schematic:

`raw trace -> QC/analysis window -> force descriptors + stability descriptors -> replicate summary -> interpretation with limitations`

The private SVG includes an accessible `<title>` and `<desc>`. A clipping defect found during visual QA was corrected before any promotion.

Avoid reproducing journal figures for the first pilot unless reuse rights are explicitly checked. Public software figures/screenshots may be considered later only with clear provenance, attribution, and a reason they are superior to an original explanatory figure.

## Citation policy

- Use the peer-reviewed article for scientific claims specific to the published study.
- Use the public software repository/release for workflow, implementation, QC, provenance, validation, and current software behavior.
- Use the public thesis record only for bibliographic relationship and embargo context.
- Use the four general peel-mechanics papers only for the limited mechanics claims identified above.
- Citation existence is not enough; each citation must support the nearby claim.

## Provenance/disclosure rule for the note

The public note should state that it discusses work the author co-authored and software the author co-developed. Funding and conflict-of-interest statements for the underlying study remain those of the peer-reviewed article. The note introduces no new experimental results or unpublished thesis material, and its explanatory figures are original schematics rather than measured data.

## Pilot status

Completed privately/local-only:

- public-source inventory and disclosure boundary;
- Quarto-style `.qmd` candidate scaffold;
- curated `.bib` bibliography;
- four-source general peel-mechanics expansion;
- DOI/title/retraction screening for the five peer-reviewed references;
- Pandoc citeproc dry run;
- two original SVG explanatory figures;
- visual QA of both figures and correction of a Figure 2 clipping defect;
- provenance/disclosure block in the private candidate.

Still required before any Note 001 source enters `content/notes/`:

- actual Quarto `hugo-md` render in an environment with Quarto installed;
- claim-level scientific review against the full cited sources;
- final mapping to the repository governance front matter;
- Hugo/mobile/print/accessibility integration QA;
- final rights/provenance review at promotion time;
- passing governance, dependency-review, full build, accessibility, and Lighthouse checks.

Quarto has not been added to portfolio CI and no Quarto-render success is claimed yet.

No Note 001 prose or figures should enter `content/notes/` until the private pilot is scientifically reviewed, the promotion checks above are complete, and `repository_safe: true` is defensible under the Research Notes governance standard.
