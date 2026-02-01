---
title: "Integrated Optical Metrology System"
summary: "<span style='background-color: #e8f5e9; color: #2e7d32; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em; border: 1px solid #2e7d32;'>DEPLOYED</span> Engineered a high-throughput Python/OpenCV pipeline to quantify mechanochromic response, synchronizing sub-pixel tracking with CIEDE2000 colorimetry."
tags: ["Computer Vision", "Python", "Metrology", "Data Pipelines", "Smart Textiles","Academic Research"]
date: 2025-01-31
status_label: "COMPLETED"
type: project
toc: true
---

## 1. The Situation: The Limits of the Human Eye

**The Context:** Developing **mechanochromic wearables** (smart textiles that change color under strain) for athletic monitoring and injury prevention requires precise correlation between mechanical stretch and optical response.

**The Gap:** Manual analysis was impossible. High-dynamic-range (HDR) lighting artifacts, mechanical "drift" (clamp slippage), and the sheer volume of video data (600+ frames per test) made manual quantification inaccurate. Existing commercial software could not handle the complex "stick-slip" mechanics of soft fabrics.

## 2. The Task: Automating the Unseeable

I needed to engineer a **"Ground Truth" Analysis Pipeline** that could process raw high-speed video into actionable material science data.

**Key Requirements:**
- **Auto-Correct Video:** Standardize lighting and color profiles (HDR to SDR) to ensure color consistency.
- **Zero-Drift Tracking:** Track specific textile yarns with sub-pixel accuracy, ignoring clamp slippage.
- **Perceptual Quantization:** Convert RGB pixels into **CIEDE2000 (ΔE)** values—a metric that matches human visual perception of color change.

## 3. The Action: The Master Pipeline (V17.3)

I developed a modular **Python/OpenCV** architecture to bridge Computer Vision and Materials Science.

### A. Smart HDR & Pre-processing
Standard cameras use auto-exposure that ruins scientific color analysis. I implemented an **FFmpeg-based Tone Mapping engine** (Hable method) to linearize the color space, recovering "True Black" levels and standardizing the lighting baseline before tracking begins.

### B. Sub-Pixel Drift Guard
Instead of simple object tracking, I utilized **ECC (Enhanced Correlation Coefficient)** algorithms to lock onto the rigid clamps separately from the stretching fabric. This creates a "Virtual Extensometer" that calculates strain based on the *geometry of the clamps*, removing fabric slippage noise entirely.

### C. Feature Ranking via PCA
The code doesn't just measure color; it determines *which* color shift matters. I integrated **Principal Component Analysis (PCA)** to rank 85+ metrics (Hue, Saturation, Lab, RGB ratios), automatically identifying that **PC1 (Primary Strain Axis)** was driven by ΔE00, identifying the most sensitive signal for injury detection.

```mermaid
graph TD
    %% Define Professional "Classy" Styles
    classDef input fill:#f8f9fa,stroke:#6c757d,stroke-width:1px,color:#212529,stroke-dasharray: 5 5;
    classDef process fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px,color:#0d47a1;
    classDef logic fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#1b5e20;
    classDef output fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#e65100;

    %% Nodes
    Video[/"Raw High-Speed Video<br/>(HDR/MOV)"/]:::input
    
    subgraph "Preprocessing Engine"
        FFmpeg["FFmpeg Tone Mapping<br/>(Hable Algorithm)"]:::process
        BlackLevel["Black Level Correction<br/>(Recover True Zero)"]:::process
    end

    subgraph "Computer Vision Core"
        Tracker["ECC Sub-Pixel Tracker<br/>(Zero-Drift Lock)"]:::logic
        ROI["Dynamic ROI Anchoring<br/>(Compensates for Jitter)"]:::logic
    end

    subgraph "Colorimetry & Physics"
        Lab["RGB to CIELAB Conversion"]:::process
        DE00["Calculate DeltaE 2000<br/>(Perceptual Difference)"]:::logic
        PCA["PCA Feature Ranking<br/>(Identify Signal vs Noise)"]:::logic
    end

    Out[/"Hysteresis Loops &<br/>Strain-Color Correlation"/]:::output

    %% Flow
    Video --> FFmpeg --> BlackLevel
    BlackLevel --> Tracker --> ROI
    ROI --> Lab --> DE00 --> PCA
    PCA --> Out
