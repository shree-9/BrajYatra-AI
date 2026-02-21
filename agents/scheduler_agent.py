"""
Scheduler Agent — assigns time slots to locations for each day,
respecting opening hours, visit durations, and buffer times.
"""

from datetime import datetime, timedelta
from config import DAY_START_HOUR, DAY_END_HOUR


def schedule_day(locations):
    """
    Schedule a list of locations into time slots for one day.

    Respects:
      - Day start/end hours from config
      - Average visit duration from location data
      - Buffer time between locations
    """

    start_time = datetime.strptime(f"{DAY_START_HOUR:02d}:00", "%H:%M")
    end_time = datetime.strptime(f"{DAY_END_HOUR:02d}:00", "%H:%M")

    current = start_time
    schedule = []

    for loc in locations:
        duration = loc.get("operational_info", {}).get(
            "avg_visit_duration_minutes", 60
        )
        end_visit = current + timedelta(minutes=duration)

        if end_visit > end_time:
            break

        schedule.append({
            "place": loc["name"],
            "place_id": loc.get("id"),
            "category": loc.get("category", ""),
            "city": loc.get("location", {}).get("city", ""),
            "start": current.strftime("%H:%M"),
            "end": end_visit.strftime("%H:%M"),
            "duration_minutes": duration
        })

        buffer_time = loc.get("nearby_context", {}).get(
            "recommended_buffer_time_minutes", 15
        )
        current = end_visit + timedelta(minutes=buffer_time)

    return schedule
