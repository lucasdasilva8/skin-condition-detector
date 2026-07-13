"""Build skin-classification backbones with a shared 22-class head."""

from __future__ import annotations

import torch.nn as nn
from torchvision import models

SUPPORTED_BACKBONES = ("resnet18", "efficientnet_b0", "mobilenet_v3_large")


def build_model(backbone: str = "resnet18", num_classes: int = 22) -> nn.Module:
    backbone = backbone.lower()
    if backbone not in SUPPORTED_BACKBONES:
        raise ValueError(
            f"Unsupported backbone '{backbone}'. "
            f"Choose from: {', '.join(SUPPORTED_BACKBONES)}"
        )

    if backbone == "resnet18":
        model = models.resnet18(weights=None)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes),
        )
        return model

    if backbone == "efficientnet_b0":
        model = models.efficientnet_b0(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes),
        )
        return model

    model = models.mobilenet_v3_large(weights=None)
    in_features = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(in_features, num_classes)
    return model


def infer_backbone_from_state_dict(state_dict: dict) -> str:
    """Guess backbone from checkpoint keys when metadata is missing."""
    keys = list(state_dict.keys())
    if any(key.startswith("fc.") for key in keys):
        return "resnet18"
    if any(key.startswith("classifier.1.") for key in keys):
        return "efficientnet_b0"
    if any(key.startswith("classifier.3.") for key in keys):
        return "mobilenet_v3_large"
    return "resnet18"
