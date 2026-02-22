"""
Generate expanded location data for BrajYatra AI.
Adds ~60 new locations for underrepresented cities.
"""

import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "locations_v2.json")

# Load existing locations
with open(DATA_PATH, "r", encoding="utf-8") as f:
    locations = json.load(f)

existing_ids = {loc["id"] for loc in locations}
next_id = max(existing_ids) + 1


def make_loc(name, category, city, lat, lng, description,
             duration=60, opening="06:00-20:00", best_time=None,
             fee_indian=0, fee_foreign=0, fee_child=0, avg_expense=100,
             is_indoor=False, avoid_rain=False, avoid_heat=False,
             crowd="Medium", senior_ok=True, child_ok=True,
             recommended_for=None, intensity="Low", religion="Hindu",
             significance=3, ritual_time=False, parking=True,
             food_nearby=True, restrooms=True, guided=False,
             booking_url=None, closed_on=None, peak_hours=None,
             tags=None):
    global next_id
    loc = {
        "id": next_id,
        "name": name,
        "category": category,
        "description": description,
        "location": {
            "address": city,
            "city": city,
            "state": "Uttar Pradesh",
            "country": "India",
            "coordinates": {"lat": lat, "lng": lng}
        },
        "operational_info": {
            "opening_hours": {"daily": opening},
            "avg_visit_duration_minutes": duration,
            "best_visit_time": best_time or ["Morning", "Evening"],
            "peak_hours": peak_hours or ["10:00-13:00"],
            "closed_on": closed_on or []
        },
        "pricing": {
            "entry_fee": {
                "Indians": fee_indian,
                "Foreigners": fee_foreign,
                "Children": fee_child
            },
            "avg_additional_expense": avg_expense,
            "booking_url": booking_url
        },
        "crowd_data": {
            "base_crowd_level": crowd,
            "weekend_multiplier": 1.3,
            "festival_multiplier": 1.5,
            "seasonal_variation": {
                "Winter": crowd,
                "Summer": "Medium" if crowd == "High" else "Low",
                "Monsoon": "Low"
            }
        },
        "weather_sensitivity": {
            "is_indoor": is_indoor,
            "is_outdoor": not is_indoor,
            "avoid_in_rain": avoid_rain,
            "avoid_in_extreme_heat": avoid_heat
        },
        "visitor_profile_fit": {
            "senior_friendly": senior_ok,
            "wheelchair_accessible": False,
            "child_friendly": child_ok,
            "recommended_for": recommended_for or ["Spiritual", "Exploration"],
            "physical_intensity_level": intensity
        },
        "facilities": {
            "restrooms": restrooms,
            "parking": parking,
            "food_available": food_nearby,
            "guided_tours": guided,
            "locker_facility": False
        },
        "spiritual_metadata": {
            "religion": religion,
            "significance_level": significance,
            "ritual_time_specific": ritual_time
        },
        "nearby_context": {
            "transport_hub_nearby": True,
            "market_nearby": food_nearby,
            "recommended_buffer_time_minutes": 15
        },
        "ratings": {
            "overall_rating": round(3.5 + (significance * 0.2), 1),
            "review_count": significance * 1000
        },
        "embedding_metadata": {
            "tags": tags or [category, city, religion]
        }
    }
    next_id += 1
    return loc


# ──────────────────────────────────────────────
# MATHURA — 15 new locations
# ──────────────────────────────────────────────
new_locs = []

new_locs.append(make_loc(
    "Shri Krishna Janmasthan Temple", "Hindu Temple", "Mathura",
    27.5046, 77.6838,
    "The birthplace of Lord Krishna, one of the holiest sites in Hinduism. The temple complex includes the prison cell where Krishna was born.",
    duration=90, crowd="High", significance=5, ritual_time=True,
    best_time=["Morning", "Evening"], recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Mathura", "Krishna", "Birthplace"]
))

