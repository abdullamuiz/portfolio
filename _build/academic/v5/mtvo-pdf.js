// Regenerate the one-page PDF of academic/mtvo.html (light theme, A4, scaled to fit one page).
// Run from the repo root with the local server on 8791: node _build/academic/v5/mtvo-pdf.js
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({colorScheme:'light'});
await p.goto('http://localhost:8791/academic/mtvo.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:'academic/MTVO_Research_Intent_OnePager_v0.1.pdf',format:'A4',printBackground:true,preferCSSPageSize:true,scale:0.6});await b.close()})();
