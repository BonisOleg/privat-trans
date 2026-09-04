function fillLeadFromParams(params) {
  const map = {
    from: "#id_from_city",
    to: "#id_to_city",
    cargo: "#id_cargo",
    note: "#id_message",
  };
  Object.entries(map).forEach(([key, selector]) => {
    const value = params.get(key);
    const field = document.querySelector(selector);
    if (value && field) field.value = value;
  });
}

export function initQuoteBridge() {
  const heroForm = document.querySelector("[data-hero-form]");
  const leadForm = document.querySelector("[data-lead-form]");
  if (heroForm && leadForm) {
    heroForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(heroForm);
      const from = leadForm.querySelector("[name='from_city']");
      const to = leadForm.querySelector("[name='to_city']");
      const cargo = leadForm.querySelector("[name='cargo']");
      const phone = leadForm.querySelector("[name='phone']");
      if (from) from.value = data.get("from") || "";
      if (to) to.value = data.get("to") || "";
      if (cargo) cargo.value = data.get("cargo") || "";
      if (phone && !phone.value) phone.value = data.get("phone") || "";
      document.querySelector("#lead-form")?.scrollIntoView({ behavior: "smooth", block: "start" });
      window.setTimeout(() => leadForm.querySelector("[name='name']")?.focus(), 450);
    });
  }
  fillLeadFromParams(new URLSearchParams(window.location.search));
}