new_locs.append(make_loc(
    "Dwarkadhish Temple", "Hindu Temple", "Mathura",
    27.5066, 77.6862,
    "A magnificent temple dedicated to Lord Krishna as the King of Dwarka. Famous for its intricate carvings and Rajasthani architecture.",
    duration=60, crowd="High", significance=5, ritual_time=True,
    is_indoor=True, recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Mathura", "Krishna", "Architecture"]
))

new_locs.append(make_loc(
    "Vishram Ghat", "Spiritual Site", "Mathura",
    27.5056, 77.6875,
    "The most sacred ghat on the Yamuna in Mathura, where Lord Krishna is said to have rested after slaying Kansa. Evening aarti is spectacular.",
    duration=60, crowd="High", significance=5, ritual_time=True,
    avoid_rain=True, best_time=["Evening"],
    recommended_for=["Spiritual", "Nature"],
    tags=["Ghat", "Mathura", "Yamuna", "Aarti"]
))

new_locs.append(make_loc(
    "Potara Kund", "Heritage Site", "Mathura",
    27.5035, 77.6830,
    "Ancient stepped tank near Krishna Janmasthan where baby Krishna's clothes were washed. A serene architectural marvel.",
    duration=30, crowd="Low", significance=3,
    recommended_for=["Heritage", "Exploration"],
    tags=["Heritage", "Mathura", "Tank", "Ancient"]
))

new_locs.append(make_loc(
    "Government Museum Mathura", "Museum", "Mathura",
    27.4968, 77.6734,
    "One of India's finest museums with sculptures from the Kushan and Gupta periods. Houses exquisite Mathura school of art pieces.",
    duration=90, crowd="Low", significance=4, is_indoor=True,
    opening="10:30-16:30", fee_indian=20, fee_foreign=200,
    closed_on=["Monday"], recommended_for=["Heritage", "Exploration"],
    tags=["Museum", "Mathura", "Art", "History"]
))

new_locs.append(make_loc(
    "Kusum Sarovar", "Spiritual Site", "Mathura",
    27.5850, 77.4528,
    "A beautiful stepped water tank surrounded by ancient cenotaphs. Associated with Radha's collection of flowers for Krishna.",
    duration=45, crowd="Low", significance=4,
    avoid_rain=True, recommended_for=["Spiritual", "Heritage", "Nature"],
    tags=["Sarovar", "Mathura", "Radha", "Nature"]
))

new_locs.append(make_loc(
    "Rangji Temple", "Hindu Temple", "Mathura",
    27.5032, 77.6790,
    "A unique temple blending South Indian and Mughal architectural styles. Features a stunning 50-foot tall gopuram.",
    duration=45, crowd="Medium", significance=3, is_indoor=True,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Mathura", "Architecture", "South Indian"]
))

new_locs.append(make_loc(
    "Kans Qila (Kansa Fort)", "Fort", "Mathura",
    27.5072, 77.6880,
    "An ancient fort overlooking the Yamuna, believed to be the palace of the tyrant king Kansa. Offers panoramic views of the river.",
    duration=45, crowd="Low", significance=3,
    avoid_rain=True, avoid_heat=True,
    recommended_for=["Heritage", "Exploration"],
    tags=["Fort", "Mathura", "Kansa", "Views"]
))

new_locs.append(make_loc(
    "Gita Mandir", "Hindu Temple", "Mathura",
    27.4785, 77.6633,
    "Modern temple with the entire Bhagavad Gita inscribed on its walls. Also houses a depiction of all 24 avatars of Vishnu.",
    duration=40, crowd="Low", significance=3, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Mathura", "Gita", "Vishnu"]
))

new_locs.append(make_loc(
    "Brijwasi Mithai Wala", "Restaurant", "Mathura",
    27.5050, 77.6845,
    "Iconic Mathura sweet shop famous for its pedas, kachori, and lassi. A must-visit for authentic Braj cuisine.",
    duration=30, crowd="Medium", significance=2,
    is_indoor=True, religion="None", opening="08:00-21:00",
    recommended_for=["Food", "Exploration"], avg_expense=150,
    tags=["Restaurant", "Mathura", "Peda", "Sweets"]
))

