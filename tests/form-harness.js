// Local preview server only. Never copied into dist. No real submissions or bookings.
(() => {
  const original=window.fetch.bind(window);
  window.fetch=async (...args)=>{
    if(String(args[0]).startsWith('https://api.web3forms.com/')){
      if('__MODE__'==='network')throw new Error('Simulated network failure');
      const success='__MODE__'==='success';
      return new Response(JSON.stringify({success}),{status:success?200:400,headers:{'Content-Type':'application/json'}});
    }
    return original(...args);
  };
  window.Cal=function(){};
  window.Cal.ns={ds:function(){}};
})();
