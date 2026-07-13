"""Lookup helpers for skin condition metadata."""

from condition_catalog import CONDITIONS, HIGH_RISK_CODES, LEGACY_CODE_MAP

# Canonical class order for the 22-class PacificRM model.
CLASS_CODES = [
    "acne",
    "actinic_keratosis",
    "benign_tumors",
    "bullous",
    "candidiasis",
    "drug_eruption",
    "eczema",
    "infestations_bites",
    "lichen",
    "lupus",
    "moles",
    "psoriasis",
    "rosacea",
    "seborrheic_keratoses",
    "skin_cancer",
    "sun_damage",
    "tinea",
    "normal",
    "vascular_tumors",
    "vasculitis",
    "vitiligo",
    "warts",
]

# Maps Kaggle folder names (normalized) to canonical codes.
FOLDER_TO_CODE = {
    "acne": "acne",
    "actinic_keratosis": "actinic_keratosis",
    "benign_tumors": "benign_tumors",
    "bullous": "bullous",
    "candidiasis": "candidiasis",
    "drug_eruption": "drug_eruption",
    "eczema": "eczema",
    "infestations_bites": "infestations_bites",
    "infestations": "infestations_bites",
    "lichen": "lichen",
    "lupus": "lupus",
    "moles": "moles",
    "psoriasis": "psoriasis",
    "rosacea": "rosacea",
    "seborrheic_keratoses": "seborrheic_keratoses",
    "seborrh_keratoses": "seborrheic_keratoses",
    "skin_cancer": "skin_cancer",
    "sun_sunlight_damage": "sun_damage",
    "sun_damage": "sun_damage",
    "tinea": "tinea",
    "unknown_normal": "normal",
    "normal": "normal",
    "vascular_tumors": "vascular_tumors",
    "vasculitis": "vasculitis",
    "vitiligo": "vitiligo",
    "warts": "warts",
}


def normalize_folder_name(name: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def folder_name_to_code(folder_name: str) -> str:
    normalized = normalize_folder_name(folder_name)
    return FOLDER_TO_CODE.get(normalized, normalized)


def resolve_condition_code(code: str) -> str:
    return LEGACY_CODE_MAP.get(code, code)


def get_condition_info(code: str) -> dict:
    """Return condition info for a class code, with safe fallbacks."""
    resolved = resolve_condition_code(code)
    info = CONDITIONS.get(resolved, {})
    return {
        "code": resolved,
        "name": info.get("name", resolved.replace("_", " ").title()),
        "short_name": info.get("short_name", resolved.replace("_", " ").title()),
        "risk_level": info.get("risk_level", "moderate"),
        "description": info.get("description", "No description available."),
        "explanation": info.get(
            "explanation",
            "Consult a dermatologist for a detailed explanation of your skin finding.",
        ),
        "common_signs": info.get("common_signs", []),
        "what_it_means": info.get(
            "what_it_means", "Consult a dermatologist for an accurate assessment."
        ),
        "when_to_see_doctor": info.get(
            "when_to_see_doctor", "See a dermatologist if you have concerns."
        ),
        "recommended_actions": info.get("recommended_actions", []),
        "sources": info.get("sources", []),
    }
