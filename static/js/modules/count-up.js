/**
 * Лічильник-анімація для чисел (факти, діапазон калькулятора).
 * Прогресивне покращення: у розмітці вже лежить фінальне значення,
 * тож без JS або з prefers-reduced-motion користувач бачить коректне число миттєво.
 */
const DEFAULT_DURATION_MS = 900;

function animateCount(el) {
  const target = Number.parseFloat(el.dataset.countTo);
  if (Number.isNaN(target)) return;

  const duration = Number.parseInt(el.dataset.countDuration, 10) || DEFAULT_DURATION_MS;
  const start = performance.now();

  const step = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = Math.round(target * eased);
    el.textContent = String(value);
    if (progress < 1) {
      requestAnimationFrame(step);
    } else {
      el.textContent = String(target);
    }
  };

  requestAnimationFrame(step);
}

export function initCountUp(root = document) {
  const nodes = root.querySelectorAll("[data-count-to]:not([data-count-done])");
  if (!nodes.length) return;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.setAttribute("data-count-done", "true");
          animateCount(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 },
  );

  nodes.forEach((el) => observer.observe(el));
}
