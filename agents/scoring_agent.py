"""
Scoring Agent — calculates a composite score for each location
based on ratings, crowd levels, weather sensitivity, and user preferences.
"""

from agents.crowd_agent import crowd_penalty


def score_location(loc, intent, weights):
    """
    Score a single location based on intent and adaptive weights.

    Higher score = better match for the user's trip.
    """

    score = 0.0

    # Base score from overall rating (0-5 scale)
    rating = loc.get("ratings", {}).get("overall_rating", 3.0)
    score += rating * weights.get("rating_weight", 1.0)

    # Crowd penalty
    score -= crowd_penalty(loc, intent.get("avoid_crowd", False)) * weights.get("crowd_penalty", 2.0) / 2.0

    # Weather / indoor preference penalty
    if intent.get("prefer_indoor", False):
        is_indoor = loc.get("weather_sensitivity", {}).get("is_indoor", False)
        if not is_indoor:
            score -= weights.get("weather_penalty", 1.5)

    # Theme matching bonus
    themes = intent.get("themes", [])
    if themes:
        recommended_for = loc.get("visitor_profile_fit", {}).get("recommended_for", [])
        matches = len(set(themes) & set(recommended_for))
        if matches > 0:
            score += matches * 0.5

    # City preference bonus
    cities = intent.get("cities", [])
    if cities:
        loc_city = loc.get("location", {}).get("city", "")
        if loc_city in cities:
            score += 1.0
        else:
            score -= 2.0  # Penalize locations outside preferred cities

    # Group type adjustments
    group_type = intent.get("group_type", "family")
    vp = loc.get("visitor_profile_fit", {})

    if group_type == "elderly" and vp.get("senior_friendly"):
        score += 0.5
    if group_type == "family" and vp.get("child_friendly"):
        score += 0.3
    if group_type in ("elderly", "family"):
        intensity = vp.get("physical_intensity_level", "Medium")
        if intensity == "High":
            score -= 0.5

    return round(score, 2)
