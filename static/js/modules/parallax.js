/**
 * Легкий паралакс: лише transform + rAF.
 * Hero — від scrollY; секції — відносний зсув фонового шару.
 */
export function initParallax() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const layers = [];

  document.querySelectorAll("[data-parallax]").forEach((el) => {
    layers.push({
      el,
      speed: Number.parseFloat(el.dataset.parallax ?? "0.2") || 0.2,
      mode: el.dataset.parallaxMode || "relative",
    });
  });

  document.querySelectorAll(".section--alt, .section--soft").forEach((section) => {
    if (section.querySelector("[data-parallax-layer]")) return;
    const layer = document.createElement("div");
    layer.className = "section__parallax-layer";
    layer.setAttribute("data-parallax-layer", "");
    layer.setAttribute("aria-hidden", "true");
    section.prepend(layer);
    section.classList.add("has-parallax-bg");
    layers.push({
      el: layer,
      speed: section.classList.contains("section--alt") ? 0.06 : 0.08,
      mode: "relative",
      host: section,
    });
  });

  if (!layers.length) return;

  let ticking = false;

  const update = () => {
    const scrollY = window.scrollY;
    const viewportMid = window.innerHeight * 0.5;

    layers.forEach(({ el, speed, mode, host }) => {
      let y = 0;
      if (mode === "scroll") {
        y = scrollY * speed;
      } else {
        const rect = (host || el).getBoundingClientRect();
        y = (rect.top + rect.height * 0.5 - viewportMid) * -speed;
      }
      el.style.transform = `translate3d(0, ${y.toFixed(2)}px, 0)`;
    });

    ticking = false;
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(update);
  };

  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
}
