export function initHeaderScroll() {
  const header = document.querySelector("[data-header]");
  if (!header) return;

  const hero = document.querySelector("[data-hero]");

  const update = () => {
    const y = window.scrollY;
    header.classList.toggle("is-scrolled", y > 8);

    if (!hero) {
      header.classList.remove("is-over-hero");
      return;
    }

    const headerH = header.offsetHeight || 76;
    const heroH = hero.offsetHeight || 0;
    const leaveAt = Math.max(heroH - headerH - 48, 64);
    header.classList.toggle("is-over-hero", y < leaveAt);
  };

  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update, { passive: true });

  if (hero) {
    header.classList.add("header--ready");
  }
}

export function initDrawer() {
  const toggle = document.querySelector("[data-drawer-toggle]");
  const drawer = document.querySelector("[data-drawer]");
  const closeBtn = document.querySelector("[data-drawer-close]");
  if (!toggle || !drawer) return;

  const open = () => {
    drawer.setAttribute("data-open", "true");
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("is-locked");
    drawer.querySelector(".drawer__link")?.focus();
  };

  const close = () => {
    drawer.setAttribute("data-open", "false");
    toggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("is-locked");
    toggle.focus();
  };

  toggle.addEventListener("click", () => {
    const isOpen = drawer.getAttribute("data-open") === "true";
    isOpen ? close() : open();
  });
  closeBtn?.addEventListener("click", close);
  drawer.querySelector(".drawer__backdrop")?.addEventListener("click", close);
  drawer.addEventListener("keydown", (event) => {
    if (event.key === "Escape") close();
  });
  drawer.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", close);
  });
}

export function initFaqAccordion() {
  document.querySelectorAll("[data-faq]").forEach((group) => {
    const items = group.querySelectorAll(".faq-item");
    items.forEach((item) => {
      const btn = item.querySelector(".faq-item__q");
      btn?.addEventListener("click", () => {
        const isOpen = item.getAttribute("data-open") === "true";
        items.forEach((other) => {
          other.setAttribute("data-open", "false");
          other.querySelector(".faq-item__q")?.setAttribute("aria-expanded", "false");
        });
        if (!isOpen) {
          item.setAttribute("data-open", "true");
          btn.setAttribute("aria-expanded", "true");
        }
      });
    });
  });
}

export function initHeroVideo() {
  const hero = document.querySelector("[data-hero]");
  const video = document.querySelector("[data-hero-video]");
  if (!video) return;
  const sources = [...video.querySelectorAll("source")].map((source) => ({
    el: source,
    src: source.getAttribute("src"),
  }));
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  const apply = () => {
    if (reduce.matches) {
      hero?.classList.add("is-static");
      video.removeAttribute("autoplay");
      video.setAttribute("preload", "none");
      video.pause();
      sources.forEach(({ el }) => el.removeAttribute("src"));
      video.removeAttribute("src");
      video.load();
      return;
    }
    hero?.classList.remove("is-static");
    video.setAttribute("preload", "metadata");
    sources.forEach(({ el, src }) => {
      if (src) el.setAttribute("src", src);
    });
    video.setAttribute("autoplay", "");
    video.load();
    video.play().catch(() => {});
  };
  apply();
  reduce.addEventListener("change", apply);
}

export function initRoutesFilter() {
  const map = document.querySelector("[data-routes-map]");
  const buttons = document.querySelectorAll("[data-routes-filter]");
  const countries = document.querySelectorAll("[data-routes-countries] [data-region]");
  if (!map || !buttons.length) return;

  const applyFilter = (region) => {
    map.classList.remove("is-europe", "is-asia");
    if (region === "europe") map.classList.add("is-europe");
    if (region === "asia") map.classList.add("is-asia");

    countries.forEach((chip) => {
      const match = region === "all" || chip.getAttribute("data-region") === region;
      chip.classList.toggle("is-active", match && region !== "all");
      chip.classList.toggle("is-dim", region !== "all" && !match);
    });
  };

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((other) => other.classList.remove("is-active"));
      btn.classList.add("is-active");
      applyFilter(btn.getAttribute("data-routes-filter") || "all");
    });
  });

  applyFilter("all");
}
