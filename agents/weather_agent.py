"""
Weather Agent — fetches real weather data from OpenWeather API
and filters locations based on weather conditions.
"""

import requests
from config import OPENWEATHER_API_KEY


def fetch_weather(city="Mathura"):
    """
    Fetch current weather for a city using OpenWeather API.

    Returns:
        dict with temperature, conditions, humidity, rain probability, etc.
        Returns None if API call fails.
    """

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city},IN&appid={OPENWEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"[WeatherAgent] API error {response.status_code} for {city}")
            return None

        data = response.json()

        weather = {
            "city": city,
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "is_rainy": data["weather"][0]["main"].lower() in [
                "rain", "drizzle", "thunderstorm"
            ],
            "is_extreme_heat": data["main"]["temp"] > 40,
            "is_cold": data["main"]["temp"] < 10
        }

        return weather

    except Exception as e:
        print(f"[WeatherAgent] Error fetching weather for {city}: {e}")
        return None


def apply_weather_filter(locations, intent, weather=None):
    """
    Filter locations based on weather conditions and user preferences.

    - If user prefers indoor and it's rainy/extreme heat → remove outdoor places
    - If weather data unavailable → fall back to intent-only filtering
    """

    if intent.get("prefer_indoor"):
        locations = [
            loc for loc in locations
            if loc.get("weather_sensitivity", {}).get("is_indoor", False)
        ]
        return locations

    if weather is None:
        return locations

    filtered = []
    for loc in locations:
        sensitivity = loc.get("weather_sensitivity", {})

        # Skip outdoor places if it's raining and they should be avoided in rain
        if weather["is_rainy"] and sensitivity.get("avoid_in_rain", False):
            continue

        # Skip outdoor places in extreme heat
        if weather["is_extreme_heat"] and sensitivity.get("avoid_in_extreme_heat", False):
            continue

        filtered.append(loc)

    return filtered if filtered else locations  # Fallback: return all if filter too aggressive
