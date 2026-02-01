---
title: "Supply Chain & Chemical Data Operations"
summary: "Spearheaded the digital transformation of chemical supply chain workflows as Technical Project Manager, leveraging Python/Docker to standardize nomenclature and accelerate R&D decision-making."
tags: ["Technical Project Management", "Chemical Operations", "Supply Chain", "Data Strategy", "Industry"]
status_label: "COMPLETED"
date: 2022-10-01
type: project
toc: true
---

## 1. The Situation: The Nomenclature Barrier

**The Context:** In the pharmaceutical supply chain, speed is critical. At **Kreative Organics**, the Business Development team needed to rapidly identify gaps in the global market for specific chemical intermediates.

**The Gap:** The industry suffers from severe data fragmentation. A single molecule might be listed under a Trade Name, an IUPAC name, or a generic identifier across different global databases.
- **The Chemical Problem:** Mismatched **CAS Numbers** (Chemical Abstracts Service) led to missed market opportunities.
- **The Operational Problem:** Researchers spent 70% of their time manually cross-referencing safety data sheets (SDS) and trade logs rather than analyzing market strategy.

## 2. The Task: Operationalizing Data

I was assigned as the **Technical Project Manager** to lead the **Digital Transformation** of this workflow. My objective was not just "software," but **Process Engineering**: creating a robust, standardized pipeline that could translate ambiguous market data into actionable chemical intelligence.

**Key Objectives:**
- **Standardization:** Define a logic to resolve chemical synonym conflicts and establish a "Single Source of Truth."
- **Reliability:** Ensure the tool was robust enough for non-technical staff to run independently.
- **Market Speed:** Compress the timeline from "Data Gathering" to "Sales Action."

## 3. The Action: Engineering the Process

I operated as the **Technical Lead**, bridging the gap between chemical domain knowledge and technical execution.

### A. Defining the "Chemical Logic" (Strategy)
I engineered the standardization algorithm. Unlike a generic developer, I understood the nuances of chemical naming conventions. I defined the rulesets for mapping inconsistent trade names to verified **CAS Names**, ensuring scientific accuracy in the output.

### B. Containerizing the Workflow (Docker)
To ensure operational continuity, I packaged the solution using **Docker**. This wasn't just about code; it was about **Process Reliability**. By containerizing the environment, I ensured that the standardization engine ran identically on every machine, immune to local configuration errors—critical for a regulated industrial environment.

### C. Visualizing Market Gaps (Tableau)
I developed **Strategic Dashboards** in Tableau that mapped global trade volume against our internal inventory. This transformed raw rows of data into stratergic insights, allowing the sales team to navigate and spot the under-served regions for specific chemical classes.

```mermaid
graph TD
  %% Style Definitions
  classDef input fill:#f8f9fa,stroke:#6c757d,stroke-width:1px,stroke-dasharray: 5 5;
  classDef chemistry fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
  classDef ops fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
  classDef output fill:#fff3e0,stroke:#e65100,stroke-width:2px;

  %% Nodes (use \n instead of <br/>)
  Raw["Raw Global Trade Data\n(Ambiguous Naming)"]:::input

  subgraph SE["Standardization Engine"]
    direction TB
    Logic["Chemical Logic Definition\n(CAS Mapping)"]:::chemistry
    Docker["Docker Containerization\n(Process Reliability)"]:::ops
  end

  subgraph BI["Business Intelligence"]
    direction TB
    Viz["Tableau Market Heatmaps\n(Supply/Demand Gaps)"]:::ops
  end

  Result["Qualified Sales Targets"]:::output

  %% Flow
  Raw --> Logic --> Docker --> Viz --> Result
```
## 4. The Result
- Operational Efficiency: Slashed market research time by 70%, effectively automating the "grunt work" of data collection.
- Data Integrity: Achieved a 90% accuracy uplift in chemical identification, virtually eliminating errors caused by synonym confusion.
