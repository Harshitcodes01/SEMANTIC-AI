from vector_search import search_traits


def fast_parse(input_text):
    input_text = input_text.lower()

    crop = "unknown"
    location = "unknown"
    temperature = 25
    stress = []

    # crop detection
    if "wheat" in input_text:
        crop = "wheat"
    elif "rice" in input_text:
        crop = "rice"
    elif "millet" in input_text:
        crop = "millet"

    # temperature + stress
    if "cold" in input_text:
        temperature = 10
        stress.append("cold")

    if "heat" in input_text or "hot" in input_text:
        temperature = 45
        stress.append("heat")

    if "desert" in input_text:
        location = "desert"
        stress.append("drought")

    return {
        "crop": crop,
        "location": location,
        "temperature": temperature,
        "stress": stress
    }


def fast_pipeline(user_input):
    parsed = fast_parse(user_input)

    traits = search_traits(user_input)

    return {
        "crop": parsed["crop"],
        "location": parsed["location"],
        "temperature": parsed["temperature"],
        "stress": parsed["stress"],
        "traits": [t["trait"] for t in traits],
        "scientific_basis": [],
        "confidence": 0.7
    }