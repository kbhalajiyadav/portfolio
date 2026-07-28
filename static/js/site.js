(() => {
  const menu = document.querySelector('.menu-button');
  const nav = document.querySelector('#site-nav');
  if (menu && nav) {
    const close = (focus = false) => {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
      if (focus) menu.focus();
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') === 'true';
      menu.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    nav.addEventListener('click', () => close());
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') close(true);
    });
    document.addEventListener('click', (event) => {
      if (!nav.contains(event.target) && !menu.contains(event.target)) close();
    });
  }

  document.addEventListener('click', async (event) => {
    const button = event.target.closest('.js-copy');
    if (!button) return;
    const text = button.getAttribute('data-copy') || '';
    const original = button.textContent;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const area = document.createElement('textarea');
        area.value = text;
        area.setAttribute('readonly', '');
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.appendChild(area);
        area.select();
        document.execCommand('copy');
        area.remove();
      }
      button.textContent = 'Copied';
    } catch (error) {
      console.error('Clipboard copy failed', error);
      button.textContent = 'Copy failed';
    }
    window.setTimeout(() => { button.textContent = original; }, 1200);
  });

  const navLinks = Array.from(document.querySelectorAll('#site-nav a[href*="#"]'));
  const sections = navLinks.map((link) => {
    const hash = new URL(link.href, window.location.href).hash;
    return hash ? { link, target: document.querySelector(hash) } : null;
  }).filter((item) => item && item.target);
  if (sections.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      const current = entries.filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!current) return;
      navLinks.forEach((link) => link.classList.remove('is-active'));
      const match = sections.find((item) => item.target === current.target);
      if (match) match.link.classList.add('is-active');
    }, { rootMargin: '-20% 0px -65% 0px', threshold: [0.05, 0.25] });
    sections.forEach((item) => observer.observe(item.target));
  }

  const tocLinks = Array.from(document.querySelectorAll('.toc-disclosure a[href^="#"]'));
  const tocTargets = tocLinks.map((link) => {
    const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
    return target ? { link, target } : null;
  }).filter(Boolean);
  if (tocTargets.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      const current = entries.filter((entry) => entry.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (!current) return;
      tocLinks.forEach((link) => link.classList.remove('active-toc-link'));
      const match = tocTargets.find((item) => item.target === current.target);
      if (match) match.link.classList.add('active-toc-link');
    }, { rootMargin: '-18% 0px -72% 0px', threshold: 0.01 });
    tocTargets.forEach((item) => observer.observe(item.target));
  }
})();
