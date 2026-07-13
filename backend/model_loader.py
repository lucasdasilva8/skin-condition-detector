from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn

from condition_catalog import HIGH_RISK_CODES
from condition_info import CLASS_CODES, get_condition_info
from model_factory import build_model, infer_backbone_from_state_dict

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
DEFAULT_MODEL_PATH = MODELS_DIR / "skin_model.pth"
ENSEMBLE_CONFIG_PATH = MODELS_DIR / "ensemble.json"

DEFAULT_ENSEMBLE_CONFIG = {
    "models": [
        {"file": "skin_model.pth", "backbone": "resnet18", "weight": 1.0},
        {
            "file": "skin_model_efficientnet_b0.pth",
            "backbone": "efficientnet_b0",
            "weight": 1.0,
        },
        {
            "file": "skin_model_mobilenet_v3_large.pth",
            "backbone": "mobilenet_v3_large",
            "weight": 1.0,
        },
    ],
    "uncertain_threshold": 0.35,
    "close_margin": 0.08,
}


@dataclass
class LoadedModel:
    backbone: str
    path: Path
    weight: float
    class_codes: list[str]
    model: nn.Module


class EnsemblePredictor:
    """Average softmax probabilities across one or more trained backbones."""

    def __init__(
        self,
        models_dir: Path = MODELS_DIR,
        config_path: Path = ENSEMBLE_CONFIG_PATH,
        fallback_model_path: Path = DEFAULT_MODEL_PATH,
    ):
        self.models_dir = models_dir
        self.config = self._load_config(config_path)
        self.uncertain_threshold = float(self.config.get("uncertain_threshold", 0.35))
        self.close_margin = float(self.config.get("close_margin", 0.08))

        self.loaded_models = self._load_models(fallback_model_path)
        if not self.loaded_models:
            raise FileNotFoundError(
                f"No model checkpoints found in {models_dir}. "
                "Train on Kaggle (training/train_skin_diseases.ipynb) "
                "or run scripts/create_demo_model.py."
            )

        self.class_codes = self.loaded_models[0].class_codes
        for loaded in self.loaded_models[1:]:
            if loaded.class_codes != self.class_codes:
                raise ValueError(
                    "All ensemble models must share the same class order. "
                    f"Mismatch between {self.loaded_models[0].path.name} "
                    f"and {loaded.path.name}."
                )

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        for loaded in self.loaded_models:
            loaded.model.to(self.device)
            loaded.model.eval()

    @property
    def class_codes_list(self) -> list[str]:
        return self.class_codes

    def predict(self, tensor) -> dict:
        member_results = []
        weighted_probs = torch.zeros(len(self.class_codes), device=self.device)
        total_weight = 0.0

        for loaded in self.loaded_models:
            probs = self._predict_probabilities(loaded.model, tensor)
            weighted_probs += probs * loaded.weight
            total_weight += loaded.weight

            top_idx = int(probs.argmax().item())
            member_results.append(
                {
                    "backbone": loaded.backbone,
                    "file": loaded.path.name,
                    "prediction": self.class_codes[top_idx],
                    "prediction_name": get_condition_info(self.class_codes[top_idx])["name"],
                    "confidence": round(probs[top_idx].item(), 4),
                }
            )

        probabilities = weighted_probs / total_weight
        agreement = self._compute_agreement(member_results)
        uncertain = self._is_uncertain(probabilities, agreement)

        result = self._format_result(probabilities, uncertain=uncertain)
        result["ensemble"] = {
            "models_used": len(self.loaded_models),
            "agreement": agreement,
            "uncertain": uncertain,
            "members": member_results,
        }
        return result

    def _predict_probabilities(self, model: nn.Module, tensor) -> torch.Tensor:
        """Average predictions over original + horizontal flip (test-time augmentation)."""
        tensor = tensor.to(self.device)
        variants = [tensor, torch.flip(tensor, dims=[3])]
        probs = []

        with torch.no_grad():
            for variant in variants:
                logits = model(variant)
                probs.append(torch.softmax(logits, dim=1)[0])

        return torch.stack(probs).mean(dim=0)

    def _compute_agreement(self, member_results: list[dict]) -> str:
        if len(member_results) <= 1:
            return "single_model"

        predictions = [member["prediction"] for member in member_results]
        top_count = max(predictions.count(code) for code in set(predictions))
        ratio = top_count / len(predictions)

        if ratio == 1.0:
            return "high"
        if ratio >= 0.5:
            return "moderate"
        return "low"

    def _is_uncertain(self, probabilities: torch.Tensor, agreement: str) -> bool:
        sorted_probs, _ = torch.sort(probabilities, descending=True)
        top_conf = sorted_probs[0].item()
        second_conf = sorted_probs[1].item() if len(sorted_probs) > 1 else 0.0

        if top_conf < self.uncertain_threshold:
            return True
        if top_conf - second_conf < self.close_margin:
            return True
        if agreement == "low":
            return True
        return False

    def _format_result(self, probabilities: torch.Tensor, uncertain: bool = False) -> dict:
        top_idx = int(probabilities.argmax().item())
        top_code = self.class_codes[top_idx]
        top_confidence = probabilities[top_idx].item()

        all_probs = {
            code: round(probabilities[i].item(), 4)
            for i, code in enumerate(self.class_codes)
        }

        sorted_alternatives = sorted(
            all_probs.items(), key=lambda item: item[1], reverse=True
        )
        alternatives = [
            {
                "code": code,
                "confidence": conf,
                **get_condition_info(code),
            }
            for code, conf in sorted_alternatives[1:4]
        ]

        condition = get_condition_info(top_code)
        risk_level = condition["risk_level"]

        if uncertain:
            if top_code in HIGH_RISK_CODES:
                risk_level = "moderate"
            elif risk_level == "low":
                risk_level = "moderate"
        elif top_code in HIGH_RISK_CODES and top_confidence >= 0.4:
            risk_level = "high"
        elif top_code in HIGH_RISK_CODES:
            risk_level = "moderate"

        return {
            "prediction": top_code,
            "prediction_name": condition["name"],
            "confidence": round(top_confidence, 4),
            "risk_level": risk_level,
            "uncertain": uncertain,
            "condition": condition,
            "alternatives": alternatives,
            "probabilities": all_probs,
        }

    def _load_config(self, config_path: Path) -> dict:
        if config_path.exists():
            return json.loads(config_path.read_text(encoding="utf-8"))
        return DEFAULT_ENSEMBLE_CONFIG

    def _load_models(self, fallback_model_path: Path) -> list[LoadedModel]:
        loaded: list[LoadedModel] = []
        entries = self.config.get("models", DEFAULT_ENSEMBLE_CONFIG["models"])

        for entry in entries:
            file_name = entry["file"]
            model_path = self.models_dir / file_name
            if not model_path.exists():
                continue

            checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
            class_codes = checkpoint.get("class_codes", CLASS_CODES)
            backbone = checkpoint.get("backbone") or entry.get("backbone")
            if not backbone:
                backbone = infer_backbone_from_state_dict(checkpoint["model_state_dict"])

            model = build_model(backbone=backbone, num_classes=len(class_codes))
            model.load_state_dict(checkpoint["model_state_dict"])

            loaded.append(
                LoadedModel(
                    backbone=backbone,
                    path=model_path,
                    weight=float(entry.get("weight", 1.0)),
                    class_codes=class_codes,
                    model=model,
                )
            )

        if loaded:
            return loaded

        if fallback_model_path.exists():
            checkpoint = torch.load(
                fallback_model_path, map_location="cpu", weights_only=False
            )
            class_codes = checkpoint.get("class_codes", CLASS_CODES)
            backbone = checkpoint.get("backbone") or infer_backbone_from_state_dict(
                checkpoint["model_state_dict"]
            )
            model = build_model(backbone=backbone, num_classes=len(class_codes))
            model.load_state_dict(checkpoint["model_state_dict"])
            return [
                LoadedModel(
                    backbone=backbone,
                    path=fallback_model_path,
                    weight=1.0,
                    class_codes=class_codes,
                    model=model,
                )
            ]

        return []


# Backward-compatible alias used by older scripts.
SkinConditionPredictor = EnsemblePredictor

_predictor: Optional[EnsemblePredictor] = None


def get_predictor() -> EnsemblePredictor:
    global _predictor
    if _predictor is None:
        _predictor = EnsemblePredictor()
    return _predictor
