(() => {
  const decodeHash = () => {
    if (!window.location.hash) return '';
    try {
      return decodeURIComponent(window.location.hash.slice(1));
    } catch (error) {
      return window.location.hash.slice(1);
    }
  };

  document.querySelectorAll('details[id]').forEach((details) => {
    details.addEventListener('toggle', () => {
      if (details.open || !details.id || decodeHash() !== details.id) return;
      const cleanUrl = `${window.location.pathname}${window.location.search}`;
      window.history.replaceState(window.history.state, '', cleanUrl);
    });
  });
})();
