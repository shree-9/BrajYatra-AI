"""
Orchestrator — the central multi-agent pipeline that coordinates
all agents to generate, customize, and manage trip itineraries.
"""

import json
from config import LOCATIONS_PATH
from agents.constraint_agent import parse_intent
from agents.semantic_agent import SemanticAgent
from agents.scoring_agent import score_location
from agents.weather_agent import apply_weather_filter, fetch_weather, fetch_weather_multi, get_weather_alerts
from agents.diversity_agent import enforce_diversity
from agents.planner_agent import distribute_across_days
from agents.routing_agent import optimize_route
from agents.rl_agent import load_weights
from agents.budget_agent import estimate_budget
from utils.filters import filter_by_city, filter_by_theme, filter_accessible


class Orchestrator:
    """
    Multi-agent orchestrator for BrajYatra trip planning.

    Pipeline:
    1. Parse user intent (ConstraintAgent + LLM)
    2. Semantic search for relevant locations (SemanticAgent)
    3. Filter by city, theme, weather, accessibility
    4. Score and rank locations (ScoringAgent + CrowdAgent)
    5. Enforce diversity across categories AND cities
    6. Optimize route within each day (RoutingAgent)
    7. Schedule time slots with lunch breaks (SchedulerAgent)
    8. Distribute across days by city (PlannerAgent)
    9. Generate Google Maps route + weather alerts
    """

    def __init__(self, data_path=None):

        path = data_path or LOCATIONS_PATH

        with open(path, "r", encoding="utf-8") as f:
            self.locations = json.load(f)

        self.semantic = SemanticAgent(self.locations)
        self._location_map = {loc["id"]: loc for loc in self.locations}

        print(f"[Orchestrator] Loaded {len(self.locations)} locations.")

    def plan_trip(self, query, weather_city="Mathura"):
        """
        Generate a complete trip itinerary from a natural language query.

        Returns:
            dict with keys: intent, itinerary, weather, weather_alerts,
                           locations_used, budget
        """

        # Step 1: Parse intent from user query
        intent = parse_intent(query)
        print(f"[Orchestrator] Intent: {json.dumps(intent, indent=2)}")

        cities = intent.get("cities", [])

        # Step 2: Semantic search — get more candidates for better selection
        candidates = self.semantic.search(query, k=60)

        # Step 3: Apply filters

        # 3a: City filter — if user specified cities, filter but ensure we
        #     have enough from each city
        if cities:
            filtered = filter_by_city(candidates, cities)
            if filtered:
                candidates = filtered
            else:
                # If semantic search missed the cities, pull from full DB
                candidates = filter_by_city(self.locations, cities)

            # Guarantee at least 5 non-food locations per city
            min_per_city_needed = 5
            candidate_ids = {c["id"] for c in candidates}
            for city in cities:
                city_count = sum(
                    1 for c in candidates
                    if (c.get("location", {}).get("city", "") == city
                        and c.get("category", "") not in ("Restaurant", "Food Stall", "Hotel"))
                )
                if city_count < min_per_city_needed:
                    # Pull more from full DB for this city
                    for loc in self.locations:
                        if (loc["id"] not in candidate_ids
                                and loc.get("location", {}).get("city", "") == city
                                and loc.get("category", "") not in ("Restaurant", "Food Stall", "Hotel")):
                            candidates.append(loc)
                            candidate_ids.add(loc["id"])
                            city_count += 1
                            if city_count >= min_per_city_needed:
                                break

        # 3b: Theme filter — only apply if every city retains enough locations
        if intent.get("themes"):
            filtered = filter_by_theme(candidates, intent["themes"])
            # Only use theme filter if each city still has at least 4 sightseeing spots
            if cities:
                city_ok = True
                for city in cities:
                    city_sights = sum(
                        1 for c in filtered
                        if (c.get("location", {}).get("city", "") == city
                            and c.get("category", "") not in ("Restaurant", "Food Stall", "Hotel"))
                    )
                    if city_sights < 4:
                        city_ok = False
                        break
                if city_ok:
                    candidates = filtered
            elif len(filtered) >= 8:
                candidates = filtered

        # 3c: Accessibility filter
        filtered = filter_accessible(candidates, intent.get("group_type", "family"))
        if filtered:
            candidates = filtered

        # 3d: Weather — fetch for ALL cities (not just one)
        weather_cities = cities if cities else [weather_city]
        weather_data = fetch_weather_multi(weather_cities)
        weather_alerts = []

        if weather_data:
            candidates = apply_weather_filter(candidates, intent, weather_data)

            # Get alerts
            alerts, _ = get_weather_alerts(weather_cities)
            weather_alerts = alerts

        # Step 4: Score and rank
        weights = load_weights()
        ranked = sorted(
            candidates,
            key=lambda x: score_location(x, intent, weights),
            reverse=True
        )

        # Step 5: Enforce diversity — both category AND city balanced
        days = intent.get("days", 2)
        diverse = enforce_diversity(
            ranked,
            max_per_category=4,
            cities=cities,
            min_per_city=max(4, days * 2)  # At least 4 per city for full-day
        )

        # Step 6: Determine how many locations we need
        max_per_day = 7
        total_needed = min(len(diverse), days * max_per_day)
        selected = diverse[:total_needed]

        # Step 7: Optimize route within city groups
        # Group by city, optimize each group separately
        city_groups = {}
        for loc in selected:
            city = loc.get("location", {}).get("city", "Unknown")
            city_groups.setdefault(city, []).append(loc)

        optimized = []
        for city_locs in city_groups.values():
            optimized.extend(optimize_route(city_locs))

        # Step 8: Distribute across days (city-aware) and schedule
        itinerary = distribute_across_days(optimized, days, cities=cities)

        # Build weather response — single city or multi-city
        if len(weather_data) == 1:
            weather_response = list(weather_data.values())[0]
        else:
            weather_response = weather_data

        return {
            "intent": intent,
            "itinerary": itinerary,
            "weather": weather_response,
            "weather_alerts": weather_alerts,
            "locations_used": [
                {
                    "id": loc["id"],
                    "name": loc["name"],
                    "city": loc.get("location", {}).get("city", ""),
                    "entry_fee": loc.get("pricing", {}).get("entry_fee", {}),
                    "booking_url": loc.get("pricing", {}).get("booking_url")
                }
                for loc in selected
            ]
        }

    def get_weather_check(self, cities):
        """
        Quick weather check for chat messages — returns alerts if any.
        """
        if not cities:
            cities = ["Mathura", "Vrindavan"]
        alerts, weather_data = get_weather_alerts(cities)
        return {
            "weather": weather_data,
            "alerts": alerts
        }

    def customize_itinerary(self, itinerary, action, params):
        """
        Customize an existing itinerary.

        Actions:
            - "remove": Remove a place. params = {"day": "Day 1", "place": "Taj Mahal"}
            - "add": Add a place. params = {"day": "Day 1", "place_id": 5}
            - "swap": Swap a place. params = {"day": "Day 1", "old_place": "Taj Mahal", "new_place_id": 5}
            - "reorder": Move a place. params = {"day": "Day 1", "place": "Taj Mahal", "position": 0}

        Returns:
            updated itinerary dict
        """

        if action == "remove":
            day = params.get("day")
            place = params.get("place")

            if day in itinerary:
                itinerary[day] = [
                    act for act in itinerary[day]
                    if act["place"] != place
                ]

                # Re-schedule the remaining places
                if itinerary[day]:
                    day_locs = self._get_locations_for_day(itinerary[day])
                    from agents.scheduler_agent import schedule_day
                    itinerary[day] = schedule_day(day_locs)

        elif action == "add":
            day = params.get("day")
            place_id = params.get("place_id")

            if day in itinerary and place_id in self._location_map:
                loc = self._location_map[place_id]
                day_locs = self._get_locations_for_day(itinerary[day])
                day_locs.append(loc)

                from agents.scheduler_agent import schedule_day
                itinerary[day] = schedule_day(day_locs)

        elif action == "swap":
            day = params.get("day")
            old_place = params.get("old_place")
            new_place_id = params.get("new_place_id")

            if day in itinerary and new_place_id in self._location_map:
                new_loc = self._location_map[new_place_id]
                day_locs = self._get_locations_for_day(itinerary[day])

                day_locs = [
                    new_loc if loc["name"] == old_place else loc
                    for loc in day_locs
                ]

                from agents.scheduler_agent import schedule_day
                itinerary[day] = schedule_day(day_locs)

        elif action == "reorder":
            day = params.get("day")
            place = params.get("place")
            position = params.get("position", 0)

            if day in itinerary:
                day_locs = self._get_locations_for_day(itinerary[day])

                target = None
                remaining = []
                for loc in day_locs:
                    if loc["name"] == place:
                        target = loc
                    else:
                        remaining.append(loc)

                if target:
                    remaining.insert(position, target)
                    from agents.scheduler_agent import schedule_day
                    itinerary[day] = schedule_day(remaining)

        return itinerary

    def get_location_by_id(self, place_id):
        """Get a location dict by its ID."""
        return self._location_map.get(place_id)

    def get_all_locations(self, city=None, category=None):
        """Get all locations, optionally filtered by city or category."""
        result = self.locations

        if city:
            result = [
                loc for loc in result
                if loc.get("location", {}).get("city", "").lower() == city.lower()
            ]

        if category:
            result = [
                loc for loc in result
                if loc.get("category", "").lower() == category.lower()
            ]

        return result

    def _get_locations_for_day(self, day_schedule):
        """Convert a day's schedule back into full location objects."""

        locations = []
        for item in day_schedule:
            place_id = item.get("place_id")
            if place_id and place_id in self._location_map:
                locations.append(self._location_map[place_id])
            else:
                # Fallback: find by name
                for loc in self.locations:
                    if loc["name"] == item["place"]:
                        locations.append(loc)
                        break

        return locations
