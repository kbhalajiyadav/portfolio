---
title: "Optical Metrology for Mechanochromic Textiles"
date: "2026-04-22T00:00:00Z"
lastmod: "2026-10-10T00:00:00Z"
status: "Presented research"
summary: "A Python and OpenCV workflow for measuring deformation and color response in mechanochromic textiles from synchronized image data."
tags:
  - Optical Metrology
  - Computer Vision
  - Smart Textiles
  - Python
  - OpenCV
type: project
toc: false
weight: 2
---

## Measurement problem

A visible color change is not, by itself, a quantitative measurement. The
analysis must distinguish material response from changes caused by motion,
framing, illumination, and the test setup. This work developed a
computer-vision workflow for relating deformation in a textile specimen to its
measured optical response during loading.

## Measurement workflow

The workflow uses Python and OpenCV to:

- track deformation from recorded image sequences;
- define and follow regions used for optical measurement;
- convert sampled color values to CIE L\*a\*b\* coordinates;
- compare strain and color response over the loading history; and
- produce repeatable outputs that can be reviewed alongside mechanical data.

{{< method-schematic id="optical-metrology-schematic" title="Optical metrology measurement sequence" steps="Synchronized~imaging|Deformation~tracking|Region~selection|CIE L*a*b*~conversion|Strain and color~comparison" caption="The steps summarize a synchronized image-to-color measurement workflow." >}}

## Presentations and outputs

The work was presented in 2026 as **“Quantifying Mechanochromic Response in
Smart Textiles: A Computer Vision Approach”** at the VCU Engineering Graduate
Research and Postdoc Showcase and the 29th VCU Graduate Student Research
Symposium.

Related first-author research on the influence of textile substrates on
mechanochromic sensitivity was [accepted for publication in *ACS Applied Polymer Materials*](/publication/mechanochromic-textiles/) on October 27, 2026.

- [Research overview](/research/#measure-response)
- [Presentation record](/engagement/)
- [Accepted journal manuscript](/publication/mechanochromic-textiles/)

The presentations document the optical-metrology workflow described here.
No public dataset or standalone code release is linked to this project.
