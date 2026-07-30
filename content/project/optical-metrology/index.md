---
title: "Optical Metrology for Mechanochromic Textiles"
date: "2026-04-22T00:00:00Z"
lastmod: "2026-07-30T00:00:00Z"
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

The method treats image acquisition, deformation tracking, and color analysis
as one measurement sequence rather than as separate visual observations.

## Public record

The work was presented in 2026 as **“Quantifying Mechanochromic Response in
Smart Textiles: A Computer Vision Approach”** at the VCU Engineering Graduate
Research and Postdoc Showcase and the 29th VCU Graduate Student Research
Symposium.

- [Research overview](/research/#measure-response)
- [Presentation record](/#presentations)

## Evidence boundary

This page describes the public method at a high level. It does not claim
clinical validation, product deployment, a published performance benchmark, or
public release of the underlying experimental data. Detailed acquisition
settings, specimen data, and unpublished analysis results are not included.
