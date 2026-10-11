(() => {
  const dismissedClass = 'is-target-dismissed';

  const decodeHash = () => {
    if (!window.location.hash) return '';
    try {
      return decodeURIComponent(window.location.hash.slice(1));
    } catch (error) {
      return window.location.hash.slice(1);
    }
  };

  const restoreCurrentTarget = () => {
    const id = decodeHash();
    if (!id) return;
    document.getElementById(id)?.classList.remove(dismissedClass);
  };

  restoreCurrentTarget();
  window.addEventListener('hashchange', restoreCurrentTarget);

  document.querySelectorAll('details[id]').forEach((details) => {
    details.addEventListener('toggle', () => {
      if (details.open || !details.id || decodeHash() !== details.id) return;
      details.classList.add(dismissedClass);
      const cleanUrl = `${window.location.pathname}${window.location.search}`;
      window.history.replaceState(window.history.state, '', cleanUrl);
    });
  });
})();
