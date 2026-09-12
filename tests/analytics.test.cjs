const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function run(saved){
 const listeners={},scripts=[],els=[],storage=new Map(saved?[['directsite-analytics-consent-v1',saved]]:[]);
 const element=()=>({dataset:{},setAttribute(){},addEventListener(n,f){this[n]=f;},querySelector(){return {focus(){}};}});
 const document={currentScript:{dataset:{measurementId:'G-TEST123'}},title:'Website design',referrer:'https://chatgpt.com/?email=private@example.com',cookie:'',createElement(){const e=element();els.push(e);return e;},head:{append(s){scripts.push(s);}},body:{append(){}}};
 const ctx={document,URL,Date,Set,location:{origin:'https://directsite.com.au',hostname:'directsite.com.au',pathname:'/web-design/',search:'?email=private@example.com'},localStorage:{getItem:k=>storage.get(k),setItem:(k,v)=>storage.set(k,v)},addEventListener:(n,f)=>listeners[n]=f};ctx.window=ctx;
 vm.createContext(ctx);vm.runInContext(fs.readFileSync('public/analytics.js','utf8'),ctx);
 const fire=event=>listeners['directsite:analytics']({detail:event});
 const choose=choice=>els[0].click({target:{closest:()=>({dataset:{choice}})}});
 return {ctx,scripts,fire,choose};
}
const fresh=run();fresh.fire({event:'form_submit'});assert.equal(fresh.scripts.length,0);assert.equal(fresh.ctx.dataLayer.length,0);
fresh.choose('denied');assert.equal(fresh.scripts.length,0);
fresh.choose('granted');assert.equal(fresh.scripts.length,1);fresh.fire({event:'page_view'});
fresh.fire({event:'form_submit',email:'private@example.com',step:'brief',placement:'bad@example.com'});
let commands=fresh.ctx.dataLayer.map(x=>Array.from(x));assert.equal(commands.filter(x=>x[0]==='event'&&x[1]==='page_view').length,1);assert.equal(commands.filter(x=>x[0]==='event'&&x[1]==='generate_lead').length,1);assert(!JSON.stringify(commands).includes('private'));assert(!JSON.stringify(commands).includes('bad@'));
fresh.choose('denied');const count=fresh.ctx.dataLayer.length;fresh.fire({event:'form_submit'});assert.equal(fresh.ctx.dataLayer.length,count);assert.equal(fresh.ctx['ga-disable-G-TEST123'],true);
assert.equal(run('denied').scripts.length,0);const returning=run('granted');assert.equal(returning.scripts.length,1);returning.fire({event:'page_view'});assert.equal(returning.ctx.dataLayer.filter(x=>x[0]==='event'&&x[1]==='page_view').length,1);
console.log('PASS: GA opt-in gate, rejection/revocation, single pageview, accepted-lead mapping and PII stripping.');

const attributed=run();attributed.fire({event:'page_view',referral_source:'chatgpt.com'});attributed.choose('granted');assert.equal(attributed.ctx.dataLayer.find(x=>x[0]==='event'&&x[1]==='page_view')[2].referral_source,'chatgpt.com');
