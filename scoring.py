def compute_confidence(traits, expected_traits=3):
    if not traits:
        return 0.3

    score = len(traits) / expected_traits

    # clamp between 0.3 and 0.95
    return max(0.3, min(score, 0.95))