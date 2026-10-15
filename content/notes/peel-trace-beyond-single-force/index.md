---
title: What a Peel Trace Can Tell You Beyond a Single Force Value
date: 2026-10-14 20:52:00-04:00
lastmod: 2026-10-14 20:52:00-04:00
draft: true
summary: Peel tests produce force–displacement histories before they produce a single force value. This note explains how trace shape, peak-oriented initiation descriptors, oscillation/stability, analysis-window quality, and replicate repeatability can complement conventional peel-strength reporting—and why the interpretation remains protocol-dependent.
in_brief: A peel trace can preserve information that a single average or peak force does not represent, including force fluctuations, analysis-window quality, and repeatability-related descriptors. In a published soft-textile proof of concept and its public analysis workflow, these features complemented conventional peel-strength reporting. They must be interpreted within the test system, geometry, protocol, and analysis settings and should not be treated as intrinsic adhesive constants or mechanism identifiers.
note_type: method
status: evolving
featured: true
toc: true
social_card: research
tags:
- Adhesion
- Peel testing
- Soft materials
- Reproducibility
image: ''
image_alt: ''
revision_note: ''
status_reason: ''
replacement_url: ''
funding_statement: The underlying published study was funded in part by the U.S. Army Combat Capabilities Development Command Soldier Center (W911QY2220002) and the Virginia Commonwealth University College of Engineering.
acknowledgements: The underlying study was co-authored by Bhalaji Yadav Kantepalle, Udena Epitawala Arachchige, Daeha Joung, and Christina Tang. This Research Note is an explanatory synthesis by Bhalaji Yadav Kantepalle. AI-assisted tools supported editorial and adversarial review; they were not treated as scientific sources.
governance:
  repository_safe: true
  repository_staging_decision: approved
  disclosure_basis: published_own_work
  contains_unpublished_research: false
  contains_unpublished_collaborator_material: false
  contains_confidential_or_sponsor_material: false
  potentially_patent_sensitive: false
  ip_clearance: not_applicable
  venue_policy_review: not_applicable
  embargo_status: none
  regulated_research_material: false
  ethics_review: not_applicable
  export_control_review: not_applicable
  dual_use_review: not_applicable
  ownership_review: complete
  contributor_review: complete
  editorial_value_review: complete
  funding_review: complete
  privacy_review: complete
  external_tool_review: complete
  external_scientific_review_required: true
  external_scientific_review_status: pending
  coi_status: none_declared
  coi_statement: The underlying peer-reviewed study states that the authors declared no conflicts of interest.
  copyright_review: complete
  source_status_review: complete
  source_status_reviewed_on: 2026-10-14
  author_release_decision: pending
sources:
- https://doi.org/10.3390/polym18121504
- https://doi.org/10.5281/zenodo.20301242
- https://doi.org/10.1088/0022-3727/8/13/005
- https://doi.org/10.1039/C5SM00260E
- https://doi.org/10.1039/C8SM01946K
- https://doi.org/10.1039/C6SM00119J
- https://doi.org/10.1007/BF01113769
related_publications:
- /publication/adhesives-wearable/
- /publication/masters-thesis/
related_software:
- /project/peel-trace-evaluation/
related_projects: []
related_notes: []
---
## What this note adds

The peer-reviewed paper reports the textile adhesive comparison and defines the study-specific metrics; the public software documents the extraction workflow. This note does **not** claim a new metric, dataset, or experimental result.

Its purpose is interpretive: to make the reasoning chain explicit—

**trace → QC and analysis window → descriptor → replicate summary → decision**

—and to show where information can be lost or overinterpreted at each reduction step. That makes the note a companion to the paper and software rather than a substitute for either.

## The measurement is a trace before it is a scalar

A peel experiment records force while displacement progresses. Reducing that record to a single average, maximum, or width-normalized force can be useful, but the reduction necessarily discards information about *how* the force evolved.

