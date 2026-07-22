/**
 * Map educational condition codes → existing habits to soft-suggest.
 * No product recommendations — only habits already in the Habits catalog.
 */
(function (global) {
  const BY_CODE = {
    acne: ["cleanse", "moisturize", "water"],
    actinic_keratosis: ["sunscreen", "skin_check"],
    benign_tumors: ["skin_check", "sunscreen"],
    bullous: ["moisturize", "skin_check"],
    candidiasis: ["cleanse", "moisturize"],
    drug_eruption: ["skin_check"],
    eczema: ["moisturize", "cleanse", "nourish"],
    infestations_bites: ["cleanse", "skin_check"],
    lichen: ["moisturize", "skin_check"],
    lupus: ["sunscreen", "skin_check"],
    moles: ["skin_check", "sunscreen"],
    psoriasis: ["moisturize", "cleanse"],
    rosacea: ["sunscreen", "cleanse", "moisturize"],
    seborrheic_keratoses: ["skin_check", "sunscreen"],
    skin_cancer: ["skin_check", "sunscreen"],
    sun_damage: ["sunscreen", "skin_check"],
    tinea: ["cleanse", "moisturize"],
    normal: ["sunscreen", "skin_check"],
    vascular_tumors: ["skin_check", "sunscreen"],
    vasculitis: ["skin_check"],
    vitiligo: ["sunscreen", "skin_check"],
    warts: ["cleanse", "skin_check"],
  };

  const FALLBACK = ["sunscreen", "skin_check", "moisturize"];

  const REASONS = {
    sunscreen: "Sun protection helps reduce UV stress on the skin over time.",
    skin_check: "A quick recurring check helps you notice changes earlier.",
    moisturize: "Keeping the barrier comfortable supports many common skin findings.",
    cleanse: "Gentle cleansing can help remove irritants without stripping oil.",
    water: "Steady hydration supports overall skin comfort.",
    nourish: "Balanced meals support skin from the inside as part of a routine.",
  };

  function habitIdsForCode(code) {
    if (!code) return FALLBACK.slice();
    return (BY_CODE[code] || FALLBACK).slice();
  }

  /**
   * Returns suggestion cards: { habit, alreadyEnabled, reason }
   */
  function suggestionsFor(code, state) {
    const store = global.SkinScanHabits;
    if (!store) return [];
    const current = state || store.load();
    const byId = Object.fromEntries(current.habits.map((h) => [h.id, h]));

    return habitIdsForCode(code)
      .map((id) => {
        const habit = byId[id] || store.DEFAULT_HABITS.find((h) => h.id === id);
        if (!habit) return null;
        return {
          habit,
          alreadyEnabled: habit.enabled !== false,
          reason: REASONS[id] || habit.funFact || "",
        };
      })
      .filter(Boolean);
  }

  function enableSuggested(ids) {
    const store = global.SkinScanHabits;
    if (!store) return null;
    const state = store.load();
    let changed = false;
    for (const id of ids) {
      const habit = state.habits.find((h) => h.id === id);
      if (habit && !habit.enabled) {
        habit.enabled = true;
        changed = true;
      }
    }
    if (changed) store.save(state);
    return state;
  }

  global.SkinScanHabitSuggestions = {
    habitIdsForCode,
    suggestionsFor,
    enableSuggested,
    REASONS,
  };
})(window);
