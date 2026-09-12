import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {spawn} from 'node:child_process';
const allRoutes=JSON.parse(await readFile('seo/content-manifest.json','utf8')).map(x=>x.slug);
const requested=process.argv.slice(2);
if(requested.some(x=>!allRoutes.includes(x)))throw new Error('Unknown route');
const routes=requested.length?requested:allRoutes;
await mkdir('seo/audit/lighthouse',{recursive:true});
const results=[];let next=0;
async function worker(){
  while(next<routes.length){
    const route=routes[next++],name=route==='/'?'home':route.replaceAll('/','-').replace(/^-|-$/g,'');
    const path=`seo/audit/lighthouse/${name}.json`;
    const args=['node_modules/lighthouse/cli/index.js','http://127.0.0.1:8765'+route,'--chrome-flags=--headless --disable-gpu','--only-categories=performance,accessibility,seo','--output=json',`--output-path=${path}`,'--quiet'];
    const code=await new Promise(resolve=>{const child=spawn(process.execPath,args,{stdio:['ignore','ignore','pipe']});let error='';child.stderr.on('data',x=>error+=x);child.on('error',e=>resolve(String(e)));child.on('exit',c=>resolve(c===0?0:error.slice(-400)));});
    if(code!==0){results.push({route,error:code});continue;}
    const report=JSON.parse(await readFile(path,'utf8'));
    const scores=Object.fromEntries(Object.entries(report.categories).map(([k,v])=>[k,v.score]));
    const findings=Object.values(report.audits).filter(x=>x.score!==null && x.score<1 && x.scoreDisplayMode!=='informative').map(x=>({id:x.id,title:x.title,score:x.score,displayValue:x.displayValue}));
    results.push({route,scores,labLcp:report.audits['largest-contentful-paint'].numericValue,labCls:report.audits['cumulative-layout-shift'].numericValue,labTbt:report.audits['total-blocking-time'].numericValue,findings});
    console.log(route,JSON.stringify(scores));
  }
}
await Promise.all([worker(),worker()]);
let previous=[];
if(requested.length){try{previous=JSON.parse(await readFile('seo/audit/lighthouse-summary.json','utf8')).results.filter(x=>!requested.includes(x.route));}catch{}}
await writeFile('seo/audit/lighthouse-summary.json',JSON.stringify({method:'Lighthouse simulated mobile, localhost, up to two concurrent audit processes. Not production field data. Preview noindex is intentional.',measuredAt:new Date().toISOString(),results:[...previous,...results]},null,2)+'\n');
console.log('Lighthouse sweep complete:',results.length);
