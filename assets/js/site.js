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

  const responsiveToc = document.querySelector('.toc-disclosure[data-responsive-toc]');
  if (responsiveToc) {
    const desktopToc = window.matchMedia('(min-width: 981px)');
    responsiveToc.open = desktopToc.matches;
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

  const privacyBanner = document.querySelector('[data-privacy-banner]');
  if (privacyBanner) {
    const root = document.documentElement;
    const consentKey = 'bhalaji.analyticsConsent.v1';
    const clarityProject = 'xuo3lvzchr';
    const allowButton = privacyBanner.querySelector('[data-consent-allow]');
    const declineButton = privacyBanner.querySelector('[data-consent-decline]');
    const openButtons = Array.from(document.querySelectorAll('[data-open-privacy]'));

    const queueClarity = () => {
      if (typeof window.clarity !== 'function') {
        window.clarity = function clarityQueue() {
          (window.clarity.q = window.clarity.q || []).push(arguments);
        };
      }
    };

    const grantAnalytics = () => {
      queueClarity();
      window.clarity('consentv2', {
        ad_Storage: 'denied',
        analytics_Storage: 'granted'
      });
      if (!document.querySelector('script[data-clarity-project]')) {
        const script = document.createElement('script');
        script.async = true;
        script.dataset.clarityProject = clarityProject;
        script.src = `https://www.clarity.ms/tag/${clarityProject}?ref=bwt`;
        document.head.appendChild(script);
      }
    };

    const denyAnalytics = () => {
      if (typeof window.clarity !== 'function') return;
      window.clarity('consentv2', {
        ad_Storage: 'denied',
        analytics_Storage: 'denied'
      });
      window.clarity('consent', false);
    };

    const readConsent = () => {
      try {
        const choice = window.localStorage.getItem(consentKey);
        return choice === 'granted' || choice === 'denied' ? choice : null;
      } catch (error) {
        return null;
      }
    };

    const setConsentState = (choice) => {
      root.dataset.analyticsConsent = choice || 'unset';
    };

    const setBannerVisible = (visible, reopened = false) => {
      privacyBanner.hidden = !visible;
      privacyBanner.classList.toggle('is-open', Boolean(visible && reopened));
    };

    const saveConsent = (choice) => {
      try {
        window.localStorage.setItem(consentKey, choice);
      } catch (error) {
        console.warn('Privacy preference could not be stored', error);
      }
      setConsentState(choice);
      if (choice === 'granted') grantAnalytics();
      else denyAnalytics();
      setBannerVisible(false);
    };

    const currentChoice = readConsent();
    setConsentState(currentChoice);
    if (currentChoice === 'granted') grantAnalytics();
    setBannerVisible(currentChoice === null);

    if (allowButton) allowButton.addEventListener('click', () => saveConsent('granted'));
    if (declineButton) declineButton.addEventListener('click', () => saveConsent('denied'));
    openButtons.forEach((button) => {
      button.addEventListener('click', () => {
        setBannerVisible(true, true);
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        privacyBanner.scrollIntoView({ block: 'start', behavior: reducedMotion ? 'auto' : 'smooth' });
        window.requestAnimationFrame(() => {
          if (allowButton) allowButton.focus({ preventScroll: true });
        });
      });
    });
  }
})();