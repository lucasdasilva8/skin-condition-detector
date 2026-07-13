"""Ollama vision assist for analysis support and follow-up chat.

Requires a local Ollama server with a vision model, e.g.:
  ollama pull qwen2.5vl:7b

Env vars:
  OLLAMA_BASE_URL   default http://127.0.0.1:11434
  OLLAMA_MODEL      default qwen2.5vl:7b
  OLLAMA_TIMEOUT    seconds, default 90
"""

from __future__ import annotations

import base64
import json
import os
import re
from io import BytesIO
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image, ImageEnhance, ImageOps

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5vl:7b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "90"))

FALLBACK_MODELS = [
    "qwen2.5vl:7b",
    "qwen2.5vl",
    "qwen3-vl",
    "llava",
]

SYSTEM_RULES = (
    "You assist SkinScan, an educational skin-photo tool. "
    "You are NOT a doctor and must not diagnose or prescribe. "
    "Do not recommend brand-name products. "
    "Be calm, plain-spoken, and cautious. "
    "Encourage seeing a dermatologist for concerning or changing findings."
)


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


def ollama_status() -> dict:
    """Report whether Ollama is reachable and which model will be used."""
    try:
        tags = _get_json(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        names = [m.get("name", "") for m in tags.get("models", [])]
        model = _resolve_model(names)
        return {
            "available": True,
            "base_url": OLLAMA_BASE_URL,
            "model": model,
            "installed_models": names[:20],
            "ready": model is not None,
        }
    except Exception as exc:
        return {
            "available": False,
            "base_url": OLLAMA_BASE_URL,
            "model": OLLAMA_MODEL,
            "ready": False,
            "error": str(exc),
        }


def _context_block(analysis: dict) -> str:
    alternatives = analysis.get("alternatives") or []
    alt_text = ", ".join(
        f"{a.get('name', a.get('code', '?'))} ({float(a.get('confidence', 0)):.0%})"
        for a in alternatives[:3]
    ) or "none"
    condition = analysis.get("condition") or {}
    return (
        f"Ensemble prediction: {analysis.get('prediction_name', 'unknown')} "
        f"({float(analysis.get('confidence') or 0):.0%} confidence).\n"
        f"Risk level: {analysis.get('risk_level', 'unknown')}.\n"
        f"Uncertain: {'yes' if analysis.get('uncertain') else 'no'}.\n"
        f"Other possible matches: {alt_text}.\n"
        f"Catalog summary: {condition.get('description') or condition.get('explanation') or 'n/a'}\n"
        f"When to see a doctor (catalog): {condition.get('when_to_see_doctor') or 'n/a'}"
    )


def analyze_with_ollama(image_bytes: bytes, analysis: dict) -> dict:
    """Vision pass that supports the ensemble analysis (not a separate toggle)."""
    status = ollama_status()
    if not status.get("available"):
        return {
            "available": False,
            "error": status.get("error") or "Ollama is not reachable.",
            "hint": "Start Ollama locally, then: ollama pull qwen2.5vl:7b",
        }

    model = status.get("model")
    if not model:
        return {
            "available": True,
            "ready": False,
            "error": f"No vision model found. Try: ollama pull {OLLAMA_MODEL}",
            "installed_models": status.get("installed_models", []),
        }

    prompt = f"""{SYSTEM_RULES}

You are reviewing a skin photo to help interpret a classifier ensemble result.

{_context_block(analysis)}

Look at the photo and reply with ONLY valid JSON (no markdown):
{{
  "photo_quality": "good" | "fair" | "poor",
  "quality_score": 0.0 to 1.0,
  "is_skin_photo": true or false,
  "photo_tips": ["up to 3 short tips if the photo could be better for analysis"],
  "visible_features": "2-3 sentences on what you can see (color, texture, borders, distribution) without diagnosing",
  "analysis_support": "2-4 sentences explaining how the visible features may support, conflict with, or leave uncertain the ensemble prediction and top alternatives",
  "what_to_watch": ["up to 3 plain-language things to monitor over coming days/weeks"],
  "questions_to_ask_doctor": ["up to 3 useful questions a person could ask a clinician"],
  "recommend_retake": true or false,
  "opening_message": "2 short sentences inviting the user to ask follow-up questions about this result"
}}

Rules:
- Prioritize analysis support over generic photo tips.
- If quality is poor, say so and how that limits confidence.
- Never invent a diagnosis that overrides the ensemble.
- Keep language educational and non-alarmist.
"""

    try:
        content = _chat_vision(model=model, prompt=prompt, image_bytes=image_bytes)
        parsed = _parse_json_object(content)
        return {
            "available": True,
            "ready": True,
            "model": model,
            "photo_quality": parsed.get("photo_quality", "fair"),
            "quality_score": _clamp01(parsed.get("quality_score")),
            "is_skin_photo": bool(parsed.get("is_skin_photo", True)),
            "photo_tips": _as_str_list(parsed.get("photo_tips"))[:3],
            "visible_features": str(parsed.get("visible_features") or "").strip(),
            "analysis_support": str(parsed.get("analysis_support") or "").strip(),
            "what_to_watch": _as_str_list(parsed.get("what_to_watch"))[:3],
            "questions_to_ask_doctor": _as_str_list(parsed.get("questions_to_ask_doctor"))[:3],
            "recommend_retake": bool(parsed.get("recommend_retake", False)),
            "opening_message": str(
                parsed.get("opening_message")
                or "You can ask me about this result, what to watch for, or when to see a doctor."
            ).strip(),
        }
    except Exception as exc:
        return {
            "available": True,
            "ready": True,
            "model": model,
            "error": f"Ollama analysis assist failed: {exc}",
        }


def chat_about_result(
    message: str,
    analysis: dict,
    history: Optional[list[dict]] = None,
    image_bytes: Optional[bytes] = None,
) -> dict:
    """Follow-up chat grounded in the current analysis result."""
    status = ollama_status()
    if not status.get("ready"):
        return {
            "ok": False,
            "error": status.get("error")
            or "Ollama is not ready. Start it and pull a vision model (qwen2.5vl:7b).",
            "available": status.get("available", False),
        }

    model = status["model"]
    history = history or []
    trimmed = history[-8:]

    assist = analysis.get("assist") or {}
    assist_bits = []
    if assist.get("analysis_support"):
        assist_bits.append(f"Prior vision notes: {assist['analysis_support']}")
    if assist.get("visible_features"):
        assist_bits.append(f"Visible features noted: {assist['visible_features']}")

    system = (
        f"{SYSTEM_RULES}\n\n"
        f"Current screening context:\n{_context_block(analysis)}\n"
        + ("\n".join(assist_bits) + "\n" if assist_bits else "")
        + "Answer the user's follow-up question helpfully in 2-5 short paragraphs or bullets. "
        "Stay within educational guidance. If unsure, say so."
    )

    messages: list[dict] = [{"role": "system", "content": system}]
    for turn in trimmed:
        role = turn.get("role")
        content = str(turn.get("content") or "").strip()
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content[:2000]})

    user_msg: dict[str, Any] = {"role": "user", "content": message.strip()[:2000]}
    if image_bytes:
        compact = _compact_jpeg(image_bytes, max_side=768)
        user_msg["images"] = [base64.b64encode(compact).decode("ascii")]
    messages.append(user_msg)

    try:
        reply = _chat_messages(model=model, messages=messages)
        return {"ok": True, "model": model, "reply": reply}
    except Exception as exc:
        return {"ok": False, "model": model, "error": str(exc)}


