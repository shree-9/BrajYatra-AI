"""
BrajYatra AI — Interactive Conversational Agent

A rich, chat-like terminal experience for trip planning.
Features:
  - Conversational onboarding (asks origin, budget, interests)
  - Full trip planning with food/restaurant inclusion
  - Travel fare estimation from origin city
  - Complete budget breakdown (travel + food + accommodation + sightseeing)
  - Itinerary customization (add/remove places)
  - Weather checking
  - Feedback/rating system

Works WITHOUT a GPU using smart rule-based parsing.
"""

import json
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(__file__))

from config import LOCATIONS_PATH, BRAJ_CITIES
from agents.smart_parser import parse_intent_local, detect_command
from agents.semantic_agent import SemanticAgent
from agents.scoring_agent import score_location
from agents.weather_agent import apply_weather_filter, fetch_weather
from agents.diversity_agent import enforce_diversity
from agents.planner_agent import distribute_across_days
from agents.routing_agent import optimize_route
from agents.budget_agent import estimate_budget, estimate_full_trip_budget
from agents.travel_estimator import get_travel_estimate
from agents.rl_agent import load_weights, update_weights
from core.memory_store import create_session, add_feedback, get_session, update_session


# ─── Terminal Colors ───
class C:
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    RESET = "\033[0m"


def ask(prompt, default=None):
    """Ask user a question with a default value."""
    suffix = f" [{default}]" if default else ""
    try:
        ans = input(f"  {C.GREEN}{C.BOLD}You ▸ {C.RESET}{prompt}{C.DIM}{suffix}{C.RESET}: ").strip()
    except (KeyboardInterrupt, EOFError):
        return default
    return ans if ans else default


def banner():
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🙏  BRAJYATRA AI  🙏                                 ║
║     Your Intelligent Braj Region Travel Companion        ║
║                                                          ║
║   Mathura • Vrindavan • Agra • Gokul • Barsana • Govardhan║
╚══════════════════════════════════════════════════════════╝{C.RESET}
""")


def show_help():
    print(f"""
{C.CYAN}{C.BOLD}What I can do:{C.RESET}

  {C.GREEN}🗺  Plan a trip{C.RESET}     → Just type what you want!
  {C.GREEN}✏️  Customize{C.RESET}       → "remove X from Day 1" / "add #5 to Day 2"
  {C.GREEN}🌤  Weather{C.RESET}         → "weather Mathura"
  {C.GREEN}📍 Locations{C.RESET}        → "show places" / "show food in Mathura"
  {C.GREEN}💰 Travel cost{C.RESET}      → "travel from Delhi"
  {C.GREEN}⭐ Feedback{C.RESET}         → "feedback 5"
  {C.GREEN}❌ Exit{C.RESET}             → "exit"
