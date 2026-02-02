---
title: "Integrated Optical Metrology System"
summary: "Engineered a high-throughput Python/OpenCV pipeline to quantify mechanochromic response, synchronizing sub-pixel tracking with rigorous CIE L*a*b* colorimetry."
tags: ["Computer Vision", "Python", "Metrology", "Data Pipelines", "Smart Textiles", "Academic Research"]
status: "DEPLOYED"
date: 2025-01-31
type: project
toc: true

image:
    filename: featured.png
    focal_point: smart
    preview_only: false
---

## 1. The Situation: Beyond the Human Eye

**The Context:** Validating mechanochromic materials requires more than just seeing a color change; it requires quantifying it. To prove a material is viable for injury monitoring, we need a precise correlation between mechanical strain and optical response in the **CIE L*a*b*** color space.

**The Gap:** Manual analysis was insufficient. High-speed video data (2000+ frames/test) suffered from lighting variances and mechanical "drift" (clamp slippage), making it impossible to separate true color shifts from environmental noise.

## 2. The Task: A "Ground Truth" Pipeline

I needed to architect a **Computer Vision System** capable of isolating the material's physical response from experimental artifacts.

**Key Requirements:**
- **Input Compliance:** Automatically reject or correct video inputs (HDR/SDR) to ensure lighting standardization.
- **Structural Integrity:** Track the material's texture (yarns) independent of the testing rig to eliminate mechanical noise.
- **Rigorous Colorimetry:** Quantify response using **CIE Lab** scalars, moving beyond basic RGB values to measure Perceptual Color Difference Delta E00/E76.

## 3. The Action: The approach

I developed a modular **Python/OpenCV** architecture that operates on two distinct analytical layers: **Structural (Texture)** and **Scalar (Color Physics)**.

### A. Gateway: Input Compliance & Pre-processing
Before analysis begins, the pipeline acts as a quality gate. It detects High-Dynamic-Range (HDR) profiles and uses an **FFmpeg-based Tone Mapping engine** (Hable method) to enforce a standardized SDR color profile. This ensures that every pixel analyzed represents true material reflectance, not camera auto-exposure artifacts.

### B. Layer 1: Structural Analysis (Texture Tracking)
To solve the "drift" problem, I implemented **ECC (Enhanced Correlation Coefficient)** tracking. Instead of tracking the machine's movement, the code locks onto the *texture* of the rigid clamps with sub-pixel accuracy. This creates a "Virtual Extensometer" that calculates strain based on the actual material deformation, removing fabric slippage noise entirely.

### C. Layer 2: Scalar Analysis (CIE Colorimetry)
Once the region of interest is structurally stabilized, the pipeline performs deep colorimetry. It converts raw pixel data into **CIE Lab** coordinates—separating Lightness L* from Chromaticity a*, b*. This allows us to calculate Delta E00$ (CIEDE2000), providing a mathematically rigorous metric for "Visible Color Change" that matches human perception.

```mermaid
graph TD
    %% Professional Style Definitions
    classDef input fill:#f8f9fa,stroke:#6c757d,stroke-width:1px,stroke-dasharray: 5 5;
    classDef gateway fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef structure fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef scalar fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    %% Nodes
    Video[/"Raw High-Speed Video<br/>(HDR/MOV)"/]:::input
    
    subgraph "The Compliance Gateway"
        Check{"HDR Check"}:::gateway
        Norm["Standardization<br/>(Hable Tone Mapping)"]:::gateway
    end

    subgraph "Layer 1: Structural Analysis"
        ECC["Sub-Pixel ECC Tracking<br/>(Texture Locking)"]:::structure
        Drift["Zero-Drift Compensation"]:::structure
    end

    subgraph "Layer 2: Scalar Analysis (CIE)"
        Lab["RGB to CIE L*a*b*<br/>Conversion"]:::scalar
        Metrics["Calculate ΔE2000<br/>(Perceptual Difference)"]:::scalar
        PCA["Feature Ranking<br/>(Signal Isolation)"]:::scalar
    end

    Out[/"Quantified Color<br/>Response Curves"/]:::input

    %% Flow
    Video --> Check
    Check -- "Compliance Fail" --> Norm
    Norm --> ECC
    Check -- "Pass" --> ECC
    ECC --> Drift
    Drift --> Lab
    Lab --> Metrics
    Metrics --> PCA
    PCA --> Out
```

## 4. The Result
- **Scientific Precision:** Successfully decoupled mechanical noise from optical signal, revealing a "Hysteresis Loop" in the color response (fatigue history) that was previously invisible in manual analysis.
- **Throughput:** Reduced data processing time by >90% (from 4 hours/video to 5 minutes), enabling high-volume statistical validation.
- **Standardization:** This pipeline is now the primary validation tool, providing the quantitative CIE metrics required to benchmark new mechanochromic materials against known literature work.
