export function initReveal(root = document) {
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
    { threshold: 0.12, rootMargin: "0px 0px -48px 0px" },
  );
  nodes.forEach((el) => observer.observe(el));
}
