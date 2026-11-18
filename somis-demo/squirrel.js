// Placeholder squirrel + lip-sync hook. Later: replace markup with SVG/Lottie and feed real viseme cues (e.g. Rhubarb output).
function squirrelHTML(){return '<div class="squirrel" id="sq"><div class="tail"></div><div class="body"></div><div class="head"><div class="ear" style="left:8px"></div><div class="ear" style="right:8px"></div><div class="eye" style="left:20px"></div><div class="eye" style="right:20px"></div><div class="mouth" id="mouth"></div></div></div>'}
window.setMouth=function(open){const m=document.getElementById('mouth');if(m)m.classList.toggle('open',!!open)};
// cues: [[ms,open],...]. Fake cues generated from text until real audio/visemes exist.
window.playCues=function(cues){cues.forEach(([t,o])=>setTimeout(()=>setMouth(o),t))};
window.fakeCues=function(text){const c=[];let t=0;text.split(/\s+/).forEach(w=>{c.push([t,1]);t+=60*Math.min(w.length,6);c.push([t,0]);t+=70});return c};
window.speakTime=function(text){return text.split(/\s+/).length*330+600};
