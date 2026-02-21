"""
BrajYatra AI — Travel Fare Estimator

Estimates travel cost and options from any Indian city to the Braj region.
Uses a combination of hardcoded data for major cities and distance-based estimation.
"""

import math


# Approximate coordinates of major Indian cities
CITY_COORDINATES = {
    "Delhi": (28.6139, 77.2090),
    "New Delhi": (28.6139, 77.2090),
    "Chandigarh": (30.7333, 76.7794),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Bangalore": (12.9716, 77.5946),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Pune": (18.5204, 73.8567),
    "Varanasi": (25.3176, 82.9739),
    "Kanpur": (26.4499, 80.3319),
    "Indore": (22.7196, 75.8577),
    "Bhopal": (23.2599, 77.4126),
    "Dehradun": (30.3165, 78.0322),
    "Amritsar": (31.6340, 74.8723),
    "Noida": (28.5355, 77.3910),
    "Gurgaon": (28.4595, 77.0266),
    "Gurugram": (28.4595, 77.0266),
    "Faridabad": (28.4089, 77.3178),
    "Ghaziabad": (28.6692, 77.4538),
    "Meerut": (28.9845, 77.7064),
    "Aligarh": (27.8974, 78.0880),
    "Agra": (27.1751, 78.0421),
    "Haridwar": (29.9457, 78.1642),
    "Rishikesh": (30.0869, 78.2676),
    "Patna": (25.6093, 85.1376),
    "Ranchi": (23.3441, 85.3096),
    "Nagpur": (21.1458, 79.0882),
    "Surat": (21.1702, 72.8311),
    "Udaipur": (24.5854, 73.7125),
    "Jodhpur": (26.2389, 73.0243),
}

# Mathura as the reference point for Braj region
BRAJ_CENTER = (27.4924, 77.6737)  # Mathura


# Hardcoded fare data for major routes (more accurate than formula)
KNOWN_ROUTES = {
    "Delhi": {
        "distance_km": 180,
        "train": {"fare_low": 150, "fare_high": 600, "duration_hours": 2.5, "options": "Shatabdi, Express, Passenger"},
        "bus": {"fare_low": 200, "fare_high": 500, "duration_hours": 3.5, "options": "UPSRTC, Volvo AC, Private"},
        "car": {"fare_low": 1800, "fare_high": 3500, "duration_hours": 3.0, "options": "Ola/Uber, Private taxi"},
        "flight": None  # Too close for flights
    },
    "Chandigarh": {
        "distance_km": 380,
        "train": {"fare_low": 350, "fare_high": 1200, "duration_hours": 6.0, "options": "Express, Shatabdi (via Delhi)"},
        "bus": {"fare_low": 500, "fare_high": 1200, "duration_hours": 7.0, "options": "Volvo, HRTC, Private"},
        "car": {"fare_low": 4000, "fare_high": 7000, "duration_hours": 5.5, "options": "Private taxi, Carpool"},
        "flight": {"fare_low": 3000, "fare_high": 6000, "duration_hours": 1.5, "options": "To Delhi + train/taxi"}
    },
    "Jaipur": {
        "distance_km": 240,
        "train": {"fare_low": 200, "fare_high": 800, "duration_hours": 4.0, "options": "Express, Superfast"},
        "bus": {"fare_low": 300, "fare_high": 700, "duration_hours": 4.5, "options": "RSRTC, Private AC"},
        "car": {"fare_low": 2500, "fare_high": 4500, "duration_hours": 3.5, "options": "Ola/Uber, Private taxi"},
        "flight": None
    },
    "Lucknow": {
        "distance_km": 330,
        "train": {"fare_low": 250, "fare_high": 1000, "duration_hours": 5.0, "options": "Shatabdi, Express"},
        "bus": {"fare_low": 400, "fare_high": 900, "duration_hours": 6.0, "options": "UPSRTC, Private AC"},
        "car": {"fare_low": 3500, "fare_high": 6000, "duration_hours": 5.0, "options": "Private taxi"},
        "flight": None
    },
    "Mumbai": {
        "distance_km": 1200,
        "train": {"fare_low": 600, "fare_high": 2500, "duration_hours": 16.0, "options": "Rajdhani, AC Express, Sleeper"},
        "bus": {"fare_low": 1000, "fare_high": 2500, "duration_hours": 18.0, "options": "Volvo AC, Sleeper"},
        "car": {"fare_low": 12000, "fare_high": 20000, "duration_hours": 14.0, "options": "Private taxi (not recommended)"},
        "flight": {"fare_low": 3500, "fare_high": 8000, "duration_hours": 2.0, "options": "To Delhi/Agra + taxi"}
    },
    "Varanasi": {
        "distance_km": 600,
        "train": {"fare_low": 350, "fare_high": 1500, "duration_hours": 8.0, "options": "Express, Superfast"},
        "bus": {"fare_low": 600, "fare_high": 1200, "duration_hours": 10.0, "options": "UPSRTC, Private"},
        "car": {"fare_low": 6000, "fare_high": 10000, "duration_hours": 8.0, "options": "Private taxi"},
        "flight": None
    },
    "Kolkata": {
        "distance_km": 1300,
        "train": {"fare_low": 700, "fare_high": 2800, "duration_hours": 18.0, "options": "Rajdhani, AC Express"},
        "bus": None,
        "car": None,
        "flight": {"fare_low": 4000, "fare_high": 9000, "duration_hours": 2.5, "options": "To Delhi/Agra + taxi"}
    },
    "Bangalore": {
        "distance_km": 1800,
        "train": {"fare_low": 900, "fare_high": 3500, "duration_hours": 28.0, "options": "Rajdhani, AC Express"},
        "bus": None,
        "car": None,
        "flight": {"fare_low": 4000, "fare_high": 10000, "duration_hours": 2.5, "options": "To Delhi/Agra + taxi"}
    },
    "Noida": {
        "distance_km": 160,
        "train": {"fare_low": 120, "fare_high": 500, "duration_hours": 2.0, "options": "Express from Nizamuddin"},
        "bus": {"fare_low": 200, "fare_high": 450, "duration_hours": 3.0, "options": "UPSRTC"},
        "car": {"fare_low": 1500, "fare_high": 3000, "duration_hours": 2.5, "options": "Ola/Uber"},
        "flight": None
    },
    "Gurgaon": {
        "distance_km": 190,
        "train": {"fare_low": 150, "fare_high": 550, "duration_hours": 2.5, "options": "Express from Gurgaon"},
        "bus": {"fare_low": 250, "fare_high": 500, "duration_hours": 3.5, "options": "Private AC"},
        "car": {"fare_low": 1800, "fare_high": 3500, "duration_hours": 3.0, "options": "Ola/Uber"},
        "flight": None
    },
}


