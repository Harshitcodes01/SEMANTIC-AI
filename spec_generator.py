def generate_final_spec(parsed, traits, insights):
    return {
        "crop": parsed["crop"],
        "location": parsed["location"],
        "temperature": parsed["temperature"],
        "stress": parsed["stress"],
        "traits": [t["trait"] for t in traits],
        "scientific_basis": insights,
        "confidence": 0.90
    }