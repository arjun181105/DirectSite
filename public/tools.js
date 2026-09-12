(() => {
  const box=document.querySelector('[data-tool]'); if(!box) return;
  const controls=box.querySelector('.tool-controls'); const money=n=>new Intl.NumberFormat('en-AU',{style:'currency',currency:'AUD',maximumFractionDigits:0}).format(n);
  function input(id,label,value,min=0,max=100000000,step='any'){
    return `<label for="${id}">${label}<input id="${id}" name="${id}" type="number" value="${value}" min="${min}" max="${max}" step="${step}" required></label>`;
  }
  if(box.dataset.tool==='checklist'){
    const items=['The main heading explains our actual services.','Our real service area and availability are clear.','The phone link calls the correct number.','Urgent calls and planned quotes have appropriate routes.','Every form input has a visible label.','A controlled test enquiry reaches the intended inbox or system.','A failed submission shows an error and allows retry.','Project photos and testimonials are real and permissioned.','Licence and business details are accurate.','Pages work on a narrow screen without horizontal scrolling.','Buttons and dialogs work using the keyboard.','Valuable old URLs redirect to relevant pages after a redesign.','The public pages have correct titles, canonicals and sitemap entries.','A named person is responsible for keeping content current.'];
    controls.innerHTML=items.map((x,i)=>`<label class="growth-check"><input type="checkbox" data-check="${i}">${x}</label>`).join('')+'<output class="growth-result" aria-live="polite"></output><button type="button" id="save-check">Save on this device</button><button type="button" id="reset-check">Reset</button><button type="button" id="print-check">Print checklist</button><p id="save-status" role="status"></p>';
    const checks=[...controls.querySelectorAll('[data-check]')],status=document.getElementById('save-status'),key='directsite-checklist-v1';
    try{const saved=JSON.parse(localStorage.getItem(key));if(Array.isArray(saved))checks.forEach((x,i)=>x.checked=saved[i]===true);}catch{}
    const update=()=>controls.querySelector('output').textContent=`${checks.filter(x=>x.checked).length} of ${items.length} checks completed. This is progress, not a quality score.`;
    controls.addEventListener('change',update);update();
    document.getElementById('save-check').onclick=()=>{try{localStorage.setItem(key,JSON.stringify(checks.map(x=>x.checked)));status.textContent='Saved on this browser only.';}catch{status.textContent='This browser could not save progress. You can print it instead.';}};
    document.getElementById('reset-check').onclick=()=>{checks.forEach(x=>x.checked=false);try{localStorage.removeItem(key);}catch{}update();status.textContent='Checklist reset.';};
    document.getElementById('print-check').onclick=()=>window.print(); return;
  }
  const isRoi=box.dataset.tool==='roi';
  const fields=isRoi?[['visitors','Monthly visitors',1000],['before','Current enquiry rate (%)',2,0,100],['after','Scenario enquiry rate (%)',3,0,100],['close','Enquiry-to-customer rate (%)',25,0,100],['value','Revenue per customer (AUD)',1000],['margin','Gross margin (%)',40,0,100],['cost','Website project cost (AUD)',3000]]:[['pages','Number of pages',5,1,100,1],['base','Base design/build hours',12],['perPage','Hours per additional page',2],['low','Low hourly rate (AUD)',80],['high','High hourly rate (AUD)',140],['ecommerce','Ecommerce setup hours',0],['booking','Booking integration hours',0],['copy','Copywriting hours',0],['seo','SEO setup hours',0],['integrations','Other integration hours',0]];
  controls.innerHTML='<p class="growth-note">Illustrative starting inputs. Replace them with your own assumptions. No data is submitted.</p><form><div class="growth-inputs">'+fields.map(f=>input(...f)).join('')+'</div><button type="submit">Update calculation</button></form><p class="growth-error" role="alert"></p><output class="growth-result" aria-live="polite"></output>';
  const form=controls.querySelector('form'),output=controls.querySelector('output'),error=controls.querySelector('[role=alert]');
  function calculate(){
    try{
      if(!form.checkValidity())throw new Error('Complete every field with a number inside its allowed range.');
      const x=Object.fromEntries(fields.map(([id])=>[id,document.getElementById(id).valueAsNumber]));
      if(isRoi){const r=DirectSiteMath.roi(x);output.textContent=`Enquiries: ${r.before.toFixed(1)} → ${r.after.toFixed(1)} per month. Incremental revenue: ${money(r.revenue)}/month. Incremental contribution: ${money(r.contribution)}/month. Simple payback: ${r.payback===null?'not reached in this scenario':r.payback.toFixed(1)+' months'}.`;}
      else{const r=DirectSiteMath.budget({...x,extras:{ecommerce:x.ecommerce,booking:x.booking,copy:x.copy,seo:x.seo,integrations:x.integrations}});output.textContent=`${r.hours.toFixed(1)} assumed hours × your hourly rates = ${money(r.low)}–${money(r.high)}. Excludes tax and recurring costs. Planning estimate only; not a DirectSite quote.`;}
      error.textContent='';
    }catch(e){error.textContent=e.message;output.textContent='Update the inputs to calculate a scenario.';}
  }
  form.addEventListener('submit',e=>{e.preventDefault();calculate();});form.addEventListener('input',calculate);calculate();
})();
