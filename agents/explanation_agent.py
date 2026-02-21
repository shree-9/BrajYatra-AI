"""
Explanation Agent — uses LLM to generate a natural language
explanation of why the itinerary was planned the way it was.

Falls back to a template-based explanation when LLM is unavailable.
"""

_llm_available = True
try:
    from core.llm_loader import LLM
except Exception:
    _llm_available = False


def _fallback_explanation(query, itinerary, intent):
    """Template-based explanation when LLM is unavailable."""
    days = intent.get("days", len(itinerary))
    themes = intent.get("themes", ["General"])
    cities = intent.get("cities", ["Mathura", "Vrindavan"])
    budget = intent.get("budget", "moderate")

    place_count = sum(len(acts) for acts in itinerary.values())

    theme_str = ", ".join(themes) if themes else "spiritual and cultural"
    city_str = " and ".join(cities[:3]) if cities else "the Braj region"

    return (
        f"🙏 Your {days}-day {theme_str.lower()} itinerary covers {place_count} "
        f"handpicked locations across {city_str}. Places were selected based on "
        f"their cultural significance, visitor ratings, and your {budget} budget preference. "
        f"We've optimized the route to minimize travel time between stops. "
        f"Start early each day to enjoy the peaceful morning aarti at temples! 🛕"
    )


def generate_explanation(query, itinerary, intent):
    """
    Generate a human-readable explanation of the generated itinerary.
    Uses LLM when available, falls back to template on CPU.
    """

    if _llm_available:
        try:
            llm = LLM()
            if llm.model is not None:
                itinerary_summary = ""
                for day, activities in itinerary.items():
                    places = [a["place"] for a in activities]
                    itinerary_summary += f"  {day}: {', '.join(places)}\n"

                prompt = f"""You are BrajYatra AI, a travel assistant for the Braj region (Mathura, Vrindavan, Agra, Gokul, Barsana, Govardhan).

A user asked: "{query}"

Their preferences:
- Days: {intent.get('days', 2)}
- Themes: {', '.join(intent.get('themes', ['General']))}
- Budget: {intent.get('budget', 'moderate')}
- Avoid crowds: {intent.get('avoid_crowd', False)}
- Group: {intent.get('group_type', 'family')}

Generated itinerary:
{itinerary_summary}

Write a brief, friendly explanation (3-5 sentences) of:
1. Why these places were chosen
2. How they match the user's preferences
3. Any helpful tips for the trip

Be concise and warm. Do not repeat the full itinerary."""

                return llm.generate(prompt, max_tokens=300)
        except Exception as e:
            print(f"[ExplanationAgent] LLM failed, using fallback: {e}")

    return _fallback_explanation(query, itinerary, intent)
