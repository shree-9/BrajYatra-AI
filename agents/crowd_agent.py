"""
Crowd Agent — adjusts scores based on crowd levels.
"""


def crowd_penalty(location, avoid_crowd):
    """
    Calculate crowd penalty for a location.

    Returns a negative score adjustment (higher = worse).
    """

    if not avoid_crowd:
        return 0

    crowd_level = location.get("crowd_data", {}).get("base_crowd_level", "Medium")

    penalties = {
        "High": 3.0,
        "Medium": 1.0,
        "Low": 0.0
    }

    return penalties.get(crowd_level, 1.0)
