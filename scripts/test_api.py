"""Test API: Full itinerary output."""
import requests
import json

r = requests.post("http://127.0.0.1:8000/plan", json={
    "query": "2-day trip to Mathura and Vrindavan for family"
})
d = r.json()

print("=== FULL ITINERARY ===")
for day, acts in d.get("itinerary", {}).items():
    cities = set(a["city"] for a in acts)
    print(f"\n{day} ({', '.join(cities)}) — {len(acts)} activities")
    for act in acts:
        fee = f" Rs{act['entry_fee']}" if act.get("entry_fee") else " Free"
        t = act.get("type", "sightseeing")
        tag = " [LUNCH]" if t == "lunch_break" else ""
        maps = " [MAPS]" if act.get("maps_route_url") else ""
        booking = f" [BOOK: {act['booking_url']}]" if act.get("booking_url") else ""
        print(f"  {act['start']}-{act['end']} | {act['place']} ({act['city']}) | {act['category']} | {act['duration_minutes']}min{fee}{tag}{maps}{booking}")

print(f"\nTotal activities: {sum(len(acts) for acts in d.get('itinerary', {}).values())}")
print(f"Weather alerts: {len(d.get('weather_alerts', []))}")
if d.get('weather_alerts'):
    for a in d['weather_alerts']:
        print(f"  [{a['alert_type']}] {a['message']}")
