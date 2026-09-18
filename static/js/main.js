import { initDrawer, initFaqAccordion, initHeaderScroll, initHeroVideo, initRoutesFilter } from "./nav.js";
import { initReveal } from "./modules/reveal.js";
import { initParallax } from "./modules/parallax.js";
import { initCountUp } from "./modules/count-up.js";
import { initQuoteBridge } from "./pages/home.js?v=6";
import { initCustomSelects } from "./modules/custom-select.js?v=2";
import { initCalculator } from "./pages/calculator.js";
import { initPartnersMarquee } from "./modules/partners-marquee.js";
import { initReviewsCarousel } from "./modules/reviews-carousel.js";
import { initGallery } from "./modules/gallery.js";
import { initAnalytics } from "./modules/analytics.js";

const PT_CITIES = [
  "Київ", "Одеса", "Львів", "Дніпро", "Харків",
  "Warsaw", "Gdańsk", "Berlin", "Munich", "Prague", "Budapest", "Bucharest", "Sofia",
  "Istanbul", "Tbilisi", "Baku", "Almaty", "Tashkent", "Riyadh", "Shanghai",
];

function initCityDatalists() {
  document.querySelectorAll("datalist[data-cities]").forEach((list) => {
    list.replaceChildren(
      ...PT_CITIES.map((city) => {
        const option = document.createElement("option");
        option.value = city;
        return option;
      }),
    );
  });
}

function initCitySelects() {
  document.querySelectorAll("select[data-cities-select]").forEach((select) => {
    if (select.dataset.citiesReady === "true") return;
    PT_CITIES.forEach((city) => {
      const option = document.createElement("option");
      option.value = city;
      option.textContent = city;
      select.appendChild(option);
    });
    select.dataset.citiesReady = "true";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initAnalytics();
  initCityDatalists();
  initCitySelects();
  initHeaderScroll();
  initDrawer();
  initFaqAccordion();
  initHeroVideo();
  initRoutesFilter();
  initReveal();
  initParallax();
  initCountUp();
  initCustomSelects();
  initQuoteBridge();
  initCalculator();
  initPartnersMarquee();
  initReviewsCarousel();
  initGallery();
});

document.body.addEventListener("htmx:afterSwap", (event) => {
  const target = event.detail.target;
  initCitySelects();
  initCustomSelects(target);
  initReveal(target);
  initCountUp(target);
  initFaqAccordion(target);
  initPartnersMarquee(target);
  initReviewsCarousel(target);
  initGallery(target);
});
