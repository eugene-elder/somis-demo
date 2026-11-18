const p=require('/tmp/r/node_modules/puppeteer-core');(async()=>{
const b=await p.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const pg=await b.newPage();
await pg.setViewport({width:1280,height:720});await pg.goto(`http://localhost:8765/index.html?render&${Date.now()}`);
await pg.waitForFunction('window.ready');require('fs').mkdirSync('/tmp/frames',{recursive:true});
for(let i=0;i<10*24;i++){await pg.evaluate(t=>seek(t),i/24);await pg.screenshot({path:`/tmp/frames/f${String(i).padStart(4,'0')}.png`});}
await b.close();})();