new_locs.append(make_loc(
    "Mathura Chaat Gali", "Food Stall", "Mathura",
    27.5048, 77.6860,
    "Famous street food lane near Vishram Ghat serving Mathura's legendary chaat, kachori, jalebi, and dahi vada.",
    duration=30, crowd="Medium", significance=2,
    religion="None", opening="09:00-21:00",
    recommended_for=["Food", "Exploration"], avg_expense=100,
    tags=["Food", "Mathura", "Chaat", "Street Food"]
))

new_locs.append(make_loc(
    "Hotel Brijwasi Royal", "Hotel", "Mathura",
    27.4920, 77.6730,
    "Popular mid-range hotel near the city center with AC rooms, restaurant, and parking. Good base for Mathura-Vrindavan tour.",
    duration=0, crowd="Low", significance=1,
    is_indoor=True, religion="None", opening="24 hours",
    recommended_for=["Exploration"], avg_expense=1500,
    tags=["Hotel", "Mathura", "Stay"]
))

new_locs.append(make_loc(
    "Yamuna Aarti Point", "Spiritual Site", "Mathura",
    27.5058, 77.6878,
    "The main aarti point on the Yamuna at Vishram Ghat. The evening aarti with hundreds of diyas floating is mesmerizing.",
    duration=45, crowd="High", significance=4, ritual_time=True,
    best_time=["Evening"], avoid_rain=True,
    recommended_for=["Spiritual"],
    tags=["Aarti", "Mathura", "Yamuna", "Evening"]
))

new_locs.append(make_loc(
    "Dauji Temple", "Hindu Temple", "Mathura",
    27.4533, 77.7833,
    "Ancient temple dedicated to Balarama (Krishna's elder brother). Famous for the Huranga Holi celebration.",
    duration=45, crowd="Low", significance=3,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Mathura", "Balarama", "Dauji"]
))

new_locs.append(make_loc(
    "Keshav Dev Temple", "Hindu Temple", "Mathura",
    27.5048, 77.6840,
    "Temple within the Krishna Janmasthan complex, built on the original site of Krishna's birth. Deeply spiritual atmosphere.",
    duration=45, crowd="High", significance=5, ritual_time=True,
    is_indoor=True, recommended_for=["Spiritual"],
    tags=["Temple", "Mathura", "Krishna", "Sacred"]
))


# ──────────────────────────────────────────────
# VRINDAVAN — 15 new locations
# ──────────────────────────────────────────────

new_locs.append(make_loc(
    "Banke Bihari Temple", "Hindu Temple", "Vrindavan",
    27.5790, 77.6920,
    "The most popular temple in Vrindavan, famous for the enchanting deity of Krishna in his tribhangi pose. Known for its unique darshan style.",
    duration=60, crowd="High", significance=5, ritual_time=True,
    is_indoor=True, best_time=["Morning"],
    recommended_for=["Spiritual"],
    tags=["Temple", "Vrindavan", "Krishna", "Banke Bihari"]
))

new_locs.append(make_loc(
    "ISKCON Vrindavan (Krishna Balaram Mandir)", "Hindu Temple", "Vrindavan",
    27.5835, 77.6870,
    "The international headquarters of ISKCON in Vrindavan. Beautiful marble temple with devotional programs throughout the day.",
    duration=90, crowd="High", significance=5, ritual_time=True,
    is_indoor=True, recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Vrindavan", "ISKCON", "Krishna"]
))

new_locs.append(make_loc(
    "Prem Mandir", "Hindu Temple", "Vrindavan",
    27.5862, 77.6789,
    "A stunning white marble temple illuminated at night. Depicts scenes of Krishna's leelas with Radha. Musical fountain show in evening.",
    duration=60, crowd="High", significance=5,
    best_time=["Evening"], recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Vrindavan", "Prem Mandir", "Marble"]
))

new_locs.append(make_loc(
    "Nidhivan", "Spiritual Site", "Vrindavan",
    27.5782, 77.6905,
    "Sacred grove where Krishna is believed to perform Raas Leela every night. The trees grow in pairs and the tulsi plants remain green year-round.",
    duration=30, crowd="Medium", significance=5,
    opening="05:30-17:30", avoid_rain=True,
    recommended_for=["Spiritual"],
    tags=["Spiritual", "Vrindavan", "Raas Leela", "Sacred Grove"]
))

