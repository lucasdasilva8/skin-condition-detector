"""Validate that the skin model checkpoint loads and runs inference."""

import sys
from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from model_loader import EnsemblePredictor  # noqa: E402

MODEL_PATH = ROOT / "models" / "skin_model.pth"


def main() -> None:
    if not MODEL_PATH.exists():
        print(f"Model not found at {MODEL_PATH}")
        print("Run: python scripts/create_demo_model.py")
        sys.exit(1)

    predictor = EnsemblePredictor(MODEL_PATH.parent, MODEL_PATH.parent / "ensemble.json", MODEL_PATH)

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    dummy = Image.new("RGB", (224, 224), color=(200, 150, 120))
    tensor = transform(dummy).unsqueeze(0)
    result = predictor.predict(tensor)

    print("Model loaded successfully.")
    print(f"Models in ensemble: {len(predictor.loaded_models)}")
    print(f"Backbones: {[m.backbone for m in predictor.loaded_models]}")
    print(f"Classes: {predictor.class_codes_list}")
    print(f"Sample prediction: {result['prediction_name']} ({result['confidence']:.2%})")
    print(f"Risk level: {result['risk_level']}")
    if result.get("ensemble"):
        print(f"Agreement: {result['ensemble']['agreement']}")


if __name__ == "__main__":
    main()
