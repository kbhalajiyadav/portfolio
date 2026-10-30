---
title: "Peel Trace Evaluation for Soft Substrates"
date: "2026-06-16T00:00:00Z"
lastmod: "2026-10-10T00:00:00Z"
status: "Open source"
summary: "A versioned, reproducible workflow for protocol-defined analysis of force–displacement peel traces from soft and stretchable substrates."
tags:
  - Research Software
  - Adhesion
  - Reproducibility
  - Python
toc: false
---

## Purpose

Peel Trace Evaluation for Soft Substrates supports reproducible analysis of
force–displacement traces from compliant interfaces. The workflow documents
trace-window selection, initiation behavior, stability metrics, and
sample-level summaries.

## What the workflow supports

- protocol-defined steady-peel window selection;
- initiation and steady-peel force summaries;
- peel-stability and oscillation metrics;
- sample-level and group-level outputs; and
- versioned, citable analysis records.

{{< method-schematic id="peel-trace-schematic" title="Peel Trace Evaluation workflow" steps="Reference~validation|Force-displacement~data|Column and~profile mapping|Steady-peel~window|Peel-trace~descriptors|QC plots~and records" caption="The notebook blocks user-data analysis until the bundled Scotch Tape reference check passes, then extracts protocol-defined descriptors with provenance records." >}}

## Example analysis output

The software repository includes a bundled Scotch Tape reference example used for quality control. This is an authentic plot from that example, **not experimental data from the wearable-textile adhesion article**.

{{< source-figure src="/media/research/peel-trace-reference-qc.png" width="3993" height="1350" alt="Reference peel-trace quality-control plot produced by the Peel Trace Evaluation workflow from its bundled Scotch Tape example." caption="Reference quality-control plot from the bundled Scotch Tape example. It illustrates the software's diagnostic output, not a result from the published wearable-textile experiment." source="https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates/blob/main/docs/example_outputs/scotch_tape_qc_trace.png" >}}

## Resources

- [Source repository](https://github.com/VCU-Soft-Functional-Materials-Lab/Peel-Trace-Evaluation-for-Soft-Substrates)
- [Manuscript-baseline release, v1.4.0-rc15](https://doi.org/10.5281/zenodo.20301242)
- [All archived versions](https://doi.org/10.5281/zenodo.20278327)

## Related research outputs

- [Peer-reviewed article: Multi-Criteria Selection of Adhesives for Wearable Textiles](https://doi.org/10.3390/polym18121504)
- [VCU M.S. thesis: Multi-Criteria Selection of Adhesives for Wearable Textiles](https://doi.org/10.25772/f6wc-rh09) (public repository record; full manuscript under embargo until July 20, 2031)
- [Experimental source dataset](https://doi.org/10.5281/zenodo.20278428) (archived separately from the software release)

## Recommended citation

Kantepalle, B. Y.; Tang, C. *Peel Trace Evaluation for Soft Substrates*,
version 1.4.0-rc15; Zenodo, 2026.

## Availability

The repository and Zenodo releases provide the source code, version history,
and citable release metadata. Experimental datasets and source images are not
distributed with the software release.