That matters because peel force is not determined by interface chemistry alone. Even in classical elastic peeling, geometry and elastic deformation contribute to the energy balance ([Kendall, 1975](https://doi.org/10.1088/0022-3727/8/13/005)). In soft or pressure-sensitive adhesive systems, rate-dependent viscoelastic dissipation and large deformation can materially affect the measured response ([Villey et al., 2015](https://doi.org/10.1039/C5SM00260E); [Perrin et al., 2019](https://doi.org/10.1039/C8SM01946K)). Unstable peeling can also generate stick–slip or inertial oscillations rather than a smooth force history ([Dalbe et al., 2016](https://doi.org/10.1039/C6SM00119J)).

{{< figure src="figures/figure-1-illustrative-traces.svg" alt="Two qualitative force-displacement traces at similar central force level. The left is relatively stable and the right has large oscillations. No experimental data are shown." caption="**Illustrative schematic; not experimental data.** A single force summary can be similar even when the force histories differ substantially." >}}

The purpose is conceptual: inspect the trace before deciding which scalar descriptors are mechanically meaningful.

## What information can disappear in one force value?

### Peak-oriented initiation descriptor—and restart terminology in the public workflow

The published textile study labels \(F_{ci}\) as crack-initiation force and defines it operationally as the mean of the retained five highest local maxima within the selected analysis window, reported separately from the continuing peel-force descriptor ([Kantepalle et al., 2026](https://doi.org/10.3390/polym18121504)). Because this is a protocol-defined peak-oriented quantity, it should not be read as a universal measurement of the instant a crack first nucleates.

The public software uses initiation/restart-force terminology for its defined workflows ([Kantepalle & Tang, 2026](https://doi.org/10.5281/zenodo.20301242)). These labels are method-specific and should not be assumed to be mechanically equivalent across different peel tests.

### Stability and oscillation

Two traces can occupy a similar force range while showing very different fluctuation patterns. Stick–slip is a well-established peeling instability in many adhesive systems, but oscillation in a force trace alone does not prove a particular interfacial mechanism. Peel dynamics can depend on rate, geometry, peeled-arm mechanics, and machine compliance; changing machine stiffness has been shown to change observed peel behavior and suppress force oscillations in some systems ([Dalbe et al., 2016](https://doi.org/10.1039/C6SM00119J); [Andrews et al., 1985](https://doi.org/10.1007/BF01113769)).

In our published textile study, trace-shape and stability criteria—including the peel stability index and the operationally named stick–slip amplitude—helped distinguish candidate adhesives beyond conventional peel-strength ranking ([Kantepalle et al., 2026](https://doi.org/10.3390/polym18121504)). In this note, those quantities are treated as trace descriptors unless a physical mechanism has been established independently. They are useful only when the selected trace region and extrema are physically interpretable.

### Drift and analysis-window quality

A numerical summary is only as defensible as the portion of the trace being summarized. The public software therefore couples metric extraction to a protocol-defined analysis window, diagnostics, and visual QC rather than treating every recorded point as equally suitable for averaging ([Kantepalle & Tang, 2026](https://doi.org/10.5281/zenodo.20301242)).

A drifting region, an initiation transient, an end-of-test drop, or a region with insufficient valid extrema can each change what a scalar summary means. This is an analysis-quality problem before it is a ranking problem.

### Replicate repeatability

A high value observed once is different from a response that is consistently reproduced across nominally similar specimens. The published framework therefore considered inter-sample repeatability alongside trace-level descriptors ([Kantepalle et al., 2026](https://doi.org/10.3390/polym18121504)).

Repeatability does not prove general reproducibility across laboratories or protocols. It addresses a narrower question: whether the result is consistent across the tested replicate set under the stated conditions. The published adhesive comparison was a proof of concept with the replicate counts reported in the paper, not a universal validation study.

## Why QC belongs next to the metric

The public software exports QC plots so that the selected window, retained extrema, and diagnostic flags can be compared with the original force–displacement trace before interpretation ([Kantepalle & Tang, 2026](https://doi.org/10.5281/zenodo.20301242)).

A scripted workflow can standardize how descriptors are extracted and can preserve analysis provenance. It cannot make every automatically extracted number mechanically meaningful.

{{< figure src="figures/figure-2-trace-to-interpretation.svg" alt="Conceptual workflow from a raw force-displacement trace through quality control and analysis-window selection, force and stability descriptors, replicate summaries, and interpretation within geometry and limitations. No experimental data are shown." caption="**Original workflow schematic; no experimental data shown.** From raw trace through QC and protocol-defined descriptors to replicate-level interpretation." >}}

The force–displacement trace and its QC context are the evidence from which the scalar descriptors are derived; those descriptors should be interpreted within the relevant geometry, protocol, and limitations.

## The descriptors are conditional, not universal constants

The measured peel response can combine interface separation with deformation and dissipation elsewhere in the system. Classical and modern peel literature both make clear that geometry, deformation, rate, and viscoelastic behavior can affect the measured force or apparent adherence ([Kendall, 1975](https://doi.org/10.1088/0022-3727/8/13/005); [Villey et al., 2015](https://doi.org/10.1039/C5SM00260E); [Perrin et al., 2019](https://doi.org/10.1039/C8SM01946K)).

Accordingly, the public software explicitly describes its outputs as protocol-defined descriptors under a specified specimen geometry, test protocol, and analysis profile ([Kantepalle & Tang, 2026](https://doi.org/10.5281/zenodo.20301242)).

The published textile study used these descriptors in a proof-of-concept multi-criteria framework for a defined fabric–adhesive–fabric system. Its conclusion was not that one new metric universally replaces peel strength. Rather, trace shape, stability, deformation tolerance, and repeatability provided additional information that changed the practical selection compared with ranking by the highest peel strength alone ([Kantepalle et al., 2026](https://doi.org/10.3390/polym18121504)).

## A practical reading order

This is interpretive guidance layered on a defined peel test, not a replacement for an applicable test standard, validated laboratory SOP, or method-specific acceptance criterion.

For this class of peel measurement, a defensible sequence is:

1. inspect the complete force–displacement trace;
2. verify units, specimen geometry, and test conditions;
3. identify a mechanically interpretable analysis region;
4. report conventional force-level descriptors;
5. add initiation, stability, or oscillation descriptors only when their extraction is valid;
6. inspect QC plots and diagnostic flags;
7. examine repeatability across specimens;
8. interpret every metric within the stated geometry, protocol, and analysis settings.

This ordering keeps the trace as evidence and treats scalar metrics as summaries of that evidence—not substitutes for checking whether the underlying measurement is credible.

## Evidence and interpretation boundary

Claims specific to the textile study come from the peer-reviewed article. Statements about extraction, QC, diagnostics, provenance, and the initiation/restart workflow come from the public software release. The external peel-mechanics papers are used only to establish general boundaries around geometry, deformation, viscoelastic dissipation, rate dependence, and unstable stick–slip behavior.

The practical reading order is an author methodological recommendation synthesized from those public sources; it is not presented as a universal test standard.

## Limitations

This staging draft still requires independent human scientific review before live publication because it interprets collaborative published work and method terminology.

This note explains the interpretation logic of an already-public peel-trace framework and places it within general peel mechanics. It does not establish that the same metrics, thresholds, analysis windows, mechanism labels, or profiles are appropriate for every adhesive, substrate, geometry, instrument, or standard. It also does not turn the underlying proof-of-concept comparison into a validated universal screening rule.

The two figures are original explanatory schematics and contain no experimental data. Applying the same descriptors to another system requires method-specific validation and the relevant literature or test standard.

The VCU thesis repository record is related public work, but the embargoed manuscript is not used as a technical source for this note.

## References

1. Kantepalle, B. Y., Epitawala Arachchige, U., Joung, D., & Tang, C. (2026). *Multi-Criteria Selection of Adhesives for Wearable Textiles*. Polymers, 18(12), 1504. <https://doi.org/10.3390/polym18121504>
2. Kantepalle, B. Y., & Tang, C. (2026). *Peel Trace Evaluation for Soft Substrates* (v1.4.0-rc15). Zenodo. <https://doi.org/10.5281/zenodo.20301242>
3. Kendall, K. (1975). Thin-film peeling—the elastic term. *Journal of Physics D: Applied Physics, 8*(13), 1449–1452. <https://doi.org/10.1088/0022-3727/8/13/005>
4. Villey, R., et al. (2015). Rate-dependent elastic hysteresis during the peeling of pressure sensitive adhesives. *Soft Matter, 11*(17), 3480–3491. <https://doi.org/10.1039/C5SM00260E>
5. Perrin, H., et al. (2019). Peeling an elastic film from a soft viscoelastic adhesive: experiments and scaling laws. *Soft Matter, 15*(4), 770–778. <https://doi.org/10.1039/C8SM01946K>
6. Dalbe, M.-J., et al. (2016). Inertial and stick-slip regimes of unstable adhesive tape peeling. *Soft Matter, 12*(20), 4537–4548. <https://doi.org/10.1039/C6SM00119J>
7. Andrews, E. H., Khan, T. A., & Majid, H. A. (1985). Adhesion to skin: Part 1 Peel tests with hard and soft machines. *Journal of Materials Science, 20*, 3621–3630. <https://doi.org/10.1007/BF01113769>