new_locs.append(make_loc(
    "Radha Raman Temple", "Hindu Temple", "Vrindavan",
    27.5799, 77.6914,
    "A 500-year-old temple housing a self-manifested deity of Krishna. One of the most important Vaishnavite temples in Vrindavan.",
    duration=45, crowd="Medium", significance=5, ritual_time=True,
    is_indoor=True, recommended_for=["Spiritual"],
    tags=["Temple", "Vrindavan", "Radha Raman", "Ancient"]
))

new_locs.append(make_loc(
    "Radha Vallabh Temple", "Hindu Temple", "Vrindavan",
    27.5795, 77.6920,
    "One of the seven original temples of Vrindavan, dedicated to Radha as the supreme deity. Unique because the idol shows only Radha.",
    duration=30, crowd="Low", significance=4, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Vrindavan", "Radha", "Ancient"]
))

new_locs.append(make_loc(
    "Seva Kunj", "Spiritual Site", "Vrindavan",
    27.5777, 77.6910,
    "A sacred garden where Krishna is said to have served Radha. The garden closes at sunset as it's believed divine leelas occur at night.",
    duration=30, crowd="Medium", significance=4,
    opening="05:30-17:30", avoid_rain=True,
    recommended_for=["Spiritual", "Nature"],
    tags=["Garden", "Vrindavan", "Krishna", "Radha"]
))

new_locs.append(make_loc(
    "Kesi Ghat", "Spiritual Site", "Vrindavan",
    27.5802, 77.6944,
    "An ancient ghat on the Yamuna where Krishna killed the demon horse Kesi. Beautiful for morning walks and evening aarti.",
    duration=45, crowd="Medium", significance=4,
    avoid_rain=True, best_time=["Morning", "Evening"],
    recommended_for=["Spiritual", "Nature"],
    tags=["Ghat", "Vrindavan", "Yamuna", "Kesi"]
))

new_locs.append(make_loc(
    "Rangaji Temple Vrindavan", "Hindu Temple", "Vrindavan",
    27.5815, 77.6918,
    "A grand temple in South Indian Dravidian style with a 60-foot tall gopuram. Dedicated to Lord Ranganatha (Vishnu).",
    duration=40, crowd="Low", significance=3, is_indoor=True,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Vrindavan", "Dravidian", "Vishnu"]
))

new_locs.append(make_loc(
    "Vrindavan Chandrodaya Mandir", "Hindu Temple", "Vrindavan",
    27.5855, 77.6760,
    "An under-construction mega temple complex that will be one of the tallest temples in the world at 210 meters.",
    duration=45, crowd="Low", significance=3,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Vrindavan", "Modern", "Mega"]
))

new_locs.append(make_loc(
    "MVT (Meera Vihar Temple) Guest House", "Hotel", "Vrindavan",
    27.5830, 77.6880,
    "Popular spiritual stay run by ISKCON devotees. Clean, vegetarian food, and close to all major temples.",
    duration=0, crowd="Low", significance=1,
    is_indoor=True, religion="None", opening="24 hours",
    recommended_for=["Exploration"], avg_expense=800,
    tags=["Hotel", "Vrindavan", "ISKCON", "Stay"]
))

new_locs.append(make_loc(
    "Govind Dham Restaurant", "Restaurant", "Vrindavan",
    27.5818, 77.6895,
    "Pure vegetarian restaurant serving authentic North Indian thali, paneer dishes, and fresh rotis. Near Banke Bihari Temple.",
    duration=40, crowd="Medium", significance=2,
    is_indoor=True, religion="None", opening="08:00-22:00",
    recommended_for=["Food"], avg_expense=200,
    tags=["Restaurant", "Vrindavan", "Vegetarian", "Thali"]
))

