/**
 * On-device scan history (localStorage). Thumbnails only — educational records.
 */
(function (global) {
  const STORAGE_KEY = "skinscan_history_v1";
  const MAX_ENTRIES = 30;

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }

  function save(entries) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
    global.dispatchEvent(new CustomEvent("skinscan-history-updated"));
  }

  function compressImage(dataUrl, maxWidth = 280, quality = 0.55) {
    return new Promise((resolve) => {
      if (!dataUrl || typeof dataUrl !== "string") {
        resolve(null);
        return;
      }
      const img = new Image();
      img.onload = () => {
        try {
          const scale = Math.min(1, maxWidth / img.width);
          const canvas = document.createElement("canvas");
          canvas.width = Math.max(1, Math.round(img.width * scale));
          canvas.height = Math.max(1, Math.round(img.height * scale));
          const ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          resolve(canvas.toDataURL("image/jpeg", quality));
        } catch {
          resolve(null);
        }
      };
      img.onerror = () => resolve(null);
      img.src = dataUrl;
    });
  }

  async function addFromAnalysis(data, imageDataUrl) {
    const thumbnail = await compressImage(imageDataUrl);
    const entry = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      createdAt: new Date().toISOString(),
      prediction: data.prediction || data.condition?.code || "",
      predictionName: data.prediction_name || data.condition?.name || "Unknown",
      confidence: typeof data.confidence === "number" ? data.confidence : null,
      riskLevel: data.risk_level || "moderate",
      uncertain: Boolean(data.uncertain || data.ensemble?.uncertain),
      description: data.condition?.description || "",
      alternatives: (data.alternatives || []).slice(0, 3).map((alt) => ({
        code: alt.code,
        name: alt.name || alt.short_name,
        confidence: alt.confidence,
      })),
      thumbnail,
    };

    const entries = [entry, ...load()].slice(0, MAX_ENTRIES);
    save(entries);
    return entry;
  }

  function getById(id) {
    return load().find((e) => e.id === id) || null;
  }

  function remove(id) {
    const next = load().filter((e) => e.id !== id);
    save(next);
    return next;
  }

  function clear() {
    save([]);
  }

  global.SkinScanHistory = {
    load,
    addFromAnalysis,
    getById,
    remove,
    clear,
    MAX_ENTRIES,
  };
})(window);
