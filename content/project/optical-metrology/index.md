---
title: "Integrated Optical Metrology System"
summary: "<span style='background-color: #e8f5e9; color: #2e7d32; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em; border: 1px solid #2e7d32;'>DEPLOYED</span> Engineered a high-throughput Python/OpenCV pipeline to quantify mechanochromic response, synchronizing sub-pixel tracking with CIEDE2000 colorimetry."
tags: ["Computer Vision", "Python", "Metrology", "Data Pipelines", "Smart Textiles", "Academic Research"]
date: 2025-01-31
type: project
---

<style>
  /* Force Wide Layout */
  .container, .article-container {
      max-width: 96% !important; 
      margin-left: 20px !important;
      margin-right: auto !important;
      padding-left: 0 !important;
  }
  
  /* The Grid Layout */
  .project-layout {
      display: grid;
      grid-template-columns: 3fr 1fr;
      gap: 40px;
      margin-top: 20px;
  }

  /* The Sticky Sidebar */
  .toc-sidebar {
      position: -webkit-sticky;
      position: sticky;
      top: 100px;
      height: fit-content;
      border-left: 2px solid #e0e0e0;
      padding-left: 20px;
  }

  .toc-link {
      display: block;
      color: #555;
      margin-bottom: 10px;
      text-decoration: none;
      font-weight: 500;
      transition: color 0.2s;
  }
  .toc-link:hover {
      color: #0d47a1;
      border-left: 3px solid #0d47a1;
      padding-left: 5px;
      margin-left: -8px;
  }

  @media (max-width: 768px) {
      .project-layout { grid-template-columns: 1fr; }
      .toc-sidebar { display: none; }
  }
</style>

<div class="project-layout">

  <div class="main-content">
      
      <h2 id="situation">1. The Situation: The Limits of the Human Eye</h2>
      <p><strong>The Context:</strong> Developing <strong>mechanochromic wearables</strong> (smart textiles that change color under strain) for athletic monitoring and injury prevention requires precise correlation between mechanical stretch and optical response.</p>
      <p><strong>The Gap:</strong> Manual analysis was impossible. High-dynamic-range (HDR) lighting artifacts, mechanical "drift" (clamp slippage), and the sheer volume of video data (600+ frames per test) made manual quantification inaccurate. Existing commercial software could not handle the complex "stick-slip" mechanics of soft fabrics.</p>
      <br>

      <h2 id="task">2. The Task: Automating the Unseeable</h2>
      <p>I needed to engineer a <strong>"Ground Truth" Analysis Pipeline</strong> that could:</p>
      <ul>
          <li><strong>Auto-Correct Video:</strong> Standardize lighting and color profiles (HDR to SDR) to ensure color consistency.</li>
          <li><strong>Zero-Drift Tracking:</strong> Track specific textile yarns with sub-pixel accuracy, ignoring clamp slippage.</li>
          <li><strong>Perceptual Quantization:</strong> Convert RGB pixels into <strong>CIEDE2000 (ΔE)</strong> values—a metric that matches human visual perception of color change.</li>
      </ul>
      <br>

      <h2 id="action">3. The Action: The Master Pipeline (V17.3)</h2>
      <p>I developed a modular <strong>Python/OpenCV</strong> architecture to process raw experimental video into actionable material science data.</p>

      <h3>A. Smart HDR & Pre-processing</h3>
      <p>Standard cameras use auto-exposure that ruins scientific color analysis. I implemented an <strong>FFmpeg-based Tone Mapping engine</strong> (Hable method) to linearize the color space, recovering "True Black" levels and standardizing the lighting baseline before tracking begins.</p>

      <h3>B. Sub-Pixel Drift Guard</h3>
      <p>Instead of simple object tracking, I utilized <strong>ECC (Enhanced Correlation Coefficient)</strong> algorithms to lock onto the rigid clamps separately from the stretching fabric. This creates a "Virtual Extensometer" that calculates strain based on the <em>geometry of the clamps</em>, removing fabric slippage noise entirely.</p>

      <h3>C. Feature Ranking via PCA</h3>
      <p>The code doesn't just measure color; it determines <em>which</em> color shift matters. I integrated <strong>Principal Component Analysis (PCA)</strong> to rank 85+ metrics (Hue, Saturation, Lab, RGB ratios), automatically identifying that <strong>PC1 (Primary Strain Axis)</strong> was driven by ΔE00, identifying the most sensitive signal for injury detection.</p>

      <div class="mermaid">
graph TD
    %% Styles
    classDef input fill:#f8f9fa,stroke:#6c757d,stroke-width:1px,stroke-dasharray: 5 5;
    classDef process fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef logic fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef output fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;

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
        DE00["Calculate ΔE2000<br/>(Perceptual Difference)"]:::logic
        PCA["PCA Feature Ranking<br/>(Identify Signal vs Noise)"]:::logic
    end

    Out[/"Hysteresis Loops &<br/>Strain-Color Correlation"/]:::output

    %% Flow
    Video --> FFmpeg --> BlackLevel
    BlackLevel --> Tracker --> ROI
    ROI --> Lab --> DE00 --> PCA
    PCA --> Out
      </div>
      <p><em>Figure 1: The V17.3 Pipeline Architecture. Note the transition from raw signal processing to physics-based logic (ΔE2000) and finally statistical learning (PCA). </em></p>
      <br>

      <h2 id="result">4. The Result</h2>
      <p>This system transformed the lab's capability to validate wearable sensors.</p>
      <ul>
        <li><strong>Throughput:</strong> Reduced analysis time by <strong>>90%</strong> (from 4 hours/video to 5 minutes).</li>
        <li><strong>Discovery:</strong> Revealed a <strong>"Hysteresis Loop"</strong> in the color response—proving that the sensor tracks not just peak strain, but also the <em>history</em> of deformation (fatigue), critical for athlete recovery monitoring.</li>
        <li><strong>Application:</strong> The code is now the standard validation tool for the $30,000 CCI Grant project, ensuring every prototype meets the "Visual Strain Threshold" required for field use.</li>
      </ul>

  </div>

  <div class="toc-sidebar">
      <h4 style="margin-top:0;">On This Page</h4>
      <a href="#situation" class="toc-link">1. The Situation</a>
      <a href="#task" class="toc-link">2. The Task</a>
      <a href="#action" class="toc-link">3. The Action</a>
      <a href="#result" class="toc-link">4. The Result</a>
  </div>

</div>