""")


# ─── Display Functions ───

def print_itinerary(itinerary):
    print(f"\n{C.CYAN}{C.BOLD}{'═' * 58}")
    print(f"  🗓  YOUR BRAJ YATRA ITINERARY")
    print(f"{'═' * 58}{C.RESET}\n")

    for day, activities in itinerary.items():
        print(f"  {C.YELLOW}{C.BOLD}📅 {day}{C.RESET}")
        print(f"  {C.DIM}{'─' * 53}{C.RESET}")

        if not activities:
            print(f"    {C.DIM}No activities scheduled{C.RESET}")
        else:
            for i, act in enumerate(activities):
                city = act.get("city", "")
                category = act.get("category", "")
                place_id = act.get("place_id", "")
                connector = "├──" if i < len(activities) - 1 else "└──"

                city_tag = f" {C.DIM}[{city}]{C.RESET}" if city else ""
                cat_tag = f" {C.MAGENTA}({category}){C.RESET}" if category else ""
                id_tag = f" {C.DIM}#{place_id}{C.RESET}" if place_id else ""

                # Emoji per category
                emoji = "📍"
                if "Food" in category or "Restaurant" in category:
                    emoji = "🍽"
                elif "Hotel" in category:
                    emoji = "🏨"
                elif "Market" in category:
                    emoji = "🛍"
                elif "Temple" in category or "Spiritual" in category:
                    emoji = "🛕"
                elif "Heritage" in category or "Fort" in category:
                    emoji = "🏰"
                elif "Garden" in category or "Park" in category:
                    emoji = "🌳"

                print(
                    f"    {C.DIM}{connector}{C.RESET} "
                    f"{C.GREEN}{act['start']} - {act['end']}{C.RESET}  "
                    f"{emoji} {C.BOLD}{act['place']}{C.RESET}"
                    f"{cat_tag}{city_tag}{id_tag}"
                )

                duration = act.get("duration_minutes")
                if duration:
                    print(f"    {C.DIM}│   ⏱ {duration} min{C.RESET}")

        print()


def print_weather(weather):
    if not weather:
        print(f"  {C.RED}❌ Weather data unavailable (no API key?){C.RESET}\n")
        return

    condition = weather.get("condition", "").lower()
    emoji = "☀️"
    if "rain" in condition: emoji = "🌧️"
    elif "cloud" in condition: emoji = "☁️"
    elif "thunder" in condition: emoji = "⛈️"
    elif "mist" in condition or "fog" in condition: emoji = "🌫️"

    print(f"""
  {C.CYAN}{C.BOLD}🌤 Weather in {weather['city']}{C.RESET}
  {C.DIM}{'─' * 35}{C.RESET}
    {emoji}  {C.BOLD}{weather['description'].capitalize()}{C.RESET}
    🌡️  {C.YELLOW}{weather['temperature']}°C{C.RESET} (feels like {weather['feels_like']}°C)
    💧  Humidity: {weather['humidity']}%  |  💨 Wind: {weather['wind_speed']} m/s
