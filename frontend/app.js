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

  let selectedFile = null;

  function setStatus(message, isError = false) {
    statusEl.textContent = message;
    statusEl.classList.toggle("error", isError);
  }

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
    analyzeBtn.disabled = false;
    clearBtn.classList.remove("hidden");
    resultsSection.classList.add("hidden");
    setStatus("");
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
    resultsSection.classList.add("hidden");
    setStatus("");
  });

  analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    analyzeBtn.disabled = true;
    setStatus("Analyzing…");

    const formData = new FormData();
    formData.append("file", selectedFile);

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
      resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      setStatus(error.message || "Could not reach the API. Is the backend running?", true);
    } finally {
      analyzeBtn.disabled = false;
    }
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
        "This match is uncertain — consider the alternatives below and ask a dermatologist if you are worried."
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
        "The models did not fully agree or confidence is low. Have a dermatologist review this area if symptoms persist or change.";
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

    resultsSection.classList.remove("hidden");
  }
}
