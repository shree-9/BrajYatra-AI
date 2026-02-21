"""
Planner Agent — distributes locations across days with
proximity-based grouping for efficient multi-day itineraries.
"""

from agents.scheduler_agent import schedule_day


def distribute_across_days(locations, days):
    """
    Distribute locations across trip days.

    Groups locations by city for proximity-based scheduling,
    then distributes evenly across days.
    """

    if not locations:
        return {}

    days = max(1, min(days, 7))

    # Group locations by city for proximity
    city_groups = {}
    for loc in locations:
        city = loc.get("location", {}).get("city", "Unknown")
        if city not in city_groups:
            city_groups[city] = []
        city_groups[city].append(loc)

    # Flatten back but keep city groups together
    ordered = []
    for city_locs in city_groups.values():
        ordered.extend(city_locs)

    # Distribute evenly across days
    per_day = max(1, len(ordered) // days)
    itinerary = {}
    index = 0

    for d in range(days):
        if index >= len(ordered):
            break

        # Last day gets all remaining locations
        if d == days - 1:
            day_places = ordered[index:]
        else:
            day_places = ordered[index:index + per_day]

        scheduled = schedule_day(day_places)
        if scheduled:
            itinerary[f"Day {d + 1}"] = scheduled

        index += per_day

    return itinerary
