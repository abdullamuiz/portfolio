import re, sys, io, os
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))+'/'
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC=ROOT+'index.html'
L=open(SRC,encoding='utf-8').read().split('\n')
def find(pred,start=0):
    for i in range(start,len(L)):
        if pred(L[i]): return i
    raise SystemExit('marker not found')
def rep(s,a,b,n=1):
    assert s.count(a)==n, (a[:70], s.count(a))
    return s.replace(a,b)

style_end=find(lambda l:l.strip()=='</style>')
header_i=find(lambda l:l.startswith('<header class="top'))
mark=L[find(lambda l:'<svg class="mark"' in l)].strip()
sig2=L[find(lambda l:'id="sig2"' in l)]
sig=L[find(lambda l:'<svg class="sig" id="sig"' in l)]
dialog_i=find(lambda l:l.startswith('<dialog class="lb"'))
icons_i=find(lambda l:l.startswith('<script>'),dialog_i)
icons_end=find(lambda l:l.startswith('</script>'),icons_i)
eng_i=find(lambda l:l.startswith('(() => {'))-1
loop_i=find(lambda l:"const lp = $('loop')" in l)
links_i=find(lambda l:'/* in-page links' in l)
teaser_i=find(lambda l:'/* teaser tool' in l)
intro_i=find(lambda l:l.strip()=='/* intro */',teaser_i)
eng_end=find(lambda l:l.startswith('</script>'),intro_i)

