(function () {
  const store = window.SkinScanHabits;
  if (!store) return;

  const todayList = document.getElementById("today-list");
  const settingsList = document.getElementById("settings-list");
  const progressEl = document.getElementById("habits-progress");
  const notifyToggle = document.getElementById("notify-toggle");
  const morningHour = document.getElementById("morning-hour");
  const afternoonHour = document.getElementById("afternoon-hour");
  const notifyStatus = document.getElementById("notify-status");

  function formatDateLabel() {
    return new Date().toLocaleDateString("en-US", {
      weekday: "long",
      month: "long",
      day: "numeric",
    });
  }

  function habitCheckItem(habit, state) {
    const checked = store.isChecked(habit.id, state);
    return `
      <li>
        <label class="habit-check-row ${checked ? "is-done" : ""}">
          <input type="checkbox" data-habit-id="${habit.id}" ${checked ? "checked" : ""} />
          <span>
            <strong>${habit.label}</strong>
            <span class="habit-check-meta">${habit.detail}</span>
            <span class="habit-fun-fact">Why it helps: ${habit.funFact || ""}</span>
          </span>
        </label>
      </li>
    `;
  }

  function renderPeriodBlock(title, habits, state) {
    if (!habits.length) return "";
    return `
      <div class="habit-period-block">
        <h3 class="habit-period-title">${title}</h3>
        <ul class="habit-checklist">${habits.map((h) => habitCheckItem(h, state)).join("")}</ul>
      </div>
    `;
  }

  function render() {
    const state = store.load();
    const { done, total } = store.progress(state);
    const morning = store.habitsByPeriod("morning", state);
    const afternoon = store.habitsByPeriod("afternoon", state);

    if (progressEl) {
      progressEl.textContent =
        total === 0
          ? `${formatDateLabel()} · enable a habit below to start`
          : `${formatDateLabel()} · ${done} of ${total} done`;
    }

    if (todayList) {
      if (!morning.length && !afternoon.length) {
        todayList.innerHTML =
          '<li class="muted">No habits enabled. Turn some on in the section below.</li>';
      } else {
        // today-list is a container div now
        todayList.innerHTML =
          renderPeriodBlock("Morning", morning, state) +
          renderPeriodBlock("Afternoon", afternoon, state);
      }
    }

    if (settingsList) {
      const morningSettings = state.habits.filter((h) => h.period === "morning");
      const afternoonSettings = state.habits.filter((h) => h.period === "afternoon");

      const settingItem = (habit) => `
        <li>
          <label class="habit-setting-row">
            <input type="checkbox" data-enable-id="${habit.id}" ${habit.enabled ? "checked" : ""} />
            <span>
              <strong>${habit.label}</strong>
              <span class="habit-setting-detail">${habit.detail}</span>
              <span class="habit-fun-fact">Why it helps: ${habit.funFact || ""}</span>
            </span>
          </label>
        </li>
      `;

      settingsList.innerHTML = `
        <li class="habit-settings-group">
          <h3 class="habit-period-title">Morning habits</h3>
          <ul class="habit-settings">${morningSettings.map(settingItem).join("")}</ul>
        </li>
        <li class="habit-settings-group">
          <h3 class="habit-period-title">Afternoon habits</h3>
          <ul class="habit-settings">${afternoonSettings.map(settingItem).join("")}</ul>
        </li>
      `;
    }

    if (notifyToggle) notifyToggle.checked = state.notificationsEnabled;
    if (morningHour) morningHour.value = state.morningHour;
    if (afternoonHour) afternoonHour.value = state.afternoonHour;
  }

  todayList?.addEventListener("change", (event) => {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || !input.dataset.habitId) return;
    store.setChecked(input.dataset.habitId, input.checked);
    render();
  });

  settingsList?.addEventListener("change", async (event) => {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || !input.dataset.enableId) return;
    store.setHabitEnabled(input.dataset.enableId, input.checked);
    render();
    await syncNotifications();
  });

  async function syncNotifications() {
    const state = store.load();
    const LocalNotifications = window.SkinScanNative?.LocalNotifications;
    const isNative = Boolean(window.APP_CONFIG?.IS_NATIVE && LocalNotifications);

    if (!notifyStatus) return;

    if (!state.notificationsEnabled) {
      if (isNative) {
        try {
          const pending = await LocalNotifications.getPending();
          const ids = (pending.notifications || [])
            .filter((n) => String(n.extra?.skinscan) === "habit")
            .map((n) => ({ id: n.id }));
          if (ids.length) await LocalNotifications.cancel({ notifications: ids });
        } catch (_) {
          /* ignore */
        }
      }
      notifyStatus.textContent = "Reminders are off.";
      return;
    }

    if (!isNative) {
      notifyStatus.textContent =
        "Reminders are saved for this browser. Install the iOS app to get phone notifications.";
      return;
    }

    try {
      let perm = await LocalNotifications.checkPermissions();
      if (perm.display !== "granted") {
        perm = await LocalNotifications.requestPermissions();
      }
      if (perm.display !== "granted") {
        notifyStatus.textContent = "Notification permission denied. Enable it in iOS Settings.";
        return;
      }

      const pending = await LocalNotifications.getPending();
      const ids = (pending.notifications || [])
        .filter((n) => String(n.extra?.skinscan) === "habit")
        .map((n) => ({ id: n.id }));
      if (ids.length) await LocalNotifications.cancel({ notifications: ids });

      const morningLabels = store
        .habitsByPeriod("morning", state)
        .map((h) => h.label)
        .slice(0, 3);
      const afternoonLabels = store
        .habitsByPeriod("afternoon", state)
        .map((h) => h.label)
        .slice(0, 3);

      const notifications = [];
      if (morningLabels.length) {
        notifications.push({
          id: 71001,
          title: "SkinScan morning habits",
          body: morningLabels.join(" · "),
          schedule: {
            on: { hour: state.morningHour, minute: 0 },
            repeats: true,
            allowWhileIdle: true,
          },
          extra: { skinscan: "habit", slot: "morning" },
        });
      }
      if (afternoonLabels.length) {
        notifications.push({
          id: 71002,
          title: "SkinScan afternoon habits",
          body: afternoonLabels.join(" · "),
          schedule: {
            on: { hour: state.afternoonHour, minute: 0 },
            repeats: true,
            allowWhileIdle: true,
          },
          extra: { skinscan: "habit", slot: "afternoon" },
        });
      }

      if (notifications.length) {
        await LocalNotifications.schedule({ notifications });
      }

      notifyStatus.textContent = `Phone reminders on · morning ${state.morningHour}:00 · afternoon ${state.afternoonHour}:00`;
    } catch (error) {
      notifyStatus.textContent = `Could not schedule notifications: ${error?.message || error}`;
    }
  }

  notifyToggle?.addEventListener("change", async () => {
    store.updateSettings({ notificationsEnabled: notifyToggle.checked });
    await syncNotifications();
    render();
  });

  function onHourChange() {
    store.updateSettings({
      morningHour: Number(morningHour.value),
      afternoonHour: Number(afternoonHour.value),
    });
    syncNotifications();
    render();
  }

  morningHour?.addEventListener("change", onHourChange);
  afternoonHour?.addEventListener("change", onHourChange);

  window.addEventListener("skinscan-habits-updated", render);

  render();
  syncNotifications();
})();
