/*
  calculator.js — орієнтовний мок-розрахунок вартості перевезення.
  Не реальна тарифна формула: демонстрація UX для клієнта, дані не зберігаються і нікуди не відправляються.
*/

const BASE_FEE_EUR = 90;
const RATE_PER_KG = { ltl: 0.32, ftl: 0.11, container: 0.07 };
const RATE_PER_M3 = 9;
const BODY_MULTIPLIER = { tent: 1, reef: 1.28, adr: 1.4, oversize: 1.55 };

function calcRange(formData) {
  const weight = Math.max(parseFloat(formData.get('weight')) || 0, 0);
  const volume = Math.max(parseFloat(formData.get('volume')) || 0, 0);
  const type = formData.get('type') || 'ltl';
  const body = formData.get('body') || 'tent';

  const rate = RATE_PER_KG[type] ?? RATE_PER_KG.ltl;
  const bodyMultiplier = BODY_MULTIPLIER[body] ?? 1;

  const raw = (BASE_FEE_EUR + weight * rate + volume * RATE_PER_M3) * bodyMultiplier;
  const min = Math.round((raw * 0.85) / 10) * 10;
  const max = Math.round((raw * 1.25) / 10) * 10;
  return { min: Math.max(min, 60), max: Math.max(max, 90) };
}

function initCalculator() {
  const form = document.querySelector('[data-calculator-form]');
  const result = document.querySelector('[data-calc-result]');
  const empty = document.querySelector('[data-calc-empty]');
  const rangeEl = document.querySelector('[data-calc-range]');
  const summaryEl = document.querySelector('[data-calc-summary]');
  const leadLink = document.querySelector('[data-calc-to-lead]');
  if (!form || !result) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const { min, max } = calcRange(data);

    const from = data.get('from') || '—';
    const to = data.get('to') || '—';
    const weight = data.get('weight') || '—';

    if (rangeEl) rangeEl.textContent = `€${min}–${max}`;
    if (summaryEl) {
      summaryEl.textContent = `${from} → ${to}, ${weight} кг`;
    }

    result.setAttribute('data-visible', 'true');
    if (empty) empty.style.display = 'none';

    if (leadLink) {
      const params = new URLSearchParams({
        from,
        to,
        note: `Орієнтовний розрахунок: ${from} → ${to}, ${weight} кг, ~€${min}–${max}`
      });
      leadLink.href = `index.html?${params.toString()}#lead-form`;
    }
  });
}

document.addEventListener('DOMContentLoaded', initCalculator);
