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

  // Grow one half until it covers the viewport (plus buffer).
  let guard = 0;
  do {
    appendSet(false);
    guard += 1;
  } while (track.scrollWidth < wrap.clientWidth + 24 && guard < 12);

  // Exact duplicate for seamless translateX(-50%).
  const unitCount = track.children.length;
  for (let i = 0; i < unitCount; i += 1) {
    const clone = track.children[i].cloneNode(true);
    clone.setAttribute("aria-hidden", "true");
    track.appendChild(clone);
  }
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
      // Keep original sources as templates in a fragment store on first run.
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
    };

    rebuild();
    if (wrap.dataset.partnersReady === "true") return;
    wrap.dataset.partnersReady = "true";
    window.addEventListener("resize", debounce(rebuild, 180));
  });
}
