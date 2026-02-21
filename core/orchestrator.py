"""
Orchestrator — the central multi-agent pipeline that coordinates
all agents to generate, customize, and manage trip itineraries.
"""

import json
from config import LOCATIONS_PATH
from agents.constraint_agent import parse_intent
from agents.semantic_agent import SemanticAgent
from agents.scoring_agent import score_location
from agents.weather_agent import apply_weather_filter, fetch_weather
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
    5. Enforce diversity across categories
    6. Optimize route within each day (RoutingAgent)
    7. Schedule time slots (SchedulerAgent)
    8. Distribute across days (PlannerAgent)
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
            dict with keys: intent, itinerary, weather, locations_used
        """

        # Step 1: Parse intent from user query
        intent = parse_intent(query)
        print(f"[Orchestrator] Intent: {json.dumps(intent, indent=2)}")

        # Step 2: Semantic search for relevant locations
        candidates = self.semantic.search(query, k=25)

        # Step 3: Apply filters
        # 3a: City filter
        if intent.get("cities"):
            filtered = filter_by_city(candidates, intent["cities"])
            if filtered:
                candidates = filtered

        # 3b: Theme filter
        if intent.get("themes"):
            filtered = filter_by_theme(candidates, intent["themes"])
            if filtered:
                candidates = filtered

        # 3c: Accessibility filter
        filtered = filter_accessible(candidates, intent.get("group_type", "family"))
        if filtered:
            candidates = filtered

        # 3d: Weather filter
        weather = fetch_weather(weather_city)
        candidates = apply_weather_filter(candidates, intent, weather)

        # Step 4: Score and rank
        weights = load_weights()
        ranked = sorted(
            candidates,
            key=lambda x: score_location(x, intent, weights),
            reverse=True
        )

        # Step 5: Enforce diversity
        diverse = enforce_diversity(ranked, max_per_category=2)

        # Step 6: Determine how many locations we need
        days = intent.get("days", 2)
        max_per_day = 5
        total_needed = min(len(diverse), days * max_per_day)
        selected = diverse[:total_needed]

        # Step 7: Optimize route within city groups
        optimized = optimize_route(selected)

        # Step 8: Distribute across days and schedule
        itinerary = distribute_across_days(optimized, days)

        return {
            "intent": intent,
            "itinerary": itinerary,
            "weather": weather,
            "locations_used": [
                {"id": loc["id"], "name": loc["name"], "city": loc.get("location", {}).get("city", "")}
                for loc in selected
            ]
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

                # Replace the old location
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

                # Find and move the location
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
