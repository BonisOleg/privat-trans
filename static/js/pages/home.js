function setSelectValue(select, value) {
  if (!(select instanceof HTMLSelectElement) || value == null || value === "") return;
  const options = [...select.options];
  if (options.some((option) => option.value === value)) {
    select.value = value;
  } else {
    const byText = options.find((option) => option.textContent.trim() === value);
    if (byText) {
      select.value = byText.value;
    } else {
      const lower = String(value).toLowerCase();
      if (lower.includes("ftl") || lower.includes("повне")) select.value = "ftl";
      else if (lower.includes("контейнер") || lower.includes("container") || lower.includes("під ключ") || lower.includes("turnkey")) {
        select.value = "turnkey";
      } else if (lower.includes("ltl") || lower.includes("збір")) select.value = "ltl";
      else return;
    }
  }
  select.dispatchEvent(new Event("change", { bubbles: true }));
}

function fillLeadFromParams(params) {
  const leadForm = document.querySelector("[data-lead-form]");
  if (!leadForm) return;
  setSelectValue(leadForm.querySelector("[name='from_city']"), params.get("from"));
  setSelectValue(leadForm.querySelector("[name='to_city']"), params.get("to"));
  setSelectValue(leadForm.querySelector("[name='cargo']"), params.get("cargo"));
  const note = params.get("note");
  const message = leadForm.querySelector("[name='message']");
  if (note && message) message.value = note;
}

function focusLeadName() {
  const leadForm = document.querySelector("[data-lead-form]");
  window.setTimeout(() => leadForm?.querySelector("[name='name']")?.focus(), 450);
}

export function initQuoteBridge() {
  const heroForm = document.querySelector("[data-hero-form]");
  const leadForm = document.querySelector("[data-lead-form]");
  if (heroForm && leadForm) {
    heroForm.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!heroForm.checkValidity()) return;
      const data = new FormData(heroForm);
      setSelectValue(leadForm.querySelector("[name='from_city']"), data.get("from"));
      setSelectValue(leadForm.querySelector("[name='to_city']"), data.get("to"));
      setSelectValue(leadForm.querySelector("[name='cargo']"), data.get("cargo"));
      const phone = leadForm.querySelector("[name='phone']");
      if (phone && !phone.value) phone.value = data.get("phone") || "";
      document.querySelector("#lead-form")?.scrollIntoView({ behavior: "smooth", block: "start" });
      focusLeadName();
    });
  }

  document.querySelectorAll('a[href="#lead-form"]').forEach((link) => {
    link.addEventListener("click", () => {
      if (window.matchMedia("(max-width: 767px)").matches) focusLeadName();
    });
  });

  fillLeadFromParams(new URLSearchParams(window.location.search));
  if (window.location.hash === "#lead-form") focusLeadName();
}
