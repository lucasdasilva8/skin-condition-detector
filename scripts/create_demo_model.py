"""Create a demo model checkpoint for local API smoke testing.

Uses ImageNet-pretrained backbone with a random 22-class head.
Predictions are NOT medically meaningful — train on Kaggle for real results.
"""

import argparse
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from condition_info import CLASS_CODES  # noqa: E402
from model_factory import SUPPORTED_BACKBONES, build_model  # noqa: E402

DEFAULT_OUTPUT = {
    "resnet18": ROOT / "models" / "skin_model.pth",
    "efficientnet_b0": ROOT / "models" / "skin_model_efficientnet_b0.pth",
    "mobilenet_v3_large": ROOT / "models" / "skin_model_mobilenet_v3_large.pth",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a demo skin model checkpoint.")
    parser.add_argument(
        "--backbone",
        choices=SUPPORTED_BACKBONES,
        default="resnet18",
        help="Model backbone architecture",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output .pth path (defaults based on backbone)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Create demo checkpoints for every supported backbone",
    )
    args = parser.parse_args()

    backbones = list(SUPPORTED_BACKBONES) if args.all else [args.backbone]

    for backbone in backbones:
        output_path = args.output if args.output and not args.all else DEFAULT_OUTPUT[backbone]
        output_path.parent.mkdir(parents=True, exist_ok=True)

        model = build_model(backbone=backbone, num_classes=len(CLASS_CODES))
        checkpoint = {
            "model_state_dict": model.state_dict(),
            "class_codes": CLASS_CODES,
            "backbone": backbone,
            "dataset": "demo",
            "note": "Demo model for local testing only. Train on Kaggle for real predictions.",
        }
        torch.save(checkpoint, output_path)
        print(f"Saved {backbone} demo model to {output_path}")


if __name__ == "__main__":
    main()
