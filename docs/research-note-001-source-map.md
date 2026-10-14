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

## Figure plan

### Figure 1 — preferred

An **original conceptual schematic** showing two illustrative force–displacement traces with similar central force level but different stability/oscillation behavior.

Required label/caption language: **Illustrative schematic; not experimental data.**

Purpose: make the information-loss problem visible without reproducing a journal figure.

### Figure 2 — optional

An original workflow schematic:

`raw trace -> QC/analysis window -> force descriptors + stability descriptors -> replicate summary -> interpretation with limitations`

Avoid reproducing journal figures for the first pilot unless reuse rights are explicitly checked. Public software figures/screenshots may be considered later only with clear provenance, attribution, and a reason they are superior to an original explanatory figure.

## Citation policy

- Use the peer-reviewed article for scientific claims specific to the published study.
- Use the public software repository/release for workflow, implementation, QC, provenance, validation, and current software behavior.
- Use the public thesis record only for bibliographic relationship and embargo context.
- Add general peel-mechanics primary literature or standards only after claim-level source verification.
- Citation existence is not enough; each citation must support the nearby claim.

## Pilot status

A private/local Quarto scaffold has been created outside public Git using only the sources above. It has **not** been rendered because Quarto is not installed in the current execution environment, and Quarto has not been added to portfolio CI.

No Note 001 prose should enter `content/notes/` until the private pilot is scientifically reviewed, source status is verified, the proposed figures are cleared, and `repository_safe: true` is defensible under the Research Notes governance standard.
