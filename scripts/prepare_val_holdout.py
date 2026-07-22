"""Build a stratified 20% validation holdout matching the training recipe.

Uses the same split settings as training:
  train_test_split(..., test_size=0.2, random_state=42, stratify=labels)

Writes class-folder symlinks under --output-dir so evaluate_ensemble.py can
score only held-out images (not the training portion).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from condition_info import CLASS_CODES, FOLDER_TO_CODE  # noqa: E402

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SPLIT_FOLDERS = {"train", "test", "val", "validation", "training", "testing"}


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


def scan_images(input_dir: Path) -> list[tuple[Path, str]]:
    rows: list[tuple[Path, str]] = []
    for pattern in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.bmp", "**/*.webp"):
        for image_path in sorted(input_dir.glob(pattern)):
            code = code_from_image_path(image_path)
            if code is None:
                continue
            rows.append((image_path, code))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare stratified val holdout folders.")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "data" / "val_holdout",
    )
    parser.add_argument("--limit-per-class", type=int, default=None)
    args = parser.parse_args()

    rows = scan_images(args.data_dir)
    if not rows:
        raise SystemExit(f"No labeled images under {args.data_dir}")

    paths = [p for p, _ in rows]
    labels = [c for _, c in rows]
    _, val_paths, _, val_labels = train_test_split(
        paths,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    by_code: dict[str, list[Path]] = defaultdict(list)
    for path, code in zip(val_paths, val_labels):
        by_code[code].append(path)

    if args.output_dir.exists():
        for child in args.output_dir.rglob("*"):
            if child.is_symlink() or child.is_file():
                child.unlink()
        for child in sorted(args.output_dir.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for code, code_paths in sorted(by_code.items()):
        chosen = code_paths
        if args.limit_per_class is not None:
            chosen = code_paths[: args.limit_per_class]
        class_dir = args.output_dir / code
        class_dir.mkdir(parents=True, exist_ok=True)
        for src in chosen:
            dest = class_dir / src.name
            if dest.exists():
                dest = class_dir / f"{src.stem}_{abs(hash(str(src))) % 10_000_000}{src.suffix}"
            dest.symlink_to(src.resolve())
            total += 1

    print(f"Wrote {total} val images across {len(by_code)} classes → {args.output_dir}")
    for code, code_paths in sorted(by_code.items(), key=lambda item: -len(item[1])):
        n = len(code_paths) if args.limit_per_class is None else min(len(code_paths), args.limit_per_class)
        print(f"  {code:22s} {n}")


if __name__ == "__main__":
    main()
