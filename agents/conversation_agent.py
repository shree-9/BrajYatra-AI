"""
Conversation Agent — LLM-powered conversational assistant
that maintains context across a dialogue for trip planning.

Includes a smart fallback for when LLM is unavailable (CPU mode).
"""

import re

# Try to import LLM, but don't block if it fails
_llm_available = True
try:
    from core.llm_loader import LLM
except Exception:
    _llm_available = False


# ─── Fallback Knowledge Base ───

BRAJ_INFO = {
    "mathura": "Mathura is the birthplace of Lord Krishna. Key temples: Shri Krishna Janmasthan, Dwarkadhish Temple, Vishram Ghat. Best time: Oct-Mar, especially during Holi and Janmashtami.",
    "vrindavan": "Vrindavan is where Lord Krishna spent his childhood. Must visit: Banke Bihari Temple, ISKCON Temple, Prem Mandir, Nidhivan. Famous for its 5,000+ temples.",
    "agra": "Agra is home to the Taj Mahal, Agra Fort, and Fatehpur Sikri. Combine it with Mathura (60 km away) for a spiritual + heritage trip.",
    "gokul": "Gokul is where Krishna was raised by Nanda Baba. Visit Nand Bhawan, Raman Reti, and Brahmand Ghat. A peaceful, less-crowded destination.",
    "barsana": "Barsana is the birthplace of Radha Rani. Famous for Lathmar Holi festival and Radha Rani Temple atop a hill with stunning views.",
    "govardhan": "Govardhan has the sacred Govardhan Hill that Krishna lifted on his finger. Do the 21 km Govardhan Parikrama. Visit Kusum Sarovar and Manasi Ganga.",
}

TRIP_TIPS = [
    "🙏 Start your day early (6-7 AM) to enjoy the peaceful temple aarti.",
    "🪔 Vrindavan's Banke Bihari Temple is most serene during morning darshan.",
    "🍽️ Try local Braj delicacies: peda, lassi, kachori, and chaat.",
    "👟 Wear comfortable shoes — temple visits involve a lot of walking.",
    "📸 Photography is not allowed inside most sacred temples.",
    "🚕 Auto-rickshaws are the easiest way to get around Mathura-Vrindavan.",
    "🌡️ Summers (Apr-Jun) are very hot. Carry water and an umbrella.",
    "🎉 Plan around festivals: Holi (Mar), Janmashtami (Aug), Diwali (Nov).",
]


def _fallback_response(user_input):
    """Smart rule-based response when LLM is unavailable."""
    text = user_input.lower().strip()

    # Greetings
    if any(w in text for w in ["hello", "hi", "namaste", "hare krishna", "radhe", "jai"]):
        return (
            "🙏 Radhe Radhe! Welcome to BrajYatra AI! I'm your guide to the sacred Braj region. "
            "Ask me about Mathura, Vrindavan, Govardhan, or say 'plan a trip' to get started!"
        )

    # City-specific info
    for city, info in BRAJ_INFO.items():
        if city in text:
            import random
            tip = random.choice(TRIP_TIPS)
            return f"🛕 **{city.title()}**: {info}\n\n💡 **Tip**: {tip}"

    # Trip planning redirect
    if any(w in text for w in ["plan", "trip", "itinerary", "visit", "travel", "yatra"]):
        return (
            "🗺️ I'd love to help plan your Braj Yatra! Try asking something like:\n\n"
            "• *'Plan a 3-day spiritual trip to Vrindavan'*\n"
            "• *'2 days in Mathura with temples and food'*\n"
            "• *'Family trip to Braj for 4 days'*\n\n"
            "This will generate a full day-wise itinerary with timings and budget! 🙏"
        )

    # Weather
    if "weather" in text:
        return (
            "🌤️ I can check the weather! Try asking:\n"
            "• *'What's the weather in Vrindavan?'*\n"
            "• *'Weather in Mathura today'*"
        )

    # Thank you
    if any(w in text for w in ["thank", "thanks", "dhanyavaad"]):
        return "🙏 Jai Shri Krishna! It's my pleasure to help you on your spiritual journey. Radhe Radhe! 🙏"

    # Default helpful response
    import random
    tip = random.choice(TRIP_TIPS)
    return (
        f"🙏 I'm BrajYatra AI, your guide to the sacred Braj region — the land of Lord Krishna.\n\n"
        f"I can help you with:\n"
        f"• 🗺️ **Plan a trip** — just describe what you want!\n"
        f"• 🛕 **Know about places** — ask about Mathura, Vrindavan, Gokul, Barsana, Govardhan, Agra\n"
        f"• 🌤️ **Check weather** — current conditions in any Braj city\n\n"
        f"💡 **Did you know?** {tip}"
    )


def generate_response(history, user_input):
    """
    Generate a conversational response with full dialogue history.

    Uses LLM when available (GPU/Kaggle), falls back to smart
    rule-based responses on CPU.
    """

    # Try LLM if available and already loaded
    if _llm_available:
        try:
            llm = LLM()
            if llm.model is not None:
                conversation_text = ""
                recent_history = history[-6:] if len(history) > 6 else history
                for msg in recent_history:
                    role = msg["role"].capitalize()
                    conversation_text += f"{role}: {msg['content']}\n"

                prompt = f"""You are BrajYatra AI, a helpful travel planning assistant for the Braj region in India (Mathura, Vrindavan, Agra, Gokul, Barsana, Govardhan).

You help users plan spiritual, heritage, and cultural trips. You can:
- Suggest itineraries
- Answer questions about locations, temples, and attractions
- Help customize travel plans
- Provide budget and weather advice

Previous conversation:
{conversation_text}

User: {user_input}

Respond helpfully and concisely. If the user asks to plan a trip, suggest they use the /plan feature."""

                return llm.generate(prompt, max_tokens=300)
        except Exception as e:
            print(f"[ConversationAgent] LLM failed, using fallback: {e}")

    # Fallback — instant response
    return _fallback_response(user_input)
