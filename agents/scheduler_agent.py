"""
Scheduler Agent — assigns time slots to locations for each day,
respecting opening hours, visit durations, buffer times,
and auto-inserts lunch breaks at nearby restaurants.
"""

import json
import os
from datetime import datetime, timedelta
from config import DAY_START_HOUR, DAY_END_HOUR, LOCATIONS_PATH


# Load all locations once for restaurant lookup
_all_locations = None

def _get_all_locations():
    global _all_locations
    if _all_locations is None:
        with open(LOCATIONS_PATH, "r", encoding="utf-8") as f:
            _all_locations = json.load(f)
    return _all_locations


def schedule_day(locations):
    """
    Schedule a list of locations into time slots for one day.

    Features:
    - Uses actual visit durations from data (not fixed 90 min)
    - Auto-inserts lunch break between 12:00-14:00
    - Generates Google Maps route URL for the day
    - Fills the full day (08:00-18:00)
    """

    start_time = datetime.strptime(f"{DAY_START_HOUR:02d}:00", "%H:%M")
    end_time = datetime.strptime(f"{DAY_END_HOUR:02d}:00", "%H:%M")
    lunch_window_start = datetime.strptime("12:00", "%H:%M")
    lunch_window_end = datetime.strptime("14:00", "%H:%M")

    current = start_time
    schedule = []
    lunch_inserted = False

    # Separate actual sightseeing from food places
    sightseeing = []
    food_places = []
    for loc in locations:
        cat = loc.get("category", "")
        if cat in ("Restaurant", "Food Stall"):
            food_places.append(loc)
        else:
            sightseeing.append(loc)

    all_locs = _get_all_locations()

    for loc in sightseeing:
        # Check if it's lunch time (between 12:00-14:00)
        if not lunch_inserted and current >= lunch_window_start and current < lunch_window_end:
            lunch_city = loc.get("location", {}).get("city", "")
            lunch_loc = _pick_lunch(food_places, lunch_city, all_locs)
            if lunch_loc:
                lunch_duration = 45
                lunch_end = current + timedelta(minutes=lunch_duration)
                schedule.append({
                    "place": lunch_loc["name"],
                    "place_id": lunch_loc.get("id"),
                    "category": lunch_loc.get("category", "Restaurant"),
                    "city": lunch_loc.get("location", {}).get("city", ""),
                    "start": current.strftime("%H:%M"),
                    "end": lunch_end.strftime("%H:%M"),
                    "duration_minutes": lunch_duration,
                    "type": "lunch_break",
                    "entry_fee": 0,
                    "booking_url": None
                })
                current = lunch_end + timedelta(minutes=10)
                lunch_inserted = True

        # Get actual visit duration from data
        duration = loc.get("operational_info", {}).get(
            "avg_visit_duration_minutes", 60
        )

        end_visit = current + timedelta(minutes=duration)

        if end_visit > end_time:
            break

        # Entry fee info
        pricing = loc.get("pricing", {})
        entry_fee = pricing.get("entry_fee", {}).get("Indians", 0)
        booking_url = pricing.get("booking_url")

        schedule.append({
            "place": loc["name"],
            "place_id": loc.get("id"),
            "category": loc.get("category", ""),
            "city": loc.get("location", {}).get("city", ""),
            "start": current.strftime("%H:%M"),
            "end": end_visit.strftime("%H:%M"),
            "duration_minutes": duration,
            "type": "sightseeing",
            "entry_fee": entry_fee,
            "booking_url": booking_url
        })

        buffer_time = loc.get("nearby_context", {}).get(
            "recommended_buffer_time_minutes", 15
        )
        current = end_visit + timedelta(minutes=buffer_time)

    # If lunch wasn't inserted yet and we passed through mid-day
    if not lunch_inserted and current >= lunch_window_start and current < lunch_window_end:
        city = schedule[-1]["city"] if schedule else ""
        lunch_loc = _pick_lunch(food_places, city, all_locs)
        if lunch_loc:
            lunch_duration = 45
            lunch_end = current + timedelta(minutes=lunch_duration)
            if lunch_end <= end_time:
                schedule.append({
                    "place": lunch_loc["name"],
                    "place_id": lunch_loc.get("id"),
                    "category": lunch_loc.get("category", "Restaurant"),
                    "city": lunch_loc.get("location", {}).get("city", ""),
                    "start": current.strftime("%H:%M"),
                    "end": lunch_end.strftime("%H:%M"),
                    "duration_minutes": lunch_duration,
                    "type": "lunch_break",
                    "entry_fee": 0,
                    "booking_url": None
                })

    # Generate Google Maps route URL
    route_url = _build_maps_url(schedule, locations)

    # Attach route_url to first item
    if schedule:
        schedule[0]["maps_route_url"] = route_url

    return schedule


def _pick_lunch(food_places, city, all_locations):
    """Pick the best restaurant for lunch, preferring same city."""
    # First: from the passed food places
    if food_places:
        city_food = [r for r in food_places if r.get("location", {}).get("city", "") == city]
        if city_food:
            return city_food[0]
        return food_places[0]

    # Fallback: find any restaurant from all_locations in same city
    if city and all_locations:
        for loc in all_locations:
            if (loc.get("category", "") in ("Restaurant", "Food Stall")
                    and loc.get("location", {}).get("city", "") == city):
                return loc

    return None


def _build_maps_url(schedule, locations):
    """Build a Google Maps directions URL from the scheduled places."""
    waypoints = []

    for item in schedule:
        place_id = item.get("place_id")
        if place_id:
            for loc in locations:
                if loc.get("id") == place_id:
                    coords = loc.get("location", {}).get("coordinates", {})
                    lat = coords.get("lat")
                    lng = coords.get("lng")
                    if lat and lng:
                        waypoints.append(f"{lat},{lng}")
                    break
            else:
                # Also search in all locations
                for loc in _get_all_locations():
                    if loc.get("id") == place_id:
                        coords = loc.get("location", {}).get("coordinates", {})
                        lat = coords.get("lat")
                        lng = coords.get("lng")
                        if lat and lng:
                            waypoints.append(f"{lat},{lng}")
                        break
        else:
            name = item.get("place", "").replace(" ", "+")
            city = item.get("city", "").replace(" ", "+")
            if name:
                waypoints.append(f"{name},{city}")

    if len(waypoints) < 2:
        return None

    url = f"https://www.google.com/maps/dir/{'/'.join(waypoints)}"
    return url
