"""
Budget Agent — full trip cost estimation including travel, food, accommodation, and sightseeing.
"""

from agents.travel_estimator import (
    get_travel_estimate,
    get_daily_food_budget,
    get_accommodation_estimate
)


def estimate_budget(locations, budget_type="moderate"):
    """
    Estimate sightseeing budget for a list of locations.
    This covers entry fees and on-site expenses only.
    """

    breakdown = []
    total = 0

    for loc in locations:
        pricing = loc.get("pricing", {})
        entry_fee = pricing.get("entry_fee", {})
        extras = pricing.get("avg_additional_expense", 0)

        fee = entry_fee.get("Indians", 0)
        location_cost = fee + extras
        total += location_cost

        breakdown.append({
            "place": loc["name"],
            "category": loc.get("category", ""),
            "entry_fee": fee,
            "additional_expense": extras,
            "subtotal": location_cost
        })

    multiplier = {"low": 0.7, "high": 1.5}.get(budget_type, 1.0)

    return {
        "estimated_total": int(total * multiplier),
        "budget_type": budget_type,
        "multiplier": multiplier,
        "breakdown": breakdown,
        "note": "Sightseeing costs only (entry fees + on-site expenses)."
    }


def estimate_full_trip_budget(
    locations, budget_type="moderate", days=2, origin_city=None, persons=1
):
    """
    Estimate FULL trip cost including travel, accommodation, food, and sightseeing.

    Returns a comprehensive breakdown dict.
    """

    # 1. Sightseeing costs
    sightseeing = estimate_budget(locations, budget_type)

    # 2. Food costs
    food_daily = get_daily_food_budget(budget_type)
    food_total = food_daily["total"] * days * persons

    # 3. Accommodation costs
    nights = max(0, days - 1)
    accommodation = get_accommodation_estimate(budget_type, nights)
    accommodation_total_min = accommodation["total_min"]
    accommodation_total_max = accommodation["total_max"]

    # 4. Travel costs
    travel = None
    travel_total_min = 0
    travel_total_max = 0

    if origin_city:
        travel = get_travel_estimate(origin_city)
        if travel.get("train"):
            travel_total_min = travel["train"]["fare_low"] * persons * 2  # round trip
            travel_total_max = travel["train"]["fare_high"] * persons * 2
        elif travel.get("bus"):
            travel_total_min = travel["bus"]["fare_low"] * persons * 2
            travel_total_max = travel["bus"]["fare_high"] * persons * 2

    # 5. Totals
    grand_total_min = (
        sightseeing["estimated_total"]
        + food_total
        + accommodation_total_min
        + travel_total_min
    )

    grand_total_max = (
        int(sightseeing["estimated_total"] * 1.3)
        + food_total
        + accommodation_total_max
        + travel_total_max
    )

    return {
        "summary": {
            "days": days,
            "nights": nights,
            "persons": persons,
            "budget_type": budget_type,
            "origin_city": origin_city,
            "grand_total_min": grand_total_min,
            "grand_total_max": grand_total_max
        },
        "breakdown": {
            "travel": {
                "origin": origin_city,
                "destination": "Braj Region (Mathura)",
                "round_trip": True,
                "cost_min": travel_total_min,
                "cost_max": travel_total_max,
                "details": travel
            } if origin_city else None,
            "accommodation": {
                "type": accommodation["accommodation_type"],
                "per_night_min": accommodation["per_night_min"],
                "per_night_max": accommodation["per_night_max"],
                "nights": nights,
                "cost_min": accommodation_total_min,
                "cost_max": accommodation_total_max
            },
            "food": {
                "per_day": food_daily["total"],
                "per_day_breakdown": food_daily,
                "days": days,
                "persons": persons,
                "cost_total": food_total
            },
            "sightseeing": {
                "places_count": len(locations),
                "cost_total": sightseeing["estimated_total"],
                "breakdown": sightseeing["breakdown"]
            }
        },
        "tips": _get_budget_tips(budget_type, origin_city)
    }


def _get_budget_tips(budget_type, origin_city=None):
    tips = []

    if budget_type == "low":
        tips.append("Stay at dharamshalas for cheapest accommodation (₹200-500/night)")
        tips.append("Eat at food stalls and local bhojanalays instead of restaurants")
        tips.append("Use local shared autos and buses instead of taxis")
        tips.append("Visit free entry temples and ghats")

    elif budget_type == "high":
        tips.append("Book premium hotels for the best experience")
        tips.append("Hire a private car with driver for ₹2000-3000/day")
        tips.append("Try fine dining at hotel restaurants")

    if origin_city:
        tips.append("Book train tickets 2-3 weeks in advance for best fares")
        tips.append("Consider overnight trains to save on one night's accommodation")

    tips.append("Carry cash — many places in Braj don't accept UPI/cards")
    tips.append("Best season to visit: Oct-Mar (pleasant weather)")

    return tips
