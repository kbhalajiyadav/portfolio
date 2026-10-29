---
title: "Research Program"
kicker: "Research overview"
summary: "How processing histories organize soft functional materials, and how to measure the resulting response reliably."
date: "2026-07-28T00:00:00Z"
lastmod: "2026-10-29T00:00:00Z"
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

For a focused account of my research background, doctoral questions, and experimental approach, see the [research statement](/research-statement/).

## Research focus

My research asks how thermal and mechanical histories organize soft functional
materials, which structural changes explain their responses, and what makes
those measurements trustworthy. The work connects five stages:

{{< research-signature >}}

## Measure response

Current work develops mechanics-consistent measurements for soft, stretchable,
and textile-supported systems. The methods combine force–displacement analysis,
deformation tracking, optical colorimetry, and computer vision instead of
relying on a single maximum-force value or a visual assessment of color change.

Related work:

- a [first-author article on multi-criteria adhesive selection](/publication/adhesives-wearable/) for wearable textiles;
- the [associated M.S. thesis](/publication/masters-thesis/);
- [versioned research software](/project/peel-trace-evaluation/) for protocol-defined peel-trace analysis;
- an [optical-metrology project](/project/optical-metrology/) for computer-vision measurement of mechanochromic textiles;
- the [patent-pending Quantitative Thermal Imaging technology](/project/quantitative-thermal-imaging/) (VCU Tech # TAN-26-099); and
- presentation records for [adhesion and soft wearable interfaces](/engagement/#adhesion-soft-wearable-interfaces) and [computer-vision metrology](/engagement/#computer-vision-mechanochromic-textiles).

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

The broader goal is to test which **measurement and analysis methods** can transfer
to other responsive materials and process-sensitive formulations. Functional
printing inks, extrusion-processed soft composites, and liquid-crystal
elastomers pose adjacent processing–structure–response questions; they do not
necessarily share the cholesteric model system's molecular mechanism.

Published examples of [flow-programmed alignment in printed liquid-crystal
elastomers](https://doi.org/10.1073/pnas.2414960122) and
[temperature- and shear-controlled smectic ink printing](https://doi.org/10.1038/s41467-026-75368-z)
illustrate that connection. They are studies by other groups, not findings
from my cholesteric experiments.

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

- process-history-aware characterization of responsive formulations;
- rheology-guided evaluation of printable functional inks and soft composites,
  requiring system-specific measurements; and
- repeatable calibration of passive thermal indicators and wearable interfaces
  before any application-level performance claim.

Separately, **exploratory computational thermography** applies infrared-image
analysis independently of liquid-crystal-based color indicators.

Infrared thermography and thermochromic color sensing use different physical
measurement principles. Estimating physiological quantities such as body-fat
percentage or metabolic rate from skin-temperature imagery would require
independent reference data and rigorous validation; these are **not** current
capabilities or diagnostic claims.

A Spring 2026 applied-innovation prototype explored this translation through a
battery-free thermochromic foot-care sock concept for personalized heat-pattern
monitoring in people with diabetes. It was demonstrated as a prototype rather
than evaluated as a clinical device; see the [applied-innovation record](/engagement/#engagement-contributions-heading).

## Connected research outputs

The first-author adhesion work connects three complementary outputs:

1. [Peer-reviewed article](/publication/adhesives-wearable/)
2. [M.S. thesis](/publication/masters-thesis/)
3. [Research software](/project/peel-trace-evaluation/)

Together, the article reports the scientific result, the thesis records the
degree and embargo status, and the software provides a citable implementation
of the analysis workflow.

The separate [Quantitative Thermal Imaging page](/project/quantitative-thermal-imaging/)
summarizes the patent-pending technology and its current Virginia Commonwealth
University intellectual-property status.

## Open research questions

- **Processing history and molecular order:** How do heating, cooling, and shear alter cholesteric orientation, structural transitions, and recovery? When does helical order persist, reorient, or unwind?
- **Structure and trustworthy measurement:** Which combinations of rheology, scattering, and optical measurements can distinguish structural changes from hysteresis, experimental drift, and competing interpretations?
- **Calibrating response across thermal cycles:** How consistently can temperature-dependent optical responses be calibrated over repeated heating and cooling cycles, and what limits their use as quantitative thermal indicators?
