# Skin Condition Detector

Educational skin condition identification tool. Upload a photo of a skin area and get an AI-assisted identification with explanations, care guidance, and trusted sources.

**This is not a medical diagnosis. See a dermatologist for any concerning skin changes.**

## What it detects (22 conditions)

Trained on the [Skin Disease Dataset](https://www.kaggle.com/datasets/pacificrm/skindiseasedataset) (PacificRM), covering a broad range of common skin findings:

| Category | Conditions |
|----------|------------|
| **Inflammatory** | Acne, Eczema, Psoriasis, Rosacea, Lichen, Lupus, Drug Eruption, Bullous |
| **Infections** | Tinea (ringworm), Candidiasis, Warts, Infestations/Bites |
| **Lesions & growths** | Moles, Seborrheic Keratoses, Benign Tumors, Vascular Tumors, Warts |
| **Pigment & sun** | Vitiligo, Sun Damage, Actinic Keratosis |
| **Serious** | Skin Cancer |
| **Other** | Vasculitis, Normal/Unknown |

> **Note:** No AI model covers literally every skin condition. This covers 22 common categories — much broader than HAM10000 (7 lesion types only), but not exhaustive dermatology.

## Ensemble inference

Predictions combine up to **3 models** (ResNet18 + EfficientNet-B0 + MobileNetV3-Large) by averaging probabilities. Place these files in `models/`:

- `skin_model.pth`
- `skin_model_efficientnet_b0.pth`
- `skin_model_mobilenet_v3_large.pth`

Train the extra backbones with `training/train_ensemble_backbones.ipynb`. Config lives in `models/ensemble.json`.

## Optional: Ollama analysis chat (local)

When [Ollama](https://ollama.com) is running with a vision model, SkinScan automatically
folds it into analysis (no checkbox) and unlocks a chat under the results:

```bash
ollama pull qwen2.5vl:7b
```

- Mild image enhancement still runs before the ensemble
- Vision notes help interpret the ensemble prediction (features, uncertainty, what to watch)
- **Talk through this result** lets you ask follow-up questions about the photo and matches
- Without Ollama, ensemble analysis still works; chat stays locked until Ollama is ready

Env vars: `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT`

## Project structure

```
skin-condition-detector/
├── backend/          # FastAPI inference API (ensemble-aware)
├── frontend/         # Upload site + skin care Updates page
├── models/           # Ensemble checkpoints after Kaggle training
├── training/         # Kaggle notebooks (ResNet + ensemble backbones)
└── scripts/          # Helper scripts
```

## Quick start (local)

### 1. Create a demo model (optional, for testing)

```bash
python scripts/create_demo_model.py
```

### 2. Train the real model (Kaggle — free GPU)

1. Open **[Skin Disease Dataset](https://www.kaggle.com/datasets/pacificrm/skindiseasedataset)** on Kaggle.
2. Click **New Notebook** (dataset attaches automatically).
3. Upload or copy cells from `training/train_skin_diseases.ipynb`.
4. **Settings** → **Accelerator** → **GPU T4 x2** → Run all cells.
5. Download `skin_model.pth` → place in `models/skin_model.pth`.

**Can't find the dataset?** Search **"Skin Disease Dataset"** or **"pacificrm"** in Add Input — not "kmader".

See [DATASETS.md](DATASETS.md) for why we moved beyond HAM10000.

### 3. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 4. Start the frontend

```bash
cd frontend
python -m http.server 3000
```

Open http://localhost:3000

## API endpoints

- `GET /health` — health check
- `GET /conditions` — list all 22 detectable conditions with info
- `POST /predict` — upload an image, get identification + explanation + sources

## Disclaimer

Educational project only. Trained on web-collected images with varying quality. May not perform well on all skin tones or phone photos. Always consult a qualified healthcare professional for medical advice.
