---
title: Mechanics-Consistent Adhesion in Soft Wearables
summary: Developing stability-driven fracture metrics to prevent "False Positive" adhesion in stretchable electronics.
tags:
  - Materials Science
  - Fracture Mechanics
  - Soft Robotics
date: 2024-01-30

# Optional external link for the project (replaces the project page)
external_link: ''

image:
  caption: ''
  focal_point: Smart

links:
url_code: ''
url_pdf: ''
url_slides: ''
url_video: ''

# Slides (optional).
#   Associate this project with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides: ""
---

**Status:** Active Research (Aims 1 & 2)

## Overview
Conventional peel metrics (like ASTM D1876) often fail for soft, extensible interfaces because they cannot distinguish between **true interfacial adhesion** and **bulk dissipation** (stretching/bending). This leads to a "False Positive Trap," where an adhesive appears strong on paper but fails functionally in a wearable device due to stick-slip instability.

This project establishes a **mechanics-consistent framework** to predict reliability in wearable strain sensors.

## Key Innovations

### 1. The Peel Stability Index (PSI)
We introduced the **Peel Stability Index (PSI)**, defined as the ratio of mean peel force to its standard deviation ($ \mu_F / \sigma_F $).
* **High PSI:** Indicates steady-state crack propagation (Category II), allowing for valid fracture energy ($G_c$) extraction.
* **Low PSI:** Indicates stick-slip instability (Category III), which generates electrical noise artifacts in wearable sensors.

### 2. Eliminating the "False Positive"
We demonstrated that adhesives with high nominal peel strength often exhibit "limited propagation," failing to exit the initiation phase. By filtering these out, we prevent signal drift in critical monitoring applications like knee rehabilitation.

## Applications
* **Wearable Demonstrator:** A printed serpentine strain sensor on a knitted knee sleeve, utilizing a PSI-optimized primer layer to minimize hysteresis and resistance drift.
* **Medical Monitoring:** Ensuring signal fidelity for 30-40% strain monitoring in Total Knee Arthroplasty (TKA) rehabilitation.

## Methodologies
* **T-Peel Testing (ASTM D2724 Adapted):** Customized for porous knitted substrates.
* **IC-Peel Protocol:** For extracting intrinsic fracture energy decoupled from plasticity.
* **Uniaxial Tensile Profiling:** ASTM D5035 characterization of substrate compliance.
