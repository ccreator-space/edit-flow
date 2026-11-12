// Copy into a HyperFrames project. Pure composition-time helpers; no clock/state.
export const clamp01 = x => Math.max(0, Math.min(1, x));
export const smoothstep = x => { x=clamp01(x); return x*x*(3-2*x); };
// Exactly GSAP power2.inOut (cubic), shared by speaker and outgoing objects.
export const power2InOut = x => { x=clamp01(x); return x<.5 ? 4*x*x*x : 1-(-2*x+2)**3/2; };

export function splitAmount(time, windows) {
  let amount=0;
  for (const {start,end,transition=.65} of windows) {
    if (!(Number.isFinite(start)&&Number.isFinite(end)&&transition>0&&end-start>=2*transition))
      throw new Error('Invalid split window: allow a complete entrance and return.');
    const enter=power2InOut((time-start)/transition);
    const exit=power2InOut((time-(end-transition))/transition);
    amount=Math.max(amount,enter*(1-exit));
  }
  return amount;
}

export function speakerPose(time, windows, {scale=.8,y=-340,cropBottom=910}={}) {
  const p=splitAmount(time,windows);
  return {scale:1+(scale-1)*p,y:y*p,cropBottom:cropBottom*p};
}

export function objectEnvelope(time,start,end,{enterDuration=.5,exitDuration=.35,exitEase=smoothstep,visibleAtStart=false}={}) {
  if (!(end>start&&enterDuration>0&&exitDuration>0&&end-start>=enterDuration+exitDuration))
    throw new Error('Object lifecycle too short or invalid.');
  if (time<start||time>=end) return 0;
  const enter=visibleAtStart?1:smoothstep((time-start)/enterDuration);
  return enter*(1-exitEase((time-(end-exitDuration))/exitDuration));
}

// For the LAST graphic world in each splitWindow only:
// objectEnvelope(t, worldStart, splitEnd, {exitDuration:.65,exitEase:power2InOut})
// Keep intermediate object entrances/exits and semantic actions unchanged.
