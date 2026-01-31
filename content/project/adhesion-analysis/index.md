---
title: Mechanics-Consistent Adhesion in Soft Wearables
summary: "<span style='background-color: #e8f5e9; color: #2e7d32; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em; border: 1px solid #2e7d32;'>ACTIVE RESEARCH</span> Developed a First-Principles framework to identify 'False Positive' adhesion failures, utilizing a custom Python pipeline to automate fracture mechanics analysis."
tags:
  - Fracture Mechanics
  - Soft Robotics
  - Python (Signal Analysis)
  - Instron
date: 2025-01-30
---

**Status:** <span style="color: #2e7d32; font-weight: bold;">Active Research (Aims 1 & 2)</span> | **Output:** Presented at [ACS Fall 2025](https://www.acs.org/)

## 1. The Situation: The "False Positive" Trap
**The Gap:** Current industry standards (like ASTM D1876) assume that higher average peel force equals better adhesion.
**The Problem:** I identified that this assumption fails for soft wearables. In stretchable textiles, up to 90% of the "measured force" is actually just the fabric stretching (dissipation), not the glue holding. This creates a **"False Positive Trap"**: selecting adhesives that look strong in the lab but fail functionally on the human body due to "stick-slip" instability.

## 2. The Action: Rational Engineering
Instead of relying on misleading averages, I applied **First Principles Thinking** to re-engineer how we define failure.

* **Logic over Data:** I deconstructed the force profile to distinguish between **True Adhesion** (the peaks, representing crack resistance) and **Artifacts** (the troughs, representing slip).
* **The Metric:** I introduced the **Peel Stability Index (PSI)**. Unlike raw force, this metric quantifies *consistency*. A high PSI predicts that a sensor will perform reliably without electrical noise, preventing costly device failures downstream.

## 3. The Execution: Automated Python Pipeline
To remove human bias and speed up analysis, I built a custom Python pipeline that operationalizes this physics-based logic.

```mermaid
graph TD
    %% Define Professional "Classy" Styles
    classDef input fill:#f8f9fa,stroke:#6c757d,stroke-width:1px,color:#212529,stroke-dasharray: 5 5;
    classDef logic fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px,color:#0d47a1;
    classDef result fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#1b5e20;

    %% Nodes
    Raw[/"Raw Force Data<br/>(Noisy & Unreliable)"/]:::input
    
    subgraph "The Python Pipeline (Automated Logic)"
        Clean["Step 1: Signal Cleaning<br/>(Remove Vibration Artifacts)"]:::logic
        Detect{"Step 2: Physics Check<br/>Is it Adhesion or Stretching?"}:::logic
        Filter["Step 3: Feature Extraction<br/>Isolate True Peak Load"]:::logic
    end

    Output[/"Final Output:<br/>Reliability Score (PSI)"/]:::result

    %% Connections
    Raw --> Clean
    Clean --> Detect
    Detect -- "Stretching (Dissipation)" --> Clean
    Detect -- "True Adhesion" --> Filter
    Filter --> Output
