import {readdir} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
for(const directory of ['public','src','tests']){
  for(const file of await readdir(directory)){
    if(!/\.(js|cjs)$/.test(file))continue;
    const result=spawnSync(process.execPath,['--check',directory+'/'+file],{stdio:'inherit'});
    if(result.status!==0)process.exit(result.status||1);
  }
}
const result=spawnSync('python3',['scripts/validate.py'],{stdio:'inherit'});
process.exit(result.status||0);
