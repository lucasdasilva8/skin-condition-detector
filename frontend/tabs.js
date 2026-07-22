/**
 * Bottom tab bar for phone / Capacitor app layout.
 */
(function () {
  const tabs = [
    { href: "index.html", id: "home", label: "Home" },
    { href: "analyze.html", id: "analyze", label: "Analyze" },
    { href: "history.html", id: "history", label: "History" },
    { href: "reminders.html", id: "habits", label: "Habits" },
    { href: "blog.html", id: "updates", label: "Updates" },
    { href: "about.html", id: "about", label: "About" },
  ];

  function currentPage() {
    const path = (location.pathname || "").split("/").pop() || "index.html";
    if (!path || path === "" || path === "/") return "index.html";
    return path;
  }

  function mount() {
    document.body.classList.add("app-shell");
    if (window.APP_CONFIG?.IS_NATIVE || window.Capacitor?.isNativePlatform?.()) {
      document.body.classList.add("is-native");
    }

    if (document.querySelector(".bottom-tabs")) return;

    const page = currentPage();
    const nav = document.createElement("nav");
    nav.className = "bottom-tabs";
    nav.setAttribute("aria-label", "Main");
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
