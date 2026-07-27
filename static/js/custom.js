(function () {
  // -----------------------------
  // 1) Copy-to-clipboard buttons
  // -----------------------------
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest(".js-copy");
    if (!btn) return;

    const text = btn.getAttribute("data-copy") || "";
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const area = document.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.opacity = "0";
        document.body.appendChild(area);
        area.select();
        document.execCommand("copy");
        area.remove();
      }
      const old = btn.textContent;
      const oldLabel = btn.getAttribute("aria-label");
      btn.textContent = "Copied!";
      btn.setAttribute("aria-label", "Copied to clipboard");
      setTimeout(() => {
        btn.textContent = old;
        if (oldLabel) btn.setAttribute("aria-label", oldLabel);
        else btn.removeAttribute("aria-label");
      }, 900);
    } catch (err) {
      console.error("Clipboard copy failed:", err);
    }
  });

  // -----------------------------
  // 2) Reading progress bar
  // -----------------------------
  function updateReadingProgress() {
    const bar = document.getElementById("reading-progress");
    if (!bar) return;

    const doc = document.documentElement;
    const scrollTop = doc.scrollTop || document.body.scrollTop;
    const scrollHeight = (doc.scrollHeight || document.body.scrollHeight) - doc.clientHeight;

    if (scrollHeight <= 0) {
      bar.style.width = "0%";
      return;
    }

    const p = Math.min(100, Math.max(0, (scrollTop / scrollHeight) * 100));
    bar.style.width = p.toFixed(2) + "%";
  }

  window.addEventListener("scroll", updateReadingProgress, { passive: true });
  window.addEventListener("resize", updateReadingProgress);
  document.addEventListener("DOMContentLoaded", updateReadingProgress);

  // -----------------------------
  // 3) ToC highlight (active section)
  // -----------------------------
  function setupTocHighlight() {
    const tocContainers = document.querySelectorAll(".toc-sidebar");
    if (!tocContainers.length) return;

    // Collect TOC links
    const tocLinks = Array.from(document.querySelectorAll(".toc-sidebar a[href^='#']"));
    if (!tocLinks.length) return;

    // Map to target headings
    const targets = tocLinks
      .map((a) => {
        const id = decodeURIComponent(a.getAttribute("href").slice(1));
        const el = document.getElementById(id);
        return el ? { link: a, el } : null;
      })
      .filter(Boolean);

    if (!targets.length) return;

    const setActive = (activeLink) => {
      tocLinks.forEach((l) => l.classList.remove("active-toc-link"));
      if (activeLink) activeLink.classList.add("active-toc-link");
    };

    // Use IntersectionObserver if available
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          // Pick the entry closest to top that is intersecting
          const visible = entries
            .filter((e) => e.isIntersecting)
            .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

          if (visible.length) {
            const match = targets.find((t) => t.el === visible[0].target);
            if (match) setActive(match.link);
          }
        },
        {
          root: null,
          // Trigger when heading crosses upper portion of viewport
          rootMargin: "-20% 0px -70% 0px",
          threshold: 0.01,
        }
      );

      targets.forEach((t) => observer.observe(t.el));
    } else {
      // Fallback: scroll-based
      const onScroll = () => {
        const y = window.scrollY + window.innerHeight * 0.2;
        let current = null;

        for (const t of targets) {
          if (t.el.offsetTop <= y) current = t;
        }
        setActive(current ? current.link : null);
      };

      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
  }

  document.addEventListener("DOMContentLoaded", setupTocHighlight);
})();

document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".js-copy-cite");
  if (!btn) return;

  const text = btn.getAttribute("data-cite") || "";
  try {
    await navigator.clipboard.writeText(text);
    const old = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => (btn.textContent = old), 1200);
  } catch (err) {
    alert("Copy failed. Please copy manually.");
  }
});
