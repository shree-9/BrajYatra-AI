"""
Explanation Agent — uses LLM to generate a natural language
explanation of why the itinerary was planned the way it was.
"""

from core.llm_loader import LLM


def generate_explanation(query, itinerary, intent):
    """
    Generate a human-readable explanation of the generated itinerary.
    """

    llm = LLM()

    # Build a concise summary of the itinerary for the prompt
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
