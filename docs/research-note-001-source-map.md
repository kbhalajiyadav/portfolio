# Research Note 001 — public-source boundary and review record

Current title: **What a Peel Trace Can Tell You Beyond a Single Force Value**

This document records the evidence boundary, adversarial review, and public-source staging status for Research Note 001. The staged note uses only already-public material; the embargoed M.S. thesis manuscript is not a technical source.

## Current decision

The candidate has passed claim-level scientific review, source-status review, disclosure/IP review, adversarial red-team review, editorial-value review, rights/asset review, and explicit author approval for public-source staging.

**Repository-boundary status:** staged in public Git as `draft: true`.

This is **not** website-publication approval. The live author release decision remains pending, and independent human scientific review is required before `draft: false`.

Current governance state:

- `repository_safe: true`
- `repository_staging_decision: approved`
- `editorial_value_review: complete`
- `external_scientific_review_required: true`
- `external_scientific_review_status: pending`
- `source_status_review: complete`
- `author_release_decision: pending`
- `draft: true`

A substantive scientific edit reopens the relevant review.

## Why the note exists

The peer-reviewed paper reports the textile adhesive comparison and defines the study-specific metrics; the public software documents the extraction workflow. The Research Note does not claim a new metric, dataset, or experimental result.

Its distinct reader value is interpretive: it makes the reasoning chain explicit—

`trace -> QC / analysis window -> descriptor -> replicate summary -> decision`

—and identifies where information can be lost or overinterpreted at each reduction step. This is intended as a companion to the paper and software rather than a duplicate or substitute.

## Approved public sources

### Peer-reviewed article

Kantepalle, B. Y.; Epitawala Arachchige, U.; Joung, D.; Tang, C. **Multi-Criteria Selection of Adhesives for Wearable Textiles.** *Polymers* 2026, 18(12), 1504. DOI: `10.3390/polym18121504`.

Use for claims specific to the published textile study, including its T-peel framework, operational crack-initiation-force descriptor, peel stability index, stick–slip amplitude terminology, deformation tolerance, inter-sample repeatability, funding, authorship, and published conclusions.

### Public research software

**Peel Trace Evaluation for Soft Substrates**, manuscript-baseline release `v1.4.0-rc15`.

- GitHub: <https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates>
- Release DOI: `10.5281/zenodo.20301242`
- All-version DOI: `10.5281/zenodo.20278327`
- Repository license: Apache-2.0

Use for public workflow behavior, initiation/restart terminology, QC-first interpretation, protocol-defined force/stability descriptors, analysis windows, diagnostics, validation, provenance, and reproducibility controls.

The public GitHub release `v1.4.0-rc15` remains available and is explicitly identified as a manuscript-baseline release candidate.

### Public source-data record

The peer-reviewed article states that the original T-peel source data are archived at Zenodo DOI `10.5281/zenodo.20278428`.

Note 001 does not perform new calculations from this dataset and does not introduce unpublished data analysis.

### Public thesis repository record

VCU Scholars Compass: <https://scholarscompass.vcu.edu/etd/8456/>

The record is related public work only. The embargoed thesis manuscript is not used as a technical source and is not included in the note's formal reference list.

## General peel-mechanics sources

The note uses a deliberately small set of primary sources for general mechanics boundaries:

- Kendall, K. **Thin-film peeling—the elastic term.** *Journal of Physics D: Applied Physics* 1975, 8, 1449–1452. DOI `10.1088/0022-3727/8/13/005` — geometry/elastic-deformation contribution to peel force.
- Villey, R. et al. **Rate-dependent elastic hysteresis during the peeling of pressure sensitive adhesives.** *Soft Matter* 2015, 11, 3480–3491. DOI `10.1039/C5SM00260E` — rate/rheology/dissipation sensitivity in pressure-sensitive adhesive peeling.
- Perrin, H. et al. **Peeling an elastic film from a soft viscoelastic adhesive: experiments and scaling laws.** *Soft Matter* 2019, 15, 770–778. DOI `10.1039/C8SM01946K` — coupling among peel force, velocity, geometry, and viscoelastic dissipation in a soft adhesive system.
- Dalbe, M.-J. et al. **Inertial and stick-slip regimes of unstable adhesive tape peeling.** *Soft Matter* 2016, 12, 4537–4548. DOI `10.1039/C6SM00119J` — stick–slip/inertial peeling as a physical instability in the studied tape system.
- Andrews, E. H.; Khan, T. A.; Majid, H. A. **Adhesion to skin: Part 1 Peel tests with hard and soft machines.** *Journal of Materials Science* 1985, 20, 3621–3630. DOI `10.1007/BF01113769` — counter-evidence showing that machine compliance can materially alter observed peel behavior and suppress force oscillations.

