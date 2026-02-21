"""
Constraint Agent — parses user's natural language query into structured intent.
Uses LLM first, falls back to rule-based smart_parser if LLM fails.
"""

import json
import re
from agents.smart_parser import parse_intent_local


def parse_intent(query):
    """
    Parse a natural language travel query into structured intent.
    Tries LLM first, falls back to smart_parser.

    Returns:
        dict with keys: days, themes, budget, avoid_crowd,
        prefer_indoor, cities, group_type
    """

    # Try LLM-based parsing first
    try:
        from core.llm_loader import LLM
        llm = LLM()

        if llm.model is not None:
            prompt = f"""You are a travel query parser for the Braj region in India.
Extract structured travel intent from the user's query.

Return ONLY a valid JSON object with these exact keys:
- "days": integer (number of trip days, default 2)
- "themes": list from ["Spiritual", "Heritage", "Exploration", "Nature", "Shopping", "Food"]
- "budget": one of "low", "moderate", "high" (default "moderate")
- "avoid_crowd": boolean (default false)
- "prefer_indoor": boolean (default false)
- "cities": list from ["Mathura", "Vrindavan", "Agra", "Gokul", "Barsana", "Govardhan"]
- "group_type": one of "solo", "couple", "family", "friends", "elderly" (default "family")

User Query: "{query}"

JSON:"""

            response = llm.generate(prompt, max_tokens=200)

            if response and "{" in response:
                json_match = re.search(r"\{.*\}", response, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())

                    result = {
                        "days": max(1, min(int(parsed.get("days", 2)), 15)),
                        "themes": parsed.get("themes", []),
                        "budget": parsed.get("budget", "moderate"),
                        "avoid_crowd": bool(parsed.get("avoid_crowd", False)),
                        "prefer_indoor": bool(parsed.get("prefer_indoor", False)),
                        "cities": parsed.get("cities", []),
                        "group_type": parsed.get("group_type", "family")
                    }

                    if result["budget"] not in ("low", "moderate", "high"):
                        result["budget"] = "moderate"

                    # LLM parsed successfully
                    if result["themes"] or result["cities"]:
                        print("[ConstraintAgent] Parsed via LLM ✓")
                        return result

    except Exception as e:
        print(f"[ConstraintAgent] LLM parsing failed: {e}")

    # Fallback: smart rule-based parser (always works)
    print("[ConstraintAgent] Using smart_parser (rule-based) ✓")
    return parse_intent_local(query)