def _resolve_model(installed: list[str]) -> Optional[str]:
    preferred = [OLLAMA_MODEL, *FALLBACK_MODELS]
    for candidate in preferred:
        for name in installed:
            if name == candidate or name.startswith(f"{candidate}:"):
                return name
            base = candidate.split(":")[0]
            if name.startswith(base):
                return name
    return None


def _chat_vision(model: str, prompt: str, image_bytes: bytes) -> str:
    compact = _compact_jpeg(image_bytes, max_side=768)
    messages = [
        {
            "role": "user",
            "content": prompt,
            "images": [base64.b64encode(compact).decode("ascii")],
        }
    ]
    return _chat_messages(model=model, messages=messages)


def _chat_messages(model: str, messages: list[dict]) -> str:
    payload = {
        "model": model,
        "stream": False,
        "messages": messages,
        "options": {"temperature": 0.3},
    }
    data = _post_json(f"{OLLAMA_BASE_URL}/api/chat", payload, timeout=OLLAMA_TIMEOUT)
    message = data.get("message") or {}
    content = message.get("content") or data.get("response") or ""
    if not content.strip():
        raise RuntimeError("Empty response from Ollama")
    return content.strip()


def _compact_jpeg(image_bytes: bytes, max_side: int = 768) -> bytes:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image.thumbnail((max_side, max_side))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()


def _parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            text = text[start : end + 1]
    return json.loads(text)


def _as_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _clamp01(value: Any) -> Optional[float]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, min(1.0, number))


def _get_json(url: str, timeout: float) -> dict:
    req = Request(url, headers={"User-Agent": "SkinScan-OllamaAssist/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post_json(url: str, payload: dict, timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SkinScan-OllamaAssist/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail[:200]}") from exc
    except URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc
