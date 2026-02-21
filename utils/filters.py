"""
Utility filters for the location dataset.
"""


def filter_by_city(locations, cities):
    """Filter locations to only include specified cities."""
    if not cities:
        return locations
    return [
        loc for loc in locations
        if loc.get("location", {}).get("city", "") in cities
    ]


def filter_by_category(locations, categories):
    """Filter locations to only include specified categories."""
    if not categories:
        return locations
    return [
        loc for loc in locations
        if loc.get("category", "") in categories
    ]


def filter_by_theme(locations, themes):
    """
    Filter locations that match at least one of the given themes.
    Matches against the 'recommended_for' field.
    """
    if not themes:
        return locations

    filtered = []
    for loc in locations:
        recommended = loc.get("visitor_profile_fit", {}).get("recommended_for", [])
        if any(theme in recommended for theme in themes):
            filtered.append(loc)

    return filtered if filtered else locations  # Fallback to all if nothing matches


def filter_accessible(locations, group_type="family"):
    """
    Filter locations based on accessibility for the group type.
    """
    if group_type == "elderly":
        return [
            loc for loc in locations
            if loc.get("visitor_profile_fit", {}).get("senior_friendly", False)
        ]

    if group_type == "family":
        return [
            loc for loc in locations
            if loc.get("visitor_profile_fit", {}).get("child_friendly", True)
        ]

    return locations
