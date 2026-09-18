export function initGallery(root = document) {
  root.querySelectorAll("[data-gallery]").forEach(bindGallery);
}

function bindGallery(section) {
  if (section.dataset.galleryReady === "true") return;
  const dialog = section.querySelector("[data-gallery-dialog]");
  const full = section.querySelector("[data-gallery-full]");
  const tiles = [...section.querySelectorAll("[data-gallery-open]")];
  if (!dialog || !full || !tiles.length) return;

  const items = tiles.map((tile) => {
    const img = tile.querySelector("img");
    return { src: img?.currentSrc || img?.src || "", alt: img?.alt || "" };
  });

  let index = 0;

  const show = (next) => {
    index = (next + items.length) % items.length;
    full.src = items[index].src;
    full.alt = items[index].alt;
  };

  const open = (next) => {
    show(next);
    if (typeof dialog.showModal === "function") dialog.showModal();
  };

  const close = () => {
    if (dialog.open) dialog.close();
  };

  tiles.forEach((tile, tileIndex) => {
    tile.addEventListener("click", () => open(tileIndex));
  });
  section.querySelector("[data-gallery-close]")?.addEventListener("click", close);
  section.querySelector("[data-gallery-prev]")?.addEventListener("click", () => show(index - 1));
  section.querySelector("[data-gallery-next]")?.addEventListener("click", () => show(index + 1));
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) close();
  });
  dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") show(index - 1);
    if (event.key === "ArrowRight") show(index + 1);
  });

  let touchX = null;
  dialog.addEventListener("touchstart", (event) => {
    touchX = event.changedTouches[0]?.clientX ?? null;
  }, { passive: true });
  dialog.addEventListener("touchend", (event) => {
    if (touchX == null) return;
    const delta = (event.changedTouches[0]?.clientX ?? touchX) - touchX;
    if (Math.abs(delta) > 40) show(index + (delta < 0 ? 1 : -1));
    touchX = null;
  }, { passive: true });

  section.dataset.galleryReady = "true";
}
