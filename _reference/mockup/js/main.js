/*
  main.js — спільна поведінка chrome: sticky header shadow, мобільний drawer,
  FAQ accordion, lang-switch (стаб з toast), список міст без РФ для datalist.
  Vanilla JS, без inline onclick/style.
*/

/* Європа + Азія, свідомо без Росії/Білорусі — єдине джерело для всіх форм сайту. */
const PT_CITIES = [
  'Київ', 'Одеса', 'Львів', 'Дніпро', 'Харків',
  'Варшава', 'Гданськ', 'Берлін', 'Мюнхен', 'Прага', 'Будапешт', 'Бухарест', 'Софія',
  'Стамбул', 'Тбілісі', 'Баку', 'Алмати', 'Ташкент', 'Ер-Ріяд', 'Шанхай'
];
window.PT_CITIES = PT_CITIES;

function initCityDatalists() {
  document.querySelectorAll('datalist[data-cities]').forEach((list) => {
    list.innerHTML = PT_CITIES.map((city) => `<option value="${city}"></option>`).join('');
  });
}

function initHeaderScroll() {
  const header = document.querySelector('[data-header]');
  if (!header) return;
  const onScroll = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

function initDrawer() {
  const toggle = document.querySelector('[data-drawer-toggle]');
  const drawer = document.querySelector('[data-drawer]');
  const closeBtn = document.querySelector('[data-drawer-close]');
  if (!toggle || !drawer) return;

  const links = drawer.querySelectorAll('a, button');

  const open = () => {
    drawer.setAttribute('data-open', 'true');
    toggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    const firstLink = drawer.querySelector('.drawer__link');
    if (firstLink) firstLink.focus();
  };

  const close = () => {
    drawer.setAttribute('data-open', 'false');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    toggle.focus();
  };

  toggle.addEventListener('click', () => {
    const isOpen = drawer.getAttribute('data-open') === 'true';
    isOpen ? close() : open();
  });

  if (closeBtn) closeBtn.addEventListener('click', close);

  drawer.querySelector('.drawer__backdrop')?.addEventListener('click', close);

  drawer.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') close();
  });

  links.forEach((link) => {
    if (link.tagName === 'A') link.addEventListener('click', close);
  });
}

function initFaqAccordion() {
  document.querySelectorAll('[data-faq]').forEach((group) => {
    const items = group.querySelectorAll('.faq-item');
    items.forEach((item) => {
      const btn = item.querySelector('.faq-item__q');
      btn?.addEventListener('click', () => {
        const isOpen = item.getAttribute('data-open') === 'true';
        items.forEach((other) => {
          other.setAttribute('data-open', 'false');
          other.querySelector('.faq-item__q')?.setAttribute('aria-expanded', 'false');
        });
        if (!isOpen) {
          item.setAttribute('data-open', 'true');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  });
}

function showToast(message) {
  let toast = document.querySelector('[data-toast]');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('data-toast', '');
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.setAttribute('data-visible', 'true');
  window.clearTimeout(toast._hideTimer);
  toast._hideTimer = window.setTimeout(() => {
    toast.setAttribute('data-visible', 'false');
  }, 2600);
}

function initHeroVideo() {
  const video = document.querySelector('[data-hero-video]');
  if (!video) return;
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) {
    video.removeAttribute('autoplay');
    video.pause();
  }
}

function initLangSwitch() {
  document.querySelectorAll('[data-lang-btn]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang-btn');
      if (lang === 'uk') return;
      showToast('EN-версія готується. Поки що доступна українська.');
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initCityDatalists();
  initHeaderScroll();
  initDrawer();
  initFaqAccordion();
  initHeroVideo();
  initLangSwitch();
});
