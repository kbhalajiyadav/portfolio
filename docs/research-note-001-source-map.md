# Research Note 001 — public-source boundary and review record

Working title: **What a Peel Trace Tells You That a Single Force Value Cannot**

This document records the evidence boundary and pre-staging review for Research Note 001. The note itself remains private/local. Only already-public material may support it, and the embargoed M.S. thesis manuscript is not treated as a technical source.

## Current decision

The reviewed private candidate has passed the claim-level scientific review and disclosure/source-status review with targeted edits.

**Repository-boundary status:** eligible for public-source staging as `draft: true` if the author chooses.

This is not publication approval. The author release decision remains separate and pending.

## Approved public sources

### Peer-reviewed article

Kantepalle, B. Y.; Epitawala Arachchige, U.; Joung, D.; Tang, C. **Multi-Criteria Selection of Adhesives for Wearable Textiles.** *Polymers* 2026, 18(12), 1504. DOI: `10.3390/polym18121504`.

Use for claims specific to the published textile study, including its T-peel framework, crack-initiation force, peel stability index, stick–slip amplitude, deformation tolerance, inter-sample repeatability, funding, authorship, and published conclusions.

### Public research software

**Peel Trace Evaluation for Soft Substrates**, manuscript-baseline release `v1.4.0-rc15`.

- GitHub: <https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates>
- Release DOI: `10.5281/zenodo.20301242`
- All-version DOI: `10.5281/zenodo.20278327`
- Repository license: Apache-2.0

Use for public workflow behavior, initiation/restart terminology, QC-first interpretation, protocol-defined force/stability descriptors, analysis windows, diagnostics, validation, provenance, and reproducibility controls.

The public GitHub release `v1.4.0-rc15` remains available and is explicitly identified as the manuscript-baseline release candidate.

### Public source-data record

The peer-reviewed article states that its original T-peel source data are archived at Zenodo DOI `10.5281/zenodo.20278428`.

Note 001 does not currently rely on unpublished data analysis or on new calculations from this archive.

### Public thesis repository record

VCU Scholars Compass: <https://scholarscompass.vcu.edu/etd/8456/>

The public record may be used only for bibliographic relationship and public repository metadata. The embargoed thesis manuscript is not used as a technical source for Note 001.

The reviewed candidate therefore removes the thesis record from the formal reference list and keeps it only as related public work.

## General peel-mechanics sources

The note uses four primary papers only for limited general-mechanics boundaries:

- Kendall, K. **Thin-film peeling—the elastic term.** *Journal of Physics D: Applied Physics* 1975, 8, 1449–1452. DOI: `10.1088/0022-3727/8/13/005` — elastic deformation/geometry contribution to peel force.
- Villey, R. et al. **Rate-dependent elastic hysteresis during the peeling of pressure sensitive adhesives.** *Soft Matter* 2015, 11, 3480–3491. DOI: `10.1039/C5SM00260E` — rate, large-deformation rheology, and dissipation in PSA peeling.
- Perrin, H. et al. **Peeling an elastic film from a soft viscoelastic adhesive: experiments and scaling laws.** *Soft Matter* 2019, 15, 770–778. DOI: `10.1039/C8SM01946K` — coupling among peel force, velocity, geometry, and viscoelastic dissipation in a soft adhesive system.
- Dalbe, M.-J. et al. **Inertial and stick-slip regimes of unstable adhesive tape peeling.** *Soft Matter* 2016, 12, 4537–4548. DOI: `10.1039/C6SM00119J` — stick–slip/inertial peeling as a physical instability rather than generic measurement noise.

The note must not imply that pressure-sensitive tape, polymer-gel, and textile-interface systems are mechanically identical.

## Source-status review

On October 14, 2026, the four general-mechanics papers and the 2026 *Polymers* article were independently checked for DOI/title agreement and retraction/expression-of-concern signals. All five matched their identifiers and none was flagged as retracted.

The specific software release used by the note was also checked against the public GitHub release record.

The reviewed private candidate therefore uses:

- `source_status_review: complete`
- `repository_safe: true`
- `author_release_decision: pending`
- `draft: true`

These values apply to the reviewed candidate only. A later substantive edit reopens the relevant review.

## Claim-level review outcome

The scientific review passed with several tightening edits:

1. The peer-reviewed article's **crack-initiation force** is now distinguished from the public software's broader **initiation/restart** descriptor.
2. A broad statement that automation improves reproducibility was replaced with the narrower claim that a scripted workflow can standardize extraction and preserve analysis provenance.
3. The note now states that the force–displacement trace **and its QC context** are the evidence from which scalar descriptors are derived.
4. The practical reading sequence is explicitly labeled an author methodological recommendation rather than a universal standard.
5. The thesis repository record is no longer a formal technical citation.
6. The external mechanics papers remain limited to the specific general claims listed above.

## Core claim envelope

The note may explain that a force–displacement peel history can contain information beyond one scalar force summary, including:

- crack-initiation behavior in the published textile framework;
- initiation/restart behavior in the public software workflow;
- continuing force level;
- oscillation/stick–slip;
- stability;
- drift and analysis-window quality;
- displacement/break behavior; and
- repeatability across specimens.

The note must preserve the public software's interpretation boundary: these are **protocol-defined descriptors of the measured peel response**, not universal intrinsic adhesive material constants.

## Explicit exclusions

Do not introduce into Note 001:

- embargoed thesis-manuscript text or thesis-only technical detail;
- ongoing Ph.D. data, results, figures, methods, or conclusions that are not already public;
- lab-internal discussion or internal documents;
- unpublished collaborator material;
- sponsor-confidential information;
- private reviewer/editorial correspondence;
- patent-sensitive or invention-enabling detail not already publicly disclosed;
- third-party figures or images without verified reuse rights.

## Figures and rights

The private candidate uses two original explanatory SVG schematics:

1. stable versus oscillatory illustrative peel traces, explicitly labeled **illustrative; not experimental data**;
2. raw trace → QC/window → descriptors → replicate summary → interpretation/limitations.

Both were created specifically for the note, include accessible SVG metadata, and contain no experimental data. No journal figure is reproduced.

## Provenance and disclosure

The public note should make clear that it discusses work the author co-authored and software the author co-developed. The underlying study's funding and conflict-of-interest statements remain those of the peer-reviewed paper.

AI/external-tool assistance is not an evidentiary source. The candidate contains only already-public research information, and all scientific claims are tied to the underlying public sources.

## Authoring decision

The private Note 001 comparison concluded that native Hugo Markdown is the appropriate default for this note. Quarto remains optional and feature-triggered for future notes that genuinely need executable computation, dense numbered cross-references, equation-heavy authoring, citation-heavy synthesis, or multi-format scientific output.

The durable decision is recorded in `docs/research-note-authoring-decision.md`; issue #79 is closed as completed.

## Remaining gate before public-source staging

Only the author's intentional staging decision remains. If staged, Note 001 should enter the public repository as `draft: true` with the reviewed governance fields and should then pass the ordinary governance, presentation, dependency-review, full-build, accessibility, responsive, and Lighthouse checks before publication is considered.

No automatic promotion is permitted.