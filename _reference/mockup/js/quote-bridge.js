/*
  quote-bridge.js — місток між міні-формою в hero та повною формою заявки #lead-form.
  Також приймає дані з калькулятора через query-параметри (?from=&to=&cargo=&note=).
*/

function fillLeadFromParams(params) {
  const map = {
    from: '#lead-from',
    to: '#lead-to',
    cargo: '#lead-cargo',
    note: '#lead-message'
  };
  let filledAny = false;
  Object.entries(map).forEach(([key, selector]) => {
    const value = params.get(key);
    const field = document.querySelector(selector);
    if (value && field) {
      field.value = value;
      filledAny = true;
    }
  });
  return filledAny;
}

function bridgeHeroForm() {
  const heroForm = document.querySelector('[data-hero-form]');
  const leadForm = document.querySelector('[data-lead-form]');
  if (!heroForm || !leadForm) return;

  heroForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(heroForm);
    ['from', 'to', 'cargo'].forEach((key) => {
      const value = data.get(key);
      const target = leadForm.querySelector(`[name="${key}"]`);
      if (value && target) target.value = value;
    });
    const phone = data.get('phone');
    const leadPhone = leadForm.querySelector('[name="phone"]');
    if (phone && leadPhone && !leadPhone.value) leadPhone.value = phone;

    const leadFormSection = document.querySelector('#lead-form');
    leadFormSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    window.setTimeout(() => {
      leadForm.querySelector('[name="name"]')?.focus();
    }, 450);
  });
}

function initLeadFormSubmit() {
  const leadForm = document.querySelector('[data-lead-form]');
  const success = document.querySelector('[data-form-success]');
  if (!leadForm) return;

  leadForm.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!leadForm.checkValidity()) {
      leadForm.reportValidity();
      return;
    }
    success?.setAttribute('data-visible', 'true');
    leadForm.reset();
    success?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}

function prefillServiceFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const service = params.get('service');
  if (!service) return;

  document.querySelectorAll('[data-service-name]').forEach((el) => {
    el.textContent = service;
  });
  const serviceField = document.querySelector('#lead-service');
  if (serviceField) serviceField.value = service;
}

document.addEventListener('DOMContentLoaded', () => {
  bridgeHeroForm();
  initLeadFormSubmit();
  prefillServiceFromQuery();

  const leadForm = document.querySelector('[data-lead-form]');
  if (leadForm) {
    const params = new URLSearchParams(window.location.search);
    fillLeadFromParams(params);
  }
});
