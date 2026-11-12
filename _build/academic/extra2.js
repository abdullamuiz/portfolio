<script>
/* academic page: teaching loop, evidence chart, modules, class sizes, clips */
(function(){
  var $ = function (id) { return document.getElementById(id); };
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var D = {}; try { D = JSON.parse($('acData').textContent); } catch (e) {}
  var esc = function (s) { var d = document.createElement('div'); d.innerHTML = s; return d.textContent; };

  /* the teaching loop orbits while it is on screen, like the work-philosophy loop */
  var lp = $('loop');
  if (lp && !reduce) new IntersectionObserver(function (es) { lp.classList.toggle('on', es[0].isIntersecting); }, { threshold: .3 }).observe(lp);


  /* modules: four core cards, five compact ones; each opens a details panel */
  var mods = D.mods || [], core = $('mods'), more = $('modsMore');
  if (core) core.innerHTML = mods.filter(function (m) { return m.core; }).map(function (m, i) {
    return '<button class="panel mod lift reveal in" type="button" data-mod="' + m.c + '" style="--rd:' + (i * .06) + 's"><span class="code">' + m.c + '</span><h3>' + m.n + '</h3><span class="lvl">' + m.l + (m.coord ? ' · ' + m.coord.split(',')[0].toLowerCase() : '') + '</span>' +
      (m.app ? '<span class="uses"><i>' + IC('upright') + '</i>' + m.app[0] + '</span>' : '<span class="uses muted-u">Details</span>') + '</button>';
  }).join('');
  if (more) more.innerHTML = mods.filter(function (m) { return !m.core; }).map(function (m) {
    return '<li><button type="button" data-mod="' + m.c + '"><b>' + m.c + '</b>' + m.n + '<span>' + m.l + (m.lt ? ' (to confirm)' : '') + '</span></button></li>';
  }).join('');
  var dlg = $('mdlg');
  function openMod(code) {
    var m = mods.filter(function (x) { return x.c === code; })[0]; if (!m || !dlg) return;
    $('mdCode').textContent = m.c; $('mdTitle').innerHTML = m.n; $('mdLvl').textContent = m.l + (m.coord ? ' · ' + m.coord : '');
    var h = '<div class="md-sec"><span class="label">Terms taught</span><ul class="md-terms">' + m.terms.map(function (t) { return '<li>' + t[0] + (D.full && t[1] ? '<b>' + t[1] + ' students</b>' : '') + '</li>'; }).join('') + '</ul></div>';
    if (m.lt) h += '<p><span class="todo">[TODO: confirm the level]</span></p>';
    h += '<div class="md-sec"><span class="label">Learning outcomes</span><span class="todo">[TODO: course learning outcomes from the module descriptor]</span></div>';
    var A = D.asg && D.asg[m.c];
    h += '<div class="md-sec"><span class="label">Assessment' + (A ? ' · as delivered, ' + A[0] : '') + '</span>' + (A ? '<div class="wbar md-w">' + A[1].map(function (x) { return '<span style="--w:' + x[1] + '">' + x[0] + ' <b>' + x[1] + '</b></span>'; }).join('') + '</div>' : '<span class="todo">[TODO: assessment types and weights]</span>') + '</div>';
    if (m.app) h += '<div class="md-sec"><span class="label">What students use</span><a class="more-link" href="' + m.app[1] + '" target="_blank" rel="noopener">' + m.app[0] + ' ' + IC('upright') + '</a></div>';
    if (m.demo) h += '<div class="md-sec"><span class="label">Sample lesson</span><a class="more-link" href="#lesson" data-close>Found, Chosen, Booked ' + IC('down') + '</a></div>';
    if (D.full && m.mid) h += '<div class="md-sec md-mid"><span class="label">Midterm check-in · ' + m.mid[0] + ' · ' + m.mid[1] + ' respondent' + (m.mid[1] > 1 ? 's' : '') + '</span><p>' + m.mid[2] + '.</p><blockquote>“' + m.mid[3] + '”</blockquote></div>';
    $('mdBody').innerHTML = h;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-mod]'); if (b) { openMod(b.dataset.mod); return; }
    if (dlg && dlg.open && (e.target === dlg || e.target.closest('#mdX') || e.target.closest('[data-close]'))) dlg.close();
  });

  /* students per term: one bar per term, split by module, to the same scale */
  var ld = $('loads');
  if (ld && D.loads) {
    var mx = Math.max.apply(null, D.loads.map(function (t) { return t[1].reduce(function (a, b) { return a + b[1]; }, 0); }));
    ld.innerHTML = D.loads.map(function (t) {
      var tot = t[1].reduce(function (a, b) { return a + b[1]; }, 0);
      return '<div class="ld-row"><span class="ld-t">' + t[0] + '</span><div class="ld-bar" style="width:' + (tot / mx * 100).toFixed(1) + '%">' +
        t[1].map(function (s) { return '<span style="flex:' + s[1] + '" title="' + s[0] + ': ' + s[1] + ' students"><b>' + s[0] + '</b><em>' + s[1] + '</em></span>'; }).join('') +
        '</div><span class="ld-n">' + tot + '</span></div>';
    }).join('');
  }

  /* clips: load and play only while on screen */
  var clips = [].slice.call(document.querySelectorAll('video[data-clip]'));
  clips.forEach(function (v) { var n = v.dataset.clip; v.poster = 'video/academic/' + n + '.jpg'; v.innerHTML = '<source src="video/academic/' + n + '.mp4" type="video/mp4">'; v.addEventListener('loadeddata', function () { v.parentNode.classList.add('ready'); }); });
  var vio = new IntersectionObserver(function (es) { es.forEach(function (e) { var v = e.target; if (e.isIntersecting && !reduce) { if (v.preload === 'none') { v.preload = 'auto'; v.load(); } var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); }); }, { threshold: .4 });
  clips.forEach(function (v) { vio.observe(v); var im = new Image(); im.onload = function () { v.parentNode.classList.add('ready'); }; im.src = v.poster; });
})();
</script>
<script>
(function(){
  var D={}; try{D=JSON.parse(document.getElementById('acData').textContent)}catch(e){}
  var o=D.out; if(!o) return;
  var X=function(v){return ((v-30)/(100-30)*100).toFixed(2)+'%'};
  var db=document.getElementById('ocDumb');
  if(db) db.innerHTML=o.db.slice().sort(function(a,b){return (b[1]-b[2])-(a[1]-a[2])}).map(function(r){var g=(r[1]-r[2]).toFixed(1);var tip=r[0]+': coursework '+r[1]+'%, final exam '+r[2]+'%, gap '+g;
    return '<div class="db-row" title="'+tip+'" tabindex="0" aria-label="'+tip+'"><span class="db-l">'+r[0]+'</span><span class="db-t"><i class="db-line" style="left:'+X(r[2])+';width:calc('+X(r[1])+' - '+X(r[2])+')"></i><i class="db-ex" style="left:'+X(r[2])+'"></i><i class="db-cw" style="left:'+X(r[1])+'"></i></span><span class="db-g">'+g+'</span></div>'}).join('');
  var ax=document.querySelector('.db-axis'); if(ax) ax.innerHTML=[30,50,70,90].map(function(v){return '<span style="left:'+X(v)+'">'+v+'%</span>'}).join('');
  var ab=document.getElementById('ocAtt');
  if(ab) ab.innerHTML=o.att.map(function(r){return '<div class="ab-row"><span class="ab-l">'+r[0]+'<small>'+r[1]+' students</small></span><span class="ab-t"><i style="width:'+Math.max(r[2],.5)+'%"></i></span><b>'+Math.round(r[2])+'%</b></div>'}).join('');
})();
</script>
