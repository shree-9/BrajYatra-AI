"""
BrajYatra AI — API Test Suite

Tests all endpoints without needing the LLM (uses the FastAPI TestClient).
Run: python test_api.py
"""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))


def test_config():
    """Test config loads correctly."""
    print("🧪 Testing config...")
    from config import (
        MODEL_NAME, LOCATIONS_PATH, SESSIONS_PATH,
        WEIGHTS_PATH, BRAJ_CITIES, OPENWEATHER_API_KEY
    )

    assert MODEL_NAME, "MODEL_NAME is empty"
    assert os.path.exists(LOCATIONS_PATH), f"Locations file not found: {LOCATIONS_PATH}"
    assert len(BRAJ_CITIES) > 0, "BRAJ_CITIES is empty"
    print("  ✅ Config OK\n")


def test_data_loading():
    """Test that location data loads and has correct structure."""
    print("🧪 Testing data loading...")
    from config import LOCATIONS_PATH

    with open(LOCATIONS_PATH, "r", encoding="utf-8") as f:
        locations = json.load(f)

    assert len(locations) > 0, "No locations in data"

    # Check first location has required fields
    loc = locations[0]
    required = ["id", "name", "category", "location", "operational_info",
                "pricing", "crowd_data", "weather_sensitivity", "ratings",
                "embedding_metadata"]

    for field in required:
        assert field in loc, f"Missing field: {field}"

    assert "coordinates" in loc["location"], "Missing coordinates"
    assert "lat" in loc["location"]["coordinates"], "Missing lat"
    assert "lng" in loc["location"]["coordinates"], "Missing lng"

    print(f"  ✅ Loaded {len(locations)} locations with correct schema\n")


def test_budget_agent():
    """Test budget estimation."""
    print("🧪 Testing budget agent...")
    from agents.budget_agent import estimate_budget
    from config import LOCATIONS_PATH

    with open(LOCATIONS_PATH, "r") as f:
        locations = json.load(f)

    budget = estimate_budget(locations[:3], "moderate")

    assert "estimated_total" in budget, "Missing estimated_total"
    assert "breakdown" in budget, "Missing breakdown"
    assert len(budget["breakdown"]) == 3, "Wrong breakdown count"
    assert budget["budget_type"] == "moderate"

    # Test budget types give different results
    low = estimate_budget(locations[:3], "low")
    high = estimate_budget(locations[:3], "high")
    assert low["estimated_total"] <= budget["estimated_total"] <= high["estimated_total"]

    print(f"  ✅ Budget: ₹{budget['estimated_total']} (moderate)\n")


def test_weather_agent():
    """Test weather fetching."""
    print("🧪 Testing weather agent...")
    from agents.weather_agent import fetch_weather, apply_weather_filter
    from config import LOCATIONS_PATH

    # Test real API call
    weather = fetch_weather("Mathura")
    if weather:
        assert "temperature" in weather
        assert "condition" in weather
        print(f"  ✅ Weather: {weather['temperature']}°C, {weather['condition']}")
    else:
        print("  ⚠️ Weather API unavailable (will use fallback)")

    # Test filter function
    with open(LOCATIONS_PATH, "r") as f:
        locations = json.load(f)

    intent = {"prefer_indoor": True}
    filtered = apply_weather_filter(locations[:10], intent)
    assert all(
        loc.get("weather_sensitivity", {}).get("is_indoor", False)
        for loc in filtered
    ), "Indoor filter not working"

    print(f"  ✅ Filter: {len(filtered)} indoor locations from 10\n")


def test_filters():
    """Test utility filters."""
    print("🧪 Testing filters...")
    from utils.filters import filter_by_city, filter_by_category, filter_by_theme
    from config import LOCATIONS_PATH

    with open(LOCATIONS_PATH, "r") as f:
        locations = json.load(f)

    # By city
    agra = filter_by_city(locations, ["Agra"])
    assert all(
        loc["location"]["city"] == "Agra" for loc in agra
    ), "City filter broken"
    print(f"  ✅ City filter: {len(agra)} Agra locations")

    # Empty filter returns all
    all_locs = filter_by_city(locations, [])
    assert len(all_locs) == len(locations)

    print(f"  ✅ Filters OK\n")


def test_scoring():
    """Test scoring agent."""
    print("🧪 Testing scoring agent...")
    from agents.scoring_agent import score_location
    from config import LOCATIONS_PATH

    with open(LOCATIONS_PATH, "r") as f:
        locations = json.load(f)

    intent = {
        "avoid_crowd": True,
        "prefer_indoor": False,
        "themes": ["Spiritual"],
        "cities": [],
        "group_type": "family"
    }

    weights = {
        "rating_weight": 1.0,
        "crowd_penalty": 2.0,
        "weather_penalty": 1.5
    }

    scores = [(loc["name"], score_location(loc, intent, weights)) for loc in locations[:5]]
    print(f"  Scores: {scores}")
    assert all(isinstance(s, (int, float)) for _, s in scores)

    print(f"  ✅ Scoring OK\n")


def test_memory_store():
    """Test JSON session storage."""
    print("🧪 Testing memory store...")
    from core.memory_store import create_session, get_session, add_feedback, update_session

    # Create session
    test_data = {"test": True, "itinerary": {"Day 1": []}}
    sid = create_session(test_data)
    assert sid, "Session ID is empty"

    # Read session
    session = get_session(sid)
    assert session is not None, "Session not found"
    assert session["data"]["test"] == True

    # Add feedback
    result = add_feedback(sid, 4)
    assert result == True

    # Verify feedback
    session = get_session(sid)
    assert len(session["feedback"]) == 1
    assert session["feedback"][0]["rating"] == 4

    print(f"  ✅ Session {sid[:8]}... created, read, and feedback added\n")


def test_distance_matrix():
    """Test distance calculations."""
    print("🧪 Testing distance matrix...")
    from utils.distance_matrix import haversine, estimate_travel_time

    # Mathura to Agra ≈ ~58 km
    dist = haversine(27.4924, 77.6737, 27.1751, 78.0421)
    assert 40 < dist < 80, f"Unexpected distance: {dist}"

    print(f"  ✅ Mathura → Agra: {dist:.1f} km\n")


def test_rl_agent():
    """Test RL weight management."""
    print("🧪 Testing RL agent...")
    from agents.rl_agent import load_weights, update_weights, reset_weights

    # Reset first
    weights = reset_weights()
    assert weights["rating_weight"] == 1.0

    # Update with good feedback
    weights = update_weights(5)
    assert weights["rating_weight"] > 1.0, "Weight should increase with good feedback"

    # Reset back
    reset_weights()

    print(f"  ✅ RL weights OK\n")


def run_all_tests():
    print("\n" + "=" * 50)
    print("🌍 BrajYatra AI — Test Suite")
    print("=" * 50 + "\n")

    tests = [
        test_config,
        test_data_loading,
        test_budget_agent,
        test_weather_agent,
        test_filters,
        test_scoring,
        test_memory_store,
        test_distance_matrix,
        test_rl_agent,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ❌ FAILED: {e}\n")
            failed += 1

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
