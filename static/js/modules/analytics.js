function safeAnalyticsId(value) {
  return /^[A-Z0-9-]+$/i.test(value || "") ? value : "";
}

function loadExternalScript(src) {
  const script = document.createElement("script");
  script.src = src;
  script.async = true;
  document.head.appendChild(script);
}

export function initAnalytics() {
  const el = document.getElementById("pt-analytics");
  if (!el) return;

  const gtm = safeAnalyticsId(el.getAttribute("data-gtm"));
  const ga4 = safeAnalyticsId(el.getAttribute("data-ga4"));
  window.dataLayer = window.dataLayer || [];

  if (gtm) {
    window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
    loadExternalScript(`https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(gtm)}`);
    return;
  }

  if (!ga4) return;
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };
  window.gtag("js", new Date());
  window.gtag("config", ga4);
  loadExternalScript(`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(ga4)}`);
}
