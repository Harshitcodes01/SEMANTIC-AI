from models import Spec


def validate_spec(data):
    try:
        validated = Spec(**data)   #  strict validation

        return validated.model_dump(), True

    except Exception as e:
        print("Validation error:", e)
        return data, False