new_locs.append(make_loc(
    "Brajwasi Restaurant", "Restaurant", "Vrindavan",
    27.5805, 77.6905,
    "Popular eatery known for its puri-sabzi, lassi, and South Indian dosa. Budget-friendly and quick service.",
    duration=30, crowd="Medium", significance=2,
    is_indoor=True, religion="None", opening="07:00-21:00",
    recommended_for=["Food"], avg_expense=120,
    tags=["Restaurant", "Vrindavan", "Budget", "Quick"]
))

new_locs.append(make_loc(
    "Loi Bazaar", "Market", "Vrindavan",
    27.5793, 77.6925,
    "Vibrant market near Banke Bihari Temple selling tulsi malas, Krishna idols, bangles, and devotional items.",
    duration=45, crowd="High", significance=2,
    is_indoor=False, religion="None",
    recommended_for=["Shopping", "Exploration"], avg_expense=300,
    tags=["Market", "Vrindavan", "Shopping", "Souvenirs"]
))

new_locs.append(make_loc(
    "Yamuna Boat Ride Vrindavan", "Nature Reserve", "Vrindavan",
    27.5800, 77.6950,
    "Scenic boat ride on the Yamuna river offering views of ghats and temples. Especially beautiful at sunset.",
    duration=40, crowd="Low", significance=3,
    avoid_rain=True, best_time=["Evening"],
    recommended_for=["Nature", "Exploration"], avg_expense=100,
    tags=["Boat", "Vrindavan", "Yamuna", "Nature"]
))


# ──────────────────────────────────────────────
# BARSANA — 10 new locations
# ──────────────────────────────────────────────

new_locs.append(make_loc(
    "Radha Rani Temple (Shriji Temple)", "Hindu Temple", "Barsana",
    27.6483, 77.3783,
    "The main temple atop Barsana hill dedicated to Radha Rani. Offers breathtaking panoramic views of the entire Braj region.",
    duration=90, crowd="High", significance=5, ritual_time=True,
    intensity="Medium", avoid_heat=True,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Barsana", "Radha", "Hilltop"]
))

new_locs.append(make_loc(
    "Lathmar Holi Ground", "Heritage Site", "Barsana",
    27.6475, 77.3790,
    "The famous site where Barsana's Lathmar Holi is celebrated. Women beat men with sticks in this unique festival tradition.",
    duration=30, crowd="Low", significance=4,
    opening="06:00-18:00", recommended_for=["Heritage", "Exploration"],
    tags=["Heritage", "Barsana", "Holi", "Festival"]
))

new_locs.append(make_loc(
    "Pili Pokhar", "Spiritual Site", "Barsana",
    27.6480, 77.3775,
    "Sacred yellow pond at the base of Barsana hill. Legend says Radha used to play here with her friends.",
    duration=20, crowd="Low", significance=3,
    avoid_rain=True, recommended_for=["Spiritual", "Nature"],
    tags=["Pond", "Barsana", "Radha", "Sacred"]
))

new_locs.append(make_loc(
    "Rangibihari Temple", "Hindu Temple", "Barsana",
    27.6490, 77.3780,
    "A beautiful temple at the foot of Barsana hill known for its colorful decorations and peaceful atmosphere.",
    duration=30, crowd="Low", significance=3, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Barsana", "Krishna"]
))

new_locs.append(make_loc(
    "Maan Garh", "Heritage Site", "Barsana",
    27.6488, 77.3770,
    "Hill fort ruins where Radha would pretend to be angry (maan) with Krishna. Offers spectacular views at sunset.",
    duration=40, crowd="Low", significance=3,
    avoid_rain=True, avoid_heat=True, intensity="Medium",
    recommended_for=["Heritage", "Nature"],
    tags=["Fort", "Barsana", "Radha", "Views"]
))

new_locs.append(make_loc(
    "Daan Bihari Temple", "Hindu Temple", "Barsana",
    27.6470, 77.3795,
    "Temple marking the spot where Krishna would tease the gopis and demand toll (daan) for passing. Part of the Radha-Krishna leela.",
    duration=30, crowd="Low", significance=3, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Barsana", "Krishna", "Leela"]
))

