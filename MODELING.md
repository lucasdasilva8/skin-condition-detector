# Improving model accuracy

Practical loop for SkinScan’s 22-class ensemble (ResNet18 + EfficientNet-B0 + MobileNetV3-Large).

## Goal

Optimize for **screening usefulness**, not only top-1 accuracy:

1. Higher top-1 / top-3 on held-out images  
2. Better **high-risk** handling (`skin_cancer`, `actinic_keratosis`, `lupus`, `vasculitis`)  
3. Lower **overconfident-wrong** rate (wrong answers that are *not* marked uncertain)

## 1. Measure a baseline

Labeled folders (same layout as training):

```text
data/
  acne/*.jpg
  moles/*.jpg
  eczema/*.jpg
  …
```

Or nested `train/Acne/…` — folder names are matched to class codes.

```bash
# From repo root, with torch + torchvision + scikit-learn installed
python scripts/evaluate_ensemble.py --data-dir /path/to/pacificrm_or_holdout

# Quicker sample
python scripts/evaluate_ensemble.py --data-dir /path/to/data --limit-per-class 30

# Also search better ensemble.json knobs
python scripts/evaluate_ensemble.py --data-dir /path/to/data --tune --json reports/eval.json
```

Read carefully:

| Metric | Meaning |
|--------|---------|
| Top-1 / Top-3 | Exact / “in alternatives” hits |
| Uncertain rate | How often the app hedges |
| Overconfident-wrong | Wrong **and** not uncertain — worst UX |
| High-risk safe rate | True high-risk caught as high-risk **or** uncertain |

Also keep a small **phone-photo** folder (blurry, flash, crops). If Kaggle rises and phone does not, the product did not improve.

## 2. Retrain

Use free Kaggle GPU:

1. Open [PacificRM Skin Disease Dataset](https://www.kaggle.com/datasets/pacificrm/skindiseasedataset)  
2. **New Notebook** on that page (attaches data)  
3. Upload `training/train_ensemble_backbones.ipynb`  
4. Accelerator → GPU · `QUICK_MODE = False`  
5. Download new `.pth` files into local `models/` next to `skin_model.pth`

Or locally / on Kaggle via script:

```bash
python scripts/train_backbone.py --backbone efficientnet_b0
python scripts/train_backbone.py --backbone mobilenet_v3_large
# optional: refresh ResNet18 too
python scripts/train_backbone.py --backbone resnet18
```

Training now uses stronger **phone-like augmentations** (blur, mild JPEG noise, wider color jitter) so models harden to real captures.

Prefer fixing the **weakest** backbone first over adding a 4th model.

## 3. Tune the ensemble (cheap)

Edit `models/ensemble.json`:

```json
{
  "models": [
    { "file": "skin_model.pth", "backbone": "resnet18", "weight": 1.0 },
    { "file": "skin_model_efficientnet_b0.pth", "backbone": "efficientnet_b0", "weight": 1.25 },
    { "file": "skin_model_mobilenet_v3_large.pth", "backbone": "mobilenet_v3_large", "weight": 1.0 }
  ],
  "uncertain_threshold": 0.35,
  "close_margin": 0.08
}
```

- Raise `uncertain_threshold` → more “uncertain” (safer, less cocky)  
- Raise `close_margin` → when top-2 classes are close, mark uncertain  
- Raise a model’s `weight` if that backbone wins more on **your** eval set  

`--tune` on `evaluate_ensemble.py` suggests values — verify them on phone photos before deploying to Render.

## 4. Accept or revert

Only ship new weights when:

- Top-1 ≥ baseline **or** overconfident-wrong clearly drops, **and**  
- High-risk safe rate does not get worse on your phone holdout  

Keep old `.pth` files until the new set wins.

## 5. Optional data upgrades

See [DATASETS.md](DATASETS.md):

- Merge HAM10000 for more mole / cancer images  
- Later: Fitzpatrick17k / SCIN for skin-tone and real-world diversity  

## Suggested cadence

| When | What |
|------|------|
| Now | Run `evaluate_ensemble.py` on any labeled split you have → note weakest classes |
| This week | Full Kaggle retrain of EfficientNet + MobileNet with updated augs |
| After retrain | Re-eval + `--tune` → update `ensemble.json` → re-check phone photos |
| Ongoing | Add misclassified phone photos into a personal holdout folder |

## Files

| Path | Role |
|------|------|
| `scripts/evaluate_ensemble.py` | Measure + optional ensemble tuning |
| `scripts/train_backbone.py` | Train one backbone |
| `training/train_ensemble_backbones.ipynb` | Kaggle train (EfficientNet + MobileNet) |
| `models/ensemble.json` | Weights + uncertainty knobs |
| `backend/model_loader.py` | Live ensemble + TTA inference |
