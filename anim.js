/* 浠佑拾光官网动效：滚动显现、数字滚动、天空视差、飘字、卡片光斑、截图倾斜。
   全部为渐进增强：没有脚本或系统开启「减少动态效果」时，页面内容照常完整显示。 */
(function () {
  'use strict';
  window.__mo = true;
  var root = document.documentElement;
  var motion = root.classList.contains('mo');
  var finePointer = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- 顶栏状态、阅读进度、回到顶部 ---------- */
  var hdr = document.querySelector('header.top');
  var totop = document.querySelector('.totop');
  var skies = [].slice.call(document.querySelectorAll('.sky'));
  var scrollY0 = 0, ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      scrollY0 = window.scrollY || window.pageYOffset;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      if (hdr) {
        hdr.classList.toggle('scrolled', scrollY0 > 8);
        hdr.style.setProperty('--p', max > 0 ? Math.min(1, scrollY0 / max).toFixed(4) : 0);
      }
      if (totop) totop.classList.toggle('show', scrollY0 > 520);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (totop) totop.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: motion ? 'smooth' : 'auto' });
  });

  /* ---------- 数字滚动 ---------- */
  function countUp(scope) {
    var nums = scope.querySelectorAll ? scope.querySelectorAll('.num[data-to]') : [];
    [].forEach.call(nums, function (el) {
      if (el.__done) return;
      el.__done = true;
      var to = +el.getAttribute('data-to'), t0 = null, dur = 1500;
      function step(ts) {
        if (!t0) t0 = ts;
        var k = Math.min(1, (ts - t0) / dur);
        var e = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(to * e);
        if (k < 1) requestAnimationFrame(step);
      }
      el.textContent = '0';
      requestAnimationFrame(step);
    });
  }

  /* ---------- 滚动显现（同组元素依次错开） ---------- */
  var els = [].slice.call(document.querySelectorAll('.rv, .rv-line'));
  if (!motion || !('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('in'); });
  } else {
    els.forEach(function (e) {
      if (e.style.getPropertyValue('--d')) return;
      var sibs = [].filter.call(e.parentElement.children, function (c) { return c.classList.contains('rv'); });
      var i = sibs.indexOf(e);
      if (i > 0) e.style.setProperty('--d', (Math.min(i, 7) * 0.09).toFixed(2) + 's');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        countUp(en.target);
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0 });
    els.forEach(function (e) { io.observe(e); });
  }

  if (!motion) return;

  /* ---------- 卡片跟随光斑 ---------- */
  if (finePointer) {
    document.addEventListener('pointermove', function (e) {
      var c = e.target.closest && e.target.closest('.card');
      if (!c) return;
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });
    document.addEventListener('pointerout', function (e) {
      var c = e.target.closest && e.target.closest('.card');
      if (c && !c.contains(e.relatedTarget)) { c.style.removeProperty('--mx'); c.style.removeProperty('--my'); }
    }, { passive: true });
  }

  /* ---------- App 截图随指针轻微倾斜 ---------- */
  if (finePointer) {
    [].forEach.call(document.querySelectorAll('.tilt'), function (img) {
      var zone = img.closest('section, .hero') || img;
      zone.addEventListener('pointermove', function (e) {
        var r = img.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / (window.innerWidth / 2);
        var dy = (e.clientY - (r.top + r.height / 2)) / (window.innerHeight / 2);
        dx = Math.max(-1, Math.min(1, dx)); dy = Math.max(-1, Math.min(1, dy));
        img.style.setProperty('--ry', (dx * 10).toFixed(2) + 'deg');
        img.style.setProperty('--rx', (-dy * 8).toFixed(2) + 'deg');
      }, { passive: true });
      zone.addEventListener('pointerleave', function () {
        img.style.setProperty('--ry', '0deg');
        img.style.setProperty('--rx', '0deg');
      });
    });
  }

  /* ---------- 天空：飘字 + 视差 ---------- */
  function rand(a, b) { return a + Math.random() * (b - a); }
  var COLORS = ['rgba(45,108,223,.20)', 'rgba(123,92,255,.18)', 'rgba(255,138,91,.24)', 'rgba(45,108,223,.14)'];
  skies.forEach(function (sky) {
    var chars = (sky.getAttribute('data-chars') || '').split(' ').filter(Boolean);
    var layer = sky.querySelector('.sky-layer');
    function setH() { sky.style.setProperty('--h', (sky.offsetHeight + 140) + 'px'); }
    setH();
    window.addEventListener('resize', setH, { passive: true });
    if (layer && chars.length) {
      var n = window.innerWidth < 720 ? 6 : 12;
      for (var i = 0; i < n; i++) {
        var s = document.createElement('span');
        s.className = 'zi';
        s.textContent = chars[i % chars.length];
        var x = (i + rand(0.1, 0.9)) / n * 100;
        s.style.cssText = '--x:' + x.toFixed(1) + '%;--s:' + Math.round(rand(20, 46)) + 'px;--c:' + COLORS[i % COLORS.length] +
          ';--t:' + rand(14, 24).toFixed(1) + 's;--dl:-' + rand(0, 22).toFixed(1) + 's;--sx:' + Math.round(rand(-40, 40)) + 'px';
        layer.appendChild(s);
      }
    }
  });

  var depths = [].slice.call(document.querySelectorAll('.sky .depth'));
  if (depths.length) {
    var px = 0, py = 0, cx = 0, cy = 0, visible = true, running = false;
    if (finePointer) {
      window.addEventListener('pointermove', function (e) {
        px = e.clientX / window.innerWidth - 0.5;
        py = e.clientY / window.innerHeight - 0.5;
        kick();
      }, { passive: true });
    }
    window.addEventListener('scroll', kick, { passive: true });
    if ('IntersectionObserver' in window) {
      var vio = new IntersectionObserver(function (en) { visible = en.some(function (x) { return x.isIntersecting; }); if (visible) kick(); });
      skies.forEach(function (s) { vio.observe(s); });
    }
    function frame() {
      cx += (px - cx) * 0.06; cy += (py - cy) * 0.06;
      var y = window.scrollY || window.pageYOffset;
      depths.forEach(function (d) {
        var k = +d.getAttribute('data-k') || 0.3;
        d.style.translate = (-cx * 40 * k).toFixed(1) + 'px ' + (y * k * 0.45 - cy * 24 * k).toFixed(1) + 'px';
      });
      if (visible && (Math.abs(px - cx) > 0.001 || Math.abs(py - cy) > 0.001)) requestAnimationFrame(frame);
      else running = false;
    }
    function kick() { if (!running && visible) { running = true; requestAnimationFrame(frame); } }
    kick();
  }
})();
