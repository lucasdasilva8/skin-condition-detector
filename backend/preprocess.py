from io import BytesIO
from typing import Optional

from PIL import Image, ImageEnhance, ImageOps
from torchvision import transforms

IMAGE_SIZE = 224
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/jpg"}

DISCLAIMER = (
    "This is not a medical diagnosis. Results are for educational screening only. "
    "See a dermatologist for any concerning skin changes."
)

_inference_transform = transforms.Compose(
    [
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def validate_upload(content_type: Optional[str], file_size: int) -> None:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Only JPEG and PNG images are supported.")
    if file_size > MAX_FILE_SIZE:
        raise ValueError("Image must be 10 MB or smaller.")


def enhance_for_analysis(image_bytes: bytes) -> tuple[bytes, dict]:
    """Mild auto-contrast + sharpen so the classifier sees a clearer photo."""
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    enhanced = ImageOps.autocontrast(image, cutoff=1)
    enhanced = ImageEnhance.Sharpness(enhanced).enhance(1.15)
    enhanced = ImageEnhance.Contrast(enhanced).enhance(1.08)

    buffer = BytesIO()
    enhanced.save(buffer, format="JPEG", quality=92)
    meta = {
        "applied": True,
        "steps": ["autocontrast", "sharpen", "contrast"],
        "note": "Mild enhancement applied before model analysis.",
    }
    return buffer.getvalue(), meta


def preprocess_image(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return _inference_transform(image).unsqueeze(0)
