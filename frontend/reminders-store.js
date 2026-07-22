/**
 * Shared daily skin-care habits store (localStorage).
 * Used by Home and the Habits tab.
 */
(function (global) {
  const STORAGE_KEY = "skinscan_habits_v2";

  const DEFAULT_HABITS = [
    {
      id: "sunscreen",
      label: "Apply sunscreen",
      detail: "Broad-spectrum SPF in the morning, even on cloudy days.",
      funFact:
        "Up to 80% of UV rays can pass through clouds, so morning SPF still matters on gray days.",
      period: "morning",
      enabled: true,
    },
    {
      id: "water",
      label: "Drink water",
      detail: "A few glasses across the morning supports skin comfort.",
      funFact:
        "Well-hydrated skin isn’t about one giant bottle — steady sips help your skin barrier feel more comfortable.",
      period: "morning",
      enabled: true,
    },
    {
      id: "nourish",
      label: "Eat something nourishing",
      detail: "Include veggies, fruit, or protein with breakfast or a morning snack.",
      funFact:
        "Foods rich in colorful plants give your body antioxidants that support skin from the inside.",
      period: "morning",
      enabled: true,
    },
    {
      id: "cleanse",
      label: "Gentle afternoon cleanse",
      detail: "If your face feels oily or dusty midday, a mild wash helps — no harsh scrubbing.",
      funFact:
        "Overwashing can strip oils and make skin look duller; gentle cleansing protects the barrier that keeps moisture in.",
      period: "afternoon",
      enabled: true,
    },
    {
      id: "moisturize",
      label: "Moisturize",
      detail: "Reapply a moisturizer if skin feels tight after washing or air conditioning.",
      funFact:
        "Moisturizer works best on slightly damp skin — it seals in water instead of sitting on dry surface.",
      period: "afternoon",
      enabled: true,
    },
    {
      id: "skin_check",
      label: "Quick skin check",
      detail: "In good light, glance at moles or spots you watch; note any changes.",
      funFact:
        "Many skin cancers are found by people noticing a spot that looked different — a 30-second check adds awareness.",
      period: "afternoon",
      enabled: true,
    },
  ];

  const PERIOD_MIGRATE = {
    evening: "afternoon",
    anytime: "afternoon",
  };

  function todayKey(date = new Date()) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    return `${y}-${m}-${d}`;
  }

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY) || localStorage.getItem("skinscan_habits_v1");
      if (!raw) return createDefaultState();
      const parsed = JSON.parse(raw);
      return normalize(parsed);
    } catch {
      return createDefaultState();
    }
  }

  function createDefaultState() {
    return {
      habits: DEFAULT_HABITS.map((h) => ({ ...h })),
      checks: {},
      notificationsEnabled: false,
      morningHour: 8,
      afternoonHour: 14,
    };
  }

  function normalizePeriod(period) {
    if (period === "morning" || period === "afternoon") return period;
    return PERIOD_MIGRATE[period] || "afternoon";
  }

  function normalize(state) {
    const defaultsById = Object.fromEntries(DEFAULT_HABITS.map((h) => [h.id, h]));
    let habits = Array.isArray(state.habits) && state.habits.length
      ? state.habits.map((h) => {
          const def = defaultsById[h.id] || {};
          return {
            ...def,
            ...h,
            id: h.id,
            label: h.label || def.label || h.id,
            detail: h.detail || def.detail || "",
            funFact: h.funFact || def.funFact || "",
            period: normalizePeriod(h.period || def.period || "afternoon"),
            enabled: h.enabled !== false,
          };
        })
      : DEFAULT_HABITS.map((h) => ({ ...h }));

    for (const def of DEFAULT_HABITS) {
      if (!habits.some((h) => h.id === def.id)) {
        habits.push({ ...def });
      }
    }

    // Prefer catalog fun facts / periods from defaults when upgrading
    habits = habits.map((h) => {
      const def = defaultsById[h.id];
      if (!def) return h;
      return {
        ...h,
        funFact: def.funFact || h.funFact,
        detail: def.detail || h.detail,
        period: def.period || normalizePeriod(h.period),
        label: def.label || h.label,
      };
    });

    const afternoonHour =
      state.afternoonHour != null
        ? clampHour(state.afternoonHour, 14)
        : clampHour(state.eveningHour, 14);

    return {
      habits,
      checks: state.checks && typeof state.checks === "object" ? state.checks : {},
      notificationsEnabled: Boolean(state.notificationsEnabled),
      morningHour: clampHour(state.morningHour, 8),
      afternoonHour,
    };
  }

  function clampHour(value, fallback) {
    const n = Number(value);
    if (!Number.isFinite(n)) return fallback;
    return Math.min(23, Math.max(0, Math.round(n)));
  }

  function save(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    global.dispatchEvent(new CustomEvent("skinscan-habits-updated"));
  }

  function enabledHabits(state = load()) {
    return state.habits.filter((h) => h.enabled);
  }

  function habitsByPeriod(period, state = load()) {
    return enabledHabits(state).filter((h) => h.period === period);
  }

  function isChecked(habitId, state = load(), day = todayKey()) {
    return Boolean(state.checks[day]?.[habitId]);
  }

  function setChecked(habitId, checked, state = load(), day = todayKey()) {
    if (!state.checks[day]) state.checks[day] = {};
    if (checked) state.checks[day][habitId] = true;
    else delete state.checks[day][habitId];
    const keys = Object.keys(state.checks).sort();
    while (keys.length > 60) {
      delete state.checks[keys.shift()];
    }
    save(state);
    return state;
  }

  function toggleChecked(habitId) {
    const state = load();
    return setChecked(habitId, !isChecked(habitId, state), state);
  }

  function setHabitEnabled(habitId, enabled) {
    const state = load();
    const habit = state.habits.find((h) => h.id === habitId);
    if (habit) habit.enabled = Boolean(enabled);
    save(state);
    return state;
  }

  function updateSettings(partial) {
    const state = { ...load(), ...partial };
    state.morningHour = clampHour(state.morningHour, 8);
    state.afternoonHour = clampHour(state.afternoonHour, 14);
    delete state.eveningHour;
    save(state);
    return state;
  }

  function progress(state = load(), day = todayKey()) {
    const list = enabledHabits(state);
    const done = list.filter((h) => isChecked(h.id, state, day)).length;
    return { done, total: list.length, list };
  }

  global.SkinScanHabits = {
    DEFAULT_HABITS,
    todayKey,
    load,
    save,
    enabledHabits,
    habitsByPeriod,
    isChecked,
    setChecked,
    toggleChecked,
    setHabitEnabled,
    updateSettings,
    progress,
  };
})(window);
