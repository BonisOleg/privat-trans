function breakpointVisible() {
  if (window.matchMedia("(min-width: 1024px)").matches) return 3;
  if (window.matchMedia("(min-width: 768px)").matches) return 2;
  return 1;
}

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function slideStep(track, slide) {
  if (!slide) return 0;
  const margin = parseFloat(window.getComputedStyle(slide).marginRight) || 0;
  return slide.getBoundingClientRect().width + margin;
}

function bindCarousel(root) {
  const track = root.querySelector("[data-reviews-track]");
  const prev = root.querySelector("[data-reviews-prev]");
  const next = root.querySelector("[data-reviews-next]");
  const dots = [...root.querySelectorAll("[data-reviews-dot]")];
  const hint = root.closest("#reviews")?.querySelector("[data-reviews-hint]");
  if (!(track instanceof HTMLElement)) return;

  const slides = [...track.querySelectorAll(".reviews-carousel__slide")];
  if (!slides.length) return;

  const state = { index: 0, visible: 1, max: 0, step: 0 };

  function metrics() {
    const visible = Math.min(slides.length, breakpointVisible());
    root.dataset.reviewsVisible = String(visible);
    state.visible = visible;
    state.step = slideStep(track, slides[0]);
    state.max = Math.max(0, slides.length - visible);
    return state;
  }

  function scrollable() {
    return state.max > 0 && track.scrollWidth > track.clientWidth + 2;
  }

  function syncFromScroll() {
    if (state.step <= 0) return;
    state.index = Math.min(state.max, Math.max(0, Math.round(track.scrollLeft / state.step)));
  }

  function render() {
    const canScroll = scrollable();
    const atStart = state.index <= 0;
    const atEnd = state.index >= state.max || !canScroll;
    root.dataset.reviewsScrollable = canScroll ? "true" : "false";
    root.dataset.reviewsAtEnd = atEnd ? "true" : "false";
    if (prev instanceof HTMLButtonElement) prev.disabled = atStart || !canScroll;
    if (next instanceof HTMLButtonElement) next.disabled = atEnd || !canScroll;
    dots.forEach((dot, i) => {
      if (i === state.index) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });
    if (hint) {
      const showHint = canScroll && !atEnd && window.matchMedia("(max-width: 767px)").matches;
      hint.hidden = !showHint;
    }
  }

  function goTo(index) {
    metrics();
    const nextIndex = Math.min(state.max, Math.max(0, index));
    track.scrollTo({
      left: nextIndex * state.step,
      behavior: prefersReducedMotion() ? "auto" : "smooth",
    });
    state.index = nextIndex;
    render();
  }

  function refresh() {
    metrics();
    syncFromScroll();
    render();
  }

  if (root.dataset.reviewsReady === "true") {
    refresh();
    return;
  }
  root.dataset.reviewsReady = "true";

  prev?.addEventListener("click", () => goTo(state.index - 1));
  next?.addEventListener("click", () => goTo(state.index + 1));
  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const index = Number(dot.getAttribute("data-reviews-dot"));
      if (Number.isFinite(index)) goTo(index);
    });
  });

  track.addEventListener("scroll", () => {
    window.requestAnimationFrame(() => {
      syncFromScroll();
      render();
    });
  }, { passive: true });

  track.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      goTo(state.index - 1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      goTo(state.index + 1);
    }
  });

  window.addEventListener("resize", refresh);
  if (typeof ResizeObserver === "function") {
    new ResizeObserver(refresh).observe(track);
  }

  root.classList.add("is-ready");
  refresh();
}

export function initReviewsCarousel(root = document) {
  const scope = root instanceof Element ? root : document;
  const nodes = [];
  if (scope.matches?.("[data-reviews-carousel]")) nodes.push(scope);
  scope.querySelectorAll?.("[data-reviews-carousel]").forEach((el) => nodes.push(el));
  nodes.forEach(bindCarousel);
}
