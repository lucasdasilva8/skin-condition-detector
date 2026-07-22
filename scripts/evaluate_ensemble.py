"""Evaluate the SkinScan ensemble on a labeled image folder.

Expected layout (same as training):
  data/acne/*.jpg
  data/moles/*.jpg
  …or… data/train/Acne/*.jpg

Examples:
  python scripts/evaluate_ensemble.py --data-dir /path/to/pacificrm
  python scripts/evaluate_ensemble.py --data-dir ./data/phone_holdout --limit-per-class 20
  python scripts/evaluate_ensemble.py --data-dir ./data --tune
  python scripts/evaluate_ensemble.py --data-dir ./data --json reports/eval.json

Focus metrics (educational screening):
  - overall top-1 / top-3 accuracy
  - high-risk recall (skin_cancer, actinic_keratosis, lupus, vasculitis)
  - overconfident-wrong rate (wrong + not marked uncertain)
  - uncertain rate
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import torch
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
from torchvision import transforms

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from condition_catalog import HIGH_RISK_CODES  # noqa: E402
from condition_info import CLASS_CODES, FOLDER_TO_CODE  # noqa: E402
from model_loader import EnsemblePredictor  # noqa: E402

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SPLIT_FOLDERS = {"train", "test", "val", "validation", "training", "testing"}

INFERENCE_TF = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def normalize_folder(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def folder_to_code(name: str) -> str:
    return FOLDER_TO_CODE.get(normalize_folder(name), normalize_folder(name))


def code_from_image_path(image_path: Path) -> str | None:
    skip = SPLIT_FOLDERS | {"input", "kaggle", "working", "data"}
    for part in reversed(image_path.parts):
        if part.lower() in skip:
            continue
        if part.startswith("skin") and "disease" in part.lower():
            continue
        code = folder_to_code(part)
        if code in CLASS_CODES:
            return code
    return None


def scan_images(input_dir: Path, limit_per_class: int | None = None) -> list[tuple[Path, str]]:
    by_code: dict[str, list[Path]] = defaultdict(list)
    for pattern in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.bmp", "**/*.webp"):
        for image_path in sorted(input_dir.glob(pattern)):
            code = code_from_image_path(image_path)
            if code is None:
                continue
            by_code[code].append(image_path)

    rows: list[tuple[Path, str]] = []
    for code, paths in sorted(by_code.items()):
        chosen = paths if limit_per_class is None else paths[:limit_per_class]
        rows.extend((path, code) for path in chosen)
    return rows


def agreement_from_preds(preds: list[str]) -> str:
    if len(preds) <= 1:
        return "single_model"
    top_count = max(preds.count(code) for code in set(preds))
    ratio = top_count / len(preds)
    if ratio == 1.0:
        return "high"
    if ratio >= 0.5:
        return "moderate"
    return "low"


def is_uncertain(probs: torch.Tensor, agreement: str, threshold: float, margin: float) -> bool:
    sorted_probs, _ = torch.sort(probs, descending=True)
    top_conf = sorted_probs[0].item()
    second_conf = sorted_probs[1].item() if len(sorted_probs) > 1 else 0.0
    if top_conf < threshold:
        return True
    if top_conf - second_conf < margin:
        return True
    if agreement == "low":
        return True
    return False


def combine_members(
    member_probs: list[torch.Tensor],
    weights: list[float],
    class_codes: list[str],
    threshold: float,
    margin: float,
) -> dict:
    stacked = torch.zeros(len(class_codes))
    total_w = 0.0
    member_preds: list[str] = []
    for probs, weight in zip(member_probs, weights):
        stacked = stacked + probs * weight
        total_w += weight
        member_preds.append(class_codes[int(probs.argmax().item())])

    probs = stacked / max(total_w, 1e-8)
    top_idx = int(probs.argmax().item())
    sorted_idx = torch.argsort(probs, descending=True)
    top3 = [class_codes[int(i)] for i in sorted_idx[:3]]
    agreement = agreement_from_preds(member_preds)
    uncertain = is_uncertain(probs, agreement, threshold, margin)
    return {
        "prediction": class_codes[top_idx],
        "confidence": float(probs[top_idx].item()),
        "top3": top3,
        "uncertain": uncertain,
        "agreement": agreement,
        "probs": probs,
    }


@torch.no_grad()
def collect_cache(predictor: EnsemblePredictor, rows: list[tuple[Path, str]]) -> list[dict]:
    cache: list[dict] = []
    for index, (path, true_code) in enumerate(rows, start=1):
        image = Image.open(path).convert("RGB")
        tensor = INFERENCE_TF(image).unsqueeze(0)
        members: list[torch.Tensor] = []
        for loaded in predictor.loaded_models:
            probs = predictor._predict_probabilities(loaded.model, tensor).detach().cpu()
            members.append(probs)
        cache.append(
            {
                "path": str(path),
                "true": true_code,
                "members": members,
            }
        )
        if index % 25 == 0 or index == len(rows):
            print(f"  Cached {index}/{len(rows)} images…")
    return cache


def score_cache(
    cache: list[dict],
    weights: list[float],
    class_codes: list[str],
    threshold: float,
    margin: float,
) -> dict:
    y_true: list[str] = []
    y_pred: list[str] = []
    top3_hits = 0
    uncertain_count = 0
    overconfident_wrong = 0
    high_risk_total = 0
    high_risk_caught = 0  # predicted high-risk OR marked uncertain
    high_risk_exact = 0

    confusion_pairs: Counter[tuple[str, str]] = Counter()

    for row in cache:
        result = combine_members(row["members"], weights, class_codes, threshold, margin)
        true = row["true"]
        pred = result["prediction"]
        y_true.append(true)
        y_pred.append(pred)

        if true in result["top3"]:
            top3_hits += 1
        if result["uncertain"]:
            uncertain_count += 1
        if pred != true and not result["uncertain"]:
            overconfident_wrong += 1
        if pred != true:
            confusion_pairs[(true, pred)] += 1

        if true in HIGH_RISK_CODES:
            high_risk_total += 1
            if pred == true:
                high_risk_exact += 1
            if pred in HIGH_RISK_CODES or result["uncertain"]:
                high_risk_caught += 1

    n = len(cache) or 1
    top1 = sum(t == p for t, p in zip(y_true, y_pred)) / n
    return {
        "n": len(cache),
        "top1": top1,
        "top3": top3_hits / n,
        "uncertain_rate": uncertain_count / n,
        "overconfident_wrong_rate": overconfident_wrong / n,
        "high_risk_total": high_risk_total,
        "high_risk_recall": (high_risk_exact / high_risk_total) if high_risk_total else None,
        "high_risk_safe_rate": (high_risk_caught / high_risk_total) if high_risk_total else None,
        "y_true": y_true,
        "y_pred": y_pred,
        "confusion_pairs": confusion_pairs,
        "threshold": threshold,
        "margin": margin,
        "weights": weights,
    }


def screening_score(metrics: dict) -> float:
    """Composite for threshold/weight tuning (higher is better)."""
    safe = metrics["high_risk_safe_rate"]
    safe_term = safe if safe is not None else metrics["top1"]
    return (
        0.45 * metrics["top1"]
        + 0.25 * metrics["top3"]
        + 0.25 * safe_term
        - 0.35 * metrics["overconfident_wrong_rate"]
    )


def print_summary(metrics: dict, class_codes: list[str], detailed: bool = True) -> None:
    print("\n=== Ensemble evaluation ===")
    print(f"Images: {metrics['n']}")
    print(f"Top-1 accuracy:              {metrics['top1']:.1%}")
    print(f"Top-3 accuracy:              {metrics['top3']:.1%}")
    print(f"Uncertain rate:              {metrics['uncertain_rate']:.1%}")
    print(f"Overconfident-wrong rate:    {metrics['overconfident_wrong_rate']:.1%}")
    if metrics["high_risk_total"]:
        print(
            f"High-risk exact recall:      {metrics['high_risk_recall']:.1%} "
            f"({metrics['high_risk_total']} images)"
        )
        print(f"High-risk safe rate*:        {metrics['high_risk_safe_rate']:.1%}")
        print("  * predicted high-risk class OR marked uncertain")
    print(
        f"Config: threshold={metrics['threshold']:.2f} "
        f"margin={metrics['margin']:.2f} weights={metrics['weights']}"
    )
    print(f"Screening score:             {screening_score(metrics):.4f}")

    if not detailed:
        return

    print("\n--- Per-class report ---")
    labels = [c for c in class_codes if c in set(metrics["y_true"]) | set(metrics["y_pred"])]
    print(
        classification_report(
            metrics["y_true"],
            metrics["y_pred"],
            labels=labels,
            zero_division=0,
            digits=3,
        )
    )

    pairs = metrics["confusion_pairs"].most_common(12)
    if pairs:
        print("--- Top confusion pairs (true → predicted) ---")
        for (true, pred), count in pairs:
            print(f"  {true:22s} → {pred:22s}  {count}")

    present = sorted(set(metrics["y_true"]))
    if len(present) >= 2:
        cm = confusion_matrix(metrics["y_true"], metrics["y_pred"], labels=present)
        # Spot classes with weakest diagonal recall
        weak = []
        for i, code in enumerate(present):
            row_sum = cm[i].sum()
            if row_sum == 0:
                continue
            recall = cm[i, i] / row_sum
            weak.append((recall, code, int(row_sum)))
        weak.sort()
        print("\n--- Weakest classes (recall) ---")
        for recall, code, count in weak[:8]:
            print(f"  {code:22s}  recall={recall:.1%}  n={count}")


def tune(
    cache: list[dict],
    class_codes: list[str],
    base_weights: list[float],
    n_members: int,
) -> dict:
    print("\n=== Tuning thresholds / weights ===")
    thresholds = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    margins = [0.04, 0.06, 0.08, 0.10, 0.12]
    weight_sets = [base_weights]

    # Simple per-model emphasis sweeps (others stay 1.0)
    if n_members >= 2:
        for i in range(n_members):
            for bump in (1.25, 1.5, 2.0):
                w = [1.0] * n_members
                w[i] = bump
                weight_sets.append(w)

    best = None
    best_score = float("-inf")
    best_base = None
    best_base_score = float("-inf")
    tried = 0
    for weights in weight_sets:
        is_base = list(weights) == list(base_weights)
        for threshold in thresholds:
            for margin in margins:
                metrics = score_cache(cache, weights, class_codes, threshold, margin)
                # Keep uncertain rate in a useful band for UX
                if not (0.05 <= metrics["uncertain_rate"] <= 0.55):
                    continue
                score = screening_score(metrics)
                tried += 1
                if score > best_score:
                    best_score = score
                    best = metrics
                if is_base and score > best_base_score:
                    best_base_score = score
                    best_base = metrics

    print(f"Tried {tried} configs in band (uncertain 5–55%).")
    if best is None:
        print("No config in band; falling back to current defaults.")
        return score_cache(
            cache, base_weights, class_codes, 0.35, 0.08
        )

    if best_base is not None and best_base is not best:
        print("\n--- Best threshold/margin only (weights unchanged) ---")
        print_summary(best_base, class_codes, detailed=False)

    print("\n--- Best overall (incl. weight sweep) ---")
    print_summary(best, class_codes, detailed=False)
    print(
        "\nSuggested models/ensemble.json updates:\n"
        f'  "uncertain_threshold": {best["threshold"]},\n'
        f'  "close_margin": {best["margin"]},'
    )
    print("  model weights:", best["weights"])
    return best


def metrics_to_jsonable(metrics: dict) -> dict:
    return {
        "n": metrics["n"],
        "top1": metrics["top1"],
        "top3": metrics["top3"],
        "uncertain_rate": metrics["uncertain_rate"],
        "overconfident_wrong_rate": metrics["overconfident_wrong_rate"],
        "high_risk_total": metrics["high_risk_total"],
        "high_risk_recall": metrics["high_risk_recall"],
        "high_risk_safe_rate": metrics["high_risk_safe_rate"],
        "threshold": metrics["threshold"],
        "margin": metrics["margin"],
        "weights": metrics["weights"],
        "screening_score": screening_score(metrics),
        "top_confusions": [
            {"true": t, "pred": p, "count": c}
            for (t, p), c in metrics["confusion_pairs"].most_common(20)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate SkinScan ensemble accuracy.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Root folder with class-named subfolders of images",
    )
    parser.add_argument(
        "--models-dir",
        type=Path,
        default=ROOT / "models",
        help="Directory with .pth checkpoints + ensemble.json",
    )
    parser.add_argument(
        "--limit-per-class",
        type=int,
        default=None,
        help="Optional cap per class (useful for quick phone holdouts)",
    )
    parser.add_argument(
        "--tune",
        action="store_true",
        help="Search better uncertain_threshold / close_margin / member weights",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="Write summary metrics JSON to this path",
    )
    args = parser.parse_args()

    if not args.data_dir.exists():
        raise SystemExit(f"Data dir not found: {args.data_dir}")

    rows = scan_images(args.data_dir, args.limit_per_class)
    if not rows:
        raise SystemExit(
            f"No labeled images under {args.data_dir}. "
            "Expect folders named like acne/, moles/, eczema/, …"
        )

    counts = Counter(code for _, code in rows)
    print(f"Found {len(rows)} images across {len(counts)} classes in {args.data_dir}")
    for code, count in counts.most_common():
        print(f"  {code:22s} {count}")

    config_path = args.models_dir / "ensemble.json"
    fallback = args.models_dir / "skin_model.pth"
    print(f"\nLoading ensemble from {args.models_dir} …")
    predictor = EnsemblePredictor(args.models_dir, config_path, fallback)
    print(
        f"Loaded {len(predictor.loaded_models)} models: "
        f"{[m.backbone for m in predictor.loaded_models]}"
    )

    print("\nRunning inference (with TTA flip, same as API)…")
    cache = collect_cache(predictor, rows)
    base_weights = [float(m.weight) for m in predictor.loaded_models]

    metrics = score_cache(
        cache,
        base_weights,
        predictor.class_codes,
        predictor.uncertain_threshold,
        predictor.close_margin,
    )
    print_summary(metrics, predictor.class_codes, detailed=True)

    tuned = None
    if args.tune:
        tuned = tune(
            cache,
            predictor.class_codes,
            base_weights,
            len(predictor.loaded_models),
        )

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "data_dir": str(args.data_dir),
            "models_dir": str(args.models_dir),
            "baseline": metrics_to_jsonable(metrics),
        }
        if tuned is not None:
            payload["tuned"] = metrics_to_jsonable(tuned)
        args.json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nWrote {args.json}")


if __name__ == "__main__":
    main()