new_locs.append(make_loc(
    "Bhanukhar (Vrishbhanu Kund)", "Spiritual Site", "Barsana",
    27.6465, 77.3810,
    "The birthplace of Radha Rani, marked by a sacred kund (pond). King Vrishbhanu found baby Radha on a lotus here.",
    duration=30, crowd="Low", significance=5,
    recommended_for=["Spiritual"],
    tags=["Kund", "Barsana", "Radha", "Birthplace"]
))

new_locs.append(make_loc(
    "Barsana View Point", "Nature Reserve", "Barsana",
    27.6495, 77.3765,
    "Scenic viewpoint atop the Barsana hills offering 360-degree views of the Braj countryside and green valleys.",
    duration=30, crowd="Low", significance=2,
    avoid_rain=True, avoid_heat=True,
    recommended_for=["Nature", "Exploration"],
    tags=["Viewpoint", "Barsana", "Nature", "Panoramic"]
))

new_locs.append(make_loc(
    "Radha Rani Bhojanalaya", "Restaurant", "Barsana",
    27.6468, 77.3800,
    "Simple vegetarian restaurant near the temple serving fresh rotis, sabzi, dal-chawal, and lassi. Affordable pilgrim food.",
    duration=30, crowd="Low", significance=1,
    is_indoor=True, religion="None", opening="08:00-20:00",
    recommended_for=["Food"], avg_expense=80,
    tags=["Restaurant", "Barsana", "Vegetarian", "Budget"]
))

new_locs.append(make_loc(
    "Priya Kund", "Spiritual Site", "Barsana",
    27.6460, 77.3805,
    "Ancient sacred kund where Radha and her sakhis would bathe. Surrounded by old trees and a peaceful atmosphere.",
    duration=20, crowd="Low", significance=3,
    recommended_for=["Spiritual", "Nature"],
    tags=["Kund", "Barsana", "Radha", "Sacred"]
))


# ──────────────────────────────────────────────
# GOKUL — 10 new locations
# ──────────────────────────────────────────────

new_locs.append(make_loc(
    "Nand Bhawan", "Hindu Temple", "Gokul",
    27.4390, 77.7160,
    "The house of Nanda Baba where Krishna grew up. Features beautiful paintings and murals depicting Krishna's childhood leelas.",
    duration=60, crowd="Medium", significance=5, is_indoor=True,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Gokul", "Krishna", "Nanda"]
))

new_locs.append(make_loc(
    "Raman Reti", "Spiritual Site", "Gokul",
    27.4375, 77.7145,
    "Sacred sandy ground where little Krishna played and rolled in the dust. Pilgrims apply this sand on their foreheads.",
    duration=30, crowd="Low", significance=4,
    avoid_rain=True, recommended_for=["Spiritual"],
    tags=["Spiritual", "Gokul", "Krishna", "Sacred"]
))

new_locs.append(make_loc(
    "Brahmand Ghat", "Spiritual Site", "Gokul",
    27.4395, 77.7170,
    "The ghat on the Yamuna where mother Yashoda saw the entire universe in baby Krishna's mouth. Deeply spiritual site.",
    duration=40, crowd="Low", significance=5,
    avoid_rain=True, best_time=["Morning"],
    recommended_for=["Spiritual", "Nature"],
    tags=["Ghat", "Gokul", "Krishna", "Yamuna"]
))

new_locs.append(make_loc(
    "Chintaharan Mahadev Temple", "Hindu Temple", "Gokul",
    27.4385, 77.7155,
    "Ancient Shiva temple believed to remove all worries (chinta). Nanda Baba is said to have worshipped here for Krishna's protection.",
    duration=30, crowd="Low", significance=3, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Gokul", "Shiva", "Ancient"]
))

new_locs.append(make_loc(
    "Yashodanandan Temple", "Hindu Temple", "Gokul",
    27.4388, 77.7162,
    "Temple celebrating the mother-son bond of Yashoda and Krishna. Features a beautiful idol of baby Krishna with butter.",
    duration=30, crowd="Low", significance=3, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Gokul", "Krishna", "Yashoda"]
))

