# Dataset Guide

## Why not HAM10000 (kmader)?

HAM10000 is excellent for **pigmented skin lesions** but only has **7 classes** — mostly moles, keratoses, and skin cancers. It does **not** include:

- Acne, eczema, psoriasis, rosacea
- Fungal or viral infections (tinea, warts, candidiasis)
- Vitiligo, lupus, drug reactions
- Normal skin

If you want **broad skin condition coverage**, use the PacificRM dataset instead.

## Recommended dataset (22 classes)

**[Skin Disease Dataset](https://www.kaggle.com/datasets/pacificrm/skindiseasedataset)** by pacificrm

| How to add on Kaggle | |
|---|---|
| Search term | `Skin Disease Dataset` or `pacificrm` |
| Direct link | https://www.kaggle.com/datasets/pacificrm/skindiseasedataset |
| Easiest method | Open dataset page → click **New Notebook** |

### Classes included

Acne, Actinic Keratosis, Benign Tumors, Bullous, Candidiasis, Drug Eruption, Eczema, Infestations/Bites, Lichen, Lupus, Moles, Psoriasis, Rosacea, Seborrheic Keratoses, Skin Cancer, Sun/Sunlight Damage, Tinea, Unknown/Normal, Vascular Tumors, Vasculitis, Vitiligo, Warts

## Training (one session)

Use **`training/train_skin_diseases.ipynb`** — one **Run All** on Kaggle produces a single model for all 22 classes.

| Approach | Datasets to add | Time (GPU) | Best for |
|----------|-----------------|------------|----------|
| **Fastest** | PacificRM only | ~45–90 min | Broad skin coverage — start here |
| **Quick test** | PacificRM only + `QUICK_MODE = True` | ~25 min | Smoke test before full run |
| **Optional boost** | PacificRM + HAM10000 | ~60–120 min | Extra mole/cancer images (merged automatically) |

You do **not** need separate training runs for HAM10000 and PacificRM.

## Limitations (honest expectations)

Even with 22 classes, this does **not** cover all dermatology:

- Rare diseases may be missing
- Image quality and skin tone representation varies
- Phone photos may perform worse than clinical images
- "Normal" class helps but isn't perfect

### Future upgrades

- Merge [SCIN](https://github.com/google-research-datasets/scin) (Google) for more diverse real-world photos
- Add Fitzpatrick17k for broader skin tone coverage
- Fine-tune on phone-photo feedback over time

## Legacy: HAM10000 notebook

`training/train_ham10000_multiclass.ipynb` remains for reference if you only want the original 7 lesion types.
