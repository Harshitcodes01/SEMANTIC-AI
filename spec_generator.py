import json

"""def generate_final_spec(parsed, traits, insights):
    return {
        "crop": parsed["crop"],
        "location": parsed["location"],
        "temperature": parsed["temperature"],
        "stress": parsed["stress"],
        "traits": [t["trait"] for t in traits],
        "scientific_basis": insights,
        "confidence": 0.90
    }"""
def generator_agent(plan, science):
    prompt = f"""
Generate final JSON.

STRICT RULES:
- temperature must be number (if unknown → use 25)
- location must be clear
- traits must match environment

Plan:
{plan}

Science:
{science}

Return:
{{
  "crop": "",
  "location": "",
  "temperature": 25,
  "stress": [],
  "traits": [],
  "scientific_basis": [],
  "confidence": 0.8
}}
"""
    output = run_llama(prompt)

    try:
        return json.loads(extract_json(output))
    except:
        return {
            "crop": "unknown",
            "location": "unknown",
            "temperature": 25,
            "stress": [],
            "traits": [],
            "scientific_basis": [],
            "confidence": 0.0
        }
    
def generate_final_spec(parsed, traits, insights):
    return {
        "crop": parsed.get("crop", "unknown"),
        "location": parsed.get("location", "unknown"),
        "temperature": parsed.get("temperature", 25),
        "stress": parsed.get("stress", []),
        "traits": [t["trait"] for t in traits],
        "scientific_basis": insights,
        "confidence": 0.8
    }