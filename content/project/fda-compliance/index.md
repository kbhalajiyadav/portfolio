---
title: "Dummy Layout Test"
summary: "Testing Wide Layout & Left Alignment"
date: 2025-01-31
tags:
  - Test
  - Layout

# This prevents the default narrow column layout
design:
  columns: '1'
---

## 1. This Should Be Left Aligned
This text should span the entire width of your screen (or close to it), rather than being stuck in a narrow column in the middle. 

## 2. The Header Test
Look at the Title "Dummy Layout Test" at the very top. Is it aligned to the far left, or is it still centered?

## 3. Visual Width Check
If this line breaks early, we are still in "narrow mode." If it stretches all the way to the right side of your monitor, we have successfully unlocked "Wide Mode."

<style>
  /* 1. Force the container to be wide */
  .container, .article-container {
      max-width: 95% !important; 
      margin-left: 20px !important;
      margin-right: auto !important;
      padding-left: 0 !important;
  }

  /* 2. Force text alignment to the left */
  h1, h2, h3, p, .page-title, .article-title {
      text-align: left !important;
  }
  
  /* 3. Ensure the main header (Avatar + Title area) aligns left */
  .page-header {
      text-align: left !important;
      align-items: flex-start !important;
  }
</style>
