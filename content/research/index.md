---
title: "Research Program"
kicker: "Research overview"
summary: "How processing histories organize soft functional materials, and how to measure the resulting response reliably."
date: "2026-07-28T00:00:00Z"
lastmod: "2026-10-30T00:00:00Z"
toc: true
tags:
  - Stimuli-Responsive Materials
  - Soft Materials
  - Liquid Crystals
  - Quantitative Metrology
  - Rheology
  - Neutron Scattering
url: /research/
---

This page provides an overview of the research program, its supporting work, and open questions. For the fuller scientific narrative and experimental direction, see the [research statement](/research-statement/).

## Research focus

The research program examines how thermal and mechanical histories affect soft
materials, from a defined stimulus through reproducible measurement and translation:

{{< research-signature >}}

## Measure response

Earlier work developed mechanics-consistent measurements for soft, stretchable,
and textile-supported systems, combining force–displacement analysis,
deformation tracking, optical colorimetry, and computer vision. These methods
go beyond a single maximum-force reading or a visual assessment of color change.

Examples include the [optical-metrology project](/project/optical-metrology/) and
[accepted research on textile mechanochromism](/publication/mechanochromic-textiles/).
The published adhesion article, associated thesis, and software are grouped under
[Connected research outputs](#connected-research-outputs).

## Resolve structure under stimuli

Small-molecule cholesteric mixtures provide a **model system** for investigating
how cooling and shear reorganize liquid-crystalline order. They show optical
textures under controlled processing without introducing polymer-chain
dynamics, while leaving important structural mechanisms open to investigation.

One question is whether a change in optical texture under shear reflects
reorientation of helical structure, changes in local orientation, or unwinding.
Optics alone need not distinguish those possibilities. Rheology records the
mechanical response; appropriately selected scattering measurements can
provide complementary structural information when their length scale,
contrast, and geometry support the comparison. These are research hypotheses,
not claims that the competing mechanisms have been resolved.

Shear-induced optical-texture changes in cholesteric mixtures were already
[documented in 1971](https://doi.org/10.1103/PhysRevLett.27.790).
The question here is not whether shear can change texture, but which
structural processes explain the measured optical and rheological responses
for a specified mixture and processing history.

The broader goal is to identify which **controlled protocols and measurement
methods** can be useful across process-sensitive materials without assuming a
shared molecular mechanism. Published work on [printed liquid-crystal
elastomers](https://doi.org/10.1073/pnas.2414960122),
[smectic 3D-printing inks](https://doi.org/10.1038/s41467-026-75368-z),
and [rheology–printability relationships in direct ink writing](https://doi.org/10.1016/j.pmatsci.2023.101188)
illustrates adjacent problems in how flow history affects alignment, print
fidelity, and final response.

## Translate reproducibly

Reproducible measurements must distinguish changes in material state from
heating/cooling hysteresis, recovery effects, environmental conditions, and
instrument drift. Documenting thermal and shear protocols, acquisition timing,
calibration, and analysis versions is therefore as important as increasing
experimental throughput.

The [peel-trace analysis software](/project/peel-trace-evaluation/) is an
existing example of versioned measurement analysis. Synchronized thermal,
optical, mechanical, and structural workflows are a **prospective direction**;
they are not presented here as a completed automation platform.

## Application directions

Potential translation paths include:

- rheological characterization of functional inks and extrusion-based 3D
  printing, with deposition and shape retention assessed for each formulation;
- process–microstructure–property studies in printed coatings and electronics,
  including film formation and electrical performance where relevant; and
- calibration and repeatability of passive thermal indicators and wearable
  interfaces, with application-specific validation before performance claims.

**Separate exploratory direction:** computational infrared thermography uses
different sensing physics from thermochromic indicators. No physiological
inference or diagnostic capability is claimed. The
[2026 thermochromic foot-care prototype](/engagement/#engagement-contributions-heading)
was a demonstration concept, not a clinically evaluated device.

## Connected research outputs

Two first-author research directions are represented here: the [accepted ACS manuscript on mechanochromic textile sensitivity](/publication/mechanochromic-textiles/) and the separately published adhesion study. Related 2026 presentations are documented under [adhesion and soft wearable interfaces](/engagement/#adhesion-soft-wearable-interfaces) and [computer-vision metrology](/engagement/#computer-vision-mechanochromic-textiles). The adhesion study connects three complementary outputs:

1. [Peer-reviewed article](/publication/adhesives-wearable/)
2. [M.S. thesis](/publication/masters-thesis/)
3. [Research software](/project/peel-trace-evaluation/)

Together, the article reports the scientific result, the thesis records the
degree and embargo status, and the software provides a citable implementation
of the analysis workflow.

The separate [Quantitative Thermal Imaging page](/project/quantitative-thermal-imaging/)
summarizes the patent-pending technology and its current Virginia Commonwealth
University intellectual-property status (VCU Tech # TAN-26-099).

## Open research questions

- **Processing history and molecular order:** How do heating, cooling, and shear alter cholesteric orientation, structural transitions, and recovery? When does helical order persist, reorient, or unwind?
- **Structure and trustworthy measurement:** Which combinations of rheology, scattering, and optical measurements can distinguish structural changes from hysteresis, experimental drift, and competing interpretations?
- **Calibrating response across thermal cycles:** How consistently can temperature-dependent optical responses be calibrated over repeated heating and cooling cycles, and what limits their use as quantitative thermal indicators?
