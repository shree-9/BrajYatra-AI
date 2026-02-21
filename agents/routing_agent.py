"""
Routing Agent — optimizes travel routes between locations.
Uses Google Distance Matrix API when available, falls back to Haversine.
Uses OR-Tools for TSP (Traveling Salesman Problem) solving.
"""

import requests
from config import GOOGLE_API_KEY, USE_GOOGLE_MAPS
from utils.distance_matrix import haversine


def get_distance_matrix(locations, use_google=None):
    """
    Build a distance matrix for a list of locations.
    Uses Google Maps API if enabled, otherwise Haversine formula.
    """

    if use_google is None:
        use_google = USE_GOOGLE_MAPS

    if use_google:
        return _google_distance_matrix(locations)
    return _haversine_distance_matrix(locations)


def _haversine_distance_matrix(locations):
    """Build distance matrix using Haversine formula (free, offline)."""

    matrix = []
    for loc1 in locations:
        row = []
        coords1 = loc1.get("location", {}).get("coordinates", {})
        lat1 = coords1.get("lat", 0)
        lng1 = coords1.get("lng", 0)

        for loc2 in locations:
            coords2 = loc2.get("location", {}).get("coordinates", {})
            lat2 = coords2.get("lat", 0)
            lng2 = coords2.get("lng", 0)

            # Convert km to estimated travel time in seconds (avg 30 km/h in cities)
            dist_km = haversine(lat1, lng1, lat2, lng2)
            travel_time_sec = int((dist_km / 30) * 3600)
            row.append(travel_time_sec)

        matrix.append(row)

    return matrix


def _google_distance_matrix(locations):
    """Build distance matrix using Google Distance Matrix API."""

    try:
        origins = "|".join([
            f"{loc['location']['coordinates']['lat']},{loc['location']['coordinates']['lng']}"
            for loc in locations
        ])

        url = (
            f"https://maps.googleapis.com/maps/api/distancematrix/json"
            f"?origins={origins}&destinations={origins}"
            f"&departure_time=now"
            f"&key={GOOGLE_API_KEY}"
        )

        response = requests.get(url, timeout=15).json()

        if response.get("status") != "OK":
            print(f"[RoutingAgent] Google API error: {response.get('status')}")
            return _haversine_distance_matrix(locations)

        matrix = []
        for row in response["rows"]:
            matrix.append([
                elem["duration"]["value"]
                for elem in row["elements"]
                if elem.get("status") == "OK"
            ])

        return matrix

    except Exception as e:
        print(f"[RoutingAgent] Google API failed, using Haversine: {e}")
        return _haversine_distance_matrix(locations)


def optimize_route(locations):
    """
    Find the optimal visit order for a list of locations using TSP.
    Returns reordered list of locations.
    """

    if len(locations) <= 2:
        return locations

    try:
        from ortools.constraint_solver import pywrapcp, routing_enums_pb2

        distance_matrix = _haversine_distance_matrix(locations)

        manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            return distance_matrix[
                manager.IndexToNode(from_index)
            ][
                manager.IndexToNode(to_index)
            ]

        transit_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_index)

        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solution = routing.SolveWithParameters(search_params)

        if solution:
            route = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                route.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))

            return [locations[i] for i in route]

    except ImportError:
        print("[RoutingAgent] OR-Tools not installed, skipping route optimization.")
    except Exception as e:
        print(f"[RoutingAgent] Route optimization failed: {e}")

    return locations
