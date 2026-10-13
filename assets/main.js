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

  /* ---- Orbes vivos junto a los proyectos «en marcha» ---- */
  var vivos = document.querySelectorAll('.orb-live');
  if (vivos.length && window.ThinkingOrbs) {
    var oscuro = function () { return root.getAttribute('data-theme') !== 'light'; };
    var color = function (el) { return getComputedStyle(el).getPropertyValue('--accent').trim(); };
    var lista = Array.prototype.map.call(vivos, function (cv) { return { cv: cv, orb: ThinkingOrbs.mount(cv, { state: 'composing', size: 20, dark: oscuro(), color: color(cv) }) }; });
    document.addEventListener('themechange', function () { lista.forEach(function (o) { o.orb.update({ dark: oscuro(), color: color(o.cv) }); }); });
  }

  /* ---- Indicador "pensando": aparece solo si cargar algo tarda más de 140 ms ---- */
  var think = document.getElementById('think');
  if (think && window.ThinkingOrbs) {
    var orb = null, timer = 0;
    var isDark = function () { return root.getAttribute('data-theme') !== 'light'; };
    var tint = function () { return getComputedStyle(document.body).getPropertyValue('--accent').trim(); };
    var show = function (state, delay) {
      clearTimeout(timer);
      timer = setTimeout(function () {
        think.hidden = false;
        if (!orb) orb = ThinkingOrbs.mount(think.querySelector('canvas'), { state: state, size: 32, dark: isDark(), color: tint() });
        else { orb.update({ state: state, dark: isDark(), color: tint() }); orb.resume(); }
      }, delay);
    };
    var hide = function () { clearTimeout(timer); think.hidden = true; if (orb) orb.pause(); };
    document.addEventListener('themechange', function () { if (orb) orb.update({ dark: isDark(), color: tint() }); });
    var demo = /[?&]orbs\b/.test(location.search);
    if (demo) { show('composing', 0); setTimeout(hide, 4000); }
    else if (document.readyState !== 'complete') { show('composing', 140); window.addEventListener('load', hide); }
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if ((a.target && a.target !== '_self') || a.hasAttribute('download')) return;
      var u = new URL(a.href, location.href);
      if (u.origin !== location.origin || (u.pathname === location.pathname && u.search === location.search)) return;
      show('composing', 140);
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) hide(); });
  }
})();
