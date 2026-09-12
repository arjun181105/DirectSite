var servicesSubmitting=false;
window.__submit = async function() {
  const form=document.getElementById('bookform');
  if(servicesSubmitting || !form.reportValidity()) return;
  servicesSubmitting=true;
  const button=form.querySelector('button[type=submit]');
  const status=form.querySelector('.growth-submit-status');
  const fields=form.querySelectorAll('input,select');
  button.disabled=true; status.textContent='Sending your enquiry…';
  try {
    const response=await fetch('https://api.web3forms.com/submit',{
      method:'POST',signal:AbortSignal.timeout(15000),headers:{'Content-Type':'application/json','Accept':'application/json'},
      body:JSON.stringify({access_key:'__WEB3FORMS_KEY__',subject:'DirectSite service enquiry',from_name:'DirectSite Website',name:fields[0].value.trim(),business:fields[1].value.trim(),contact:fields[2].value.trim(),service:fields[3].value,message:'Service requested: '+fields[3].value+'\nContact: '+fields[2].value.trim()})
    });
    const result=await response.json();
    if(!response.ok || result.success !== true) throw new Error('Not accepted');
    window.dsTrack?.('form_submit',{project_type:'service'});
    formDiv.style.display='none'; doneDiv.style.display='block';
    doneDiv.querySelector('a').focus();
  } catch(error) {
    status.textContent='Your enquiry could not be confirmed. Please retry or use the direct booking link.';
    window.dsTrack?.('form_error');
  } finally {servicesSubmitting=false;button.disabled=false;}
};
