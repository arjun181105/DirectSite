(function(root){
  function nonnegative(value){if(!Number.isFinite(value)||value<0)throw new Error('Use a finite number of zero or more.');return value;}
  function rate(value){nonnegative(value);if(value>100)throw new Error('Percentages must be between 0 and 100.');return value/100;}
  function roi(x){
    const visits=nonnegative(x.visitors), before=visits*rate(x.before), after=visits*rate(x.after);
    const revenue=(after-before)*rate(x.close)*nonnegative(x.value);
    const contribution=revenue*rate(x.margin), cost=nonnegative(x.cost);
    return {before,after,revenue,contribution,payback:contribution>0?cost/contribution:null};
  }
  function budget(x){
    if(!Number.isInteger(x.pages)||x.pages<1||x.pages>100)throw new Error('Choose 1–100 whole pages.');
    if(x.low>x.high)throw new Error('The low hourly rate cannot exceed the high rate.');
    const hours=nonnegative(x.base)+(x.pages-1)*nonnegative(x.perPage)+Object.values(x.extras).reduce((a,b)=>a+nonnegative(b),0);
    return {hours,low:hours*nonnegative(x.low),high:hours*nonnegative(x.high)};
  }
  const api={roi,budget}; if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.DirectSiteMath=api;
})(typeof window!=='undefined'?window:globalThis);
