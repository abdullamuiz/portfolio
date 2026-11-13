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
<script>
(function () {
  document.querySelectorAll('.cmt-filter').forEach(function (g) {
    var cards = g.parentNode.querySelectorAll('.cmts-all .cmt');
    g.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      g.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      var m = b.getAttribute('data-m');
      cards.forEach(function (c) { c.hidden = !!m && (' ' + c.getAttribute('data-mods') + ' ').indexOf(' ' + m + ' ') < 0; });
    });
  });
})();
</script>
<script>
(function () {
  var rows = document.querySelectorAll('.mgroup a[data-pk]');
  if (!rows.length) return;
  var pop = document.getElementById('pkPop'), sheet = document.getElementById('pkSheet');
  var fine = matchMedia('(hover:hover) and (pointer:fine)');
  var lastPt = '';
  addEventListener('pointerdown', function (e) { lastPt = e.pointerType; }, true);
  function touchy() { return lastPt === 'touch' || lastPt === 'pen' || !fine.matches; }
  var list = Array.prototype.map.call(rows, function (a) { return a.getAttribute('data-pk'); });
  function content(code) { var t = document.getElementById('pk-' + code); return t ? t.innerHTML : ''; }
  var showT, hideT, cur = null;
  function place(a) {
    var r = a.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight, g = 14;
    var x = r.right + g; if (x + w > innerWidth - 12) x = r.left - w - g; if (x < 12) x = Math.min(innerWidth - w - 12, Math.max(12, r.left));
    var y = Math.min(Math.max(12, r.top + r.height / 2 - h / 2), innerHeight - h - 12);
    pop.style.left = x + 'px'; pop.style.top = y + 'px';
  }
  function show(a) {
    clearTimeout(hideT);
    if (cur === a) return;
    if (cur) cur.classList.remove('is-peek');
    cur = a; a.classList.add('is-peek');
    pop.innerHTML = content(a.getAttribute('data-pk')); pop.hidden = false; place(a);
    requestAnimationFrame(function () { pop.classList.add('on'); });
  }
  function hide() {
    pop.classList.remove('on'); if (cur) cur.classList.remove('is-peek'); cur = null;
    setTimeout(function () { if (!cur) pop.hidden = true; }, 180);
  }
  rows.forEach(function (a) {
    a.addEventListener('mouseenter', function () { if (touchy()) return; clearTimeout(showT); clearTimeout(hideT); showT = setTimeout(function () { show(a); }, cur ? 0 : 220); });
    a.addEventListener('mouseleave', function () { clearTimeout(showT); hideT = setTimeout(hide, 160); });
    a.addEventListener('focus', function () { if (!touchy()) show(a); });
    a.addEventListener('blur', function () { hideT = setTimeout(hide, 160); });
    a.addEventListener('click', function (e) {
      if (!touchy() || !sheet || !sheet.showModal || e.metaKey || e.ctrlKey) return;
      clearTimeout(showT); hide();
      e.preventDefault(); openSheet(a.getAttribute('data-pk'));
    });
  });
  pop.addEventListener('mouseenter', function () { clearTimeout(hideT); });
  pop.addEventListener('mouseleave', function () { hideT = setTimeout(hide, 160); });
  addEventListener('scroll', function () { if (cur) hide(); }, { passive: true });
  addEventListener('keydown', function (e) { if (e.key === 'Escape' && cur) hide(); });
  function openSheet(code) {
    var i = list.indexOf(code), body = sheet.querySelector('.pk-body');
    body.innerHTML = content(code) + '<div class="pk-nav">' +
      (i > 0 ? '<button type="button" data-to="' + list[i - 1] + '">← ' + list[i - 1] + '</button>' : '') +
      (i < list.length - 1 ? '<button type="button" data-to="' + list[i + 1] + '">' + list[i + 1] + ' →</button>' : '') + '</div>';
    sheet.scrollTop = 0;
    if (!sheet.open) sheet.showModal();
  }
  if (sheet) {
    sheet.addEventListener('click', function (e) {
      var b = e.target.closest('[data-to]'); if (b) { openSheet(b.getAttribute('data-to')); return; }
      if (e.target.closest('.pk-x') || e.target === sheet) sheet.close();
    });
    var y0 = null;
    sheet.addEventListener('touchstart', function (e) { y0 = sheet.scrollTop <= 0 ? e.touches[0].clientY : null; }, { passive: true });
    sheet.addEventListener('touchend', function (e) { if (y0 !== null && e.changedTouches[0].clientY - y0 > 90) sheet.close(); y0 = null; }, { passive: true });
  }
})();
</script>
