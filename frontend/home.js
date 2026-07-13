const API_URL = window.APP_CONFIG?.API_URL || "http://localhost:8000";

async function loadConditionsGrid() {
  const grid = document.getElementById("conditions-grid");
  if (!grid) return;

  try {
    const response = await fetch(`${API_URL}/conditions`);
    if (!response.ok) throw new Error("unavailable");

    const data = await response.json();
    grid.innerHTML = (data.conditions || [])
      .map((item) => `<li class="condition-chip">${item.short_name || item.name}</li>`)
      .join("");
  } catch {
    grid.innerHTML = `
      <li class="condition-chip">Acne</li>
      <li class="condition-chip">Eczema</li>
      <li class="condition-chip">Psoriasis</li>
      <li class="condition-chip">Rosacea</li>
      <li class="condition-chip">Moles</li>
      <li class="condition-chip">Skin Cancer</li>
      <li class="condition-chip muted">+ 16 more (start backend for full list)</li>
    `;
  }
}

loadConditionsGrid();
