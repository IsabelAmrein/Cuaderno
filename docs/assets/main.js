(function () {
  'use strict';
  var root = document.documentElement;

  /* ---- Tema claro/oscuro ---- */
  var themeBtn = document.querySelector('[data-theme-toggle]');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      document.dispatchEvent(new Event('themechange'));
    });
  }

  /* ---- Filtro por tema en la lista de artículos ---- */
  var filters = document.querySelectorAll('[data-filter]');
  if (filters.length) {
    var rows = document.querySelectorAll('[data-tags]');
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var tag = btn.getAttribute('data-filter');
        filters.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        rows.forEach(function (li) {
          var has = !tag || li.getAttribute('data-tags').split(',').indexOf(tag) > -1;
          li.hidden = !has;
        });
      });
    });
  }

  /* ---- Botón copiar en bloques de código ---- */
  document.querySelectorAll('.prose pre').forEach(function (pre) {
    var code = pre.querySelector('code');
    if (!code || !navigator.clipboard) return;
    var b = document.createElement('button');
    b.className = 'copy';
    b.type = 'button';
    b.textContent = root.lang === 'en' ? 'Copy' : 'Copiar';
    b.addEventListener('click', function () {
      navigator.clipboard.writeText(code.innerText).then(function () {
        var old = b.textContent;
        b.textContent = root.lang === 'en' ? 'Copied' : 'Copiado';
        setTimeout(function () { b.textContent = old; }, 1500);
      });
    });
    pre.appendChild(b);
  });


  /* ---- Animaciones suaves: aparición al hacer scroll, cajitas por partes y brújula ---- */
  if (root.classList.contains('anim')) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.15, rootMargin: '0px 0px -5% 0px' });
    document.querySelectorAll('.prose > *').forEach(function (el) {
      if (!el.classList.contains('steps')) el.classList.add('reveal');
      io.observe(el);
    });
    var motif = document.querySelector('.post-head .motif');
    if (motif) requestAnimationFrame(function () { motif.classList.add('play'); });
  }

  /* ---- Gráfico de portada: regresión lineal que se reajusta al añadir datos ---- */
  var canvas = document.getElementById('plot');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var seed = [[.05,.2],[.1,.34],[.15,.22],[.2,.4],[.27,.33],[.32,.5],[.38,.42],[.44,.58],[.5,.47],
              [.55,.66],[.62,.55],[.68,.72],[.74,.62],[.8,.8],[.86,.7],[.92,.86],[.97,.78]];
  var pts = seed.slice();
  var cur = fit(pts), target = cur, raf = null, w = 0, h = 0;

  function fit(p) {
    var n = p.length, sx = 0, sy = 0, sxy = 0, sxx = 0;
    p.forEach(function (q) { sx += q[0]; sy += q[1]; sxy += q[0] * q[1]; sxx += q[0] * q[0]; });
    var d = n * sxx - sx * sx;
    var m = d ? (n * sxy - sx * sy) / d : 0;
    return { m: m, b: (sy - m * sx) / n };
  }
  function css(v) { return getComputedStyle(canvas).getPropertyValue(v).trim(); }
  function size() {
    var r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    w = r.width; h = r.height;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function X(x) { return 24 + x * (w - 48); }
  function Y(y) { return h - 24 - y * (h - 48); }
  function draw() {
    var ink = css('--ink'), accent = css('--accent'), line = css('--line');
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = line; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(1), Y(0)); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(0), Y(1)); ctx.stroke();
    ctx.strokeStyle = accent; ctx.globalAlpha = .4;
    pts.forEach(function (p) {
      ctx.beginPath(); ctx.moveTo(X(p[0]), Y(p[1])); ctx.lineTo(X(p[0]), Y(cur.m * p[0] + cur.b)); ctx.stroke();
    });
    ctx.globalAlpha = 1; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(X(0), Y(cur.b)); ctx.lineTo(X(1), Y(cur.m + cur.b)); ctx.stroke();
    ctx.fillStyle = ink;
    pts.forEach(function (p) { ctx.beginPath(); ctx.arc(X(p[0]), Y(p[1]), 4, 0, 6.2832); ctx.fill(); });
  }
  function step() {
    var dm = target.m - cur.m, db = target.b - cur.b;
    if (reduce || (Math.abs(dm) < .001 && Math.abs(db) < .001)) { cur = target; draw(); raf = null; return; }
    cur = { m: cur.m + dm * .18, b: cur.b + db * .18 };
    draw(); raf = requestAnimationFrame(step);
  }
  function add(x, y) {
    if (pts.length >= 80) return;
    pts.push([Math.min(1, Math.max(0, x)), Math.min(1, Math.max(0, y))]);
    target = fit(pts);
    if (!raf) raf = requestAnimationFrame(step);
  }
  canvas.addEventListener('pointerdown', function (e) {
    var r = canvas.getBoundingClientRect();
    add((e.clientX - r.left - 24) / (w - 48), 1 - (e.clientY - r.top - 24) / (h - 48));
  });
  canvas.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); add(Math.random(), Math.random()); }
  });
  var reset = document.getElementById('plot-reset');
  if (reset) reset.addEventListener('click', function () { pts = seed.slice(); target = fit(pts); if (!raf) raf = requestAnimationFrame(step); });
  window.addEventListener('resize', function () { size(); draw(); });
  document.addEventListener('themechange', draw);
  size(); draw();
})();