new_locs.append(make_loc(
    "Thakurani Ghat", "Spiritual Site", "Gokul",
    27.4398, 77.7175,
    "A serene ghat on the Yamuna perfect for meditation. Less crowded than Mathura ghats with beautiful sunrise views.",
    duration=30, crowd="Low", significance=3,
    avoid_rain=True, best_time=["Morning"],
    recommended_for=["Spiritual", "Nature"],
    tags=["Ghat", "Gokul", "Yamuna", "Meditation"]
))

new_locs.append(make_loc(
    "Gokulnath Temple", "Hindu Temple", "Gokul",
    27.4382, 77.7148,
    "A Pushti Marg temple established by Vallabhacharya. Important pilgrimage site for Vaishnavites.",
    duration=30, crowd="Low", significance=3, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Gokul", "Vallabhacharya", "Pushti Marg"]
))

new_locs.append(make_loc(
    "Gokul Barrage", "Nature Reserve", "Gokul",
    27.4350, 77.7200,
    "A scenic dam on the Yamuna offering beautiful views and a peaceful picnic spot. Good for families and photography.",
    duration=45, crowd="Low", significance=2,
    avoid_rain=True, recommended_for=["Nature", "Exploration"],
    tags=["Nature", "Gokul", "Yamuna", "Barrage"]
))

new_locs.append(make_loc(
    "Gokul Dham Bhojanalaya", "Restaurant", "Gokul",
    27.4383, 77.7150,
    "Simple pilgrim restaurant serving fresh sattvic food — rotis, dal, sabzi, and buttermilk. Clean and affordable.",
    duration=30, crowd="Low", significance=1,
    is_indoor=True, religion="None", opening="08:00-20:00",
    recommended_for=["Food"], avg_expense=70,
    tags=["Restaurant", "Gokul", "Vegetarian", "Budget"]
))

new_locs.append(make_loc(
    "Chaurasi Khamba (84 Pillars)", "Heritage Site", "Gokul",
    27.4392, 77.7158,
    "An ancient structure with 84 pillars believed to be from the Mughal era. Each pillar has unique carvings.",
    duration=20, crowd="Low", significance=2, is_indoor=True,
    recommended_for=["Heritage", "Exploration"],
    tags=["Heritage", "Gokul", "Ancient", "Pillars"]
))


# ──────────────────────────────────────────────
# GOVARDHAN — 10 new locations
# ──────────────────────────────────────────────

new_locs.append(make_loc(
    "Govardhan Hill (Giriraj)", "Spiritual Site", "Govardhan",
    27.4936, 77.4627,
    "The sacred hill that Lord Krishna lifted on his little finger for 7 days to protect the villagers from Indra's rain. Pilgrims do the 21 km parikrama.",
    duration=180, crowd="High", significance=5, intensity="High",
    avoid_rain=True, avoid_heat=True,
    recommended_for=["Spiritual", "Nature"],
    tags=["Hill", "Govardhan", "Krishna", "Parikrama"]
))

new_locs.append(make_loc(
    "Manasi Ganga", "Spiritual Site", "Govardhan",
    27.4988, 77.4636,
    "A sacred lake created by Krishna's mind (manas). Pilgrims do parikrama of this lake during festivals.",
    duration=45, crowd="Medium", significance=4,
    avoid_rain=True, recommended_for=["Spiritual", "Nature"],
    tags=["Lake", "Govardhan", "Krishna", "Sacred"]
))

new_locs.append(make_loc(
    "Daan Ghati Temple", "Hindu Temple", "Govardhan",
    27.4960, 77.4625,
    "The first major stop on the Govardhan Parikrama route. Krishna collected toll (daan) from gopis here.",
    duration=30, crowd="Medium", significance=4, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Govardhan", "Krishna", "Parikrama"]
))

