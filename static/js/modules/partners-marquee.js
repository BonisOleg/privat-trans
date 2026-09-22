const LOOP_PX_PER_SEC = 46;

function debounce(fn, wait = 150) {
  let timer = 0;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), wait);
  };
}

function sourceTiles(track) {
  const marked = [...track.querySelectorAll("[data-partner-source]")];
  if (marked.length) return marked;
  return [...track.children].filter((el) => !el.hasAttribute("aria-hidden"));
}

function whenImagesReady(root) {
  const imgs = [...root.querySelectorAll("img")];
  if (!imgs.length) return Promise.resolve();
  return Promise.all(
    imgs.map((img) => {
      if (img.complete && img.naturalWidth) return Promise.resolve();
      const loaded = new Promise((resolve) => {
        img.addEventListener("load", resolve, { once: true });
        img.addEventListener("error", resolve, { once: true });
      });
      if (typeof img.decode === "function") {
        return img.decode().catch(() => loaded);
      }
      return loaded;
    }),
  );
}

function fillPartnersTrack(wrap, track) {
  const sources = sourceTiles(track);
  if (!sources.length) return;

  const blueprint = sources.map((node) => {
    const clone = node.cloneNode(true);
    clone.removeAttribute("data-partner-source");
    return clone;
  });

  track.replaceChildren();

  const appendSet = (hidden) => {
    blueprint.forEach((node) => {
      const clone = node.cloneNode(true);
      if (hidden) clone.setAttribute("aria-hidden", "true");
      track.appendChild(clone);
    });
  };

  let guard = 0;
  do {
    appendSet(false);
    guard += 1;
  } while (track.scrollWidth < wrap.clientWidth + 24 && guard < 12);

  const unitCount = track.children.length;
  for (let i = 0; i < unitCount; i += 1) {
    const clone = track.children[i].cloneNode(true);
    clone.setAttribute("aria-hidden", "true");
    track.appendChild(clone);
  }
}

function syncLoopDuration(track) {
  const half = track.scrollWidth / 2;
  if (half < 1) return;
  const seconds = Math.max(18, Math.min(80, half / LOOP_PX_PER_SEC));
  track.style.setProperty("--partners-duration", `${seconds.toFixed(1)}s`);
}

export function initPartnersMarquee(root = document) {
  const scope = root instanceof Element ? root : document;
  const wraps = [];
  if (scope.matches?.("[data-partners-marquee]")) wraps.push(scope);
  scope.querySelectorAll?.("[data-partners-marquee]").forEach((el) => wraps.push(el));

  wraps.forEach((wrap) => {
    const track = wrap.querySelector("[data-partners-track]");
    if (!track) return;

    const rebuild = () => {
      if (!wrap._partnerBlueprint) {
        wrap._partnerBlueprint = sourceTiles(track).map((node) => node.cloneNode(true));
      }
      track.replaceChildren(
        ...wrap._partnerBlueprint.map((node) => {
          const clone = node.cloneNode(true);
          clone.setAttribute("data-partner-source", "");
          return clone;
        }),
      );
      fillPartnersTrack(wrap, track);
      syncLoopDuration(track);
    };

    const rebuildWhenReady = () => {
      const sourceRoot = wrap._partnerBlueprint
        ? track
        : wrap;
      return whenImagesReady(sourceRoot).then(rebuild);
    };

    if (wrap.dataset.partnersBound === "true") {
      rebuildWhenReady();
      return;
    }
    wrap.dataset.partnersBound = "true";
    rebuildWhenReady().then(() => {
      wrap.dataset.partnersReady = "true";
    });
    window.addEventListener("resize", debounce(rebuildWhenReady, 180));
  });
}
