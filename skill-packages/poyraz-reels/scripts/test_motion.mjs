import assert from 'node:assert/strict';
import {power2InOut,splitAmount,speakerPose,objectEnvelope} from '../assets/motion.mjs';

const windows=[{start:12,end:40,transition:.65},{start:48,end:58,transition:.65}];
assert.deepEqual(speakerPose(0,windows),{scale:1,y:-0,cropBottom:0});
assert.deepEqual(speakerPose(20,windows),{scale:.8,y:-340,cropBottom:910});
for(const w of windows){
  let previous=1;
  for(let i=0;i<=1000;i++){
    const t=w.end-w.transition+w.transition*i/1000;
    const p=splitAmount(t,windows);
    const object=objectEnvelope(t,w.start,w.end,{exitDuration:w.transition,exitEase:power2InOut});
    assert(Math.abs(p-object)<1e-12,'Speaker and graphics diverged');
    assert(p<=previous+1e-12,'Reverse step in exit');previous=p;
  }
  assert.equal(splitAmount(w.end,windows),0);
}
const seekOrder=[57.7,0,39.7,20,58,12.3,39.7];
const baseline=new Map([...new Set(seekOrder)].sort((a,b)=>a-b).map(t=>[t,speakerPose(t,windows)]));
for(const t of seekOrder) assert.deepEqual(speakerPose(t,windows),baseline.get(t),'Nonchronological seek changed pose');
assert.throws(()=>splitAmount(0,[{start:1,end:1.2,transition:.65}]));
assert.throws(()=>objectEnvelope(0,0,.2));
// Reproduce the old delayed exit: it must NOT match the corrected speaker path.
assert(Math.abs(splitAmount(39.8,windows)-objectEnvelope(39.8,12,40))>.1);
console.log('PASS: 2,002 synchronized exit samples; endpoints, reverse seeks and regression negative control.');