new_locs.append(make_loc(
    "Mukharvind Temple", "Hindu Temple", "Govardhan",
    27.4954, 77.4630,
    "Temple at the 'face' of Govardhan Hill. The hill's natural rock formation here resembles the face of Lord Krishna.",
    duration=30, crowd="Medium", significance=4, is_indoor=True,
    recommended_for=["Spiritual"],
    tags=["Temple", "Govardhan", "Krishna", "Rock"]
))

new_locs.append(make_loc(
    "Radha Kund", "Spiritual Site", "Govardhan",
    27.5150, 77.4530,
    "The holiest bathing spot in Vrindavan-Braj region, even more sacred than the Ganges according to Chaitanya Mahaprabhu.",
    duration=45, crowd="Medium", significance=5,
    avoid_rain=True, recommended_for=["Spiritual"],
    tags=["Kund", "Govardhan", "Radha", "Sacred"]
))

new_locs.append(make_loc(
    "Shyam Kund", "Spiritual Site", "Govardhan",
    27.5155, 77.4535,
    "Sacred kund adjacent to Radha Kund. Created by Krishna to match Radha's kund. They are considered the eyes of Govardhan.",
    duration=30, crowd="Medium", significance=4,
    avoid_rain=True, recommended_for=["Spiritual"],
    tags=["Kund", "Govardhan", "Krishna", "Sacred"]
))

new_locs.append(make_loc(
    "Harideva Temple", "Hindu Temple", "Govardhan",
    27.4980, 77.4640,
    "A grand red sandstone temple, one of the original temples of Braj. Features stunning Mughal-era architecture.",
    duration=40, crowd="Low", significance=4, is_indoor=True,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Temple", "Govardhan", "Heritage", "Architecture"]
))

new_locs.append(make_loc(
    "Jatipura", "Spiritual Site", "Govardhan",
    27.4900, 77.4610,
    "The starting point of the Govardhan Parikrama. Pilgrims begin their 21 km walk around the hill from here.",
    duration=30, crowd="High", significance=3,
    recommended_for=["Spiritual", "Exploration"],
    tags=["Parikrama", "Govardhan", "Start Point"]
))

new_locs.append(make_loc(
    "Govardhan Annakshetra", "Restaurant", "Govardhan",
    27.4970, 77.4635,
    "Free community kitchen (langar) near the parikrama route serving dal, roti, and rice to all pilgrims. Also has paid thali.",
    duration=30, crowd="Medium", significance=2,
    is_indoor=True, religion="None", opening="07:00-20:00",
    recommended_for=["Food"], avg_expense=0,
    tags=["Restaurant", "Govardhan", "Langar", "Free"]
))

new_locs.append(make_loc(
    "Punchari Ka Lautha", "Heritage Site", "Govardhan",
    27.4945, 77.4620,
    "Ancient spot where Krishna's footprints are imprinted on the rock. Pilgrims come to touch and worship these marks.",
    duration=20, crowd="Low", significance=3,
    recommended_for=["Spiritual", "Heritage"],
    tags=["Heritage", "Govardhan", "Krishna", "Footprints"]
))


# ──────────────────────────────────────────────
# Add ASI booking URLs to existing Agra monuments
# ──────────────────────────────────────────────

ASI_URL = "https://asi.payumoney.com/"
for loc in locations:
    city = loc.get("location", {}).get("city", "")
    name = loc.get("name", "")
    cat = loc.get("category", "")

    # Add booking_url field to all existing locations
    if "booking_url" not in loc.get("pricing", {}):
        loc["pricing"]["booking_url"] = None

    # ASI monuments in Agra
    if city == "Agra" and cat in ("Monument", "Fort", "Mausoleum"):
        if loc["pricing"]["entry_fee"].get("Indians", 0) > 0:
            loc["pricing"]["booking_url"] = ASI_URL


# Merge and save
locations.extend(new_locs)

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(locations, f, ensure_ascii=False, indent=2)

print(f"Done! Total locations: {len(locations)}")

# Print summary by city
cities = {}
for loc in locations:
    city = loc.get("location", {}).get("city", "Unknown")
    cities[city] = cities.get(city, 0) + 1

for city, count in sorted(cities.items(), key=lambda x: -x[1]):
    print(f"  {city}: {count}")
