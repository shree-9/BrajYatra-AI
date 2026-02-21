"""
Distance matrix utilities using the Haversine formula.
Used as the free fallback when Google Maps API is unavailable.
"""

import math


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on Earth using the Haversine formula.

    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in km

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    a = (
        math.sin(dLat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dLon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def create_distance_matrix(locations):
    """
    Create a distance matrix (in km) for a list of locations.

    Each location must have location.coordinates.lat and location.coordinates.lng.
    """

    matrix = []
    for loc1 in locations:
        row = []
        coords1 = loc1.get("location", {}).get("coordinates", {})

        for loc2 in locations:
            coords2 = loc2.get("location", {}).get("coordinates", {})

            row.append(haversine(
                coords1.get("lat", 0), coords1.get("lng", 0),
                coords2.get("lat", 0), coords2.get("lng", 0)
            ))

        matrix.append(row)

    return matrix


def estimate_travel_time(loc1, loc2, avg_speed_kmh=30):
    """
    Estimate travel time between two locations in minutes.
    Default speed: 30 km/h (urban roads in Indian cities).
    """

    coords1 = loc1.get("location", {}).get("coordinates", {})
    coords2 = loc2.get("location", {}).get("coordinates", {})

    dist = haversine(
        coords1.get("lat", 0), coords1.get("lng", 0),
        coords2.get("lat", 0), coords2.get("lng", 0)
    )

    return round((dist / avg_speed_kmh) * 60, 1)