def haversine(lat1, lon1, lat2, lon2):
    """Distance between two coordinates in km."""
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def estimate_fare_by_distance(distance_km):
    """Estimate travel options based on distance when no hardcoded route exists."""

    result = {
        "distance_km": round(distance_km),
        "train": {
            "fare_low": round(distance_km * 0.6),
            "fare_high": round(distance_km * 2.5),
            "duration_hours": round(distance_km / 60, 1),
            "options": "Express, Mail/Passenger"
        },
        "bus": None,
        "car": None,
        "flight": None
    }

    if distance_km <= 600:
        result["bus"] = {
            "fare_low": round(distance_km * 1.2),
            "fare_high": round(distance_km * 2.5),
            "duration_hours": round(distance_km / 50, 1),
            "options": "State roadways, Private AC"
        }
        result["car"] = {
            "fare_low": round(distance_km * 10),
            "fare_high": round(distance_km * 16),
            "duration_hours": round(distance_km / 60, 1),
            "options": "Private taxi, Ola/Uber"
        }

    if distance_km > 500:
        result["flight"] = {
            "fare_low": 3000 + round(distance_km * 2),
            "fare_high": 6000 + round(distance_km * 4),
            "duration_hours": round(distance_km / 800 + 1.5, 1),
            "options": "To Delhi/Agra + taxi to Braj"
        }

    return result


def get_travel_estimate(origin_city):
    """
    Get fare and travel options from an origin city to the Braj region.

    Args:
        origin_city: Name of the city (e.g., "Chandigarh", "Delhi")

    Returns:
        dict with distance, transport options, and recommended option
    """

    origin = origin_city.strip().title()

    # Normalize common names
    aliases = {
        "Ncr": "Delhi", "Gurugram": "Gurgaon",
        "Bengaluru": "Bangalore", "New Delhi": "Delhi"
    }
    origin = aliases.get(origin, origin)

    # Check hardcoded routes first
    if origin in KNOWN_ROUTES:
        result = KNOWN_ROUTES[origin].copy()
        result["origin"] = origin
        result["destination"] = "Mathura (Braj Region)"
        result["source"] = "known_route"
    # Estimate by distance
    elif origin in CITY_COORDINATES:
        lat, lng = CITY_COORDINATES[origin]
        dist = haversine(lat, lng, *BRAJ_CENTER)
        result = estimate_fare_by_distance(dist)
        result["origin"] = origin
        result["destination"] = "Mathura (Braj Region)"
        result["source"] = "estimated"
    else:
        # Unknown city — return a message
        return {
            "origin": origin,
            "destination": "Mathura (Braj Region)",
            "distance_km": None,
            "message": f"I don't have data for '{origin}'. Please provide approx distance in km, or try a nearby major city.",
            "train": None, "bus": None, "car": None, "flight": None,
            "source": "unknown"
        }

    # Add recommendation
    dist = result.get("distance_km", 0) or 0
    if dist <= 250:
        result["recommended"] = "🚌 Bus or 🚗 Car (short distance, fastest)"
    elif dist <= 500:
        result["recommended"] = "🚂 Train (best value, comfortable)"
    elif dist <= 1000:
        result["recommended"] = "🚂 Train (overnight, budget) or ✈️ Flight (fast, premium)"
    else:
        result["recommended"] = "✈️ Flight (best for long distance)"

    return result


def get_daily_food_budget(budget_type="moderate"):
    """Get estimated daily food budget per person."""
    food_budgets = {
        "low": {"breakfast": 50, "lunch": 80, "dinner": 80, "snacks": 40, "total": 250},
        "moderate": {"breakfast": 100, "lunch": 200, "dinner": 200, "snacks": 100, "total": 600},
        "high": {"breakfast": 200, "lunch": 500, "dinner": 500, "snacks": 200, "total": 1400}
    }
    return food_budgets.get(budget_type, food_budgets["moderate"])


def get_accommodation_estimate(budget_type="moderate", nights=1):
    """Get accommodation cost estimate."""
    per_night = {
        "low": {"min": 300, "max": 800, "type": "Dharamshala / Budget Hotel"},
        "moderate": {"min": 1500, "max": 3500, "type": "Mid-range Hotel"},
        "high": {"min": 5000, "max": 12000, "type": "Premium / Luxury Hotel"}
    }

    rate = per_night.get(budget_type, per_night["moderate"])

    return {
        "per_night_min": rate["min"],
        "per_night_max": rate["max"],
        "nights": nights,
        "total_min": rate["min"] * nights,
        "total_max": rate["max"] * nights,
        "accommodation_type": rate["type"]
    }
