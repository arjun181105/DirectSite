(() => {
  const modal = document.getElementById('modal');
  if (!modal) return;
  const card = modal.querySelector('.modal');
  let previous = null, started = false;
  const focusable = () => [...modal.querySelectorAll('input,textarea,select,button,a[href],[tabindex="0"]')].filter(x => !x.disabled && x.getClientRects().length);
  card.setAttribute('role','dialog'); card.setAttribute('aria-modal','true'); card.setAttribute('aria-label','Request a DirectSite website or consultation'); card.tabIndex = -1;
  modal.setAttribute('aria-hidden','true');
  const siblings = [...document.body.children].filter(x => x !== modal && !['SCRIPT','STYLE','LINK'].includes(x.tagName));
  const previousInert = new Map();
  const observer = new MutationObserver(() => {
    const open = modal.classList.contains('on');
    modal.setAttribute('aria-hidden', String(!open));
    if (open && !previous) {
      previous = document.activeElement; started = false;
      siblings.forEach(x => {previousInert.set(x,x.inert); x.inert=true;});
      (focusable().find(x => x.tagName === 'INPUT') || card).focus();
    } else if (!open && previous) {
      siblings.forEach(x => {x.inert=previousInert.get(x) || false;});
      previous.focus(); previous=null;
    }
  });
  observer.observe(modal,{attributes:true,attributeFilter:['class']});
  modal.addEventListener('input', () => {if(!started){started=true;window.dsTrack?.('form_start');}});
  modal.addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    const list=focusable(), first=list[0], last=list[list.length-1];
    if (!first) {e.preventDefault();card.focus();return;}
    if (e.shiftKey && (document.activeElement===first || document.activeElement===card)) {e.preventDefault();last.focus();}
    else if (!e.shiftKey && document.activeElement===last) {e.preventDefault();first.focus();}
  });
  const stepObserver=new MutationObserver(() => {
    if(!modal.classList.contains('on')) return;
    const active=modal.querySelector('.mstep.active');
    if(active && !active.contains(document.activeElement)) (active.querySelector('input,button,select') || card).focus();
  });
  modal.querySelectorAll('.mstep').forEach(x => stepObserver.observe(x,{attributes:true,attributeFilter:['class']}));
  if(location.hash === '#book') document.querySelector('[data-book]')?.click();
  window.addEventListener('hashchange', () => {if(location.hash === '#book' && !modal.classList.contains('on')) document.querySelector('[data-book]')?.click();});
})();