""")


def print_travel_info(travel):
    if not travel:
        return

    if travel.get("source") == "unknown":
        print(f"\n  {C.YELLOW}⚠️ {travel.get('message', 'Unknown city')}{C.RESET}\n")
        return

    print(f"\n  {C.CYAN}{C.BOLD}🚆 Travel: {travel['origin']} → {travel['destination']}{C.RESET}")
    print(f"  {C.DIM}{'─' * 50}{C.RESET}")
    print(f"    📏 Distance: ~{travel['distance_km']} km")

    for mode, emoji in [("train", "🚂"), ("bus", "🚌"), ("car", "🚗"), ("flight", "✈️")]:
        info = travel.get(mode)
        if info:
            print(
                f"    {emoji}  {mode.title():8s}  "
                f"₹{info['fare_low']:,} - ₹{info['fare_high']:,}  "
                f"({info['duration_hours']}h)  "
                f"{C.DIM}{info['options']}{C.RESET}"
            )

    if travel.get("recommended"):
        print(f"\n    {C.GREEN}💡 Recommended: {travel['recommended']}{C.RESET}")
    print()


def print_full_budget(budget_data):
    s = budget_data["summary"]
    b = budget_data["breakdown"]

    print(f"\n  {C.CYAN}{C.BOLD}💰 FULL TRIP BUDGET ({s['budget_type'].upper()}){C.RESET}")
    print(f"  {C.DIM}{'═' * 52}{C.RESET}")

    if s.get("origin_city"):
        print(f"    📍 From: {s['origin_city']}")
    print(f"    📅 Duration: {s['days']} days / {s['nights']} nights")
    print(f"    👥 Persons: {s['persons']}")
    print()

    # Travel
    if b.get("travel"):
        t = b["travel"]
        print(f"    {C.YELLOW}🚆 Travel (round-trip){C.RESET}")
        print(f"       ₹{t['cost_min']:,} - ₹{t['cost_max']:,}")

    # Accommodation
    a = b["accommodation"]
    print(f"    {C.YELLOW}🏨 Accommodation ({a['nights']} nights × {a['type']}){C.RESET}")
    print(f"       ₹{a['cost_min']:,} - ₹{a['cost_max']:,}")

    # Food
    f = b["food"]
    print(f"    {C.YELLOW}🍽 Food ({f['days']} days × ₹{f['per_day']}/day){C.RESET}")
    print(f"       ₹{f['cost_total']:,}")

    # Sightseeing
    si = b["sightseeing"]
    print(f"    {C.YELLOW}🎫 Sightseeing ({si['places_count']} places){C.RESET}")
    print(f"       ₹{si['cost_total']:,}")

    # Grand total
    print(f"\n  {C.DIM}{'─' * 52}{C.RESET}")
    print(f"    {C.GREEN}{C.BOLD}💵 ESTIMATED TOTAL: ₹{s['grand_total_min']:,} - ₹{s['grand_total_max']:,}{C.RESET}")
    print(f"  {C.DIM}{'─' * 52}{C.RESET}")

    # Tips
    if budget_data.get("tips"):
        print(f"\n    {C.CYAN}💡 Tips:{C.RESET}")
        for tip in budget_data["tips"][:4]:
            print(f"       • {C.DIM}{tip}{C.RESET}")
    print()


def print_locations(locations, title=None):
    title = title or f"Available Places ({len(locations)})"
    print(f"\n  {C.CYAN}{C.BOLD}📍 {title}{C.RESET}")
    print(f"  {C.DIM}{'─' * 55}{C.RESET}")

    for loc in locations:
        rating = loc.get("ratings", {}).get("overall_rating", 0)
        city = loc.get("location", {}).get("city", "")
        cat = loc.get("category", "")

        emoji = "📍"
        if cat in ("Food Stall", "Restaurant"): emoji = "🍽"
        elif cat == "Hotel": emoji = "🏨"
        elif cat == "Market": emoji = "🛍"
        elif "Temple" in cat: emoji = "🛕"

        print(
            f"    {C.DIM}#{loc['id']:2d}{C.RESET}  "
            f"{emoji} {C.BOLD}{loc['name']}{C.RESET}  "
            f"{C.MAGENTA}({cat}){C.RESET}  "
            f"{C.DIM}[{city}]{C.RESET}  "
            f"{C.YELLOW}★{rating}{C.RESET}"
        )
    print()


# ─── The Agent ───

class BrajYatraAgent:

    def __init__(self):
        print(f"\n  {C.DIM}Loading location data...{C.RESET}")
        with open(LOCATIONS_PATH, "r", encoding="utf-8") as f:
            self.locations = json.load(f)

        self.location_map = {loc["id"]: loc for loc in self.locations}

        print(f"  {C.DIM}Building semantic search index...{C.RESET}")
        self.semantic = SemanticAgent(self.locations)

        # Session state
        self.current_session_id = None
        self.current_itinerary = None
        self.current_intent = None
        self.origin_city = None
        self.persons = 1

        print(f"  {C.GREEN}✅ Ready! ({len(self.locations)} locations loaded){C.RESET}")

    # ─── Conversational Onboarding ───
    def onboarding(self):
        """Ask the user step-by-step questions before planning."""

        print(f"\n  {C.CYAN}{C.BOLD}Let's plan your Braj Yatra! 🙏{C.RESET}")
        print(f"  {C.DIM}I'll ask a few questions to personalize your trip.{C.RESET}\n")

        # 1. Origin city
        self.origin_city = ask(
            "Where are you coming from? (city name)", "Delhi"
        )

        # Show travel info immediately
        if self.origin_city:
            travel = get_travel_estimate(self.origin_city)
            print_travel_info(travel)

        # 2. Number of days
        days_str = ask("How many days is your trip?", "3")
        try:
            days = max(1, min(int(days_str), 15))
        except ValueError:
            days = 3

        # 3. Budget
        budget = ask(
            "Budget preference? (low / moderate / high)", "moderate"
        ).lower()
        if budget not in ("low", "moderate", "high"):
            budget = "moderate"

        # 4. Persons
        persons_str = ask("How many persons?", "2")
        try:
            self.persons = max(1, int(persons_str))
        except ValueError:
            self.persons = 2

        # 5. Interests
        print(f"\n  {C.DIM}Interests (pick any): spiritual, heritage, food,")
        print(f"  nature, shopping, exploration, or 'all'{C.RESET}")
        interests_str = ask("What interests you?", "all")

        themes = []
        if "all" in interests_str.lower():
            themes = ["Spiritual", "Heritage", "Food", "Exploration", "Nature", "Shopping"]
        else:
            theme_map = {
                "spiritual": "Spiritual", "temple": "Spiritual",
                "heritage": "Heritage", "history": "Heritage",
                "food": "Food", "eat": "Food", "restaurant": "Food",
                "nature": "Nature", "garden": "Nature",
                "shop": "Shopping", "market": "Shopping",
                "explore": "Exploration", "tour": "Exploration"
            }
            for word in interests_str.lower().split():
                for key, val in theme_map.items():
                    if key in word and val not in themes:
                        themes.append(val)

        if not themes:
            themes = ["Spiritual", "Heritage", "Exploration"]

        # 6. Specific cities?
        print(f"\n  {C.DIM}Braj cities: Mathura, Vrindavan, Agra, Gokul, Barsana, Govardhan")
        print(f"  Type specific cities or 'all' for everything{C.RESET}")
        cities_str = ask("Which cities to visit?", "all")

        cities = []
        if "all" not in cities_str.lower():
            for city in BRAJ_CITIES:
                if city.lower() in cities_str.lower():
                    cities.append(city)

        # 7. Group type?
        group_type = ask(
            "Group type? (solo / couple / family / friends / elderly)", "family"
        ).lower()
        if group_type not in ("solo", "couple", "family", "friends", "elderly"):
            group_type = "family"

        # Build intent
        intent = {
            "days": days,
            "themes": themes,
            "budget": budget,
            "cities": cities,
            "group_type": group_type,
            "avoid_crowd": False,
            "prefer_indoor": False
        }

        print(f"\n  {C.CYAN}🤖 Got it! Planning your {days}-day trip...{C.RESET}")
        print(f"  {C.DIM}Themes: {', '.join(themes)} | Budget: {budget} | Group: {group_type}{C.RESET}\n")

        self._execute_plan(intent, include_food=("Food" in themes or True))

    # ─── Core Planning ───
    def _execute_plan(self, intent, include_food=True):
        """Execute the planning pipeline with the given intent."""

        query_parts = []
        if intent.get("cities"):
            query_parts.append(" ".join(intent["cities"]))
        query_parts.append(" ".join(intent.get("themes", [])))
        query_parts.append(f"{intent.get('days', 3)} day trip")
        query = " ".join(query_parts)

        # Semantic search
        print(f"  {C.CYAN}🔍 Finding best places...{C.RESET}")
        candidates = self.semantic.search(query, k=40)

        # City filter
        if intent.get("cities"):
            filtered = [
                loc for loc in candidates
                if loc.get("location", {}).get("city", "") in intent["cities"]
            ]
            if filtered:
                candidates = filtered

        # Theme filter
        if intent.get("themes"):
            themed = []
            for loc in candidates:
                rec = loc.get("visitor_profile_fit", {}).get("recommended_for", [])
                if any(t in rec for t in intent["themes"]):
                    themed.append(loc)
            if themed:
                candidates = themed

        # Weather
        weather_city = intent.get("cities", ["Mathura"])[0] if intent.get("cities") else "Mathura"
        print(f"  {C.CYAN}🌤 Checking weather in {weather_city}...{C.RESET}")
        weather = fetch_weather(weather_city)
        candidates = apply_weather_filter(candidates, intent, weather)

        # Score and rank
        weights = load_weights()
        ranked = sorted(
            candidates,
            key=lambda x: score_location(x, intent, weights),
            reverse=True
        )

        # Separate sightseeing and food/restaurants
        sightseeing = [l for l in ranked if l.get("category") not in ("Food Stall", "Restaurant", "Hotel", "Market")]
        food_places = [l for l in ranked if l.get("category") in ("Food Stall", "Restaurant")]
        markets = [l for l in ranked if l.get("category") == "Market"]

        # Diversity for sightseeing
        diverse_sightseeing = enforce_diversity(sightseeing, max_per_category=3)

        # Select places per day
        days = intent.get("days", 3)
        sightseeing_per_day = 3
        food_per_day = 2  # one restaurant + one food stall per day

        total_sightseeing = min(len(diverse_sightseeing), days * sightseeing_per_day)
        total_food = min(len(food_places), days * food_per_day)

        selected_sightseeing = diverse_sightseeing[:total_sightseeing]
        selected_food = food_places[:total_food]

        # Add 1 market per 2 days
        market_count = min(len(markets), max(1, days // 2))
        selected_markets = markets[:market_count]

        # Combine
        all_selected = selected_sightseeing + selected_food + selected_markets

        # Optimize route
        print(f"  {C.CYAN}🛣️  Optimizing route...{C.RESET}")
        optimized = optimize_route(all_selected)

        # Schedule
        itinerary = distribute_across_days(optimized, days)

        # Store state
        self.current_itinerary = itinerary
        self.current_intent = intent

        result = {
            "intent": intent,
            "itinerary": itinerary,
            "weather": weather,
            "locations_used": [{"id": loc["id"], "name": loc["name"]} for loc in all_selected],
            "origin_city": self.origin_city,
            "persons": self.persons
        }

        self.current_session_id = create_session(result)

        # Display itinerary
        print_itinerary(itinerary)

        # Weather
        if weather:
            print_weather(weather)

        # Full budget
        print(f"  {C.CYAN}💰 Calculating budget...{C.RESET}")
        full_budget = estimate_full_trip_budget(
            all_selected,
            budget_type=intent.get("budget", "moderate"),
            days=days,
            origin_city=self.origin_city,
            persons=self.persons
        )
        print_full_budget(full_budget)

        # Explanation
        explanation = self._generate_explanation(intent, itinerary, all_selected)
        print(f"  {C.CYAN}{C.BOLD}🧠 About this plan:{C.RESET}")
        for line in textwrap.wrap(explanation, width=60):
            print(f"    {line}")
        print()

        print(f"  {C.DIM}💡 You can now customize: 'remove X from Day 1', 'add #5 to Day 2'{C.RESET}")
        print(f"  {C.DIM}   Or type a new query to replan!{C.RESET}\n")

    def _generate_explanation(self, intent, itinerary, locations):
        days = len(itinerary)
        total = sum(len(acts) for acts in itinerary.values())
        food_count = sum(1 for l in locations if l.get("category") in ("Food Stall", "Restaurant"))
        sight_count = total - food_count

        cities_used = set()
        for day_acts in itinerary.values():
            for act in day_acts:
                c = act.get("city", "")
                if c:
                    cities_used.add(c)

        cities_str = ", ".join(cities_used) if cities_used else "Braj region"
        themes_str = ", ".join(intent.get("themes", []))

        parts = [f"Your {days}-day itinerary covers {total} places across {cities_str}."]

        if food_count:
            parts.append(f"Includes {food_count} food stops (restaurants & famous stalls).")

        if themes_str:
            parts.append(f"Focused on: {themes_str}.")

        if self.origin_city:
            parts.append(f"Travel from {self.origin_city} factored into budget.")

        if intent.get("group_type") == "family":
            parts.append("All places are family-friendly.")
        elif intent.get("group_type") == "elderly":
            parts.append("All places are senior-friendly with easy access.")

        return " ".join(parts)

    # ─── Freeform Planning (from typed query) ───
    def plan_trip(self, query):
        """Plan trip from a freeform query (no onboarding)."""

        print(f"\n  {C.CYAN}🤔 Understanding your request...{C.RESET}")
        intent = parse_intent_local(query)

        print(f"  {C.DIM}📋 {intent['days']} days, themes: {', '.join(intent['themes'])}, "
              f"budget: {intent['budget']}, group: {intent['group_type']}{C.RESET}")

        self._execute_plan(intent)

    # ─── Customize ───
    def handle_customize(self, raw_input):
        if not self.current_itinerary:
            print(f"\n  {C.YELLOW}⚠️  No active itinerary. Plan a trip first!{C.RESET}\n")
            return

        text = raw_input.lower().strip()

        # Remove
        remove_match = re.search(r'remove\s+(.+?)\s+from\s+(day\s*\d+)', text, re.IGNORECASE)
        if remove_match:
            place_name = remove_match.group(1).strip().title()
            day_key = remove_match.group(2).strip().title()

            if day_key in self.current_itinerary:
                before = len(self.current_itinerary[day_key])
                self.current_itinerary[day_key] = [
                    act for act in self.current_itinerary[day_key]
                    if act["place"].lower() != place_name.lower()
                ]
                if len(self.current_itinerary[day_key]) < before:
                    print(f"\n  {C.GREEN}✅ Removed '{place_name}' from {day_key}{C.RESET}")
                    print_itinerary(self.current_itinerary)
                    self._save_itinerary()
                else:
                    print(f"\n  {C.RED}❌ '{place_name}' not found in {day_key}{C.RESET}")
                    self._suggest_places(day_key)
            else:
                print(f"\n  {C.RED}❌ {day_key} doesn't exist{C.RESET}")
            return

        # Add
        add_match = re.search(r'add\s+(?:#?\s*)?(\d+)\s+to\s+(day\s*\d+)', text, re.IGNORECASE)
        if add_match:
            place_id = int(add_match.group(1))
            day_key = add_match.group(2).strip().title()

            if place_id in self.location_map and day_key in self.current_itinerary:
                loc = self.location_map[place_id]
                from agents.scheduler_agent import schedule_day

                day_locs = []
                for act in self.current_itinerary[day_key]:
                    pid = act.get("place_id")
                    if pid and pid in self.location_map:
                        day_locs.append(self.location_map[pid])

                day_locs.append(loc)
                self.current_itinerary[day_key] = schedule_day(day_locs)

                print(f"\n  {C.GREEN}✅ Added '{loc['name']}' to {day_key}{C.RESET}")
                print_itinerary(self.current_itinerary)
                self._save_itinerary()
            else:
                if place_id not in self.location_map:
                    print(f"\n  {C.RED}❌ Place #{place_id} not found.{C.RESET}")
                    print(f"  {C.DIM}Use 'show places' to see IDs.{C.RESET}")
                else:
                    print(f"\n  {C.RED}❌ {day_key} doesn't exist{C.RESET}")
            return

        print(f"""
  {C.YELLOW}💡 Customize commands:{C.RESET}
    "remove <place name> from Day 1"
    "add #5 to Day 2"  (use place ID)

  {C.DIM}Use 'show places' to see all IDs.{C.RESET}
