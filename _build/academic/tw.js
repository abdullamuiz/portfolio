<script>
/* teaching wheel (inline) */
(function(){if(!document.getElementById('twWheel'))return;
const COURSES=['MKT101','MKT301','MKT303','MKT309'];
const ALL=COURSES;
const items=[
 {k:'Industry first',t:'Start from the industry floor',
  b:'A concept is only useful once you have seen the decision it supports.',
  how:'I came to the classroom from resort marketing, SME incubation and event sales, so lectures begin with a real marketing decision and work back to the theory that explains it.',
  proof:['Marketing Manager at Reethi Beach Resort: European and Asian source markets, influencers, SEO, website redesign','Manager of SME HUB: incubation programme for 23 small businesses','Promoter to Head of Marketing and Sales, MATTA Fair, Kuala Lumpur (2014–2018)'],
  c:ALL},
 {k:'Real cases',t:'Cases students can walk into',
  b:'A case should feel like a business you could visit, not a page you must read.',
  how:'I write my own teaching cases around local businesses and publish them as interactive pages students open on their phones. MKT303 runs on one continuous case instead of unrelated examples.',
  proof:['ICETO Gelato: interactive teaching case for MKT301, with more cases in the same format on the way','Kandu Stay, a 12-room local-island guesthouse, is the running case through MKT303'],
  c:['MKT301','MKT303']},
 {k:'Build as you learn',t:'Every week adds a piece of the real thing',
  b:'Students learn marketing fastest when each lecture produces something they can use.',
  how:'Weekly tutorials are tied to the lecture chapter and to the group assignment, so the marketing plan for a Maldivian brand grows a section at a time instead of arriving as a last-minute scramble.',
  proof:['MKT101 tutorials map each chapter (e.g. marketing research, buyer behaviour) to a part of the group marketing plan','A marketing-plan skeleton gives groups a clear structure to build into'],
  c:['MKT101']},
 {k:'Plain words',t:'Clear English, rigorous thinking',
  b:'Difficulty should come from the ideas, never from the wording.',
  how:'Many of my students study in their second language. I write lectures and exam questions in simple, direct English and ask for what I want to see: “give an example”, “describe”, “explain why”.',
  proof:['Exam questions reviewed for plain wording and avoiding terms that imply a diagram or model is required','Technical trade detail kept out of questions that test marketing understanding'],
  c:['MKT101','MKT301']},
 {k:'Fair by design',t:'Assessment I can defend and improve',
  b:'An exam should measure what was taught, and I change it when the evidence says it isn’t.',
  how:'Papers follow a table of specifications so every question maps to a learning outcome and a thinking level. When I saw students running out of time, I restructured the paper instead of blaming the students.',
  proof:['MKT301 Final and Resit built from one specification, with different cases and limited overlap','Section B changed to “answer any 5 of 6” focused on Understand, Apply and Analyse'],
  c:['MKT101','MKT301']},
 {k:'Practice first',t:'Practise before the pressure',
  b:'Students should meet the exam format long before the exam does.',
  how:'I am building a study portal where students practise a randomised set of questions, see how to build a strong answer, then compare with a model answer, while essays are still practised on paper under real conditions.',
  proof:['MKT101 portal: large MCQ bank, 30 random questions per practice session','Guidance and model answers for the longer questions, designed to sit beside a notepad on a phone'],
  c:['MKT101']},
 {k:'Theory with Trend',t:'Pair every theory with a trend',
  b:'A framework earns its place when students can see it working in today’s market.',
  how:'I teach the established models first, then test them against what is changing right now, such as AI search and Generative Engine Optimisation in MKT303, so students learn ideas that hold up as platforms shift.',
  proof:['Peer-reviewed paper in Tourism and Hospitality Research (2021), 36+ citations','Journal article on guesthouse e-marketing, Common Ground (2017)','MKT303 deck suite rebuilt around current texts, with GEO connected to the curriculum'],
  c:['MKT303']},
 {k:'Build Confidence',t:'Leave students able, and willing',
  b:'Confidence comes from doing the work successfully before it counts for marks.',
  how:'Small wins come first: plain explanations, weekly builds toward the group plan, and practice papers with model answers. Students walk into assessments having already done the work once, and they can see a real path into the Maldivian industry.',
  proof:['Weekly tutorials turn the assignment into steady progress instead of one big task','Practice portal lets students attempt questions, then compare with model answers before the real exam','Teaching is a step I always wanted to take, driven by a passion for passing knowledge to the next generation'],
  c:ALL}
];

const svg=document.getElementById('twWheel'),NS='http://www.w3.org/2000/svg';
const cx=300,cy=300,R=288,r=122,N=items.length,step=2*Math.PI/N,gap=.012;
const pt=(a,rad)=>[cx+rad*Math.cos(a),cy+rad*Math.sin(a)];
let sel=0,filter=null;
const segs=[];
items.forEach((it,i)=>{
  const a0=-Math.PI/2-step/2+i*step+gap, a1=a0+step-2*gap, mid=(a0+a1)/2;
  const [x0,y0]=pt(a0,R),[x1,y1]=pt(a1,R),[x2,y2]=pt(a1,r),[x3,y3]=pt(a0,r);
  const d=`M${x0} ${y0}A${R} ${R} 0 0 1 ${x1} ${y1}L${x2} ${y2}A${r} ${r} 0 0 0 ${x3} ${y3}Z`;
  const g=document.createElementNS(NS,'g');
  g.setAttribute('class','tw-seg tw-in');g.setAttribute('role','button');g.setAttribute('tabindex','0');
  g.setAttribute('aria-label',`${i+1}. ${it.t}`);
  g.style.setProperty('--i',i);
  g.style.setProperty('--tx',(Math.cos(mid)*7).toFixed(2)+'px');
  g.style.setProperty('--ty',(Math.sin(mid)*7).toFixed(2)+'px');
  const [lx,ly]=pt(mid,(R+r)/2+2);
  g.innerHTML=`<path d="${d}"/><text class="tw-num" x="${lx}" y="${ly-14}" text-anchor="middle">0${i+1}</text><text class="tw-t" x="${lx}" y="${ly+8}" text-anchor="middle">${wrap(it.k)}</text>`;
  g.addEventListener('click',()=>select(i));
  g.addEventListener('keydown',e=>{
    if(e.key==='Enter'||e.key===' '){e.preventDefault();select(i)}
    if(e.key==='ArrowRight'||e.key==='ArrowDown'){e.preventDefault();select(i+1,true)}
    if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();select(i-1,true)}
  });
  svg.appendChild(g);segs.push(g);
});
function wrap(s){
  const w=s.split(' ');
  if(w.length<2||s.length<10)return s;
  const m=Math.ceil(w.length/2);
  return `<tspan>${w.slice(0,m).join(' ')}</tspan><tspan data-x="1" dy="19">${w.slice(m).join(' ')}</tspan>`;
}
// fix tspan x for wrapped labels
segs.forEach(g=>{
  const t=g.querySelector('.tw-t'),x=t.getAttribute('x');
  t.querySelectorAll('tspan').forEach(s=>{if(s.hasAttribute('data-x')){s.setAttribute('x',x);s.removeAttribute('data-x')}});
  if(t.querySelectorAll('tspan').length>1){t.setAttribute('y',+t.getAttribute('y')-6)}
});
// hub
const hub=document.createElementNS(NS,'g');hub.setAttribute('class','tw-hub');
hub.innerHTML=`<circle class="tw-core" cx="300" cy="300" r="104"/><circle class="tw-ring" cx="300" cy="300" r="112"/>
<text class="tw-sm" x="300" y="262">How I teach</text><text class="tw-big" id="twHubnum" x="300" y="318">01</text><text class="tw-nm" x="300" y="348">Muiz Fuad</text>`;
svg.appendChild(hub);
const orb=document.createElementNS(NS,'g');orb.setAttribute('class','tw-orb');orb.innerHTML='<circle cx="300" cy="-4" r="9"/>';svg.appendChild(orb);let orbA=0;

// filters
const fbox=document.getElementById('twFilters');
function mkChip(label,val){
  const b=document.createElement('button');b.className='tw-chip';b.textContent=label;b.setAttribute('aria-pressed','false');
  b.onclick=()=>{filter=(filter===val?null:val);[...fbox.querySelectorAll('.tw-chip')].forEach(c=>c.setAttribute('aria-pressed',String(c.dataset.v===String(filter))));
    segs.forEach((g,i)=>g.classList.toggle('tw-dim',!!filter&&!items[i].c.includes(filter)));
    if(filter&&!items[sel].c.includes(filter)){const n=items.findIndex(x=>x.c.includes(filter));if(n>-1)select(n)}};
  b.dataset.v=val;fbox.appendChild(b);
}
COURSES.forEach(c=>mkChip(c,c));

// panel
const body=document.getElementById('twBody'),dots=document.getElementById('twDots');
items.forEach((_,i)=>{const d=document.createElement('button');d.className='tw-dot';d.setAttribute('aria-label','Go to principle '+(i+1));d.onclick=()=>select(i);dots.appendChild(d)});
function select(i,focus,auto){
  if(!auto)userPause();
  sel=(i+N)%N;const it=items[sel];
  segs.forEach((g,j)=>{g.classList.remove('tw-in');g.style.animation='none';g.classList.toggle('tw-sel',j===sel);g.setAttribute('aria-pressed',String(j===sel))});
  [...dots.children].forEach((d,j)=>d.classList.toggle('tw-on',j===sel));
  document.getElementById('twHubnum').textContent='0'+(sel+1);
  {let t=sel*360/N,d=((t-orbA)%360+540)%360-180;orbA+=d;orb.style.transform='rotate('+orbA+'deg)';}
  body.classList.remove('tw-swap');void body.offsetWidth;body.classList.add('tw-swap');
  body.innerHTML=`<div class="tw-pnum">PRINCIPLE 0${sel+1} / 0${N}</div>
  <h4 class="tw-ptitle">${it.t}</h4>
  <p class="tw-belief">${it.b}</p>
  <div class="tw-h">How it looks in my classroom</div><p class="tw-how">${it.how}</p>
  <div class="tw-h">Evidence</div><ul class="tw-proof">${it.proof.map(p=>`<li>${p}</li>`).join('')}</ul>
  <div class="tw-tags">${it.c.length===COURSES.length?'<span class="tw-tag">All courses</span>':it.c.map(c=>`<span class="tw-tag">${c}</span>`).join('')}</div>`;
  if(focus)segs[sel].focus();
}
const ok=i=>!filter||items[i].c.includes(filter);
function stepTo(dir){let n=sel;for(let k=0;k<N;k++){n=(n+dir+N)%N;if(ok(n))return n}return sel}
document.getElementById('twPrev').onclick=()=>select(stepTo(-1));
document.getElementById('twNext').onclick=()=>select(stepTo(1));

// auto-play: advance every 7s; a tap pauses it, and it carries on after 7s without a tap
const SHOW=7000,RESUME=7000,TICK=100;
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
let mode=reduce?'hold':'play',elapsed=0,left=RESUME,visible=true;
const status=document.getElementById('twStatus'),toggle=document.getElementById('twToggle'),fill=document.getElementById('twFill');
function paint(){
  if(mode==='play'){status.textContent='Auto-playing · tap anything to pause';toggle.textContent='Pause';fill.style.width=(elapsed/SHOW*100)+'%';fill.style.background='var(--cta)'}
  else if(mode==='pause'){status.textContent='Paused · resumes in '+Math.ceil(left/1000)+'s';toggle.textContent='Play now';fill.style.width=((RESUME-left)/RESUME*100)+'%';fill.style.background='var(--weak)'}
  else{status.textContent='Paused';toggle.textContent='Play';fill.style.width='0%'}
}
function userPause(){if(mode==='hold')return;mode='pause';left=RESUME;paint()}
['pointerdown','keydown','wheel','touchstart'].forEach(ev=>document.getElementById('teach-wheel').addEventListener(ev,()=>{if(mode==='pause')left=RESUME},{passive:true}));
toggle.onclick=()=>{if(mode==='play'){mode='hold'}else{mode='play';elapsed=0}paint()};
setInterval(()=>{
  if(!visible||document.hidden)return;
  if(mode==='play'){elapsed+=TICK;if(elapsed>=SHOW){elapsed=0;select(stepTo(1),false,true)}paint()}
  else if(mode==='pause'){left-=TICK;if(left<=0){mode='play';elapsed=0}paint()}
},TICK);
// only run while the wheel is on screen (matters when embedded lower on a page)
new IntersectionObserver(e=>{visible=e[0].isIntersecting},{threshold:.25}).observe(document.querySelector('.tw-stage'));
select(0,false,true);paint();
})();
</script>
