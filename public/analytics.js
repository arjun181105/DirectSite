(() => {
  const id = document.currentScript?.dataset.measurementId;
  if (!/^G-[A-Z0-9]+$/.test(id || '')) return;
  const key = 'directsite-analytics-consent-v1';
  let consent = null, loaded = false, pageSent = false;
  try { consent = localStorage.getItem(key); } catch {}
  window.dataLayer = window.dataLayer || [];
  const gtag = function () { window.dataLayer.push(arguments); };
  const allowed = new Set(['page_view','cta_click','form_start','form_step_complete','form_submit','demo_requested','call_booking','booking_link_click','form_error']);
  const safePage = location.origin + location.pathname;
  let referrer = '';
  try { referrer = new URL(document.referrer).origin + '/'; } catch {}
  function send(payload) {
    if (consent !== 'granted' || !loaded || !allowed.has(payload?.event)) return;
    if (payload.event === 'page_view') {
      if (pageSent) return;
      pageSent = true;
    }
    const details = {send_to:id,page_location:safePage,page_referrer:referrer,page_title:document.title};
    for (const name of ['step','placement','project_type']) {
      if (typeof payload[name] === 'string' && /^[a-z0-9_-]{1,40}$/.test(payload[name])) details[name] = payload[name];
    }
    details.referral_source = payload.referral_source === 'chatgpt.com' ? 'chatgpt.com' : 'other';
    gtag('event', payload.event, details);
    if (payload.event === 'form_submit') gtag('event', 'generate_lead', details);
  }
  function start() {
    if (loaded) return;
    loaded = true;
    window['ga-disable-' + id] = false;
    gtag('consent','default',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
    gtag('js',new Date());
    gtag('config',id,{send_page_view:false,page_location:safePage,page_referrer:referrer,allow_google_signals:false,allow_ad_personalization_signals:false,cookie_expires:60*60*24*180,cookie_update:false});
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.append(script);
  }
  window.addEventListener('directsite:analytics', e => send(e.detail));
  const panel = document.createElement('section');
  panel.className = 'ds-consent';
  panel.setAttribute('aria-label','Analytics preferences');
  panel.innerHTML = '<p><strong>Help us improve DirectSite?</strong> Allow Google Analytics cookies to measure page visits and enquiries. We do not send your form details. Your choice is saved on this browser.</p><div><button type="button" data-choice="granted">Allow analytics</button><button type="button" data-choice="denied">No thanks</button></div>';
  const preferences = document.createElement('button');
  preferences.type = 'button';
  preferences.className = 'ds-consent-preferences';
  preferences.textContent = 'Analytics preferences';
  preferences.addEventListener('click', () => { panel.hidden = false; panel.querySelector('button').focus(); });
  panel.addEventListener('click', e => {
    const choice = e.target.closest('[data-choice]')?.dataset.choice;
    if (!choice) return;
    consent = choice;
    try { localStorage.setItem(key,choice); } catch {}
    panel.hidden = true;
    if (choice === 'granted') {
      window['ga-disable-' + id] = false;
      if (loaded) gtag('consent','update',{analytics_storage:'granted'});
      start();
      send({event:'page_view'});
    } else {
      window['ga-disable-' + id] = true;
      if (loaded) gtag('consent','update',{analytics_storage:'denied'});
      for (const cookie of document.cookie.split(';')) {
        const name = cookie.trim().split('=')[0];
        if (!/^_ga(?:_|$)/.test(name)) continue;
        for (const domain of ['',location.hostname,'.'+location.hostname]) {
          document.cookie = name+'=; Max-Age=0; Path=/'+(domain?'; Domain='+domain:'');
        }
      }
    }
  });
  document.body.append(panel,preferences);
  panel.hidden = consent === 'granted' || consent === 'denied';
  if (consent === 'granted') start();
})();
