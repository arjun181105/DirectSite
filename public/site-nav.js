(() => {
  document.documentElement.classList.add('site-nav-ready');

  document.querySelectorAll('.site-nav').forEach((nav) => {
    const toggle = nav.querySelector('.site-menu-toggle');
    const menu = nav.querySelector('.site-menu');
    if (!toggle || !menu) return;

    const setOpen = (open, returnFocus = false) => {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (!open) nav.querySelector('.site-industries')?.removeAttribute('open');
      if (returnFocus) toggle.focus();
    };

    toggle.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
    menu.addEventListener('click', (event) => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && nav.classList.contains('is-open')) setOpen(false, true);
    });
    document.addEventListener('click', (event) => {
      if (!nav.contains(event.target) && nav.classList.contains('is-open')) setOpen(false);
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth > 860 && nav.classList.contains('is-open')) setOpen(false);
    });
  });
})();
