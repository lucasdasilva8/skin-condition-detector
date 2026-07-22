/**
 * Bottom tab bar for phone / Capacitor app layout.
 * Habits tab is app-only (hidden on the public website).
 */
(function () {
  const ALL_TABS = [
    { href: "index.html", id: "home", label: "Home" },
    { href: "analyze.html", id: "analyze", label: "Analyze" },
    { href: "history.html", id: "history", label: "History" },
    { href: "reminders.html", id: "habits", label: "Habits", appOnly: true },
    { href: "blog.html", id: "updates", label: "Updates" },
    { href: "about.html", id: "about", label: "About" },
  ];

  function isNative() {
    return Boolean(
      window.APP_CONFIG?.IS_NATIVE || window.Capacitor?.isNativePlatform?.()
    );
  }

  function currentPage() {
    const path = (location.pathname || "").split("/").pop() || "index.html";
    if (!path || path === "" || path === "/") return "index.html";
    return path;
  }

  function mount() {
    document.body.classList.add("app-shell");
    const native = isNative();
    if (native) {
      document.body.classList.add("is-native");
    } else {
      document.body.classList.add("is-web");
    }

    if (document.querySelector(".bottom-tabs")) return;

    const tabs = ALL_TABS.filter((tab) => native || !tab.appOnly);
    const page = currentPage();
    const nav = document.createElement("nav");
    nav.className = "bottom-tabs";
    nav.setAttribute("aria-label", "Main");
    nav.style.setProperty("--tab-count", String(tabs.length));
    nav.innerHTML = tabs
      .map((tab) => {
        const active =
          page === tab.href ||
          (page === "" && tab.href === "index.html") ||
          (tab.href === "index.html" && page === "index.html");
        return `
          <a
            href="${tab.href}"
            class="bottom-tab ${active ? "active" : ""}"
            data-tab="${tab.id}"
            ${active ? 'aria-current="page"' : ""}
          >
            <span class="bottom-tab-icon" aria-hidden="true"></span>
            <span class="bottom-tab-label">${tab.label}</span>
          </a>
        `;
      })
      .join("");

    document.body.appendChild(nav);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
