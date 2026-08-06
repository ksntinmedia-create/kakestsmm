/* Как есть — интерактив лендинга */
(function () {
  'use strict';

  var header = document.getElementById('header');
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  /* ---------- Тень у шапки при скролле ---------- */
  var onScroll = function () {
    header.classList.toggle('is-stuck', window.scrollY > 10);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Мобильное меню ---------- */
  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', String(open));
  });

  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      nav.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
    }
  });

  /* ---------- Подсветка активного пункта меню ---------- */
  // только якорные ссылки: у внешних (например, блога) селектора нет
  var links = Array.prototype.filter.call(nav.querySelectorAll('a'), function (a) {
    return a.getAttribute('href').charAt(0) === '#';
  });
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if ('IntersectionObserver' in window && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Бегущая строка клиентов: дубль для бесшовного цикла ---------- */
  var clients = document.getElementById('clients');
  if (clients) {
    Array.prototype.slice.call(clients.children).forEach(function (node) {
      var copy = node.cloneNode(true);
      copy.setAttribute('aria-hidden', 'true');
      copy.alt = '';
      clients.appendChild(copy);
    });
  }

  /* ---------- Карусель кейсов ---------- */
  var track = document.getElementById('casesTrack');
  var prev = document.getElementById('casePrev');
  var next = document.getElementById('caseNext');

  if (track && prev && next) {
    var step = function () {
      var card = track.querySelector('.case');
      if (!card) return track.clientWidth * 0.8;
      var gap = parseInt(getComputedStyle(track).columnGap || '28', 10) || 28;
      return card.getBoundingClientRect().width + gap;
    };
    var syncArrows = function () {
      prev.disabled = track.scrollLeft <= 4;
      next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 4;
    };

    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', syncArrows, { passive: true });
    window.addEventListener('resize', syncArrows);
    syncArrows();
  }

  /* ---------- Появление блоков при скролле ---------- */
  var targets = document.querySelectorAll(
    '.h2, .badge, .hero__title, .hero__sub, .hero .btn, .stats, .card, .ad, .sites, .ai__card, .process__left, .steps li, .case, .footer__card, .cta'
  );

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        obs.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });

    Array.prototype.forEach.call(targets, function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(el);
    });
  }

  /* ---------- Плавный скролл с учётом высоты шапки ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href');
    if (id === '#') return;
    var target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    var top = target.getBoundingClientRect().top + window.scrollY - header.offsetHeight - 8;
    window.scrollTo({ top: top, behavior: 'smooth' });
  });

  /* ========================================================================
     Попап «Бесплатный разбор»
     ======================================================================== */

  // Куда отправлять заявки. Пока пусто — форма только показывает «спасибо»,
  // данные никуда не уходят. Подставьте URL приёмника (см. README).
  var LEAD_ENDPOINT = '';

  var DELAY = 10000;          // через сколько показать, мс
  var SNOOZE_DAYS = 7;        // на сколько прятать после закрытия
  var STORE = 'kakest_lead';

  var modal = document.getElementById('leadModal');
  if (!modal) return;

  var form = document.getElementById('leadForm');
  var body = document.getElementById('leadBody');
  var done = document.getElementById('leadDone');
  var submitBtn = form.querySelector('.lead__submit');
  var lastFocused = null;
  var timer = null;

  /* ---------- Память о показе ---------- */
  function readState() {
    try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { return {}; }
  }
  function writeState(state) {
    try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {}
  }
  function suppressed() {
    var s = readState();
    if (s.sent) return true;                       // заявку уже оставили — больше не трогаем
    if (!s.closedAt) return false;
    return Date.now() - s.closedAt < SNOOZE_DAYS * 86400000;
  }

  /* ---------- Открытие и закрытие ---------- */
  function open() {
    if (!modal.hidden) return;
    lastFocused = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () { modal.classList.add('is-open'); });
    var first = form.querySelector('input[name="phone"]');
    if (first) setTimeout(function () { first.focus(); }, 350);
  }

  function close(remember) {
    if (modal.hidden) return;
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
    setTimeout(function () { modal.hidden = true; }, 300);
    if (remember) {
      var s = readState();
      s.closedAt = Date.now();
      writeState(s);
    }
    if (lastFocused) lastFocused.focus();
  }

  modal.addEventListener('click', function (e) {
    if (e.target.closest('[data-close]')) close(true);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) close(true);
  });

  // фокус не убегает из открытого попапа
  modal.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') return;
    var items = modal.querySelectorAll('a[href], button, input, [tabindex]:not([tabindex="-1"])');
    var list = Array.prototype.filter.call(items, function (el) { return el.offsetParent !== null; });
    if (!list.length) return;
    var first = list[0];
    var last = list[list.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ---------- Валидация ---------- */
  function setError(field, message) {
    var box = form.querySelector('[data-error="' + field + '"]');
    var input = form.querySelector('[name="' + field + '"]');
    if (box) {
      box.textContent = message || '';
      box.classList.toggle('is-shown', !!message);
    }
    if (input) input.classList.toggle('is-invalid', !!message);
    return !message;
  }

  function validate(data) {
    var digits = (data.phone || '').replace(/\D/g, '');
    var okPhone = setError('phone', digits.length < 10 ? 'Укажите номер полностью, с кодом страны' : '');
    var okAgree = setError('agree', form.agree.checked ? '' : 'Без согласия мы не можем принять заявку');
    var okTerms = setError('terms', form.terms.checked ? '' : 'Отметьте, что принимаете условия');
    return okPhone && okAgree && okTerms;
  }

  form.querySelector('[name="phone"]').addEventListener('input', function () {
    if (this.classList.contains('is-invalid')) setError('phone', '');
  });
  ['agree', 'terms'].forEach(function (field) {
    form[field].addEventListener('change', function () {
      if (this.checked) setError(field, '');
    });
  });

  /* ---------- Отправка ---------- */
  function send(data) {
    if (!LEAD_ENDPOINT) return Promise.resolve();   // приёмник не подключён
    return fetch(LEAD_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var data = {
      name: form.name.value.trim(),
      phone: form.phone.value.trim(),
      messenger: form.messenger.value,
      consent: { pdn: form.agree.checked, terms: form.terms.checked },
      page: location.href,
      at: new Date().toISOString()
    };
    if (!validate(data)) return;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправляем…';

    send(data)['catch'](function () {})['then'](function () {
      var s = readState();
      s.sent = true;
      writeState(s);
      body.hidden = true;
      done.hidden = false;
      submitBtn.disabled = false;
      submitBtn.textContent = 'Получить разбор';
    });
  });

  /* ---------- Показ через 10 секунд ---------- */
  if (!suppressed()) {
    timer = setTimeout(open, DELAY);
    // если человек уже сам дошёл до контактов — не мешаем попапом
    var contacts = document.getElementById('contacts');
    if (contacts && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries, obs) {
        if (!entries[0].isIntersecting) return;
        clearTimeout(timer);
        obs.disconnect();
      }).observe(contacts);
    }
  }
})();
