"""Quick verification of the new features."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 50)
print("BrajYatra — New Features Verification")
print("=" * 50)

# 1. Test location count
print("\n1. Location data...")
import json
from config import LOCATIONS_PATH
with open(LOCATIONS_PATH, "r", encoding="utf-8") as f:
    locs = json.load(f)
cats = {}
for l in locs:
    c = l.get("category", "Unknown")
    cats[c] = cats.get(c, 0) + 1
print(f"   Total: {len(locs)} locations")
for cat, count in sorted(cats.items()):
    print(f"   {cat}: {count}")
assert len(locs) >= 49, "Expected 49+ locations"
print("   ✅ OK")

# 2. Travel estimator
print("\n2. Travel estimator...")
from agents.travel_estimator import get_travel_estimate, get_daily_food_budget, get_accommodation_estimate

t = get_travel_estimate("Chandigarh")
print(f"   Chandigarh → Braj: {t['distance_km']} km")
print(f"   Train: ₹{t['train']['fare_low']}-{t['train']['fare_high']}")
print(f"   Recommended: {t['recommended']}")

t2 = get_travel_estimate("Mumbai")
print(f"   Mumbai → Braj: {t2['distance_km']} km")
print(f"   Flight: ₹{t2['flight']['fare_low']}-{t2['flight']['fare_high']}")

t3 = get_travel_estimate("RandomCity")
print(f"   Unknown city: source={t3['source']}")
assert t3["source"] == "unknown"
print("   ✅ OK")

# 3. Food budget
print("\n3. Food budget...")
f = get_daily_food_budget("moderate")
print(f"   Moderate: ₹{f['total']}/day")
f2 = get_daily_food_budget("low")
print(f"   Low: ₹{f2['total']}/day")
assert f2["total"] < f["total"]
print("   ✅ OK")

# 4. Accommodation
print("\n4. Accommodation...")
a = get_accommodation_estimate("moderate", 3)
print(f"   3 nights moderate: ₹{a['total_min']}-{a['total_max']} ({a['accommodation_type']})")
print("   ✅ OK")

# 5. Full budget
print("\n5. Full trip budget...")
from agents.budget_agent import estimate_full_trip_budget
budget = estimate_full_trip_budget(
    locs[:5], budget_type="moderate", days=3, origin_city="Chandigarh", persons=2
)
s = budget["summary"]
print(f"   {s['days']} days, {s['persons']} persons from {s['origin_city']}")
print(f"   Grand total: ₹{s['grand_total_min']:,} - ₹{s['grand_total_max']:,}")
assert s["grand_total_min"] > 0
print("   ✅ OK")

# 6. Smart parser — day cap
print("\n6. Smart parser (day cap)...")
from agents.smart_parser import parse_intent_local, detect_command
i = parse_intent_local("10 day trip to Mathura")
print(f"   10-day query → days={i['days']}")
assert i["days"] == 10, f"Expected 10, got {i['days']}"

i2 = parse_intent_local("15 day trip")
assert i2["days"] == 15

# Travel command
cmd = detect_command("travel from Chandigarh")
print(f"   'travel from Chandigarh' → {cmd[0]}")
assert cmd[0] == "travel"
print("   ✅ OK")

print("\n" + "=" * 50)
print("All 6 tests passed! ✅")
print("=" * 50)
