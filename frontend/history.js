(function () {
  const store = window.SkinScanHistory;
  const listEl = document.getElementById("history-list");
  const emptyEl = document.getElementById("history-empty");
  const clearBtn = document.getElementById("history-clear-btn");
  const detailEl = document.getElementById("history-detail");

  const RISK_LABELS = {
    low: "Likely benign",
    moderate: "Monitor closely",
    high: "Seek evaluation",
  };

  function formatWhen(iso) {
    try {
      const d = new Date(iso);
      return d.toLocaleString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
      });
    } catch {
      return iso;
    }
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderDetail(entry) {
    if (!detailEl || !entry) {
      detailEl?.classList.add("hidden");
      return;
    }

    const conf =
      entry.confidence != null ? `${Math.round(entry.confidence * 100)}%` : "—";
    const alts = (entry.alternatives || [])
      .map(
        (a) =>
          `<li><span>${escapeHtml(a.name)}</span><span>${
            a.confidence != null ? Math.round(a.confidence * 100) + "%" : ""
          }</span></li>`
      )
      .join("");

    detailEl.classList.remove("hidden");
    detailEl.innerHTML = `
      <div class="history-detail-card">
        <button type="button" class="btn btn-ghost history-detail-close" id="history-detail-close">← Back to list</button>
        ${
          entry.thumbnail
            ? `<img class="history-detail-thumb" src="${entry.thumbnail}" alt="Saved scan thumbnail" />`
            : ""
        }
        <div class="history-detail-meta">
          <span class="risk-badge ${escapeHtml(entry.riskLevel)}">${
            RISK_LABELS[entry.riskLevel] || "Review"
          }</span>
          <span class="confidence-pill">${conf} confidence</span>
        </div>
        <h2 class="condition-name">${escapeHtml(entry.predictionName)}</h2>
        <p class="muted">${formatWhen(entry.createdAt)}${
          entry.uncertain ? " · uncertain match" : ""
        }</p>
        ${
          entry.description
            ? `<p class="body-text">${escapeHtml(entry.description)}</p>`
            : ""
        }
        ${
          alts
            ? `<div class="history-alts"><h3>Other possible matches</h3><ul class="history-alts-list">${alts}</ul></div>`
            : ""
        }
        <p class="disclaimer-box" role="note">
          <strong>Educational record only.</strong> Not a diagnosis. Saved on this device.
        </p>
        <div class="history-detail-actions">
          <a class="btn btn-primary" href="analyze.html">New analysis</a>
          <button type="button" class="btn btn-ghost" data-delete-id="${escapeHtml(
            entry.id
          )}">Delete</button>
        </div>
      </div>
    `;

    detailEl.querySelector("#history-detail-close")?.addEventListener("click", () => {
      detailEl.classList.add("hidden");
      detailEl.innerHTML = "";
      listEl?.classList.remove("hidden");
      emptyEl?.classList.toggle("hidden", store.load().length > 0);
    });

    detailEl.querySelector("[data-delete-id]")?.addEventListener("click", (event) => {
      const id = event.currentTarget.getAttribute("data-delete-id");
      if (!id || !confirm("Delete this saved scan?")) return;
      store.remove(id);
      detailEl.classList.add("hidden");
      detailEl.innerHTML = "";
      render();
    });

    listEl?.classList.add("hidden");
    emptyEl?.classList.add("hidden");
    detailEl.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function render() {
    if (!store || !listEl) return;
    const entries = store.load();

    if (clearBtn) clearBtn.classList.toggle("hidden", entries.length === 0);

    if (!entries.length) {
      listEl.innerHTML = "";
      listEl.classList.add("hidden");
      emptyEl?.classList.remove("hidden");
      detailEl?.classList.add("hidden");
      return;
    }

    emptyEl?.classList.add("hidden");
    if (!detailEl || detailEl.classList.contains("hidden")) {
      listEl.classList.remove("hidden");
    }

    listEl.innerHTML = entries
      .map((entry) => {
        const conf =
          entry.confidence != null
            ? `${Math.round(entry.confidence * 100)}%`
            : "—";
        return `
          <li class="history-card" data-id="${escapeHtml(entry.id)}">
            <button type="button" class="history-card-btn">
              ${
                entry.thumbnail
                  ? `<img src="${entry.thumbnail}" alt="" class="history-thumb" />`
                  : `<div class="history-thumb history-thumb-empty" aria-hidden="true"></div>`
              }
              <div class="history-card-body">
                <strong>${escapeHtml(entry.predictionName)}</strong>
                <span class="history-card-meta">${formatWhen(entry.createdAt)}</span>
                <span class="history-card-meta">${conf} · ${escapeHtml(
          RISK_LABELS[entry.riskLevel] || entry.riskLevel || ""
        )}</span>
              </div>
            </button>
          </li>
        `;
      })
      .join("");

    listEl.querySelectorAll(".history-card").forEach((card) => {
      card.querySelector(".history-card-btn")?.addEventListener("click", () => {
        const entry = store.getById(card.getAttribute("data-id"));
        renderDetail(entry);
      });
    });
  }

  clearBtn?.addEventListener("click", () => {
    if (!store.load().length) return;
    if (!confirm("Clear all saved scans on this device?")) return;
    store.clear();
    render();
  });

  window.addEventListener("skinscan-history-updated", render);
  render();
})();
