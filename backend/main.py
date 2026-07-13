from typing import Any, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from condition_catalog import CONDITIONS
from model_loader import get_predictor
from ollama_assist import (
    analyze_with_ollama,
    chat_about_result,
    enhance_for_analysis,
    ollama_status,
)
from preprocess import DISCLAIMER, preprocess_image, validate_upload

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


class ChatTurn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    analysis: dict[str, Any] = Field(default_factory=dict)
    history: list[ChatTurn] = Field(default_factory=list)
    image_base64: Optional[str] = None


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
        "ollama": ollama_status(),
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

        # Integrate Ollama into analysis when available; never fail the prediction.
        status = ollama_status()
        if status.get("ready"):
            result["assist"] = analyze_with_ollama(content, result)
        else:
            result["assist"] = {
                "available": status.get("available", False),
                "ready": False,
                "error": status.get("error"),
                "hint": "Start Ollama and run: ollama pull qwen2.5vl:7b",
            }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to process image.") from exc

    return {**result, "disclaimer": DISCLAIMER}


@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    image_bytes = None
    if request.image_base64:
        import base64

        try:
            raw = request.image_base64
            if "," in raw and raw.startswith("data:"):
                raw = raw.split(",", 1)[1]
            image_bytes = base64.b64decode(raw)
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Invalid image_base64.") from exc

    history = [turn.model_dump() for turn in request.history]
    result = chat_about_result(
        message=message,
        analysis=request.analysis,
        history=history,
        image_bytes=image_bytes,
    )
    if not result.get("ok"):
        raise HTTPException(status_code=503, detail=result.get("error") or "Chat unavailable.")
    return result
