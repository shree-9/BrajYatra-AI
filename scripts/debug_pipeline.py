"""Debug: check how many candidates per city after each pipeline step."""
import json
import sys
sys.path.insert(0, '.')

from agents.constraint_agent import parse_intent
from agents.semantic_agent import SemanticAgent
from agents.scoring_agent import score_location
from agents.diversity_agent import enforce_diversity
from agents.rl_agent import load_weights
from utils.filters import filter_by_city

locs = json.load(open('data/locations_v2.json', 'r', encoding='utf-8'))
sem = SemanticAgent(locs)
query = "2-day trip to Mathura and Vrindavan for family"

intent = parse_intent(query)
print(f"Intent cities: {intent.get('cities')}")

# Step 1: Semantic search
candidates = sem.search(query, k=60)
def city_count(locs):
    cities = {}
    for l in locs:
        c = l.get("location", {}).get("city", "")
        cat = l.get("category", "")
        cities.setdefault(c, {"total": 0, "sight": 0, "food": 0})
        cities[c]["total"] += 1
        if cat in ("Restaurant", "Food Stall", "Hotel"):
            cities[c]["food"] += 1
        else:
            cities[c]["sight"] += 1
    return cities

print(f"\nAfter semantic search (k=60): {len(candidates)}")
print(json.dumps(city_count(candidates), indent=2))

# Step 2: City filter
cities = intent.get("cities", [])
if cities:
    filtered = filter_by_city(candidates, cities)
    if filtered:
        candidates = filtered
    # city guarantee
    candidate_ids = {c["id"] for c in candidates}
    for city in cities:
        ct = sum(1 for c in candidates if c.get("location",{}).get("city","")==city and c.get("category","") not in ("Restaurant","Food Stall","Hotel"))
        if ct < 5:
            for loc in locs:
                if loc["id"] not in candidate_ids and loc.get("location",{}).get("city","")==city and loc.get("category","") not in ("Restaurant","Food Stall","Hotel"):
                    candidates.append(loc)
                    candidate_ids.add(loc["id"])
                    ct += 1
                    if ct >= 5:
                        break

print(f"\nAfter city filter + guarantee: {len(candidates)}")
print(json.dumps(city_count(candidates), indent=2))

# Step 3: Score
weights = load_weights()
ranked = sorted(candidates, key=lambda x: score_location(x, intent, weights), reverse=True)
print(f"\nTop 15 ranked:")
for r in ranked[:15]:
    print(f"  {r['name']} ({r['location']['city']}) [{r['category']}] score={score_location(r, intent, weights):.2f}")

# Step 4: Diversity
diverse = enforce_diversity(ranked, max_per_category=4, cities=cities, min_per_city=max(4, 2*2))
print(f"\nAfter diversity: {len(diverse)}")
print(json.dumps(city_count(diverse), indent=2))
for d in diverse:
    print(f"  {d['name']} ({d['location']['city']}) [{d['category']}]")
