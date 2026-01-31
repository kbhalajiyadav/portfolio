---
title: Mechanics-Consistent Adhesion in Soft Wearables
summary: "<span style='background-color: #e8f5e9; color: #2e7d32; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em; border: 1px solid #2e7d32;'>ACTIVE RESEARCH</span> A stability-driven framework preventing 'False Positive' adhesion failures in skin-interfaced electronics, validated using a custom Python signal analysis pipeline."
tags:
  - Fracture Mechanics
  - Soft Robotics
  - Python (Signal Analysis)
  - Instron
date: 2025-01-30
---

**Status:** <span style="color: #2e7d32; font-weight: bold;">Active Research (Aims 1 & 2)</span>

## 1. The Challenge (First Principles Analysis)
Current industry standards (ASTM D1876) rely on the assumption that **Average Peel Force = Adhesion**.
By applying **First Principles thinking**, we identified that this assumption fails for soft wearables. In viscoelastic systems, the total work is dominated by bulk dissipation (stretching), not interfacial bonding. This creates a **"False Positive Trap"**: adhesives that appear strong in standard tests but fail functionally due to "stick-slip" instability.

## 2. The Innovation: Stability Metrics
I established a **Mechanics-Consistent Framework** to isolate true interfacial toughness.
* **Physics of Failure:** We distinguish between **Initiation Force ($F_{ci}$)** (the peaks, representing true crack resistance) and **Arrest Force ($F_{ca}$)** (the troughs, representing artifacts).
* **The Metric:** Introduced the **Peel Stability Index (PSI)** ($\mu_F / \sigma_F$). High PSI indicates stable, self-similar crack propagation (Category II), essential for low-noise sensor performance.

## 3. The Tool: Automated Python Pipeline
To operationalize this physics, I engineered a custom Python analysis pipeline (replacing manual Excel analysis) to detect $F_{ci}$ without human bias.

```mermaid
graph TD
    classDef input fill:#f1f8ff,stroke:#0366d6,stroke-width:2px,color:#000;
    classDef process fill:#ffffff,stroke:#586069,stroke-width:1px,color:#000;
    classDef innovation fill:#e6ffed,stroke:#22863a,stroke-width:2px,color:#000,stroke-dasharray: 5 5;
    classDef output fill:#fff5b1,stroke:#b08800,stroke-width:2px,color:#000;

    A["Raw Data Input<br/>Force vs. Displacement"]:::input --> B["Preprocessing<br/>Data Cleaning & Unit Conversion"]:::process
    B --> C["Baseline Correction<br/>Normalize Starting Force to 0N"]:::process
    
    subgraph "Physics-Based Core Analysis"
        direction TB
        D{"Identify Steady-State<br/>Window"}:::innovation
        E["Peak & Trough Detection<br/>Isolate Initiation Forces (F_ci)"]:::innovation
        F["Calculate Stability Metrics<br/>PSI = F_mean / Sigma_F"]:::innovation
    end

    C --> D
    D -- "Scan: Min. Std Dev" --> E
    E --> F
    F --> H["Summary Report<br/>Metrics: G_ci, PSI"]:::output
