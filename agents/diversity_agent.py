"""
Diversity Agent — ensures itinerary has variety across categories.
"""


def enforce_diversity(locations, max_per_category=2):
    """
    Limit the number of locations per category to ensure
    a diverse itinerary experience.

    Args:
        locations: sorted list of locations (best first)
        max_per_category: max locations from same category

    Returns:
        filtered list maintaining diversity
    """

    result = []
    counts = {}

    for loc in locations:
        cat = loc.get("category", "Unknown")

        if counts.get(cat, 0) < max_per_category:
            result.append(loc)
            counts[cat] = counts.get(cat, 0) + 1

    return result
