(function () {
  function initTabs(root) {
    var buttons = root.querySelectorAll("[data-cms-lang]");
    var panels = root.querySelectorAll("[data-cms-panel]");
    if (!buttons.length || !panels.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var lang = btn.getAttribute("data-cms-lang");
        buttons.forEach(function (b) {
          var on = b === btn;
          b.classList.toggle("is-active", on);
          b.setAttribute("aria-selected", on ? "true" : "false");
        });
        panels.forEach(function (panel) {
          var match = panel.getAttribute("data-cms-panel") === lang;
          panel.classList.toggle("is-active", match);
          if (match) {
            panel.removeAttribute("hidden");
          } else {
            panel.setAttribute("hidden", "hidden");
          }
        });
      });
    });
  }

  function syncTinyMCE() {
    var tinymce = window.tinymce;
    if (!tinymce) return;
    if (typeof tinymce.triggerSave === "function") {
      tinymce.triggerSave();
    }
    if (tinymce.editors) {
      tinymce.editors.forEach(function (ed) {
        if (ed && typeof ed.save === "function") ed.save();
      });
    }
  }

  function boot() {
    document.querySelectorAll("[data-cms-lang-tabs]").forEach(initTabs);
    document.querySelectorAll(".site-content-editor form").forEach(function (form) {
      form.addEventListener("submit", function () {
        syncTinyMCE();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
