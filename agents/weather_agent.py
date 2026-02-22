"""
Weather Agent — fetches real weather data from OpenWeather API
and filters locations based on weather conditions.
Supports multi-city weather and weather alerts.
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


def fetch_weather_multi(cities):
    """
    Fetch weather for multiple cities.

    Returns:
        dict of {city_name: weather_data}
    """
    result = {}
    for city in cities:
        w = fetch_weather(city)
        if w:
            result[city] = w
    return result


def get_weather_alerts(cities):
    """
    Check weather for all cities and generate alerts if conditions
    are adverse (rain, extreme heat, storms).

    Returns:
        list of alert dicts: [{city, alert_type, message, suggestion}]
    """
    alerts = []
    weather_data = fetch_weather_multi(cities)

    for city, w in weather_data.items():
        if w.get("is_rainy"):
            alerts.append({
                "city": city,
                "alert_type": "rain",
                "severity": "warning" if w["condition"] == "Thunderstorm" else "info",
                "message": f"🌧️ Rain ({w['description']}) expected in {city}. Current: {w['temperature']}°C.",
                "suggestion": f"Consider visiting indoor places in {city} — temples, museums, and restaurants are good options."
            })

        if w.get("is_extreme_heat"):
            alerts.append({
                "city": city,
                "alert_type": "heat",
                "severity": "warning",
                "message": f"🔥 Extreme heat ({w['temperature']}°C) in {city}! Feels like {w['feels_like']}°C.",
                "suggestion": f"Visit indoor/AC places in {city}. Carry water and sunscreen. Avoid outdoor sites between 11 AM - 3 PM."
            })

        if w.get("is_cold"):
            alerts.append({
                "city": city,
                "alert_type": "cold",
                "severity": "info",
                "message": f"❄️ Cold weather ({w['temperature']}°C) in {city}. Bundle up!",
                "suggestion": f"Carry warm clothes. Morning fog may reduce visibility at open sites."
            })

    return alerts, weather_data


def apply_weather_filter(locations, intent, weather=None):
    """
    Filter locations based on weather conditions and user preferences.

    - If user prefers indoor and it's rainy/extreme heat → remove outdoor places
    - If weather data unavailable → fall back to intent-only filtering
    """

    if intent.get("prefer_indoor"):
        indoor = [
            loc for loc in locations
            if loc.get("weather_sensitivity", {}).get("is_indoor", False)
        ]
        return indoor if indoor else locations

    if weather is None:
        return locations

    # Handle multi-city weather (dict of city → weather)
    if isinstance(weather, dict) and "city" not in weather:
        # Multi-city: apply per-city
        filtered = []
        for loc in locations:
            loc_city = loc.get("location", {}).get("city", "")
            city_weather = weather.get(loc_city)
            if city_weather:
                if _passes_weather(loc, city_weather):
                    filtered.append(loc)
            else:
                filtered.append(loc)  # No weather data = keep
        return filtered if filtered else locations

    # Single-city weather
    filtered = []
    for loc in locations:
        if _passes_weather(loc, weather):
            filtered.append(loc)

    return filtered if filtered else locations


def _passes_weather(loc, weather):
    """Check if a location passes weather filter."""
    sensitivity = loc.get("weather_sensitivity", {})

    if weather.get("is_rainy") and sensitivity.get("avoid_in_rain", False):
        return False

    if weather.get("is_extreme_heat") and sensitivity.get("avoid_in_extreme_heat", False):
        return False

    return True
