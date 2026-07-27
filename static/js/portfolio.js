(() => {
  const menu = document.querySelector('.menu-button');
  const nav = document.querySelector('#site-nav');
  if (menu && nav) {
    const closeMenu = ({ restoreFocus = false } = {}) => {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
      if (restoreFocus) menu.focus();
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') === 'true';
      menu.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    nav.addEventListener('click', () => closeMenu());
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        closeMenu({ restoreFocus: true });
      }
    });
    document.addEventListener('click', (event) => {
      if (!nav.contains(event.target) && !menu.contains(event.target)) closeMenu();
    });
  }

  const more = document.querySelector('[data-more]');
  const list = document.querySelector('[data-collapsible]');
  if (more && list) {
    const status = document.querySelector('[data-presentation-status]');
    const extras = Array.from(list.querySelectorAll('.is-extra'));
    more.addEventListener('click', () => {
      const open = more.getAttribute('aria-expanded') === 'true';
      more.setAttribute('aria-expanded', String(!open));
      list.classList.toggle('is-expanded', !open);
      more.firstChild.textContent = open ? `View all ${list.children.length} records ` : 'Show fewer records ';
      extras.forEach((item) => item.setAttribute('aria-hidden', String(open)));
      if (status) status.textContent = open ? 'Additional presentation records collapsed.' : 'All presentation records are now visible.';
      if (open) more.focus();
    });
    extras.forEach((item) => item.setAttribute('aria-hidden', 'true'));
  }

  const sectionLinks = Array.from(document.querySelectorAll('#site-nav a[href^="#"]'));
  const sections = sectionLinks
    .map((link) => {
      const target = document.querySelector(link.getAttribute('href'));
      return target ? { link, target } : null;
    })
    .filter(Boolean);
  if (sections.length && 'IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      sectionLinks.forEach((link) => link.classList.remove('is-active'));
      const match = sections.find((item) => item.target === visible.target);
      if (match) match.link.classList.add('is-active');
    }, { rootMargin: '-25% 0px -60% 0px', threshold: [0.05, 0.2, 0.5] });
    sections.forEach((item) => sectionObserver.observe(item.target));
  }

  const progressBar = document.querySelector('#reading-progress');
  if (progressBar) {
    const updateProgress = () => {
      const doc = document.documentElement;
      const total = Math.max(doc.scrollHeight - doc.clientHeight, 1);
      const progress = Math.min(Math.max(doc.scrollTop / total, 0), 1);
      progressBar.style.width = `${(progress * 100).toFixed(2)}%`;
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
    updateProgress();
  }

})();
