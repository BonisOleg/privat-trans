export function initHeaderScroll() {
  const header = document.querySelector("[data-header]");
  if (!header) return;

  const update = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };

  header.classList.add("header--ready");
  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update, { passive: true });
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

export function initFaqAccordion(root = document) {
  const scope = root instanceof Element ? root : document;
  const groups = [];
  if (scope.matches?.("[data-faq]")) {
    groups.push(scope);
  }
  scope.querySelectorAll?.("[data-faq]").forEach((group) => groups.push(group));

  groups.forEach((group) => {
    if (group.dataset.faqReady === "true") return;
    group.dataset.faqReady = "true";
    group.classList.add("faq-list");

    const items = [...group.querySelectorAll(".faq-item")];
    if (!items.length) return;

    const setOpen = (item, open) => {
      item.setAttribute("data-open", open ? "true" : "false");
      item.querySelector(".faq-item__q")?.setAttribute("aria-expanded", open ? "true" : "false");
    };

    const hasOpen = items.some((item) => item.getAttribute("data-open") === "true");
    if (!hasOpen) {
      setOpen(items[0], true);
    }

    items.forEach((item) => {
      const btn = item.querySelector(".faq-item__q");
      if (!btn) return;
      btn.addEventListener("click", () => {
        const willClose = item.getAttribute("data-open") === "true";
        items.forEach((other) => setOpen(other, false));
        if (!willClose) {
          setOpen(item, true);
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
  if (!map || !buttons.length) return;

  const applyFilter = (region) => {
    const safeRegion = region === "europe" || region === "asia" ? region : "all";
    map.dataset.filter = safeRegion;
    map.classList.remove("is-europe", "is-asia", "is-all");
    map.classList.add(safeRegion === "all" ? "is-all" : `is-${safeRegion}`);

    buttons.forEach((btn) => {
      const active = (btn.getAttribute("data-routes-filter") || "all") === safeRegion;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  };

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      applyFilter(btn.getAttribute("data-routes-filter") || "all");
    });
  });

  applyFilter("all");
}
