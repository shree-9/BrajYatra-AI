"""
RL Agent — simple reinforcement learning-style weight adjustment
based on user feedback ratings. Weights are stored in a JSON file.
"""

import json
import os
from config import WEIGHTS_PATH

DEFAULT_WEIGHTS = {
    "rating_weight": 1.0,
    "crowd_penalty": 2.0,
    "weather_penalty": 1.5,
    "diversity_bonus": 0.5,
    "proximity_bonus": 0.3
}


def load_weights():
    """Load scoring weights from file, or create defaults if missing."""

    if not os.path.exists(WEIGHTS_PATH):
        os.makedirs(os.path.dirname(WEIGHTS_PATH), exist_ok=True)
        with open(WEIGHTS_PATH, "w") as f:
            json.dump(DEFAULT_WEIGHTS, f, indent=2)
        return DEFAULT_WEIGHTS.copy()

    try:
        with open(WEIGHTS_PATH) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return DEFAULT_WEIGHTS.copy()


def update_weights(feedback_score):
    """
    Adjust weights based on user feedback (1-5 scale).
    Low scores increase penalties, high scores reward positive signals.
    """

    weights = load_weights()

    if feedback_score <= 2:
        # User unhappy — increase penalties
        weights["crowd_penalty"] = min(5.0, weights["crowd_penalty"] + 0.3)
        weights["weather_penalty"] = min(5.0, weights["weather_penalty"] + 0.2)
    elif feedback_score == 3:
        # Neutral — slight penalty adjustments
        weights["diversity_bonus"] = min(3.0, weights["diversity_bonus"] + 0.1)
    else:
        # User happy — reward current approach
        weights["rating_weight"] = min(3.0, weights["rating_weight"] + 0.1)
        weights["proximity_bonus"] = min(2.0, weights["proximity_bonus"] + 0.1)

    with open(WEIGHTS_PATH, "w") as f:
        json.dump(weights, f, indent=2)

    return weights


def reset_weights():
    """Reset weights to defaults."""
    with open(WEIGHTS_PATH, "w") as f:
        json.dump(DEFAULT_WEIGHTS, f, indent=2)
    return DEFAULT_WEIGHTS.copy()
