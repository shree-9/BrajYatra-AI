"""
Planner Agent — distributes locations across days with
city-aware grouping for efficient multi-day itineraries.
"""

from agents.scheduler_agent import schedule_day


def distribute_across_days(locations, days, cities=None):
    """
    Distribute locations across trip days.

    Strategy:
    - If multiple cities: assign ~1 city per day (adjacent cities can share a day)
    - If more days than cities: split the largest city group across days
    - Each day is then scheduled with time slots and lunch breaks
    """

    if not locations:
        return {}

    days = max(1, min(days, 7))

    # Group locations by city
    city_groups = {}
    for loc in locations:
        city = loc.get("location", {}).get("city", "Unknown")
        if city not in city_groups:
            city_groups[city] = []
        city_groups[city].append(loc)

    # Determine city order — requested cities first, then others
    if cities:
        ordered_cities = [c for c in cities if c in city_groups]
        for c in city_groups:
            if c not in ordered_cities:
                ordered_cities.append(c)
    else:
        # Sort by number of locations (largest group first)
        ordered_cities = sorted(city_groups.keys(), key=lambda c: -len(city_groups[c]))

    # Assign cities to days
    num_cities = len(ordered_cities)

    if num_cities == 0:
        return {}

    if num_cities >= days:
        # More cities than days — assign 1 city per day (some cities may share)
        day_assignments = []
        per_day = max(1, num_cities // days)
        idx = 0
        for d in range(days):
            if d == days - 1:
                day_assignments.append(ordered_cities[idx:])
            else:
                day_assignments.append(ordered_cities[idx:idx + per_day])
            idx += per_day
    else:
        # More days than cities — split larger city groups
        day_assignments = []
        days_per_city = {}
        remaining_days = days

        for i, city in enumerate(ordered_cities):
            if i == len(ordered_cities) - 1:
                days_per_city[city] = remaining_days
            else:
                # Assign proportionally by number of locations
                total_locs = sum(len(city_groups[c]) for c in ordered_cities[i:])
                city_locs = len(city_groups[city])
                city_days = max(1, round(remaining_days * city_locs / total_locs))
                days_per_city[city] = min(city_days, remaining_days - (len(ordered_cities) - i - 1))
            remaining_days -= days_per_city[city]

        for city in ordered_cities:
            n = days_per_city[city]
            locs = city_groups[city]
            per_day = max(1, len(locs) // n)

            for d in range(n):
                if d == n - 1:
                    day_assignments.append([city])
                else:
                    day_assignments.append([city])

    # Build the itinerary
    itinerary = {}
    used_ids = set()
    day_num = 1

    for assignment in day_assignments:
        day_locs = []
        for city in assignment:
            for loc in city_groups.get(city, []):
                if loc["id"] not in used_ids:
                    day_locs.append(loc)
                    used_ids.add(loc["id"])

        if not day_locs:
            continue

        # Limit to reasonable number per day (max 8, enough for 08:00-18:00)
        day_locs = day_locs[:8]

        scheduled = schedule_day(day_locs)
        if scheduled:
            itinerary[f"Day {day_num}"] = scheduled
            day_num += 1

    return itinerary
