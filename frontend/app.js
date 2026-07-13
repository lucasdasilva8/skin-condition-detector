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
  const analysisAssist = document.getElementById("analysis-assist");
  const assistSupport = document.getElementById("assist-support");
  const assistFeatures = document.getElementById("assist-features");
  const assistQuality = document.getElementById("assist-quality");
  const assistWatch = document.getElementById("assist-watch");
  const assistError = document.getElementById("assist-error");
  const explanation = document.getElementById("explanation");
  const commonSigns = document.getElementById("common-signs");
  const whenToSeeDoctor = document.getElementById("when-to-see-doctor");
  const recommendedActions = document.getElementById("recommended-actions");
  const sourcesList = document.getElementById("sources-list");
  const alternativesSection = document.getElementById("alternatives");
  const alternativesList = document.getElementById("alternatives-list");
  const ctaText = document.getElementById("cta-text");
  const chatPanel = document.getElementById("chat-panel");
  const chatStatus = document.getElementById("chat-status");
  const chatSuggestions = document.getElementById("chat-suggestions");
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatSend = document.getElementById("chat-send");

  let selectedFile = null;
  let latestAnalysis = null;
  let chatHistory = [];
  let imageDataUrl = null;
  let ollamaReady = false;

  function setStatus(message, isError = false) {
    statusEl.textContent = message;
    statusEl.classList.toggle("error", isError);
  }

  async function refreshOllamaStatus() {
    try {
      const response = await fetch(`${API_URL}/health`);
      const data = await response.json();
      ollamaReady = Boolean(data.ollama?.ready);
      if (chatStatus) {
        if (ollamaReady) {
          chatStatus.textContent = `Local assistant ready (${data.ollama.model}).`;
        } else if (data.ollama?.available) {
          chatStatus.textContent =
            "Ollama is running, but no vision model is installed (try qwen2.5vl:7b).";
        } else {
          chatStatus.textContent =
            "Chat unlocks when Ollama is running locally with a vision model.";
        }
      }
    } catch {
      ollamaReady = false;
      if (chatStatus) {
        chatStatus.textContent = "Could not reach the API for assistant status.";
      }
    }
  }

  refreshOllamaStatus();

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
    chatPanel?.classList.add("hidden");
    latestAnalysis = null;
    chatHistory = [];
    imageDataUrl = null;
    setStatus("");

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
    resultsSection.classList.add("hidden");
    chatPanel?.classList.add("hidden");
    latestAnalysis = null;
    chatHistory = [];
    imageDataUrl = null;
    setStatus("");
  });

  analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    analyzeBtn.disabled = true;
    setStatus(
      ollamaReady
        ? "Analyzing with ensemble + vision assistant…"
        : "Analyzing with ensemble…"
    );

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

  function renderAnalysisAssist(data) {
    if (!analysisAssist) return;
    const assist = data.assist;
    if (!assist) {
      analysisAssist.classList.add("hidden");
      return;
    }

    analysisAssist.classList.remove("hidden");

    if (assist.error && !assist.analysis_support) {
      assistSupport.textContent = "";
      assistFeatures.textContent = "";
      assistQuality.textContent = "";
      assistWatch.innerHTML = "";
      assistError.textContent =
        assist.error + (assist.hint ? ` ${assist.hint}` : "");
      assistError.classList.remove("hidden");
      return;
    }

    assistError.classList.add("hidden");
    assistSupport.textContent = assist.analysis_support || "";
    assistFeatures.textContent = assist.visible_features || "";

    const quality = (assist.photo_quality || "").toLowerCase();
    if (quality) {
      const score =
        typeof assist.quality_score === "number"
          ? ` · ${Math.round(assist.quality_score * 100)}%`
          : "";
      assistQuality.textContent = `Photo quality for analysis: ${quality}${score}${
        assist.recommend_retake ? " · a clearer retake may help" : ""
      }`;
      assistQuality.className = `assist-quality quality-${quality}`;
    } else {
      assistQuality.textContent = "";
    }

    const watch = [
      ...(assist.what_to_watch || []),
      ...(assist.photo_tips || []).map((tip) => `Photo tip: ${tip}`),
    ];
    assistWatch.innerHTML = watch.map((item) => `<li>${item}</li>`).join("");
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
        "This match is uncertain — consider the alternatives below and ask in chat if you want help comparing them."
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

  function appendChatMessage(role, content) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble chat-${role}`;
    bubble.textContent = content;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function setupChat(data) {
    if (!chatPanel) return;

    latestAnalysis = data;
    chatHistory = [];
    chatMessages.innerHTML = "";
    chatPanel.classList.remove("hidden");

    const assist = data.assist || {};
    const opening =
      assist.opening_message ||
      (assist.ready || assist.analysis_support
        ? "Ask me about this result, what to watch for, or how it compares to the alternatives."
        : "Chat needs Ollama running locally. You can still read the ensemble result above.");

    appendChatMessage("assistant", opening);
    chatHistory.push({ role: "assistant", content: opening });

    const suggestions = [];
    if (data.prediction_name) {
      suggestions.push(`What does ${data.prediction_name} usually look like?`);
    }
    suggestions.push("How does this compare to the other possible matches?");
    suggestions.push("When should I see a dermatologist about this?");
    if (assist.questions_to_ask_doctor?.length) {
      suggestions.push(assist.questions_to_ask_doctor[0]);
    }

    chatSuggestions.innerHTML = "";
    suggestions.slice(0, 4).forEach((text) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chat-suggestion";
      btn.textContent = text;
      btn.addEventListener("click", () => {
        chatInput.value = text;
        chatForm.requestSubmit();
      });
      chatSuggestions.appendChild(btn);
    });

    const canChat = Boolean(assist.ready || assist.analysis_support || ollamaReady);
    chatInput.disabled = !canChat;
    chatSend.disabled = !canChat;
    refreshOllamaStatus();
  }

  chatForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!latestAnalysis || !chatInput.value.trim()) return;

    const message = chatInput.value.trim();
    chatInput.value = "";
    appendChatMessage("user", message);
    chatHistory.push({ role: "user", content: message });

    chatSend.disabled = true;
    chatInput.disabled = true;
    appendChatMessage("assistant", "Thinking…");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          analysis: latestAnalysis,
          history: chatHistory.slice(0, -1),
          image_base64: imageDataUrl,
        }),
      });
      const data = await response.json();
      chatMessages.lastChild?.remove();

      if (!response.ok) {
        throw new Error(data.detail || "Chat failed.");
      }

      appendChatMessage("assistant", data.reply);
      chatHistory.push({ role: "assistant", content: data.reply });
    } catch (error) {
      chatMessages.lastChild?.remove();
      appendChatMessage(
        "assistant",
        error.message || "Could not reach the assistant. Is Ollama running?"
      );
    } finally {
      chatSend.disabled = false;
      chatInput.disabled = false;
      chatInput.focus();
    }
  });

  function showResults(data) {
    const condition = data.condition || {};
    const risk = data.risk_level || "moderate";
    const confidencePct = Math.round((data.confidence ?? 0) * 100);

    riskBadge.textContent = RISK_LABELS[risk] || "Review recommended";
    riskBadge.className = `risk-badge ${risk}`;

    confidenceValue.textContent = `${confidencePct}% confidence`;

    renderEnsembleNote(data);
    renderAnalysisAssist(data);

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
        "The models did not fully agree or confidence is low. Use the chat below to compare options, and see a dermatologist if you are worried.";
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

    setupChat(data);
    resultsSection.classList.remove("hidden");
  }
}
