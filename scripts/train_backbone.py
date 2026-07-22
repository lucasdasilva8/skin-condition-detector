"""Train an additional backbone for the skin-condition ensemble.

Designed for Kaggle: attach the PacificRM Skin Disease Dataset, set accelerator to GPU,
then run:

    python scripts/train_backbone.py --backbone efficientnet_b0
    python scripts/train_backbone.py --backbone mobilenet_v3_large

Outputs land in models/ (or /kaggle/working on Kaggle).
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
from glob import glob
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from condition_info import CLASS_CODES, FOLDER_TO_CODE  # noqa: E402
from model_factory import SUPPORTED_BACKBONES  # noqa: E402

CANONICAL_CODES = CLASS_CODES
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SPLIT_FOLDERS = {"train", "test", "val", "validation", "training", "testing"}


class RandomGaussianBlur:
    """Phone-like mild blur (applied with probability p)."""

    def __init__(self, p: float = 0.25, radius: tuple[float, float] = (0.1, 1.2)):
        self.p = p
        self.radius = radius

    def __call__(self, image: Image.Image) -> Image.Image:
        if torch.rand(1).item() > self.p:
            return image
        from PIL import ImageFilter

        low, high = self.radius
        r = float(torch.empty(1).uniform_(low, high).item())
        return image.filter(ImageFilter.GaussianBlur(radius=r))


class RandomJPEGCompression:
    """Simulate phone / messaging JPEG artifacts."""

    def __init__(self, p: float = 0.3, quality: tuple[int, int] = (40, 85)):
        self.p = p
        self.quality = quality

    def __call__(self, image: Image.Image) -> Image.Image:
        if torch.rand(1).item() > self.p:
            return image
        import io

        low, high = self.quality
        q = int(torch.randint(low, high + 1, (1,)).item())
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=q)
        buffer.seek(0)
        return Image.open(buffer).convert("RGB")


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
        if code in CANONICAL_CODES:
            return code
    return None


def scan_images(input_dir: Path) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    for pattern in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.bmp", "**/*.webp"):
        for image_path in input_dir.glob(pattern):
            code = code_from_image_path(image_path)
            if code is None:
                continue
            rows.append((str(image_path), CANONICAL_CODES.index(code)))
    return rows


class SkinDataset(Dataset):
    def __init__(self, rows: list[tuple[str, int]], transform):
        self.rows = rows
        self.transform = transform

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int):
        path, label = self.rows[index]
        image = Image.open(path).convert("RGB")
        return self.transform(image), label


def find_dataset_root(candidates: list[Path]) -> Path:
    for candidate in candidates:
        if candidate.exists() and scan_images(candidate):
            return candidate
    raise FileNotFoundError(
        "Could not find labeled skin images. Attach the PacificRM dataset on Kaggle "
        "or pass --data-dir pointing at train/ClassName/*.jpg folders."
    )


def build_weighted_sampler(labels: list[int]) -> torch.utils.data.WeightedRandomSampler:
    counts = torch.bincount(torch.tensor(labels), minlength=len(CANONICAL_CODES)).float()
    counts = counts.clamp(min=1.0)
    weights = 1.0 / counts[torch.tensor(labels)]
    return torch.utils.data.WeightedRandomSampler(
        weights=weights,
        num_samples=len(labels),
        replacement=True,
    )


def train_one_epoch(model, loader, criterion, optimizer, device) -> float:
    model.train()
    total_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * images.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, device) -> tuple[float, list[int], list[int]]:
    model.eval()
    correct = 0
    y_true: list[int] = []
    y_pred: list[int] = []
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        logits = model(images)
        preds = logits.argmax(dim=1)
        correct += (preds == labels).sum().item()
        y_true.extend(labels.cpu().tolist())
        y_pred.extend(preds.cpu().tolist())
    return correct / len(loader.dataset), y_true, y_pred


def build_pretrained_model(backbone: str, num_classes: int) -> nn.Module:
    """Load ImageNet weights, then replace the classification head."""
    if backbone == "resnet18":
        base = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        in_features = base.fc.in_features
        base.fc = nn.Sequential(nn.Dropout(0.3), nn.Linear(in_features, num_classes))
        return base
    if backbone == "efficientnet_b0":
        base = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
        in_features = base.classifier[1].in_features
        base.classifier = nn.Sequential(nn.Dropout(0.3), nn.Linear(in_features, num_classes))
        return base
    base = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.IMAGENET1K_V1)
    in_features = base.classifier[-1].in_features
    base.classifier[-1] = nn.Linear(in_features, num_classes)
    return base


def set_head_trainable(model: nn.Module, backbone: str) -> None:
    for param in model.parameters():
        param.requires_grad = False
    if backbone == "resnet18":
        for param in model.fc.parameters():
            param.requires_grad = True
    elif backbone == "efficientnet_b0":
        for param in model.classifier.parameters():
            param.requires_grad = True
    else:
        for param in model.classifier[-1].parameters():
            param.requires_grad = True


def main() -> None:
    parser = argparse.ArgumentParser(description="Train one ensemble backbone.")
    parser.add_argument(
        "--backbone",
        choices=SUPPORTED_BACKBONES,
        default="efficientnet_b0",
    )
    parser.add_argument("--quick", action="store_true", help="Fewer epochs for smoke tests")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Dataset root (defaults to /kaggle/input scan)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("/kaggle/working") if Path("/kaggle/working").exists() else ROOT / "models",
    )
    args = parser.parse_args()

    if args.data_dir:
        dataset_root = find_dataset_root([args.data_dir])
    else:
        dataset_root = find_dataset_root(
            [Path("/kaggle/input"), ROOT / "data", ROOT / "datasets"]
            + [Path(p) for p in glob("/kaggle/input/*") if Path(p).is_dir()]
        )

    rows = scan_images(dataset_root)
    if not rows:
        raise FileNotFoundError(f"No labeled images found under {dataset_root}")

    print(f"Found {len(rows)} images under {dataset_root}")

    train_rows, val_rows = train_test_split(
        rows,
        test_size=0.2,
        random_state=42,
        stratify=[label for _, label in rows],
    )

    train_tf = transforms.Compose(
        [
            transforms.Resize((256, 256)),
            transforms.RandomResizedCrop(224, scale=(0.65, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(p=0.1),
            transforms.RandomRotation(20),
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.25, hue=0.02),
            RandomGaussianBlur(p=0.25),
            RandomJPEGCompression(p=0.3),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            transforms.RandomErasing(p=0.15, scale=(0.02, 0.12)),
        ]
    )
    val_tf = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    train_loader = DataLoader(
        SkinDataset(train_rows, train_tf),
        batch_size=32,
        sampler=build_weighted_sampler([label for _, label in train_rows]),
        num_workers=2,
        pin_memory=torch.cuda.is_available(),
    )
    val_loader = DataLoader(
        SkinDataset(val_rows, val_tf),
        batch_size=32,
        shuffle=False,
        num_workers=2,
        pin_memory=torch.cuda.is_available(),
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training {args.backbone} on {device}")

    model = build_pretrained_model(args.backbone, len(CANONICAL_CODES)).to(device)
    criterion = nn.CrossEntropyLoss()

    head_epochs = 4 if args.quick else 8
    full_epochs = 6 if args.quick else 15

    set_head_trainable(model, args.backbone)
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)
    for epoch in range(head_epochs):
        loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        acc, _, _ = evaluate(model, val_loader, device)
        print(f"[head] epoch {epoch + 1}/{head_epochs} loss={loss:.4f} val_acc={acc:.4f}")

    for param in model.parameters():
        param.requires_grad = True
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    best_state = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(full_epochs):
        loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        acc, y_true, y_pred = evaluate(model, val_loader, device)
        print(f"[full] epoch {epoch + 1}/{full_epochs} loss={loss:.4f} val_acc={acc:.4f}")
        if acc > best_acc:
            best_acc = acc
            best_state = copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)
    _, y_true, y_pred = evaluate(model, val_loader, device)
    print(classification_report(y_true, y_pred, labels=list(range(len(CANONICAL_CODES))), target_names=CANONICAL_CODES, zero_division=0))

    output_name = {
        "resnet18": "skin_model.pth",
        "efficientnet_b0": "skin_model_efficientnet_b0.pth",
        "mobilenet_v3_large": "skin_model_mobilenet_v3_large.pth",
    }[args.backbone]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / output_name
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "class_codes": CANONICAL_CODES,
        "backbone": args.backbone,
        "dataset": "pacificrm/skindiseasedataset",
        "num_classes": len(CANONICAL_CODES),
        "val_accuracy": best_acc,
    }
    torch.save(checkpoint, output_path)
    print(f"Saved {args.backbone} checkpoint to {output_path}")


if __name__ == "__main__":
    main()
