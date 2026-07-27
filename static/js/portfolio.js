(() => {
  const menu = document.querySelector('.menu-button');
  const nav = document.querySelector('#site-nav');
  if (menu && nav) {
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') === 'true';
      menu.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    nav.addEventListener('click', () => {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    });
  }

  const more = document.querySelector('[data-more]');
  const list = document.querySelector('[data-collapsible]');
  if (more && list) {
    more.addEventListener('click', () => {
      const open = more.getAttribute('aria-expanded') === 'true';
      more.setAttribute('aria-expanded', String(!open));
      list.classList.toggle('is-expanded', !open);
      more.firstChild.textContent = open ? 'View all presentations ' : 'Show fewer ';
    });
  }

  const viz = document.querySelector('.method-viz');
  if (viz && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    viz.addEventListener('pointermove', (event) => {
      const box = viz.getBoundingClientRect();
      const x = ((event.clientX - box.left) / box.width - 0.5) * 8;
      const y = ((event.clientY - box.top) / box.height - 0.5) * 8;
      viz.style.setProperty('--rx', `${-y}deg`);
      viz.style.setProperty('--ry', `${x}deg`);
    });
    viz.addEventListener('pointerleave', () => {
      viz.style.setProperty('--rx', '0deg');
      viz.style.setProperty('--ry', '0deg');
    });
  }
})();
