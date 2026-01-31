title: "Dummy Layout Test"
summary: "Testing Wide Layout with Right-Side TOC"
date: 2025-01-31
tags:
Test
Layout
design:
columns: '1'
<div class="portfolio-layout">
  <!-- Main Content Area -->
  <main class="main-content">
    <h1>Project Title: Mechanics-Consistent Adhesion</h1>
Copy
<div class="status-pill active">ACTIVE RESEARCH</div>

<h2 id="situation">1. The Situation</h2>
<p>Current industry standards assume higher average peel force equals better adhesion. I identified this fails for soft wearables where 90% of measured force is fabric stretching, not glue holding.</p>

<h2 id="action">2. The Action</h2>
<p>Applied First Principles thinking to distinguish True Adhesion from Artifacts. Introduced Peel Stability Index (PSI) to quantify consistency.</p>

<h2 id="execution">3. The Execution</h2>
<p>Built custom Python pipeline using pandas and scipy to automate analysis, reducing processing time by 40%.</p>

<h2 id="result">4. The Result</h2>
<p>Framework prevents "False Positive" selections and ensures mechanically stable adhesives for medical devices.</p>
  </main>
  <!-- Floating TOC on Right -->
  <aside class="toc-sidebar">
    <nav class="toc-nav">
      <h4>On This Page</h4>
      <ul>
        <li><a href="#situation" class="toc-link">1. The Situation</a></li>
        <li><a href="#action" class="toc-link">2. The Action</a></li>
        <li><a href="#execution" class="toc-link">3. The Execution</a></li>
        <li><a href="#result" class="toc-link">4. The Result</a></li>
      </ul>
    </nav>
  </aside>
</div>
<style>
/* ===== LAYOUT STRUCTURE ===== */
.portfolio-layout {
  display: flex;
  gap: 3rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* ===== MAIN CONTENT (Left, ~65%) ===== */
.main-content {
  flex: 1;
  min-width: 0;
}

.main-content h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 1rem;
  text-align: left;
}

.main-content h2 {
  font-size: 1.4rem;
  font-weight: 600;
  color: #16213e;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e8f5e9;
}

.main-content p {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #333;
  margin-bottom: 1.2rem;
}

/* ===== STATUS PILL ===== */
.status-pill {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
}

.status-pill.active {
  background-color: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #2e7d32;
}

/* ===== TOC SIDEBAR (Right, ~250px) ===== */
.toc-sidebar {
  width: 250px;
  flex-shrink: 0;
  position: sticky;
  top: 100px;
  align-self: flex-start;
  height: fit-content;
}

.toc-nav {
  background: #fafafa;
  border-left: 3px solid #0d47a1;
  padding: 1.5rem;
}

.toc-nav h4 {
  font-size: 0.85rem;
  font-weight: 700;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 1rem;
}

.toc-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-nav li {
  margin-bottom: 0.6rem;
}

.toc-link {
  display: block;
  font-size: 0.9rem;
  color: #555;
  text-decoration: none;
  padding: 0.4rem 0;
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
}

.toc-link:hover {
  color: #0d47a1;
  border-bottom-color: #0d47a1;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {
  .portfolio-layout {
    flex-direction: column;
    gap: 2rem;
    padding: 1rem;
  }
  
  .toc-sidebar {
    width: 100%;
    position: static;
    order: -1;
  }
  
  .toc-nav {
    border-left: none;
    border-bottom: 3px solid #0d47a1;
  }
}
</style>
