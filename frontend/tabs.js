/**
 * Bottom tab bar for phone / Capacitor app layout.
 * Habits is app-only — never shown on the public website.
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
    const cap = window.Capacitor || window.SkinScanNative?.Capacitor;
    if (window.APP_CONFIG && typeof window.APP_CONFIG.IS_NATIVE === "boolean") {
      return window.APP_CONFIG.IS_NATIVE;
    }
    return Boolean(cap && typeof cap.isNativePlatform === "function" && cap.isNativePlatform());
  }

  function currentPage() {
    const path = (location.pathname || "").split("/").pop() || "index.html";
    if (!path || path === "" || path === "/") return "index.html";
    return path;
  }

  function injectDesktopHabitsLink() {
    const links = document.querySelector(".nav-links");
    if (!links || links.querySelector('[data-nav="habits"]')) return;
    const updates = links.querySelector('a[href="blog.html"]');
    const a = document.createElement("a");
    a.href = "reminders.html";
    a.className = "nav-link";
    a.dataset.nav = "habits";
    a.textContent = "Habits";
    if (currentPage() === "reminders.html") {
      a.classList.add("active");
    }
    if (updates) {
      links.insertBefore(a, updates);
    } else {
      links.appendChild(a);
    }
  }

  function mount() {
    document.body.classList.add("app-shell");
    const native = isNative();
    if (native) {
      document.documentElement.classList.remove("is-web");
      document.documentElement.classList.add("is-native");
      document.body.classList.remove("is-web");
      document.body.classList.add("is-native");
      injectDesktopHabitsLink();
    } else {
      document.documentElement.classList.add("is-web");
      document.body.classList.add("is-web");
      document.documentElement.classList.remove("is-native");
      document.body.classList.remove("is-native");
    }

    if (document.querySelector(".bottom-tabs")) return;

    const tabs = ALL_TABS.filter((tab) => (native ? true : !tab.appOnly));
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
