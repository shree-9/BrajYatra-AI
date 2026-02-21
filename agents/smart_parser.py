"""
BrajYatra AI — Smart Intent Parser (No LLM Required)

Parses travel queries using keyword matching and regex patterns.
This allows the agent to work locally without a GPU.
"""

import re


# Keyword mappings
THEME_KEYWORDS = {
    "Spiritual": [
        "temple", "mandir", "spiritual", "religious", "prayer", "darshan",
        "pooja", "puja", "aarti", "ashram", "devotion", "pilgrimage",
        "holy", "sacred", "divine", "bhajan", "kirtan"
    ],
    "Heritage": [
        "heritage", "historical", "history", "monument", "fort", "palace",
        "mughal", "ancient", "architecture", "ruins", "old", "museum"
    ],
    "Exploration": [
        "explore", "adventure", "sightseeing", "tourist", "visit",
        "travel", "trip", "tour", "see", "discover", "wander"
    ],
    "Nature": [
        "nature", "garden", "park", "lake", "river", "green",
        "bird", "wildlife", "forest", "yamuna", "outdoor"
    ],
    "Shopping": [
        "shopping", "market", "bazaar", "buy", "shop", "souvenir",
        "handicraft", "local market"
    ],
    "Food": [
        "food", "eat", "restaurant", "cuisine", "taste", "street food",
        "peda", "sweets", "dining", "kulfi"
    ]
}

CITY_KEYWORDS = {
    "Mathura": ["mathura", "mathura city"],
    "Vrindavan": ["vrindavan", "vrindavan city", "vrindaban"],
    "Agra": ["agra", "agra city", "taj mahal", "taj"],
    "Gokul": ["gokul"],
    "Barsana": ["barsana", "barsane"],
    "Govardhan": ["govardhan", "govardhan hill", "gowardhan"]
}

BUDGET_KEYWORDS = {
    "low": ["cheap", "budget", "low budget", "affordable", "economical", "low cost", "save money"],
    "high": ["luxury", "premium", "expensive", "high end", "lavish", "royal", "vip"],
}

GROUP_KEYWORDS = {
    "solo": ["solo", "alone", "myself", "by myself", "single"],
    "couple": ["couple", "partner", "romantic", "honeymoon", "girlfriend", "boyfriend", "wife", "husband"],
    "family": ["family", "kids", "children", "parents", "mother", "father", "baby"],
    "friends": ["friends", "group", "gang", "buddies", "mates", "squad"],
    "elderly": ["elderly", "senior", "old age", "grandparents", "grandfather", "grandmother"]
}


def parse_intent_local(query):
    """
    Parse travel intent from natural language without using an LLM.
    Uses keyword matching and regex patterns.
    """

    query_lower = query.lower().strip()

    # Extract days
    days = 2  # default
    day_match = re.search(r'(\d+)\s*(?:day|days|din|dino)', query_lower)
    if day_match:
        days = int(day_match.group(1))
        days = max(1, min(days, 15))

    # Extract themes
    themes = []
    for theme, keywords in THEME_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            themes.append(theme)

    # If no theme found, default based on context
    if not themes:
        themes = ["Spiritual", "Heritage", "Exploration"]

    # Extract cities
    cities = []
    for city, keywords in CITY_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            cities.append(city)

    # Extract budget
    budget = "moderate"
    for budget_type, keywords in BUDGET_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            budget = budget_type
            break

    # Avoid crowd
    avoid_crowd = any(w in query_lower for w in [
        "avoid crowd", "no crowd", "less crowd", "quiet", "peaceful",
        "not crowded", "less people", "empty", "calm", "secluded"
    ])

    # Indoor preference
    prefer_indoor = any(w in query_lower for w in [
        "indoor", "inside", "rain", "rainy", "hot", "heat",
        "air conditioned", "ac", "covered"
    ])

    # Group type
    group_type = "family"
    for gtype, keywords in GROUP_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            group_type = gtype
            break

    return {
        "days": days,
        "themes": themes,
        "budget": budget,
        "avoid_crowd": avoid_crowd,
        "prefer_indoor": prefer_indoor,
        "cities": cities,
        "group_type": group_type
    }


def detect_command(user_input):
    """
    Detect what the user wants to do from their message.

    Returns:
        tuple of (command, args)
        command: "plan", "customize", "weather", "budget", "feedback",
                 "locations", "help", "chat", "exit"
    """

    text = user_input.lower().strip()

    # Exit commands
    if text in ("exit", "quit", "bye", "goodbye", "q"):
        return "exit", {}

    # Help
    if text in ("help", "?", "commands", "what can you do"):
        return "help", {}

    # Weather
    if text.startswith("weather") or "weather" in text.split()[:3]:
        parts = text.replace("weather", "").strip()
        city = parts if parts else "Mathura"
        # Capitalize city name
        city = city.strip().title()
        return "weather", {"city": city}

    # Feedback
    if text.startswith("feedback") or text.startswith("rate"):
        try:
            rating = int(re.search(r'\d+', text).group())
            return "feedback", {"rating": min(5, max(1, rating))}
        except:
            return "feedback", {"rating": None}

    # Travel fare query
    travel_match = re.search(r'travel\s+(?:from\s+)?(\w+)', text)
    if travel_match and "travel" in text.split()[:2]:
        city = travel_match.group(1).strip().title()
        return "travel", {"city": city}

    # Show locations
    if any(text.startswith(w) for w in ["show", "list", "places", "locations"]):
        city = None
        for c in ["mathura", "vrindavan", "agra", "gokul", "barsana", "govardhan"]:
            if c in text:
                city = c.title()
                break
        return "locations", {"city": city}

    # Customize commands
    customize_words = ["remove", "add", "swap", "replace", "change", "move", "reorder"]
    if any(text.startswith(w) for w in customize_words):
        return "customize", {"raw": user_input}

    # Plan / itinerary request
    plan_indicators = [
        "plan", "itinerary", "trip", "travel", "visit", "tour",
        "suggest", "recommend", "i want to go", "take me",
        "show me", "create", "make", "generate", "build",
        "day", "days", "schedule"
    ]
    if any(w in text for w in plan_indicators):
        return "plan", {"query": user_input}

    # Default: treat as a plan query if it mentions cities/themes
    all_keywords = []
    for keywords in CITY_KEYWORDS.values():
        all_keywords.extend(keywords)
    for keywords in THEME_KEYWORDS.values():
        all_keywords.extend(keywords)

    if any(kw in text for kw in all_keywords):
        return "plan", {"query": user_input}

    # Fallback: chat
    return "chat", {"message": user_input}
