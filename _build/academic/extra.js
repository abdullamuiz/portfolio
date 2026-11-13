<script>
/* academic page: images, certificate viewer, copy email, menu, reading bar, current section */
(function(){
  var $ = function (id) { return document.getElementById(id); };
  var CERTS = [{poster:'img/cert-msc.webp',alt:'MSc Global Marketing Management with Merit, Asia Pacific University'},{poster:'img/cert-ba.webp',alt:'BA (Hons) Tourism Management, Asia Pacific University'},{poster:'img/cert-cth.webp',alt:'CTH Level 4 Diploma in Tourism Management'},{poster:'img/cert-abe.webp',alt:'ABE Level 4 Diploma in Human Resource Management'}];
  var lb = $('lb'), stage = $('lbStage'), cap = $('lbCap'), cur = 0;
  function show() { var it = CERTS[cur]; stage.innerHTML = ''; var im = document.createElement('img'); im.src = it.poster; im.alt = it.alt; stage.appendChild(im); cap.textContent = it.alt; }
  function step(d) { cur = (cur + d + CERTS.length) % CERTS.length; show(); }
  if (lb) {
    document.addEventListener('click', function (e) { var b = e.target.closest('[data-lb]'); if (!b) return; cur = +b.dataset.i || 0; show(); if (lb.showModal) lb.showModal(); else lb.setAttribute('open', ''); });
    $('lbPrev').addEventListener('click', function () { step(-1); });
    $('lbNext').addEventListener('click', function () { step(1); });
    $('lbX').addEventListener('click', function () { lb.close(); });
    lb.addEventListener('close', function () { stage.innerHTML = ''; });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target === stage) lb.close(); });
    lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') step(1); if (e.key === 'ArrowLeft') step(-1); });
  }

  var cm = $('copyMail');
  if (cm) cm.addEventListener('click', function () {
    var s = cm.querySelector('span'), mail = s.textContent;
    var done = function () { s.textContent = 'Email copied'; setTimeout(function () { s.textContent = mail; }, 1800); };
    if (navigator.clipboard) navigator.clipboard.writeText(mail).then(done, done); else done();
  });

  /* demo-lecture invite: a popup that works without an email app (the link stays a mailto without JS) */
  var ib = $('inviteBtn'), dlg = $('invite');
  if (ib && dlg && dlg.showModal) {
    ib.addEventListener('click', function (e) { e.preventDefault(); $('inviteStatus').textContent = ''; dlg.showModal(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    $('inviteCopy').addEventListener('click', function () {
      var m = $('inviteMail').textContent, st = $('inviteStatus');
      var ok = function () { st.textContent = 'Email copied. Paste it into any email app.'; };
      var sel = function () { var r = document.createRange(); r.selectNodeContents($('inviteMail')); var w = getSelection(); w.removeAllRanges(); w.addRange(r); st.textContent = 'Email selected. Copy it with your device’s copy command.'; };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(m).then(ok, sel); else sel();
    });
  }

  /* buttons that wait for a file say so instead of doing nothing */
  document.querySelectorAll('button.is-todo').forEach(function (b) {
    b.title = 'TODO: ' + b.dataset.todo;
    b.addEventListener('click', function () { var t = b.lastChild; if (b.dataset.busy) return; b.dataset.busy = 1; var keep = b.innerHTML; b.textContent = 'Coming soon: ' + b.dataset.todo; setTimeout(function () { b.innerHTML = keep; delete b.dataset.busy; }, 1800); });
  });

  /* phone menu */
  var head = $('top'), mb = $('menuBtn');
  function menu(open) { head.classList.toggle('nav-open', open); mb.setAttribute('aria-expanded', open); mb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu'); mb.innerHTML = '<i>' + IC(open ? 'x' : 'menu') + '</i>'; }
  if (head && mb) {
    mb.addEventListener('click', function (e) { e.stopPropagation(); menu(!head.classList.contains('nav-open')); });
    document.addEventListener('click', function (e) { if (head.classList.contains('nav-open') && (e.target.closest('nav.links a') || !e.target.closest('header'))) menu(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape' && head.classList.contains('nav-open')) { menu(false); mb.focus(); } });
  }

  /* reading bar and current section */
  var bar = $('readBar'), links = [].slice.call(document.querySelectorAll('nav.links a[data-spy]'));
  var secs = [];
  links.forEach(function (a) { a.dataset.spy.split(' ').forEach(function (id) { var el = $(id); if (el) secs.push([el, a]); }); });
  var queued = false;
  function spy() {
    queued = false;
    var max = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, scrollY / max) : 0) + ')';
    if (head) head.classList.toggle('scrolled', scrollY > 8);
    var line = innerHeight * .45, on = null, best = -1e9;
    secs.forEach(function (p) { var t = p[0].getBoundingClientRect().top; if (t <= line && t > best) { best = t; on = p[1]; } });
    links.forEach(function (a) { var c = a === on; a.classList.toggle('cur', c); if (c) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
  }
  addEventListener('scroll', function () { if (!queued) { queued = true; requestAnimationFrame(spy); } }, { passive: true });
  addEventListener('resize', spy); spy();
})();
</script>