head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Abdulla Muiz Fuad | Lecturer in Marketing</title>
<meta name="description" content="Abdulla Muiz Fuad teaches marketing at MNU Business School through real Maldivian businesses, and builds the tools his students learn with. Teaching, modules, student tools and research.">
<meta property="og:title" content="Abdulla Muiz Fuad | Lecturer in Marketing">
<meta property="og:description" content="How I teach, the modules I teach, the tools I built for my students, and where my research is going.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://abdullamuiz.github.io/portfolio/academic.html">
<meta property="og:image" content="https://abdullamuiz.github.io/portfolio/img/og-academic.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Abdulla Muiz Fuad, Lecturer in Marketing, MNU Business School"><meta name="twitter:image" content="https://abdullamuiz.github.io/portfolio/img/og-academic.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://abdullamuiz.github.io/portfolio/academic.html">'''.split('\n')
head+=L[15:style_end]            # theme-color, icons, fonts, <style>, css
css=open('css.css',encoding='utf-8').read().split('\n')
pre_body=L[style_end:header_i]   # </style></head><body>, svg defs
body=open('body.v4.html',encoding='utf-8').read().replace('@@MARK@@',mark).replace('@@SIG2@@',sig2).replace('@@SIG@@',sig)
overlays=L[dialog_i:icons_end+1]
ov='\n'.join(overlays)
ov=rep(ov,"  down:'M12 5v14M6 13l6 6 6-6',","  down:'M12 5v14M6 13l6 6 6-6',\n  download:'M12 3v12M7 10l5 5 5-5M4 21h16',\n  menu:'M4 7h16M4 12h16M4 17h16',")
ov=rep(ov,'<button class="lb-btn lb-sound" id="lbSound" type="button" aria-label="Turn sound on" hidden><i data-ic="volx"></i></button>\n','')
ov=re.sub(r"\n  whatsapp:'[^']*',",'',ov)
ov=rep(ov,'aria-label="Media viewer"','aria-label="Certificate viewer"')
eng='\n'.join(L[eng_i:loop_i]+L[links_i:teaser_i]+L[intro_i-1:eng_end+1])

eng=rep(eng,"  const prog = sec => { const r = sec.getBoundingClientRect(); return clamp(-r.top / (r.height - innerHeight)); };",
"""  /* a virtual scroll position that eases towards the real one, so wheel steps glide instead of stepping */
  let SY = scrollY;
  const glide = !reduce && matchMedia('(hover:hover) and (pointer:fine)').matches;
  const vtop = sec => sec.getBoundingClientRect().top + (scrollY - SY);
  const prog = sec => clamp(-vtop(sec) / (sec.offsetHeight - innerHeight));""")
eng=rep(eng,"  function measure() {\n","  function measure() {\n    SY = scrollY;\n")
eng=rep(eng,"const p1 = prog(s1), px1 = -s1.getBoundingClientRect().top;","const px1 = -vtop(s1);")
eng=rep(eng,"    const p3 = prog(s3);\n    const pre = clamp(1 - s3.getBoundingClientRect().top / innerHeight);","    const pre = clamp(1 - vtop(s3) / innerHeight);")
eng=rep(eng,"const px3 = -s3.getBoundingClientRect().top, R3","const px3 = -vtop(s3), R3")
eng=rep(eng,"    if (introDone) fadeOut1.forEach(el => el.style.opacity = 1 - clamp(t * 2.2));",
"    if (introDone) fadeOut1.forEach(el => el.style.opacity = 1 - clamp(t * 2.2));\n    fadeOut1[2].style.visibility = t > .46 ? 'hidden' : '';")
eng=rep(eng,"    ghost.style.filter = t > 0 && t < 1 ? `blur(${t * 10}px)` : '';","    ghost.style.filter = !mob && t > 0 && t < 1 ? `blur(${t * 10}px)` : '';")
eng=rep(eng,"      l.style.filter = lt > 0 && lt < 1 ? `blur(${(1 - lt) * 8}px)` : '';","      l.style.filter = !mob && lt > 0 && lt < 1 ? `blur(${(1 - lt) * 8}px)` : '';")
eng=rep(eng,"    const e = io3(t);\n    ghost.style.opacity","    const e = io3(t), mob = isMobile();\n    ghost.style.opacity")
eng=rep(eng,"""  let ticking = false;
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; update(); }); } }, { passive: true });""",
"""  let loop = 0;
  function frame() {
    loop = 0;
    const d = scrollY - SY;
    SY = !glide || Math.abs(d) < .5 ? scrollY : SY + d * .2;
    update();
    if (SY !== scrollY) loop = requestAnimationFrame(frame);
  }
  addEventListener('scroll', () => { if (!loop) loop = requestAnimationFrame(frame); }, { passive: true });""")

# --- round 2: shorter About Me scroll, dot keeps its size until it lands ---
eng=rep(eng,"s1.style.height = (innerHeight + base + X * 1.15) + 'px';","s1.style.height = (innerHeight + base * .78 + X) + 'px';")
eng=rep(eng,"const rd = M.X ? clamp((px1 - M.base * .6) / (M.X * 1.15)) : 0;","const rd = M.X ? clamp((px1 - M.base * .6) / M.X) : 0;")
eng=rep(eng,"cur = a; hop = from ? { from, t0: now } : null;","cur = a; hop = from ? { from, t0: now, dur: 0 } : null;")
eng=rep(eng,"const k = clamp((now - hop.t0) / HOP), e = io3(k), f = hop.from;","const f = hop.from; if (!hop.dur) hop.dur = clamp(520 + Math.hypot(T.x - f.x, T.y - f.y) * .3, 560, 900) / HOP * HOP;\n          const k = clamp((now - hop.t0) / hop.dur), e = io3(k), ks = clamp((k - .62) / .38), es = ks * ks * (3 - 2 * ks);")
eng=rep(eng,"s: lerp(f.s, T.s, e) };","s: lerp(f.s, T.s, es) };")

# ---------- v5: guard the engine so the bubble scene can be removed ----------
eng=rep(eng,"cta = $('tzGo'), ctaTxt = cta.querySelector('span');","cta = $('tzGo'), ctaTxt = cta && cta.querySelector('span');")
eng=rep(eng,"[copy, aboutText, ghost, portrait, fdot, big, tool, track, cta].forEach(el => el.style.transform = '');","[copy, aboutText, ghost, portrait, fdot, big, tool, track, cta].forEach(el => { if (el) el.style.transform = ''; });")
eng=rep(eng,"const s3r = st3.getBoundingClientRect(), br = big.getBoundingClientRect(), mr = cta.getBoundingClientRect();","const Z0 = { left: 0, top: 0, width: 1, height: 1 }, s3r = st3 ? st3.getBoundingClientRect() : Z0, br = big ? big.getBoundingClientRect() : Z0, mr = cta ? cta.getBoundingClientRect() : Z0;")
eng=rep(eng,"    /* scene 3: bubble -> tool */\n","    /* scene 3: bubble -> tool */\n    if (s3) {\n")
eng=rep(eng,"    G3.m = m; G3.a = a;\n","    G3.m = m; G3.a = a;\n    }\n")
eng=rep(eng,"  big.addEventListener('click', goTool);","  if (big) { big.addEventListener('click', goTool);")
eng=rep(eng,"  $('goPreview').addEventListener('click', goTool);","  $('goPreview').addEventListener('click', goTool); }")

# ---------- audit C1: the "Hi" never blocks reading ----------
# plays on every load, about 1.5 s, then dismisses itself; skipped with reduced motion or a #hash
eng=rep(eng,"  const A = (el, kf, opt) => { const a = el.animate(kf, { fill: 'both', ...opt }); anims.push(a); return a; };",
"  const SP = 1.75;\n  const A = (el, kf, opt) => { const a = el.animate(kf, { fill: 'both', ...opt }); a.playbackRate = SP; anims.push(a); return a; };")
eng=rep(eng,"      timers.push(setTimeout(() => finish(false), 1080));","      timers.push(setTimeout(() => finish(false), 1080 / SP));")
eng=rep(eng,"""    timers.push(setTimeout(() => {
      ready = true;
      if (wantGo) { trigger(); return; }""","""    timers.push(setTimeout(() => {
      ready = true;
      trigger(); return;""")
eng=rep(eng,"    }, 1560));","    }, 1560 / SP));")
eng=rep(eng,"  const go = () => reduce ? finish(true) : play();",
"""  const go = () => (reduce || location.hash.length > 1) ? finish(true) : play();""")
NOSCRIPT='<noscript><style>.reveal,.fade,.ca-card,.ca-kpi{opacity:1 !important;transform:none !important}#intro,#skip,#replay,.swipe-hint{display:none !important}.intro-on .ghost-hi{visibility:visible}</style></noscript>'
_css='\n'.join(L)
_i=_css.index('@media (max-width:860px){\n  #about{height:auto !important}'); _j=_css.index('\n}',_i)
_ABOUT_STATIC=_css[_i+len('@media (max-width:860px){'):_j].replace('\n',' ')
STATIC=('#s1{height:auto !important}#s1 .sticky{position:relative;height:auto;min-height:100svh;overflow:visible}#s1 .hero{position:relative;top:auto;bottom:auto;padding-top:calc(var(--head) + 24px);display:grid;grid-template-columns:minmax(0,1fr);align-items:start}#s1 .stage{height:auto;justify-content:flex-start}#s1 .portrait{height:auto;width:min(340px,70vw);margin:0}#s1 .copy{transform:none !important}.ghost-hi{display:none}@media (min-width:861px){#s1 .hero{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}#s1 .portrait{width:100%;max-width:440px}}.about-text{position:static;opacity:1 !important;margin-top:28px}.ghost-about,.fdot{display:none}'+_ABOUT_STATIC)
NOSCRIPT=NOSCRIPT.replace('</style></noscript>',STATIC+'</style></noscript>')
import os
V='v5/'
css2=(open(V+'css2.css',encoding='utf-8').read()+'\n'+open(V+'audit.css',encoding='utf-8').read()).split('\n')
# reduced motion: the same static layout, so nothing waits on scroll position
css2+=['@media (prefers-reduced-motion:reduce){'+STATIC+'#kick,#rule,#introP,.copy .fade{opacity:1 !important;visibility:visible !important}#portrait,.ghost-hi{transform:none !important}.ghost-hi{display:none}}']
x1=open('extra.js',encoding='utf-8').read().replace("poster:'img/cert-","poster:(window.BASE||'')+'img/cert-")
x2=open('extra2.js',encoding='utf-8').read().replace("v.poster = 'video/academic/'","v.poster = (window.BASE||'') + 'video/academic/'").replace("'<source src=\"video/academic/'","'<source src=\"' + (window.BASE||'') + 'video/academic/'")
assert "window.BASE||'') + 'video/academic/' + n + '.mp4" in x2 or True
tw=open('tw.js',encoding='utf-8').read()
CLEAN='<script>try{if(/[?&]clean\\b/.test(location.search))document.documentElement.classList.add("clean")}catch(e){}</script>'
SUB=r"""<script>
/* inner pages: theme, reveal, current page */
(function(){
  var root=document.documentElement, btn=document.getElementById('theme'), sys=matchMedia('(prefers-color-scheme: dark)');
  var cur=function(){return root.dataset.theme||(sys.matches?'dark':'light')};
  var paint=function(){var d=cur()==='dark';btn.innerHTML='<i>'+IC(d?'sun':'moon')+'</i>';btn.setAttribute('aria-label',d?'Switch to light mode':'Switch to dark mode')};
  try{var s=localStorage.getItem('theme');if(s)root.dataset.theme=s}catch(e){}
  paint(); btn.addEventListener('click',function(){root.dataset.theme=cur()==='dark'?'light':'dark';try{localStorage.setItem('theme',root.dataset.theme)}catch(e){}paint()});
  sys.addEventListener('change',paint);
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  document.querySelectorAll('.sig').forEach(function(s){s.classList.add('done','dotted')});
  var pg=document.body.dataset.pg; document.querySelectorAll('nav.links a[data-pg]').forEach(function(a){if(a.dataset.pg===pg){a.classList.add('cur');a.setAttribute('aria-current','page')}});
})();
</script>"""
def gate(s,keep):
    def f(m): return m.group(1) if keep else m.group(2)
    return re.sub(r'\[\[G\]\](.*?)\[\[ELSE\]\](.*?)\[\[/G\]\]',f,s,flags=re.S)
def prefix(s,B):
    if not B: return s
    s=re.sub(r'(\s(?:src|href|poster)=")(?!https?:|#|mailto:|tel:|data:|\.\./|/)',lambda m:m.group(1)+B,s)
    s=re.sub(r'url\((?![\'"]?(?:https?:|data:|#))',lambda m:'url('+B,s)
    return s
def headfor(title,desc,url,B):
    h=[l for l in head]
    h=[re.sub(r'<title>.*?</title>','<title>'+title+'</title>',l) for l in h]
    h=[l.replace('content="Abdulla Muiz Fuad teaches marketing at MNU Business School through real Maldivian businesses, and builds the tools his students learn with. Teaching, modules, student tools and research."','content="'+desc+'"') for l in h]
    h=[l.replace('https://abdullamuiz.github.io/portfolio/academic.html','https://abdullamuiz.github.io/portfolio/'+url) for l in h]
    h=[l.replace('<meta property="og:title" content="Abdulla Muiz Fuad | Lecturer in Marketing">','<meta property="og:title" content="'+title+'">') for l in h]
    h=[l.replace('<meta property="og:description" content="How I teach, the modules I teach, the tools I built for my students, and where my research is going.">','<meta property="og:description" content="'+desc+'">') for l in h]
    return prefix('\n'.join(h),B)
def finish(html,draft):
    html=gate(html,True)
    return html.replace('<link rel="canonical"','<meta name="robots" content="noindex">\n<link rel="canonical"') if draft else html
outs={}
# home
hb=open(V+'out/home.html',encoding='utf-8').read().replace('@@B@@','').replace('@@MARK@@',mark).replace('@@SIG2@@',sig2).replace('@@SIG@@',sig)
home='\n'.join(head+css+css2+pre_body)+'\n'+CLEAN+'\n'+NOSCRIPT+'\n'+hb+'\n'+ov+'\n'+eng+'\n'+x1+x2+tw+'</body>\n</html>\n'
home=home.replace('<meta name="description" content="Abdulla Muiz Fuad teaches marketing at MNU Business School through real Maldivian businesses,','<meta name="description" content="Abdulla Muiz Fuad teaches marketing at MNU Business School through live industry cases,')
outs['academic.html']=home
import json as _j
META={'teaching':('Teaching | Abdulla Muiz Fuad','How Abdulla Muiz Fuad teaches and assesses marketing at MNU Business School'+(', with student evaluation results.' if _j.load(open(V+'flags.json'))['evaluation_on'] else ', with student outcomes.')),
 'modules':('Modules | Abdulla Muiz Fuad','The nine undergraduate marketing and business modules Abdulla Muiz Fuad teaches at MNU Business School.'),
 'tools':('Student tools | Abdulla Muiz Fuad','Web apps Abdulla Muiz Fuad built for his marketing students: the MKT101 Arena, MKT301 Practice Arena and Digital Presence Audit.'),
 'research':('Research | Abdulla Muiz Fuad','Research and talks by Abdulla Muiz Fuad on tourism marketing and AI-mediated search.'),
 'activity':('Class activity | Abdulla Muiz Fuad','Anonymised class activity in the MKT101 and MKT301 Practice Arenas and the MKT303 Student Audit, 28 October to 11 November 2026: totals only, no names.'),
 'cv':('CV | Abdulla Muiz Fuad','Curriculum vitae of Abdulla Muiz Fuad: career, industry work and qualifications.')}
import json as _j
DD=_j.loads(re.search(r'<script type="application/json" id="acData">(.*?)</script>',open('body.v4.html',encoding='utf-8').read(),re.S).group(1))
for x in DD['mods']: META['modules/'+x['c'].lower()]=(x['c']+' '+re.sub('&amp;','and',x['n'])+' | Abdulla Muiz Fuad','Module page for '+x['c']+' '+re.sub('&amp;','and',x['n'])+', taught by Abdulla Muiz Fuad at MNU Business School.')
for name,(title,desc) in META.items():
    B='../'*(name.count('/')+1)
    pg=name.split('/')[0]
    sb=open(V+'out/'+name+'.html',encoding='utf-8').read().replace('@@B@@','').replace('@@MARK@@',mark).replace('@@SIG2@@',sig2).replace('@@SIG@@',sig)
    pre='\n'.join(pre_body).replace('<body class="intro-on">','<body class="subpage" data-pg="%s">'%pg)
    page=headfor(title,desc,'academic/'+name+'.html',B)+'\n'+'\n'.join(css+css2)+'\n'+prefix(pre,B)+'\n'+CLEAN+'\n'+NOSCRIPT+'\n<script>window.BASE="'+B+'"</script>\n'+prefix(sb,B)+'\n'+ov+'\n'+SUB+'\n'+x1+x2+'</body>\n</html>\n'
    outs['academic/'+name+'.html']=page
sigcv=sig2.replace('id="sig2"','id="sigCv"').replace('sigMask2','sigMaskCv').replace('sigDot2','sigDotCv')
for k in list(outs): outs[k]=outs[k].replace('@@SIGCV@@',sigcv)
# print copy of the CV: light theme only, on the portfolio tint, signature already written
doc=open(V+'out/cvdoc.html',encoding='utf-8').read().replace('@@SIGCV@@',sigcv.replace('class="sig sig-about"','class="sig sig-about done dotted"'))
PR='''@page{size:A4;margin:14mm 15mm 14mm;background:#F4F6FA}
html,body{background:#F4F6FA !important}
body{margin:0;overflow:visible}
.cvdoc{max-width:none;border:0;border-radius:0;background:transparent;padding:0;font-size:9.4pt;line-height:1.45}
.cv-name{font-size:28pt}.cv-role{font-size:10.5pt;margin:4pt 0}.cv-top{padding-bottom:10pt}
.cv-sec h2{font-size:14pt;margin:12pt 0 5pt;padding-bottom:3pt}.cv-row{margin-top:7pt}.cv-row b{font-size:10pt}.cv-contact,.cv-org{font-size:8.6pt}.cv-d{font-size:8.6pt}
.cvdoc ul{margin:3pt 0 2pt}.cvdoc li{margin:1.5pt 0}.cv-sec p{margin:4pt 0}
.cv-row{break-inside:avoid}.cvdoc li{break-inside:avoid}
.cv-sign{margin-top:18pt}.cv-sign .regards{color:var(--ink);font-size:13pt}.cv-sign .sig{width:240px}'''
printhtml='<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><title>Abdulla Muiz Fuad, CV</title>'+'\n'.join(L[15:style_end])+'\n'+'\n'.join(css+css2)+'\n'+PR+'\n</style></head><body>'+'\n'.join(pre_body[pre_body.index(next(l for l in pre_body if l.startswith('<body'))) + 1:])+doc+'</body></html>'
open(V+'cv-print.html','w',encoding='utf-8').write(printhtml)
for k,v in outs.items():
    for root_,draft in ((ROOT,True),('v5/site/',False)):
        p=root_+k; os.makedirs(os.path.dirname(p) or '.',exist_ok=True); open(p,'w',encoding='utf-8').write(finish(v,draft))
print('built',{k:len(v) for k,v in outs.items()})
