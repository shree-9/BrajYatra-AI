"""
Diversity Agent — ensures itinerary has variety across categories AND cities.
Deprioritizes restaurants/food stalls (they're auto-inserted as lunch).
"""


def enforce_diversity(locations, max_per_category=3, cities=None, min_per_city=2):
    """
    Limit locations per category to ensure a diverse itinerary,
    AND ensure each requested city gets fair representation.

    Restaurants and food stalls are limited to 1 per city max
    (since the scheduler auto-inserts lunch from the DB separately).
    """

    # Phase 1: Guarantee minimum per city (sightseeing only)
    result = []
    used_ids = set()

    if cities and len(cities) > 1:
        for city in cities:
            city_locs = [
                loc for loc in locations
                if (loc.get("location", {}).get("city", "") == city
                    and loc["id"] not in used_ids
                    and loc.get("category", "") not in ("Restaurant", "Food Stall", "Hotel"))
            ]
            for loc in city_locs[:min_per_city]:
                result.append(loc)
                used_ids.add(loc["id"])

    # Phase 2: Fill remaining with category-diverse selection
    cat_counts = {}
    for loc in result:
        cat = loc.get("category", "Unknown")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    # Count food/hotel limits per city
    food_per_city = {}

    for loc in locations:
        if loc["id"] in used_ids:
            continue

        cat = loc.get("category", "Unknown")
        city = loc.get("location", {}).get("city", "Unknown")

        # Skip restaurants/food stalls/hotels — they're auto-inserted
        if cat in ("Restaurant", "Food Stall", "Hotel"):
            if food_per_city.get(city, 0) < 1:
                food_per_city[city] = food_per_city.get(city, 0) + 1
                result.append(loc)
                used_ids.add(loc["id"])
            continue

        if cat_counts.get(cat, 0) < max_per_category:
            result.append(loc)
            used_ids.add(loc["id"])
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

    return result
