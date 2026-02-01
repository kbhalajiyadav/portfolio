document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".js-copy");
  if (!btn) return;

  const text = btn.getAttribute("data-copy") || "";
  try {
    await navigator.clipboard.writeText(text);
    const old = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => (btn.textContent = old), 900);
  } catch (err) {
    console.error("Clipboard copy failed:", err);
  }
});
