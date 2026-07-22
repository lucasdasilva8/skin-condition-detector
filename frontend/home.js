/** Canonical short names — keep in sync with backend/condition_catalog.py */
const CONDITION_SHORT_NAMES = [
  "Acne",
  "Actinic Keratosis",
  "Benign Tumor",
  "Bullous",
  "Candidiasis",
  "Drug Reaction",
  "Eczema",
  "Bites/Infestations",
  "Lichen",
  "Lupus",
  "Moles",
  "Psoriasis",
  "Rosacea",
  "Seborrheic Keratosis",
  "Skin Cancer",
  "Sun Damage",
  "Tinea",
  "Normal",
  "Vascular Tumor",
  "Vasculitis",
  "Vitiligo",
  "Warts",
];

function isNativeApp() {
  return Boolean(
    window.APP_CONFIG?.IS_NATIVE || window.Capacitor?.isNativePlatform?.()
  );
}

function renderConditionsGrid(names = CONDITION_SHORT_NAMES) {
  const grid = document.getElementById("conditions-grid");
  if (!grid) return;
  grid.innerHTML = names
    .map((name) => `<li class="condition-chip">${name}</li>`)
    .join("");
}

async function refreshConditionsFromApi() {
  const apiUrl = window.APP_CONFIG?.API_URL;
  if (!apiUrl) return;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 4000);
  try {
    const response = await fetch(`${apiUrl}/conditions`, {
      signal: controller.signal,
    });
    if (!response.ok) return;
    const data = await response.json();
    const names = (data.conditions || [])
      .map((item) => item.short_name || item.name)
      .filter(Boolean);
    if (names.length) renderConditionsGrid(names);
  } catch {
    // Static list already on the page — API is optional for this section.
  } finally {
    clearTimeout(timer);
  }
}

function habitHomeItem(habit, state, store) {
  const checked = store.isChecked(habit.id, state);
  return `
    <li>
      <label class="habit-check-row ${checked ? "is-done" : ""}">
        <input type="checkbox" data-habit-id="${habit.id}" ${checked ? "checked" : ""} />
        <span>
          <strong>${habit.label}</strong>
          <span class="habit-fun-fact">${habit.funFact || ""}</span>
        </span>
      </label>
    </li>
  `;
}

function ensureHabitsHomeSection() {
  if (document.getElementById("home-habits-list")) return true;
  const mainCol = document.querySelector(".home-main");
  if (!mainCol) return false;
  const anchor = mainCol.querySelector(".section");
  const section = document.createElement("section");
  section.className = "section habits-home-section";
  section.innerHTML = `
    <div class="habits-home-header">
      <h2>Today’s habits</h2>
      <a href="reminders.html" class="btn btn-ghost">Open Habits →</a>
    </div>
    <p id="home-habits-progress" class="section-lead">Loading today’s checklist…</p>
    <div id="home-habits-list" class="habit-today-groups"></div>
  `;
  // Place after "How to use it" (second section) when possible
  const sections = mainCol.querySelectorAll(".section");
  if (sections.length >= 2) {
    sections[1].after(section);
  } else if (anchor) {
    anchor.after(section);
  } else {
    mainCol.prepend(section);
  }
  return true;
}

function renderHomeHabits() {
  if (!isNativeApp()) return;
  if (!ensureHabitsHomeSection()) return;
  const store = window.SkinScanHabits;
  const listEl = document.getElementById("home-habits-list");
  const progressEl = document.getElementById("home-habits-progress");
  if (!store || !listEl) return;

  const state = store.load();
  const { done, total } = store.progress(state);
  const morning = store.habitsByPeriod("morning", state);
  const afternoon = store.habitsByPeriod("afternoon", state);

  if (progressEl) {
    progressEl.textContent =
      total === 0
        ? "Enable habits on the Habits tab to build a daily routine."
        : `${done} of ${total} done today — morning and afternoon check-offs with a quick “why it helps.”`;
  }

  if (!morning.length && !afternoon.length) {
    listEl.innerHTML =
      '<p class="muted"><a href="reminders.html">Set up your habits →</a></p>';
    return;
  }

  const block = (title, habits) => {
    if (!habits.length) return "";
    return `
      <div class="habit-period-block">
        <h3 class="habit-period-title">${title}</h3>
        <ul class="habit-checklist habit-checklist-compact">
          ${habits.map((h) => habitHomeItem(h, state, store)).join("")}
        </ul>
      </div>
    `;
  };

  listEl.innerHTML = block("Morning", morning) + block("Afternoon", afternoon);
}

document.addEventListener("change", (event) => {
  const input = event.target;
  const store = window.SkinScanHabits;
  if (!(input instanceof HTMLInputElement) || !input.dataset.habitId || !store) return;
  if (!document.getElementById("home-habits-list")?.contains(input)) return;
  store.setChecked(input.dataset.habitId, input.checked);
  renderHomeHabits();
});

window.addEventListener("skinscan-habits-updated", renderHomeHabits);

renderConditionsGrid();
refreshConditionsFromApi();
if (isNativeApp()) {
  renderHomeHabits();
}
