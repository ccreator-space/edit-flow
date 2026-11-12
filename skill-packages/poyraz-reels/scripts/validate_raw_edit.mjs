import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
export function validateRaw(edl, transcript, captions) {
 const errors=[],need=(ok,msg)=>{if(!ok)errors.push(msg);}, near=(a,b)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<.00001;
 need(edl.sourceSha256===transcript.sourceSha256&&!!edl.sourceSha256,'Source hash mismatch');
 need(edl.fps>0&&Number.isFinite(edl.fps),'Invalid fps');
 need(edl.keeps.length>0&&transcript.words.length>0&&captions.length>0,'Empty raw edit artifacts');
 let cursor=0,sourceEnd=0;
 for(const [i,k] of edl.keeps.entries()){
  need(k.sourceStart>=sourceEnd&&k.sourceEnd>k.sourceStart&&k.sourceEnd<=edl.sourceDuration,`Invalid source range ${i}`);
  need(near(k.start,cursor),`Gap or overlap at keep ${i}`);
  need(near(k.end-k.start,k.sourceEnd-k.sourceStart),`Duration mismatch ${i}`);
  for(const key of ['sourceStart','sourceEnd','start','end'])need(near(k[key]*edl.fps,Math.round(k[key]*edl.fps)),`Not frame aligned: ${i}.${key}`);
  cursor=k.end;sourceEnd=k.sourceEnd;
 }
 need(near(cursor,edl.duration),'EDL duration mismatch');
 let previous=-1;
 for(const [i,w] of transcript.words.entries()){
  const k=edl.keeps.find(k=>w.sourceStart>=k.sourceStart-.00001&&w.sourceEnd<=k.sourceEnd+.00001);
  need(!!k,`Word ${i} crosses a cut`);
  need(w.start>=previous-.00001&&w.end>w.start,`Invalid or overlapping word ${i}`);previous=w.end;
  if(k){need(near(w.start,k.start+w.sourceStart-k.sourceStart)&&near(w.end,k.start+w.sourceEnd-k.sourceStart),`Word ${i} retime mismatch`);}
 }
 const flattened=captions.flatMap(c=>c.words);
 need(flattened.length===transcript.words.length,'Caption word coverage mismatch');
 for(let i=0;i<Math.min(flattened.length,transcript.words.length);i++){
  const a=flattened[i],b=transcript.words[i];need(a.text===b.text&&near(a.start,b.start)&&near(a.end,b.end),`Caption word ${i} mismatch`);
 }
 let capEnd=0;
 for(const [i,c] of captions.entries()){
  need(c.start>=capEnd-.00001&&c.end>c.start&&c.end<=edl.duration+.00001,`Invalid caption ${i}`);
  need(c.words.length>0&&near(c.start,c.words[0].start)&&c.end>=c.words.at(-1).end,`Caption ${i} clips words`);capEnd=c.end;
 }
 return errors;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const files=process.argv.slice(2);if(files.length!==3)throw Error('Usage: node validate_raw_edit.mjs EDL TRANSCRIPT CAPTIONS');
 const errors=validateRaw(...files.map(p=>JSON.parse(fs.readFileSync(p,'utf8'))));console.log(JSON.stringify({ok:!errors.length,errors},null,2));process.exitCode=errors.length?1:0;
}
