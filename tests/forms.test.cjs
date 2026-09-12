const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const script=fs.readFileSync('dist/demo-form.js','utf8');
async function scenario(mode){
  const status={textContent:''},button={disabled:false},events=[];
  const form={reportValidity:()=>mode!=='invalid',querySelector:s=>s.includes('button')?button:status};
  const card={classList:{toggle(){},remove(){}},scrollTop:0};
  const modal={querySelector:()=>card,querySelectorAll:()=>[],addEventListener(){},classList:{add(){},remove(){}}};
  const nodes={'modal':modal,'modal-x':{addEventListener(){}},'form-new':form,'form-re':form};
  const document={getElementById:id=>nodes[id]||{value:'test value'},addEventListener(){},querySelectorAll:()=>[],body:{style:{},classList:{add(){},remove(){}}}};
  let requests=0;
  const window={dsTrack:(name)=>events.push(name)};
  const context={window,document,AbortSignal,setTimeout,clearTimeout,setInterval,clearInterval,fetch:async()=>{requests++;if(mode==='network')throw Error('offline');return {ok:mode!=='http-failure',json:async()=>{if(mode==='bad-json')throw Error('bad JSON');return {success:mode==='success'};}};}};
  // The object above is kept explicit to ensure tests cannot reach a real network.
  vm.createContext(context);vm.runInContext(script,context);vm.runInContext('initCal=function(){};',context);
  await window.__step2('redesign');
  if(mode==='success'){assert(events.includes('form_submit'));assert(events.includes('demo_requested'));assert.equal(status.textContent,'');}
  else{assert(!events.includes('form_submit'));assert(!events.includes('demo_requested'));if(mode!=='invalid')assert.match(status.textContent,/could not be confirmed/);}
  assert.equal(button.disabled,false);assert.equal(requests,mode==='invalid'?0:1);
}
(async()=>{for(const mode of ['success','http-failure','api-failure','network','bad-json','invalid'])await scenario(mode);console.log('PASS: real form code handles accepted, rejected, invalid and failed requests.');})().catch(e=>{console.error(e);process.exitCode=1;});
