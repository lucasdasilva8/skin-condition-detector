from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from condition_catalog import CONDITIONS
from model_loader import get_predictor
from preprocess import DISCLAIMER, enhance_for_analysis, preprocess_image, validate_upload

app = FastAPI(
    title="Skin Condition Detector API",
    description="Educational skin condition identification API. Not for medical diagnosis.",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    try:
        predictor = get_predictor()
        ensemble = {
            "models_loaded": len(predictor.loaded_models),
            "backbones": [m.backbone for m in predictor.loaded_models],
        }
    except FileNotFoundError:
        ensemble = {"models_loaded": 0, "backbones": []}

    return {
        "status": "ok",
        "service": "skin-condition-detector",
        "ensemble": ensemble,
    }


@app.get("/conditions")
def list_conditions():
    return {
        "conditions": [
            {"code": code, **info} for code, info in CONDITIONS.items()
        ]
    }


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    enhance: str = Form("true"),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    use_enhance = _as_bool(enhance)

    try:
        validate_upload(file.content_type, len(content))

        enhance_meta = {"applied": False}
        analysis_bytes = content
        if use_enhance:
            analysis_bytes, enhance_meta = enhance_for_analysis(content)

        tensor = preprocess_image(analysis_bytes)
        result = get_predictor().predict(tensor)
        result["enhancement"] = enhance_meta
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to process image.") from exc

    return {**result, "disclaimer": DISCLAIMER}
