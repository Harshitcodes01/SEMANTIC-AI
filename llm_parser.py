import json
from llm import run_llama  
import re
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_call(prompt):
    return run_llama(prompt)

def extract_temperature(text):
    match = re.search(r'(\d+)\s*(°C|C|degree|degrees)?', text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def detect_stress(text):
    text = text.lower()
    stress = []

    if "heat" in text or "hot" in text:
        stress.append("heat")

    if "cold" in text or "low temperature" in text:
        stress.append("cold")

    if "drought" in text or "dry" in text or "desert" in text:
        stress.append("drought")

    if "salinity" in text or "salt" in text:
        stress.append("salinity")

    return stress


def detect_crop(text):
    text = text.lower()

    if "wheat" in text:
        return "wheat"
    if "rice" in text:
        return "rice"
    if "millet" in text:
        return "millet"

    return "unknown"


def clean_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]


def parse_prompt(user_input: str):

    # ------------------------
    # RULE-BASED EXTRACTION
    # ------------------------
    temperature = extract_temperature(user_input)
    stress = detect_stress(user_input)
    crop = detect_crop(user_input)

    # ------------------------
    # LLM ONLY FOR MISSING
    # ------------------------
    prompt = f"""
Extract missing structured fields.

Already known:
crop: {crop}
temperature: {temperature}
stress: {stress}

Fill missing fields only.

Return JSON:
{{
  "location": "",
  "traits_required": []
}}

Input:
{user_input}
"""

    #raw = run_llama(prompt)

    raw = cached_call(prompt)
    try:
        llm_data = json.loads(clean_json(raw))
    except:
        llm_data = {}

    # ------------------------
    # MERGE RESULTS
    # ------------------------
    return {
        "crop": crop,
        "location": llm_data.get("location", "unknown"),
        "temperature": temperature if temperature else 25,
        "stress": stress,
        "traits_required": llm_data.get("traits_required", [])
    }


def clean_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]


def parse_prompt(user_input: str):
    prompt = f"""
You are a strict scientific system.

Convert input into VALID JSON ONLY.

Rules:
- No explanation
- No extra text
- Only JSON
- Follow schema strictly

Schema:
{{
  "crop": "",
  "location": "",
  "temperature": number,
  "stress": [],
  "traits_required": []
}}

Input:
{user_input}
"""

    raw = run_llama(prompt)

    try:
        return json.loads(clean_json(raw))
    except:
        return {"error": "invalid_json", "raw": raw}