""")

    def _suggest_places(self, day_key):
        """Show places in a day to help with correct name."""
        if day_key in self.current_itinerary:
            acts = self.current_itinerary[day_key]
            if acts:
                print(f"  {C.DIM}Places in {day_key}:{C.RESET}")
                for act in acts:
                    print(f"    • {act['place']}")
            print()

    def _save_itinerary(self):
        if self.current_session_id:
            session = get_session(self.current_session_id)
            if session:
                session["data"]["itinerary"] = self.current_itinerary
                update_session(self.current_session_id, session["data"])

    # ─── Show Locations ───
    def show_locations(self, city=None, category=None):
        filtered = self.locations

        if city:
            filtered = [
                l for l in filtered
                if l.get("location", {}).get("city", "").lower() == city.lower()
            ]

        if category:
            filtered = [
                l for l in filtered
                if category.lower() in l.get("category", "").lower()
            ]

        # Auto-detect category from input
        if not category and city:
            title = f"Places in {city}"
        elif category:
            title = f"{category.title()} places" + (f" in {city}" if city else "")
        else:
            title = None

        print_locations(filtered, title)

    # ─── Weather ───
    def check_weather(self, city):
        weather = fetch_weather(city)
        print_weather(weather)

    # ─── Travel Info ───
    def show_travel_info(self, city):
        travel = get_travel_estimate(city)
        print_travel_info(travel)

    # ─── Feedback ───
    def handle_feedback(self, rating):
        if rating is None:
            print(f"\n  {C.YELLOW}Usage: feedback <1-5>{C.RESET}\n")
            return

        update_weights(rating)
        if self.current_session_id:
            add_feedback(self.current_session_id, rating)

        emoji = ["😞", "😕", "😐", "😊", "🤩"][rating - 1]
        print(f"\n  {C.GREEN}✅ Thank you! Rated {rating}/5 {emoji}{C.RESET}")
        print(f"  {C.DIM}Your feedback improves future trip plans!{C.RESET}\n")

    # ─── Chat ───
    def handle_chat(self, message):
        responses = {
            "hi": "Hello! 🙏 I'm BrajYatra AI. Type 'plan' to start planning or just describe your dream trip!",
            "hello": "Namaste! 🙏 Ready to explore Braj? Type 'plan' or describe your trip!",
            "thank": "You're welcome! 😊 Jai Shri Krishna! 🙏",
            "thanks": "Happy to help! 🙏 Let me know if you need anything else.",
            "namaste": "Namaste! 🙏 Type 'plan' to start your Braj Yatra journey!",
            "who are you": "I'm BrajYatra AI — your intelligent travel companion for the sacred Braj region. I plan trips, estimate budgets, check weather, and more!",
            "what is braj": "Braj (Braj Bhoomi) is the sacred region in UP associated with Lord Krishna. It includes Mathura (birthplace), Vrindavan, Gokul, Barsana, Govardhan, and parts of Agra.",
        }

        text = message.lower().strip()
        for key, response in responses.items():
            if key in text:
                print(f"\n  {C.CYAN}🤖 {response}{C.RESET}\n")
                return

        print(f"\n  {C.CYAN}🤖 I'm best at planning trips! Try:{C.RESET}")
        print(f"     {C.WHITE}'plan' — start guided planning{C.RESET}")
        print(f"     {C.WHITE}'Plan a 3-day trip to Mathura' — quick plan{C.RESET}")
        print(f"     {C.DIM}Type 'help' for all commands.{C.RESET}\n")

    # ─── Main Loop ───
    def run(self):
        banner()
        show_help()

        while True:
            try:
                user_input = input(f"  {C.GREEN}{C.BOLD}You ▸ {C.RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n  {C.CYAN}👋 Goodbye! Jai Shri Krishna! 🙏{C.RESET}\n")
                break

            if not user_input:
                continue

            # "plan" alone triggers onboarding
            if user_input.lower().strip() in ("plan", "plan trip", "start", "new trip", "plan my trip"):
                self.onboarding()
                continue

            # Detect command
            command, args = detect_command(user_input)

            if command == "exit":
                print(f"\n  {C.CYAN}👋 Goodbye! Jai Shri Krishna! 🙏{C.RESET}\n")
                break

            elif command == "help":
                show_help()

            elif command == "plan":
                self.plan_trip(args["query"])

            elif command == "customize":
                self.handle_customize(args["raw"])

            elif command == "weather":
                self.check_weather(args["city"])

            elif command == "travel":
                self.show_travel_info(args["city"])

            elif command == "locations":
                # Check if user asked for specific category
                text = user_input.lower()
                category = None
                for cat in ["food", "restaurant", "hotel", "market"]:
                    if cat in text:
                        category = cat
                        break
                self.show_locations(args.get("city"), category)

            elif command == "feedback":
                self.handle_feedback(args.get("rating"))

            elif command == "chat":
                # Check for travel query
                text = args.get("message", "").lower()
                travel_match = re.search(r'travel\s+(?:from\s+)?(\w+)', text)
                if travel_match:
                    self.show_travel_info(travel_match.group(1))
                else:
                    self.handle_chat(args["message"])

            else:
                self.handle_chat(user_input)


def main():
    agent = BrajYatraAgent()
    agent.run()


if __name__ == "__main__":
    main()
