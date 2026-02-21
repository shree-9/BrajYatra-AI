"""
Conversation Agent — LLM-powered conversational assistant
that maintains context across a dialogue for trip planning.
"""

from core.llm_loader import LLM


def generate_response(history, user_input):
    """
    Generate a conversational response with full dialogue history.

    Args:
        history: list of {"role": "user"/"assistant", "content": "..."}
        user_input: the latest user message

    Returns:
        string response from the LLM
    """

    llm = LLM()

    conversation_text = ""
    # Keep only last 6 messages to avoid context overflow
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
