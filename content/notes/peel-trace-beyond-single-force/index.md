---
title: The Strongest Adhesive Was Not the Right One
date: 2026-10-14 20:52:00-04:00
lastmod: 2026-10-16 06:28:00-04:00
draft: true
summary: A peel-force ranking picked the strongest adhesive. The full force trace and a stretch test on printed silver traces pointed to a different choice. This note is about what that changed in how I measure materials.
in_brief: In a published study of four adhesives on stretchable knit fabric, E6000 had the highest peel force but large force swings during peeling. Fabri-Fuse peeled more steadily, and silver traces printed on it maintained electrical function to 34.95% strain, compared with 27.98% on E6000. The lesson was not to swap one favorite metric for another. It was to ask what a single number leaves out before trusting it.
note_type: reflection
status: evolving
featured: true
toc: true
social_card: research
tags:
- Adhesion
- Peel testing
- Wearable textiles
- Measurement
image: ''
image_alt: ''
revision_note: ''
status_reason: ''
replacement_url: ''
funding_statement: The underlying published study was funded in part by the U.S. Army Combat Capabilities Development Command Soldier Center (W911QY2220002) and the Virginia Commonwealth University College of Engineering.
acknowledgements: The study behind this note was co-authored by Bhalaji Yadav Kantepalle, Udena Epitawala Arachchige, Daeha Joung, and Christina Tang. The published article also acknowledges Samrawit Tesfai for technical assistance. This note is my own reflection. AI tools supported editing and adversarial review. They were not used as scientific sources.
governance:
  repository_safe: true
  repository_staging_decision: approved
  disclosure_basis: published_own_work
  contains_unpublished_research: false
  contains_unpublished_collaborator_material: false
  contains_confidential_or_sponsor_material: false
  potentially_patent_sensitive: false
  ip_clearance: not_applicable
  venue_policy_review: cleared
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
  source_status_reviewed_on: 2026-10-15
  author_release_decision: pending
sources:
- https://doi.org/10.3390/polym18121504
- https://doi.org/10.5281/zenodo.20278428
- https://doi.org/10.5281/zenodo.20301242
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
## The force ranking looked convincing

During my M.S. research, we were trying to identify an adhesive interface for a stretchable textile assembly that would also support printed silver traces during deformation. We compared four commercial adhesives with T-peel tests.

Early qualitative observations made the strongest bond seem like the obvious choice. The formal force ranking agreed. E6000 produced the highest peel force, 1.82 ± 0.27 N/mm. Ranked by peel force alone, the decision looked easy.

But the force-displacement curves did not look alike.

## The trace changed the question

A peel test records force as the bond opens. The scalar summaries come later, when the trace is reduced to one or more metrics.

E6000 showed large force oscillations while Fabri-Fuse and JB Weld showed visibly steadier curves. In the published analysis, stick-slip amplitude (SSA) described the difference between the mean retained peaks and valleys within the selected 25 mm analysis window. E6000 had an SSA of 4.05 ± 0.83 N. Fabri-Fuse had an SSA of 0.69 ± 0.29 N.

![Representative T-peel force-displacement traces for E6000, Fabri-Fuse, JB Weld, and Guo Elephant 407. E6000 reaches the highest force and shows larger oscillations, while Fabri-Fuse and JB Weld remain lower and steadier.](figure-1-representative-t-peel-traces.png)

*Figure 1. Representative T-peel force-displacement traces from Kantepalle et al. (2026), cropped to the Figure 2A panel from the published article. No plotted data or labels were altered. Reused under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Source article](https://doi.org/10.3390/polym18121504).*

That difference changed what I thought the screening question should be. It was no longer only, "Which adhesive gives the largest force?" It became, "Which candidate gives a strong enough, steady enough, and sufficiently deformation-tolerant interface for this application?" On that broader screen, Fabri-Fuse was selected. It also had the lowest reported variation in initiation force across specimens, a high Peel Stability Index, and high displacement at break.

## Checking the decision in the device

A new selection logic needed a downstream test that could contradict it. We printed conductive silver traces directly on fabric and on E6000 and Fabri-Fuse layers, then stretched the assemblies while monitoring electrical conduction.

E6000 was included because it was the peel-force winner. The device comparison asked whether the broader selection held up in the application. If E6000 had performed better, the interpretation would have needed to narrow.

Fabri-Fuse maintained electrical function over a larger strain range before failure, reaching 34.95 ± 2.43% strain compared with 27.98 ± 1.47% for E6000.

The study did not establish why the device outcomes differed. It showed that the force-based winner was not the best performer in the downstream test.

## Making the analysis visible

Once I treated the trace as evidence rather than a route to one number, the analysis became part of the experiment. Which region of the curve was analyzed, which peaks and valleys were retained, and whether those choices made sense on the original trace could all affect the resulting descriptors.

That is why I turned the analysis into a versioned [software workflow](/project/peel-trace-evaluation/) with QC plots, diagnostics, and provenance records. The goal was not to automate judgment away. It was to make the judgment inspectable.

## What I carried forward

The materials I work on now are different. I study how thermal, flow, and deformation histories organize liquid-crystalline and soft-material structure, and how optical measurements track the response. The physics is different, but I carried the same measurement habit forward.

A peak force can hide how a peel response evolves. A single color value, or a color judged by eye, can hide how an optical response changes with temperature, deformation, and processing history. In both cases, the first number available is not always the number that answers the question.

The lesson was not to replace peel strength with a new favorite metric. It was to stop letting the easiest metric define the question.

## Limits

These results come from one stretch-knit fabric system, four adhesives, one peel rate, and three replicate specimens per adhesive in the reported peel comparison. Peel force, force oscillation, and device performance depend on the system and protocol, so the reported descriptors are not intrinsic material constants. Test-system dynamics can also affect observed peel oscillations ([Andrews et al., 1985](https://doi.org/10.1007/BF01113769) and [Dalbe et al., 2016](https://doi.org/10.1039/C6SM00119J)). The association between lower SSA and higher strain-to-electrical-failure in this study does not establish that one caused the other. The full methods and statistics are in the [paper](/publication/adhesives-wearable/).

## References

1. Kantepalle, B. Y., Epitawala Arachchige, U., Joung, D., & Tang, C. (2026). Multi-Criteria Selection of Adhesives for Wearable Textiles. *Polymers, 18*(12), 1504. <https://doi.org/10.3390/polym18121504>
2. *Source data for Multi-Criteria Selection of Adhesives for Wearable Textiles*. (2026). Zenodo. <https://doi.org/10.5281/zenodo.20278428>
3. Kantepalle, B. Y., & Tang, C. (2026). *Peel Trace Evaluation for Soft Substrates* (v1.4.0-rc15). Zenodo. <https://doi.org/10.5281/zenodo.20301242>
4. Andrews, E. H., Khan, T. A., & Majid, H. A. (1985). Adhesion to skin: Part 1 Peel tests with hard and soft machines. *Journal of Materials Science, 20*, 3621-3630. <https://doi.org/10.1007/BF01113769>
5. Dalbe, M.-J., et al. (2016). Inertial and stick-slip regimes of unstable adhesive tape peeling. *Soft Matter, 12*(20), 4537-4548. <https://doi.org/10.1039/C6SM00119J>
