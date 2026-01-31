---
title: "Dummy Layout Test"
summary: "Testing Wide Layout & Sticky TOC"
date: 2025-01-31
tags: ["Test", "Layout"]
design:
  columns: '1'
---

<style>
  /* Force Wide Layout */
  .container, .article-container {
      max-width: 96% !important; 
      margin-left: 20px !important;
      margin-right: auto !important;
      padding-left: 0 !important;
  }
  
  /* The Grid Layout: 70% Text | 30% Sidebar */
  .project-layout {
      display: grid;
      grid-template-columns: 3fr 1fr; /* 3 parts text, 1 part menu */
      gap: 40px;
      margin-top: 20px;
  }

  /* The Sticky Sidebar */
  .toc-sidebar {
      position: -webkit-sticky; /* Safari */
      position: sticky;
      top: 100px; /* Stops 100px from top of screen */
      height: fit-content;
      border-left: 2px solid #e0e0e0;
      padding-left: 20px;
  }

  /* Navigation Links Style */
  .toc-link {
      display: block;
      color: #555;
      margin-bottom: 10px;
      text-decoration: none;
      font-weight: 500;
      transition: color 0.2s;
  }
  .toc-link:hover {
      color: #1976d2; /* Active Blue */
      border-left: 3px solid #1976d2;
      padding-left: 5px;
      margin-left: -8px;
  }

  /* Mobile Responsive: Stack them on small screens */
  @media (max-width: 768px) {
      .project-layout { grid-template-columns: 1fr; }
      .toc-sidebar { display: none; } /* Hide TOC on phone */
  }
</style>

<div class="project-layout">

  <div class="main-content">
      
      <h2 id="situation">1. The Situation</h2>
      <p><strong>The Gap:</strong> Current industry standards (ASTM D1876) assume that Average Peel Force = Adhesion.</p>
      <p>This text is now taking up 70% of the screen width. It allows your eyes to scan comfortably without jumping lines too often. This is the ideal width for "Deep Reading."</p>
      <br>

      <h2 id="action">2. The Action</h2>
      <p>Instead of relying on averages, I applied <strong>First Principles Thinking</strong>.</p>
      <p>I deconstructed the force profile to distinguish between True Adhesion (peaks) and Artifacts (troughs). This required building a custom Python pipeline.</p>
      <br>

      <h2 id="execution">3. The Execution</h2>
      <p>This is where your Mermaid Diagram will go. It sits perfectly inside this column.</p>
      <br>
      <br>
      <br>
      <br>
      <br>
      <p>(Adding extra space here so you can scroll and test the Sticky Sidebar)</p>
      <p>Scroll down...</p>
      <br><br><br><br><br>
      <p>Keep scrolling... watch the menu on the right!</p>

  </div>

  <div class="toc-sidebar">
      <h4 style="margin-top:0;">On This Page</h4>
      <a href="#situation" class="toc-link">1. The Situation</a>
      <a href="#action" class="toc-link">2. The Action</a>
      <a href="#execution" class="toc-link">3. The Execution</a>
      <a href="#visuals" class="toc-link">4. Visual Proof</a>
  </div>

</div>
