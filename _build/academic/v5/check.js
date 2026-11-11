const { chromium } = require('playwright');
const pages=['academic.html','academic/teaching.html','academic/modules.html','academic/tools.html','academic/research.html','academic/cv.html','academic/activity.html','academic/modules/mkt101.html','academic/modules/mkt215.html'];
(async()=>{
  const b=await chromium.launch();
  for (const vp of [{w:1440,h:900,n:'d'},{w:390,h:844,n:'m'}]) {
    const ctx=await b.newContext({viewport:{width:vp.w,height:vp.h}});
    for (const p of pages){
      const pg=await ctx.newPage(); const errs=[]; const bad=[];
      pg.on('pageerror',e=>errs.push(e.message)); pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
      pg.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url())});
      await pg.goto('http://localhost:8791/'+p,{waitUntil:'networkidle'});
      if(p==='academic.html'){ await pg.keyboard.press('Space'); await pg.waitForTimeout(1500);} 
      // scroll through to trigger reveals
      const H=await pg.evaluate(()=>document.documentElement.scrollHeight);
      for(let y=0;y<H;y+=600){await pg.evaluate(y=>scrollTo(0,y),y);await pg.waitForTimeout(60);} 
      await pg.waitForTimeout(500);
      const ow=await pg.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
      console.log(vp.n,p,'H',H,'overflowX',ow,'errs',JSON.stringify(errs),'bad',JSON.stringify(bad));
      if(p!=='academic.html'){ await pg.evaluate(()=>scrollTo(0,0)); await pg.waitForTimeout(300); await pg.screenshot({path:'v5/shot-'+vp.n+'-'+p.replace(/\//g,'_')+'.png',fullPage:true}); }
      await pg.close();
    }
    await ctx.close();
  }
  await b.close();
})();
