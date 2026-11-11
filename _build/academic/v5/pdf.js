const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const pg=await b.newPage();
await pg.emulateMedia({colorScheme:'light'});
await pg.goto('http://localhost:8791/_cvprint.html',{waitUntil:'networkidle'});
await pg.evaluate(()=>document.fonts.ready);
await pg.pdf({path:require('path').resolve(__dirname,'../../../academic/Muiz_Fuad_CV.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true});
await b.close();})();
