const STAGGER_GROUPS = [
  ".grid-3",
  ".grid-8",
  ".grid-auto",
  ".regions-grid",
  ".steps",
  ".corridor-bridge__facts",
  ".fleet-card__facts",
];
const STAGGER_STEP_MS = 70;
const STAGGER_MAX_INDEX = 5;

function applyStagger(root) {
  STAGGER_GROUPS.forEach((selector) => {
    root.querySelectorAll(selector).forEach((group) => {
      const items = [...group.children].filter((el) => el.classList.contains("reveal"));
      items.forEach((el, index) => {
        if (el.style.getPropertyValue("--reveal-delay")) return;
        const delay = Math.min(index, STAGGER_MAX_INDEX) * STAGGER_STEP_MS;
        if (delay > 0) el.style.setProperty("--reveal-delay", `${delay}ms`);
      });
    });
  });
}

export function initReveal(root = document) {
  applyStagger(root);
  const nodes = root.querySelectorAll(".reveal:not(.is-visible):not([data-reveal-hold])");
  if (!nodes.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    nodes.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.01, rootMargin: "24px 0px 0px 0px" },
  );
  const viewportBottom = window.innerHeight || 0;
  nodes.forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.bottom > 0 && rect.top < viewportBottom) {
      el.classList.add("is-visible");
      return;
    }
    observer.observe(el);
  });
}
