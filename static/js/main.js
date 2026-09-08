import { initDrawer, initFaqAccordion, initHeaderScroll, initHeroVideo, initRoutesFilter } from "./nav.js";
import { initReveal } from "./modules/reveal.js";
import { initParallax } from "./modules/parallax.js";
import { initCountUp } from "./modules/count-up.js";
import { initQuoteBridge } from "./pages/home.js";
import { initCustomSelects } from "./modules/custom-select.js";
import { initCalculator } from "./pages/calculator.js";
import { initPartnersMarquee } from "./modules/partners-marquee.js";

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
});

document.body.addEventListener("htmx:afterSwap", (event) => {
  initReveal(event.detail.target);
  initCountUp(event.detail.target);
  initFaqAccordion(event.detail.target);
  initPartnersMarquee(event.detail.target);
});
