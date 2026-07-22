const API_URL = window.APP_CONFIG?.API_URL || "http://localhost:8000";

const RISK_LABELS = {
  low: "Likely benign",
  moderate: "Monitor closely",
  high: "Seek evaluation",
};

if (document.getElementById("dropzone")) {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const preview = document.getElementById("preview");
  const analyzeBtn = document.getElementById("analyze-btn");
  const clearBtn = document.getElementById("clear-btn");
  const statusEl = document.getElementById("status");
  const resultsSection = document.getElementById("results");
  const analyzePage = document.querySelector(".analyze-page");
  const riskBadge = document.getElementById("risk-badge");
  const conditionName = document.getElementById("condition-name");
  const conditionDescription = document.getElementById("condition-description");
  const confidenceValue = document.getElementById("confidence-value");
  const ensembleNote = document.getElementById("ensemble-note");
  const explanation = document.getElementById("explanation");
  const commonSigns = document.getElementById("common-signs");
  const whenToSeeDoctor = document.getElementById("when-to-see-doctor");
  const recommendedActions = document.getElementById("recommended-actions");
  const sourcesList = document.getElementById("sources-list");
  const alternativesSection = document.getElementById("alternatives");
  const alternativesList = document.getElementById("alternatives-list");
  const ctaText = document.getElementById("cta-text");
  const nativeCameraActions = document.getElementById("native-camera-actions");
  const cameraCaptureBtn = document.getElementById("camera-capture-btn");
  const cameraLibraryBtn = document.getElementById("camera-library-btn");
  const photoChecklist = document.getElementById("photo-checklist");
  const photoTipsSkip = document.getElementById("photo-tips-skip");
  const photoTipsStatus = document.getElementById("photo-tips-status");
  const photoGuide = document.getElementById("photo-guide");
  const habitSuggest = document.getElementById("habit-suggest");
  const habitSuggestList = document.getElementById("habit-suggest-list");
  const habitSuggestAdd = document.getElementById("habit-suggest-add");
  const habitSuggestStatus = document.getElementById("habit-suggest-status");

  const PHOTO_TIPS_KEY = "skinscan_photo_tips_skipped";

  let selectedFile = null;
  let latestAnalysis = null;
  let imageDataUrl = null;
  let pendingHabitIds = [];

  function setResultsVisible(visible) {
    resultsSection.classList.toggle("hidden", !visible);
    analyzePage?.classList.toggle("has-results", visible);
  }

  function setStatus(message, isError = false) {
    statusEl.textContent = message;
    statusEl.classList.toggle("error", isError);
  }

  function tipsAcknowledged() {
    if (localStorage.getItem(PHOTO_TIPS_KEY) === "1") return true;
    if (!photoChecklist) return true;
    const boxes = [...photoChecklist.querySelectorAll('input[type="checkbox"]')];
    return boxes.length > 0 && boxes.every((box) => box.checked);
  }

  function updatePhotoTipsStatus() {
    if (!photoTipsStatus) return;
    if (localStorage.getItem(PHOTO_TIPS_KEY) === "1") {
      photoTipsStatus.textContent = "Tips skipped for this device — you can still review them above.";
      photoGuide?.classList.add("tips-skipped");
      return;
    }
    if (tipsAcknowledged()) {
      photoTipsStatus.textContent = "Ready for a photo.";
      photoGuide?.classList.add("tips-ready");
    } else {
      photoTipsStatus.textContent = "Check all tips (or skip) before analyzing.";
      photoGuide?.classList.remove("tips-ready");
    }
  }

  function syncAnalyzeEnabled() {
    analyzeBtn.disabled = !(selectedFile && tipsAcknowledged());
  }

  photoChecklist?.addEventListener("change", (event) => {
    const input = event.target;
    if (input instanceof HTMLInputElement) {
      input.closest(".photo-check-row")?.classList.toggle("is-checked", input.checked);
    }
    updatePhotoTipsStatus();
    syncAnalyzeEnabled();
  });

  photoTipsSkip?.addEventListener("click", () => {
    localStorage.setItem(PHOTO_TIPS_KEY, "1");
    photoChecklist
      ?.querySelectorAll('input[type="checkbox"]')
      .forEach((box) => {
        box.checked = true;
        box.closest(".photo-check-row")?.classList.add("is-checked");
      });
    updatePhotoTipsStatus();
    syncAnalyzeEnabled();
  });

  updatePhotoTipsStatus();
  if (localStorage.getItem(PHOTO_TIPS_KEY) === "1") {
    photoChecklist
      ?.querySelectorAll('input[type="checkbox"]')
      .forEach((box) => {
        box.checked = true;
        box.closest(".photo-check-row")?.classList.add("is-checked");
      });
  }

  const isNativeApp = Boolean(window.APP_CONFIG?.IS_NATIVE);
  if (isNativeApp && nativeCameraActions) {
    nativeCameraActions.classList.remove("hidden");
  }

  async function photoToFile(photo) {
    const dataUrl = photo?.dataUrl || photo?.webPath;
    if (!dataUrl) throw new Error("No image returned from camera.");

    if (dataUrl.startsWith("data:")) {
      const response = await fetch(dataUrl);
      const blob = await response.blob();
      const type = blob.type || "image/jpeg";
      const ext = type.includes("png") ? "png" : "jpg";
      return new File([blob], `skinscan-capture.${ext}`, { type });
    }

    const response = await fetch(dataUrl);
    const blob = await response.blob();
    const type = blob.type || "image/jpeg";
    const ext = type.includes("png") ? "png" : "jpg";
    return new File([blob], `skinscan-capture.${ext}`, { type });
  }

  async function captureFromNative(source) {
    const native = window.SkinScanNative;
    if (!native?.Camera) {
      setStatus("Camera plugin is not available.", true);
      return;
    }

    setStatus(source === "CAMERA" ? "Opening camera…" : "Opening photo library…");
    try {
      const photo = await native.Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: native.CameraResultType.DataUrl,
        source:
          source === "CAMERA"
            ? native.CameraSource.Camera
            : native.CameraSource.Photos,
        correctOrientation: true,
      });
      const file = await photoToFile(photo);
      handleFile(file);
      setStatus("");
    } catch (error) {
      const message = String(error?.message || error || "");
      if (/cancel/i.test(message)) {
        setStatus("");
        return;
      }
      setStatus(message || "Could not get a photo.", true);
    }
  }

  cameraCaptureBtn?.addEventListener("click", () => captureFromNative("CAMERA"));
  cameraLibraryBtn?.addEventListener("click", () => captureFromNative("PHOTOS"));

  function handleFile(file) {
    if (!file) return;

    if (!["image/jpeg", "image/png", "image/jpg"].includes(file.type)) {
      setStatus("Please upload a JPEG or PNG image.", true);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setStatus("Image must be 10 MB or smaller.", true);
      return;
    }

    selectedFile = file;
    preview.src = URL.createObjectURL(file);
    preview.classList.remove("hidden");
    dropzone.classList.add("has-preview");
    clearBtn.classList.remove("hidden");
    setResultsVisible(false);
    habitSuggest?.classList.add("hidden");
    latestAnalysis = null;
    imageDataUrl = null;
    pendingHabitIds = [];
    setStatus(
      tipsAcknowledged()
        ? ""
        : "Check the photo tips above (or skip) before analyzing."
    );
    syncAnalyzeEnabled();

    const reader = new FileReader();
    reader.onload = () => {
      imageDataUrl = typeof reader.result === "string" ? reader.result : null;
    };
    reader.readAsDataURL(file);
  }

  dropzone.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      fileInput.click();
    }
  });

  fileInput.addEventListener("change", (event) => {
    handleFile(event.target.files[0]);
  });

  dropzone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropzone.classList.remove("dragover");
    handleFile(event.dataTransfer.files[0]);
  });

  clearBtn.addEventListener("click", () => {
    selectedFile = null;
    fileInput.value = "";
    preview.src = "";
    preview.classList.add("hidden");
    dropzone.classList.remove("has-preview");
    analyzeBtn.disabled = true;
    clearBtn.classList.add("hidden");
    setResultsVisible(false);
    habitSuggest?.classList.add("hidden");
    latestAnalysis = null;
    imageDataUrl = null;
    pendingHabitIds = [];
    setStatus("");
  });

  analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) return;
    if (!tipsAcknowledged()) {
      setStatus("Check the photo tips above (or skip) before analyzing.", true);
      photoGuide?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      return;
    }

    analyzeBtn.disabled = true;
    setStatus("Analyzing with ensemble…");

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("enhance", "true");

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      showResults(data);
      setStatus("");
      saveToHistory(data);
      resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      setStatus(error.message || "Could not reach the API. Is the backend running?", true);
    } finally {
      syncAnalyzeEnabled();
    }
  });

  async function saveToHistory(data) {
    const history = window.SkinScanHistory;
    if (!history?.addFromAnalysis) return;
    try {
      await history.addFromAnalysis(data, imageDataUrl);
    } catch {
      /* non-blocking */
    }
  }

  function renderHabitSuggestions(data) {
    if (!window.APP_CONFIG?.IS_NATIVE) return;
    if (!habitSuggest || !habitSuggestList || !window.SkinScanHabitSuggestions) {
      return;
    }

    const code = data.prediction || data.condition?.code || "";
    const suggestions = window.SkinScanHabitSuggestions.suggestionsFor(code);
    pendingHabitIds = suggestions
      .filter((s) => !s.alreadyEnabled)
      .map((s) => s.habit.id);

    if (!suggestions.length) {
      habitSuggest.classList.add("hidden");
      return;
    }

    habitSuggestList.innerHTML = suggestions
      .map((s) => {
        const badge = s.alreadyEnabled
          ? '<span class="habit-suggest-badge">Already on</span>'
          : '<span class="habit-suggest-badge is-new">Suggested</span>';
        return `
          <li class="habit-suggest-item ${s.alreadyEnabled ? "is-on" : ""}">
            <div class="habit-suggest-item-head">
              <strong>${s.habit.label}</strong>
              ${badge}
            </div>
            <p class="habit-suggest-reason">${s.reason || s.habit.funFact || ""}</p>
          </li>
        `;
      })
      .join("");

    if (habitSuggestAdd) {
      habitSuggestAdd.disabled = pendingHabitIds.length === 0;
      habitSuggestAdd.textContent =
        pendingHabitIds.length === 0
          ? "All suggested habits are on"
          : `Add ${pendingHabitIds.length} habit${
              pendingHabitIds.length === 1 ? "" : "s"
            }`;
    }
    if (habitSuggestStatus) habitSuggestStatus.textContent = "";
    habitSuggest.classList.remove("hidden");
  }

  habitSuggestAdd?.addEventListener("click", () => {
    if (!pendingHabitIds.length || !window.SkinScanHabitSuggestions) return;
    window.SkinScanHabitSuggestions.enableSuggested(pendingHabitIds);
    if (habitSuggestStatus) {
      habitSuggestStatus.textContent =
        "Added to Habits. Check them off on the Habits tab or Home.";
    }
    if (latestAnalysis) renderHabitSuggestions(latestAnalysis);
  });

  function renderRecommendedActions(actions) {
    if (!actions?.length) {
      recommendedActions.innerHTML =
        '<li class="body-text">No recommendations available.</li>';
      return;
    }

    recommendedActions.innerHTML = actions
      .map(
        (item) => `
        <li class="action-item">
          <p class="action-text">${item.action}</p>
          <a
            class="action-source"
            href="${item.source.url}"
            target="_blank"
            rel="noopener noreferrer"
          >
            Source: ${item.source.publisher} (${item.source.domain})
          </a>
        </li>
      `
      )
      .join("");
  }

  function renderSources(sources) {
    if (!sources?.length) {
      sourcesList.innerHTML = '<li class="body-text">No sources available.</li>';
      return;
    }

    sourcesList.innerHTML = sources
      .map(
        (source) => `
        <li>
          <a
            class="source-link"
            href="${source.url}"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span class="source-domain">${source.domain || "ref"}</span>
            <span class="source-info">
              <span class="source-title">${source.title}</span>
              <span class="source-publisher">${source.publisher}</span>
            </span>
          </a>
        </li>
      `
      )
      .join("");
  }

  function renderEnsembleNote(data) {
    if (!ensembleNote) return;

    const ensemble = data.ensemble;
    if (!ensemble) {
      ensembleNote.classList.add("hidden");
      ensembleNote.textContent = "";
      return;
    }

    const parts = [];
    if (ensemble.models_used > 1) {
      parts.push(
        `Combined result from ${ensemble.models_used} models (${ensemble.agreement.replaceAll("_", " ")} agreement).`
      );
    }

    if (data.uncertain || ensemble.uncertain) {
      parts.push(
        "This match is uncertain — compare the other possible matches listed next, then read the details."
      );
      ensembleNote.classList.add("uncertain");
    } else {
      ensembleNote.classList.remove("uncertain");
    }

    if (!parts.length) {
      ensembleNote.classList.add("hidden");
      ensembleNote.textContent = "";
      return;
    }

    ensembleNote.textContent = parts.join(" ");
    ensembleNote.classList.remove("hidden");
  }

  function showResults(data) {
    latestAnalysis = data;
    const condition = data.condition || {};
    const risk = data.risk_level || "moderate";
    const confidencePct = Math.round((data.confidence ?? 0) * 100);

    riskBadge.textContent = RISK_LABELS[risk] || "Review recommended";
    riskBadge.className = `risk-badge ${risk}`;

    confidenceValue.textContent = `${confidencePct}% confidence`;

    renderEnsembleNote(data);

    conditionName.textContent = data.prediction_name || condition.name || "Unknown condition";
    conditionDescription.textContent = condition.description || "";
    explanation.textContent = condition.explanation || condition.what_it_means || "";
    whenToSeeDoctor.textContent = condition.when_to_see_doctor || "";

    commonSigns.innerHTML = (condition.common_signs || [])
      .map((sign) => `<li>${sign}</li>`)
      .join("");

    renderRecommendedActions(condition.recommended_actions);
    renderSources(condition.sources);

    if (data.alternatives?.length) {
      alternativesSection.classList.remove("hidden");
      alternativesList.innerHTML = data.alternatives
        .map(
          (alt) => `
          <div class="alternative-item">
            <span class="alt-name">${alt.name || alt.short_name}</span>
            <span class="alt-confidence">${Math.round((alt.confidence ?? 0) * 100)}%</span>
          </div>
        `
        )
        .join("");
    } else {
      alternativesSection.classList.add("hidden");
    }

    if (data.uncertain || data.ensemble?.uncertain) {
      ctaText.textContent =
        "The models did not fully agree or confidence is low. Compare the other possible matches, and see a dermatologist if you are worried.";
    } else if (risk === "high") {
      ctaText.textContent =
        "We recommend scheduling an appointment with a dermatologist as soon as possible.";
    } else if (risk === "moderate") {
      ctaText.textContent =
        "Consider having a dermatologist evaluate this area, especially if it changes over time.";
    } else {
      ctaText.textContent =
        "This appears to be a common benign condition, but see a doctor if you notice any changes.";
    }

    renderHabitSuggestions(data);
    setResultsVisible(true);
  }
}