These references do not establish that pressure-sensitive tape, polymer-gel, skin-adhesive, and textile-interface systems are mechanically identical. They support only the bounded claims stated above.

## Source-status review

On October 14, 2026, the peer-reviewed sources used in the note were checked for identifier/title agreement and retraction/expression-of-concern signals. The cited records matched their identifiers and none was flagged as retracted. The software release was independently checked against its public GitHub release record.

The Andrews citation was specifically re-verified after a discovery result initially used an abbreviated title; the DOI resolves to the full article title above and no retraction, correction, or expression-of-concern notice was found.

## Claim-level and adversarial review outcome

The review produced the following material changes:

1. The title was changed from the categorical **“What a Peel Trace Tells You That a Single Force Value Cannot”** to **“What a Peel Trace Can Tell You Beyond a Single Force Value.”**
2. The paper's `Fci` label is now accompanied by its operational peak-oriented definition; the note explicitly avoids treating it as a universal measurement of the physical instant of crack nucleation.
3. The public software's initiation/restart terminology is distinguished from the paper-specific descriptor.
4. Observed force oscillation is separated from mechanism identification. The note no longer treats an oscillatory trace by itself as proof of interfacial stick–slip.
5. Figure 2 was revised to use the mechanism-neutral label **force oscillation** rather than `oscillation / stick-slip`.
6. A broad automation/reproducibility statement was narrowed to standardization of extraction and preservation of provenance.
7. The published adhesive framework is explicitly described as a proof of concept rather than a universal screening rule.
8. Repeatability is limited to the tested replicate set and is not presented as cross-laboratory reproducibility.
9. The practical reading sequence is identified as author methodological guidance, not an ASTM/ISO test method, validated SOP, or acceptance criterion.
10. `status` was changed from `stable` to `evolving` for the initial note lifecycle.
11. Co-author attribution, underlying funding, published COI status, and AI-assisted editorial/adversarial review are surfaced transparently.
12. The note now contains an explicit **What this note adds** section to establish non-redundant reader value.

## Core claim envelope

The note may explain that a force–displacement peel history can preserve information beyond a single scalar force summary, including:

- protocol-defined peak-oriented initiation behavior;
- continuing force level;
- force oscillation and trace stability;
- drift and analysis-window quality;
- displacement/break behavior; and
- repeatability across the tested replicate set.

The note must preserve the public software's interpretation boundary: its outputs are **protocol-defined descriptors of the measured peel response**, not universal intrinsic adhesive material constants or stand-alone mechanism identifiers.

## Explicit exclusions

Do not introduce into Note 001:

- embargoed thesis-manuscript text or thesis-only technical detail;
- ongoing Ph.D. data, results, figures, methods, or conclusions that are not already public;
- lab-internal discussion or documents;
- unpublished collaborator material;
- sponsor-confidential information;
- private reviewer/editorial correspondence;
- patent-sensitive or invention-enabling detail not already publicly disclosed;
- third-party figures or images without verified reuse rights.

## Figures and rights

The staged page bundle contains two original explanatory SVG schematics:

1. stable versus oscillatory illustrative traces, explicitly labelled **illustrative; not experimental data**;
2. `raw trace -> QC/window -> protocol-defined descriptors -> replicate summary -> interpretation/limitations`.

Both contain accessible SVG `<title>`/`<desc>` metadata, no experimental data, no external asset loads, no scripts or event handlers, and no reproduced journal figure.

## Remaining publication gate

The next required substantive review is **independent human scientific review**. Because Note 001 interprets a co-authored study and method terminology, an appropriate co-author/PI or another knowledgeable researcher should check that the explanation fairly represents the public work without relying on unpublished context.

The staged source must remain `draft: true` until that review is complete, any resulting substantive edits are re-audited, all website/accessibility/performance checks pass, and the author separately sets `author_release_decision: approved`.

No automatic promotion is permitted.
