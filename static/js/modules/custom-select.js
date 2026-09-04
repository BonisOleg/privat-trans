/**
 * Кастомний select: listbox вниз, синхрон з native <select>.
 * Маркер: [data-pt-select] + select[data-pt-select-native]
 */
export function initCustomSelects(root = document) {
  root.querySelectorAll("[data-pt-select]").forEach((wrap) => {
    if (wrap.dataset.ready === "true") return;
    const native = wrap.querySelector("[data-pt-select-native]");
    if (!(native instanceof HTMLSelectElement)) return;

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const options = [...native.options];
    if (!options.length) return;

    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "pt-select__trigger";
    trigger.setAttribute("aria-haspopup", "listbox");
    trigger.setAttribute("aria-expanded", "false");
    if (native.id) trigger.setAttribute("aria-controls", `${native.id}-list`);
    trigger.innerHTML =
      '<span class="pt-select__value"></span>' +
      '<svg class="pt-select__chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';

    const valueEl = trigger.querySelector(".pt-select__value");
    const list = document.createElement("ul");
    list.className = "pt-select__list";
    list.setAttribute("role", "listbox");
    list.id = native.id ? `${native.id}-list` : "";
    list.setAttribute("aria-hidden", "true");

    options.forEach((opt, index) => {
      const item = document.createElement("li");
      item.className = "pt-select__option";
      item.setAttribute("role", "option");
      item.dataset.value = opt.value;
      item.dataset.index = String(index);
      item.textContent = opt.textContent || opt.value;
      item.tabIndex = -1;
      list.appendChild(item);
    });

    wrap.append(trigger, list);
    wrap.dataset.ready = "true";
    wrap.classList.add("is-ready");
    native.tabIndex = -1;
    native.setAttribute("aria-hidden", "true");

    const syncFromNative = () => {
      const selected = native.selectedOptions[0] || options[0];
      valueEl.textContent = selected?.textContent || selected?.value || "";
      wrap.classList.toggle("is-placeholder", !native.value);
      list.querySelectorAll(".pt-select__option").forEach((item) => {
        const isSelected = item.dataset.value === native.value;
        item.setAttribute("aria-selected", isSelected ? "true" : "false");
        item.classList.toggle("is-selected", isSelected);
      });
    };

    const field = wrap.closest(".field");

    const close = () => {
      wrap.classList.remove("is-open");
      field?.classList.remove("has-select-open");
      trigger.setAttribute("aria-expanded", "false");
      list.setAttribute("aria-hidden", "true");
    };

    const open = () => {
      list.setAttribute("aria-hidden", "false");
      trigger.setAttribute("aria-expanded", "true");
      field?.classList.add("has-select-open");
      requestAnimationFrame(() => {
        wrap.classList.add("is-open");
        list.querySelector(".is-selected")?.focus();
      });
    };

    const toggle = () => {
      if (wrap.classList.contains("is-open")) close();
      else open();
    };

    const choose = (item) => {
      if (!item) return;
      native.value = item.dataset.value;
      native.dispatchEvent(new Event("change", { bubbles: true }));
      syncFromNative();
      close();
      trigger.focus();
    };

    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      toggle();
    });

    list.addEventListener("click", (event) => {
      const item = event.target.closest(".pt-select__option");
      if (item) choose(item);
    });

    trigger.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown" || event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        if (!wrap.classList.contains("is-open")) open();
        else list.querySelector(".is-selected")?.focus();
      }
      if (event.key === "Escape") close();
    });

    list.addEventListener("keydown", (event) => {
      const items = [...list.querySelectorAll(".pt-select__option")];
      const current = document.activeElement;
      const index = items.indexOf(current);
      if (event.key === "ArrowDown") {
        event.preventDefault();
        items[Math.min(index + 1, items.length - 1)]?.focus();
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        items[Math.max(index - 1, 0)]?.focus();
      } else if (event.key === "Home") {
        event.preventDefault();
        items[0]?.focus();
      } else if (event.key === "End") {
        event.preventDefault();
        items[items.length - 1]?.focus();
      } else if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        choose(current?.closest?.(".pt-select__option") || current);
      } else if (event.key === "Escape") {
        event.preventDefault();
        close();
        trigger.focus();
      } else if (event.key === "Tab") {
        close();
      }
    });

    document.addEventListener("click", (event) => {
      if (!wrap.contains(event.target)) close();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && wrap.classList.contains("is-open")) {
        close();
        trigger.focus();
      }
    });

    if (reduceMotion) wrap.classList.add("is-reduced-motion");

    const label = native.id ? document.querySelector(`label[for="${native.id}"]`) : null;
    label?.addEventListener("click", (event) => {
      event.preventDefault();
      trigger.focus();
    });

    syncFromNative();
  });
}
