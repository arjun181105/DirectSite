(() => {
  const allowed = new Set(['page_view','cta_click','form_start','form_step_complete','form_submit','demo_requested','call_booking','booking_link_click','form_error']);
  const params = new URLSearchParams(location.search);
  let source = params.get('utm_source') === 'chatgpt.com' ? 'chatgpt.com' : 'other';
  try { if (new URL(document.referrer).hostname === 'chatgpt.com') source = 'chatgpt.com'; } catch {}
  window.dsTrack = (event, details = {}) => {
    if (!allowed.has(event)) return;
    const payload = {event, page_path: location.pathname, referral_source: source};
    for (const key of ['step','placement','project_type']) {
      if (typeof details[key] === 'string' && /^[a-z0-9_-]{1,40}$/.test(details[key])) payload[key] = details[key];
    }
    // Deliberately exclude URL query strings, names, email, phone, business and form contents.
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
    window.dispatchEvent(new CustomEvent('directsite:analytics', {detail: payload}));
  };
  dsTrack('page_view');
  document.addEventListener('click', e => {
    const el = e.target.closest('[data-book], [data-cta], a[href*="cal.com/"]');
    if (el) dsTrack(el.href?.includes('cal.com/') && !el.hasAttribute('data-book') ? 'booking_link_click' : 'cta_click', {placement: el.dataset.placement || 'page'});
  });
})();
