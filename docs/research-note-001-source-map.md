# Research Note 001 — public-source boundary and review record

Current title: **The Strongest Adhesive Was Not the Right One**

This document records the evidence boundary and public-source staging status for Research Note 001. The note is a short research reflection built from already-public work. The embargoed M.S. thesis manuscript is not a technical source.

## Current decision

**Repository status:** staged in public Git as `draft: true`.

This is not website-publication approval.

Current governance state:

- `repository_safe: true`
- `repository_staging_decision: approved`
- `editorial_value_review: complete`
- `source_status_review: complete`
- `external_scientific_review_required: true`
- `external_scientific_review_status: pending`
- `author_release_decision: pending`
- `draft: true`

No new governance gates are being added for this note. The remaining substantive work is independent human scientific review, any resulting re-audit, and the author's separate live-release decision.

## Why the note exists

The peer-reviewed paper reports the adhesive comparison. The public source-data record preserves the T-peel data, and the public software documents the analysis workflow.

The note adds a different kind of value: it explains how the engineering decision changed when force magnitude was considered alongside the full trace and downstream device performance, why that led B.Y.K. to make the analysis inspectable in software, and how the same measurement habit carries into current research.

It does not claim a new metric, dataset, experiment, or mechanism.

## Approved public sources

### Peer-reviewed article

Kantepalle, B. Y.; Epitawala Arachchige, U.; Joung, D.; Tang, C. **Multi-Criteria Selection of Adhesives for Wearable Textiles.** *Polymers* 2026, 18(12), 1504. DOI `10.3390/polym18121504`.

Use for the published adhesive ranking, SSA and related study-specific descriptors, the device-level strain-to-electrical-failure results, study authorship, funding, acknowledgements, COI statement, IRB status, and public data/software links.

The article is published open access under CC BY 4.0.

### Public source-data record

Zenodo DOI `10.5281/zenodo.20278428`.

The published article identifies this archive as the source-data record for the study and states that it includes the manuscript master data workbook and supporting documentation for the fabric-fabric T-peel force-displacement source data. The Zenodo record is licensed under CC BY 4.0.

The archive remains available for an independent future replot if the representative E6000 and Fabri-Fuse source records are mapped unambiguously. Note 001 does not depend on such a replot because the final published evidence panel is now used directly and transparently.

### Public research software

**Peel Trace Evaluation for Soft Substrates**, manuscript-baseline release `v1.4.0-rc15`.

- GitHub: <https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates>
- Release DOI: `10.5281/zenodo.20301242`
- All-version DOI: `10.5281/zenodo.20278327`

Use for public statements about QC plots, analysis windows, retained extrema, diagnostics, provenance, method-profile controls, and the versioned analysis workflow.

### General mechanics boundary sources

Only two external mechanics papers remain in the reflection:

- Andrews, E. H.; Khan, T. A.; Majid, H. A. **Adhesion to skin: Part 1 Peel tests with hard and soft machines.** *Journal of Materials Science* 1985, 20, 3621-3630. DOI `10.1007/BF01113769`.
- Dalbe, M.-J. et al. **Inertial and stick-slip regimes of unstable adhesive tape peeling.** *Soft Matter* 2016, 12(20), 4537-4548. DOI `10.1039/C6SM00119J`.

They are used only to support the limit that observed peel oscillations depend on the broader test system and should not be treated as a stand-alone mechanism identifier.

### Related public thesis record

VCU Scholars Compass: <https://scholarscompass.vcu.edu/etd/8456/>

The public record may remain linked as related work. The embargoed thesis manuscript is not used to support Note 001.

## Verified public claims used in the reflection

The published article supports the following values and comparisons used in the staged note:

- E6000 peel force: `1.82 ± 0.27 N/mm`
- E6000 SSA: `4.05 ± 0.83 N`
- Fabri-Fuse SSA: `0.69 ± 0.29 N`
- Fabri-Fuse strain-to-electrical-failure: `34.95 ± 2.43%`
- E6000 strain-to-electrical-failure: `27.98 ± 1.47%`

The note intentionally gives the two device values rather than repeating a relative percentage.

The article also supports the statement that Fabri-Fuse had the lowest reported initiation-force coefficient of variation, high peel stability, and high displacement at break within the tested system.

## Attribution, funding, COI, and AI

The paper credits:

- conceptualization to C.T.;
- methodology to B.Y.K. and U.E.A.;
- software and validation to B.Y.K.;
- investigation, formal analysis, data curation, and visualization to B.Y.K. and U.E.A.;
- original draft preparation to B.Y.K.;
- review/editing to all four authors;
- supervision and project administration to D.J. and C.T.;
- funding acquisition to C.T.

The note therefore uses **we** for the collaborative study and **I** for B.Y.K.'s personal learning and software motivation.

Published funding: U.S. Army Combat Capabilities Development Command Soldier Center award `W911QY2220002` and Virginia Commonwealth University College of Engineering.

Published IRB statement: not applicable.

Published COI statement: the authors declared no conflicts of interest.

The article acknowledges Samrawit Tesfai for technical assistance. Note 001 carries that acknowledgement forward.

AI tools assisted editing and adversarial review of the Research Note. They are not scientific sources and do not replace author responsibility.

## Figure and rights status

The two earlier schematic SVGs were removed because the reflection's central argument should be demonstrated with real evidence.

Current state: **Figure 1 added using the published representative trace panel.**

Figure 1:

- source: Kantepalle et al. (2026), final published Figure 2A;
- article DOI: `10.3390/polym18121504`;
- reuse basis: article CC BY 4.0;
- modification: cropped to the Figure 2A panel only; plotted data and labels were not altered;
- purpose: show the published representative force-displacement traces discussed in the reflection;
- accessibility: alt text identifies the four adhesive conditions and describes the visibly higher, more oscillatory E6000 trace relative to the steadier Fabri-Fuse and JB Weld traces.

The public source-data archive at DOI `10.5281/zenodo.20278428` remains the preferred source for a future independent replot if the representative source records are mapped unambiguously. That replot is not required for Note 001 now that the published evidence panel is used transparently under CC BY 4.0.

The final published article's Figure 2A contains the representative force-displacement curves. Figure 1 is the nominal peel-arm axial-stress comparison. Earlier manuscript drafts used different figure numbering, so the publication version controls.

## Explicit exclusions

Do not introduce:

- embargoed thesis-manuscript text or thesis-only technical detail;
- ongoing Ph.D. data, results, figures, methods, or conclusions that are not already public;
- lab-internal discussion;
- unpublished collaborator material;
- sponsor-confidential information;
- private reviewer/editorial correspondence;
- patent-sensitive or invention-enabling detail not already public;
- a causal claim that lower SSA produced the better device result;
- a claim that the downstream comparison was formally preregistered.

## Remaining publication gate

Before `draft: false`:

1. complete independent human scientific review;
2. re-audit any substantive reviewer edits;
3. pass ordinary governance, presentation, accessibility, build, and performance checks;
4. obtain a separate `author_release_decision: approved`.

No automatic promotion is permitted.
