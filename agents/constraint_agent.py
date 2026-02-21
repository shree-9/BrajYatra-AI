"""
Constraint Agent — uses LLM to parse user's natural language query
into a structured intent object for the planner pipeline.
"""

import json
import re
from core.llm_loader import LLM


def parse_intent(query):
    """
    Parse a natural language travel query into structured intent.

    Returns:
        dict with keys: days, themes, budget, avoid_crowd,
        prefer_indoor, cities, group_type
    """

    llm = LLM()

    prompt = f"""You are a travel query parser. Extract structured travel intent from the user's query.

Return ONLY a valid JSON object with these exact keys:
- "days": integer (number of trip days, default 2)
- "themes": list of strings from ["Spiritual", "Heritage", "Exploration", "Nature", "Adventure", "Shopping", "Food"]
- "budget": string, one of "low", "moderate", "high" (default "moderate")
- "avoid_crowd": boolean (default false)
- "prefer_indoor": boolean (default false)
- "cities": list of strings from ["Mathura", "Vrindavan", "Agra", "Gokul", "Barsana", "Govardhan"] (default all)
- "group_type": string, one of "solo", "couple", "family", "friends", "elderly" (default "family")

User Query: "{query}"

Respond with ONLY the JSON, no explanation:"""

    response = llm.generate(prompt, max_tokens=200)

    try:
        # Extract JSON from LLM response
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())

            # Validate and set defaults for missing keys
            result = {
                "days": int(parsed.get("days", 2)),
                "themes": parsed.get("themes", []),
                "budget": parsed.get("budget", "moderate"),
                "avoid_crowd": bool(parsed.get("avoid_crowd", False)),
                "prefer_indoor": bool(parsed.get("prefer_indoor", False)),
                "cities": parsed.get("cities", []),
                "group_type": parsed.get("group_type", "family")
            }

            # Clamp days to reasonable range
            result["days"] = max(1, min(result["days"], 7))

            # Validate budget
            if result["budget"] not in ("low", "moderate", "high"):
                result["budget"] = "moderate"

            return result

    except (json.JSONDecodeError, ValueError, AttributeError) as e:
        print(f"[ConstraintAgent] Failed to parse LLM output: {e}")
        print(f"[ConstraintAgent] Raw response: {response[:200]}")

    # Fallback defaults
    return {
        "days": 2,
        "themes": [],
        "budget": "moderate",
        "avoid_crowd": False,
        "prefer_indoor": False,
        "cities": [],
        "group_type": "family"
    }
