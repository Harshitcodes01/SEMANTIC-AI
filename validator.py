from models import Spec


def validate_spec(data):
    required_keys = [
        "crop",
        "location",
        "temperature",
        "stress",
        "traits",
        "scientific_basis",
        "confidence"
    ]

    for key in required_keys:
        if key not in data:
            return data, False

    return data, True