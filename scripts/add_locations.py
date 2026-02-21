"""Script to add food, restaurant, and hotel locations to the dataset."""
import json

NEW_LOCATIONS = [
    # ─── FOOD & RESTAURANTS - Mathura ───
    {
        "id": 33, "name": "Brijwasi Mithai Wala", "category": "Food Stall",
        "description": "Iconic sweet shop famous for Mathura Peda and traditional Braj sweets since 1950s.",
        "location": {"address": "Holi Gate, Mathura", "city": "Mathura", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5046, "lng": 77.6737}},
        "operational_info": {"opening_hours": {"daily": "07:00-22:00"}, "avg_visit_duration_minutes": 30, "best_visit_time": ["Morning", "Evening"], "peak_hours": ["17:00-20:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 150},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.4, "festival_multiplier": 1.8, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food", "Exploration", "Shopping"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 1, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.6, "review_count": 12000},
        "embedding_metadata": {"tags": ["Food", "Sweets", "Peda", "Mathura", "Street Food", "Famous"]}
    },
    {
        "id": 34, "name": "Zaika Restaurant", "category": "Restaurant",
        "description": "Popular multi-cuisine restaurant in Mathura offering North Indian, Chinese, and South Indian food.",
        "location": {"address": "Junction Road, Mathura", "city": "Mathura", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.4924, "lng": 77.6809}},
        "operational_info": {"opening_hours": {"daily": "09:00-23:00"}, "avg_visit_duration_minutes": 60, "best_visit_time": ["Afternoon", "Evening"], "peak_hours": ["13:00-15:00", "19:00-21:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 300},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.3, "festival_multiplier": 1.5, "seasonal_variation": {"Winter": "Medium", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.2, "review_count": 5000},
        "embedding_metadata": {"tags": ["Restaurant", "Food", "Mathura", "Dining", "North Indian"]}
    },
    {
        "id": 35, "name": "Mathura Chaat Bhandar", "category": "Food Stall",
        "description": "Famous street food stall known for Aloo Tikki, Kachori, and Chaat in the heart of Mathura.",
        "location": {"address": "Tilak Dwar, Mathura", "city": "Mathura", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5012, "lng": 77.6741}},
        "operational_info": {"opening_hours": {"daily": "08:00-21:00"}, "avg_visit_duration_minutes": 25, "best_visit_time": ["Morning", "Evening"], "peak_hours": ["17:00-19:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 100},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.5, "festival_multiplier": 2.0, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": False, "is_outdoor": True, "avoid_in_rain": True, "avoid_in_extreme_heat": True},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Food", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 5},
        "ratings": {"overall_rating": 4.4, "review_count": 8000},
        "embedding_metadata": {"tags": ["Food", "Street Food", "Chaat", "Mathura", "Snacks"]}
    },
    # ─── FOOD - Vrindavan ───
    {
        "id": 36, "name": "Govinda's Restaurant (ISKCON)", "category": "Restaurant",
        "description": "Pure vegetarian sattvic restaurant inside ISKCON Vrindavan serving prasadam meals.",
        "location": {"address": "ISKCON Temple, Vrindavan", "city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5830, "lng": 77.6930}},
        "operational_info": {"opening_hours": {"daily": "08:00-21:00"}, "avg_visit_duration_minutes": 45, "best_visit_time": ["Afternoon"], "peak_hours": ["12:00-14:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 200},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.4, "festival_multiplier": 1.7, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food", "Spiritual"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "Hinduism", "significance_level": 3, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.5, "review_count": 9000},
        "embedding_metadata": {"tags": ["Restaurant", "Food", "Vrindavan", "ISKCON", "Prasadam", "Spiritual"]}
    },
    {
        "id": 37, "name": "Vrindavan Lassi Corner", "category": "Food Stall",
        "description": "Famous lassi shop near Bankey Bihari Temple serving thick malai lassi and rabri.",
        "location": {"address": "Near Bankey Bihari Temple, Vrindavan", "city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5714, "lng": 77.7003}},
        "operational_info": {"opening_hours": {"daily": "07:00-20:00"}, "avg_visit_duration_minutes": 20, "best_visit_time": ["Morning", "Afternoon"], "peak_hours": ["10:00-12:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 80},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.5, "festival_multiplier": 2.0, "seasonal_variation": {"Winter": "Medium", "Summer": "High", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": False, "is_outdoor": True, "avoid_in_rain": True, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Food", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": False, "market_nearby": True, "recommended_buffer_time_minutes": 5},
        "ratings": {"overall_rating": 4.3, "review_count": 6000},
        "embedding_metadata": {"tags": ["Food", "Lassi", "Vrindavan", "Street Food", "Famous"]}
    },
    {
        "id": 38, "name": "MVT (Madhu Van) Restaurant", "category": "Restaurant",
        "description": "Popular vegetarian restaurant in Vrindavan with AC dining and thali meals.",
        "location": {"address": "Bhaktivedanta Swami Marg, Vrindavan", "city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5785, "lng": 77.6965}},
        "operational_info": {"opening_hours": {"daily": "08:00-22:00"}, "avg_visit_duration_minutes": 50, "best_visit_time": ["Afternoon", "Evening"], "peak_hours": ["12:30-14:30"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 250},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.3, "festival_multiplier": 1.5, "seasonal_variation": {"Winter": "Medium", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.1, "review_count": 4500},
        "embedding_metadata": {"tags": ["Restaurant", "Food", "Vrindavan", "Dining", "Vegetarian"]}
    },
    # ─── FOOD - Agra ───
    {
        "id": 39, "name": "Panchhi Petha Store", "category": "Food Stall",
        "description": "Agra's most famous petha shop since 1956. A must-visit for the iconic Agra Petha sweet.",
        "location": {"address": "MG Road, Sadar Bazaar, Agra", "city": "Agra", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.1866, "lng": 78.0153}},
        "operational_info": {"opening_hours": {"daily": "08:00-22:00"}, "avg_visit_duration_minutes": 25, "best_visit_time": ["Morning", "Evening"], "peak_hours": ["17:00-20:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 200},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.4, "festival_multiplier": 1.8, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Medium"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food", "Shopping"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.5, "review_count": 15000},
        "embedding_metadata": {"tags": ["Food", "Petha", "Agra", "Sweets", "Famous", "Shopping"]}
    },
    {
        "id": 40, "name": "Mama Chicken", "category": "Restaurant",
        "description": "Popular non-veg restaurant in Agra known for butter chicken and biryani.",
        "location": {"address": "Sanjay Place, Agra", "city": "Agra", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.1883, "lng": 78.0163}},
        "operational_info": {"opening_hours": {"daily": "11:00-23:00"}, "avg_visit_duration_minutes": 60, "best_visit_time": ["Afternoon", "Evening"], "peak_hours": ["13:00-15:00", "20:00-22:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 400},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.3, "festival_multiplier": 1.5, "seasonal_variation": {"Winter": "Medium", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.3, "review_count": 7000},
        "embedding_metadata": {"tags": ["Restaurant", "Food", "Agra", "Non-Veg", "Biryani"]}
    },
    {
        "id": 41, "name": "Deviram Sweets & Namkeen", "category": "Food Stall",
        "description": "Traditional sweet and namkeen shop in Agra famous for bedai-jalebi breakfast.",
        "location": {"address": "Sadar Bazaar, Agra", "city": "Agra", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.1856, "lng": 78.0141}},
        "operational_info": {"opening_hours": {"daily": "07:00-21:00"}, "avg_visit_duration_minutes": 30, "best_visit_time": ["Morning"], "peak_hours": ["08:00-10:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 120},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.4, "festival_multiplier": 1.6, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Medium"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 5},
        "ratings": {"overall_rating": 4.4, "review_count": 6500},
        "embedding_metadata": {"tags": ["Food", "Sweets", "Agra", "Breakfast", "Bedai"]}
    },
    # ─── FOOD - Gokul / Barsana / Govardhan ───
    {
        "id": 42, "name": "Gokul Dham Bhojanalaya", "category": "Restaurant",
        "description": "Simple vegetarian bhojanshala serving traditional Braj food near Gokul temples.",
        "location": {"address": "Main Road, Gokul", "city": "Gokul", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.4380, "lng": 77.7250}},
        "operational_info": {"opening_hours": {"daily": "08:00-20:00"}, "avg_visit_duration_minutes": 40, "best_visit_time": ["Afternoon"], "peak_hours": ["12:00-14:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 100},
        "crowd_data": {"base_crowd_level": "Low", "weekend_multiplier": 1.2, "festival_multiplier": 1.5, "seasonal_variation": {"Winter": "Medium", "Summer": "Low", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Food", "Spiritual"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "Hinduism", "significance_level": 2, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": False, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.0, "review_count": 2000},
        "embedding_metadata": {"tags": ["Restaurant", "Food", "Gokul", "Traditional", "Vegetarian"]}
    },
    {
        "id": 43, "name": "Govardhan Annakut Bhog", "category": "Food Stall",
        "description": "Famous prasad and food stall at Govardhan parikrama route offering sattvic bhog thali.",
        "location": {"address": "Parikrama Marg, Govardhan", "city": "Govardhan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.4990, "lng": 77.4630}},
        "operational_info": {"opening_hours": {"daily": "06:00-19:00"}, "avg_visit_duration_minutes": 30, "best_visit_time": ["Morning", "Afternoon"], "peak_hours": ["11:00-13:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 80},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.5, "festival_multiplier": 2.0, "seasonal_variation": {"Winter": "High", "Summer": "Low", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": False, "is_outdoor": True, "avoid_in_rain": True, "avoid_in_extreme_heat": True},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Food", "Spiritual"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "Hinduism", "significance_level": 4, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": False, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.2, "review_count": 3500},
        "embedding_metadata": {"tags": ["Food", "Prasad", "Govardhan", "Spiritual", "Bhog"]}
    },
    # ─── ACCOMMODATION - Budget ───
    {
        "id": 44, "name": "ISKCON Guesthouse Vrindavan", "category": "Hotel",
        "description": "Clean and affordable guesthouse inside ISKCON campus with spiritual atmosphere.",
        "location": {"address": "ISKCON Temple Complex, Vrindavan", "city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5835, "lng": 77.6935}},
        "operational_info": {"opening_hours": {"daily": "24 Hours"}, "avg_visit_duration_minutes": 720, "best_visit_time": ["Evening"], "peak_hours": [], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 800, "per_night_low": 500, "per_night_moderate": 1000, "per_night_high": 2000},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.4, "festival_multiplier": 2.0, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Spiritual", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": True},
        "spiritual_metadata": {"religion": "Hinduism", "significance_level": 3, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 0},
        "ratings": {"overall_rating": 4.3, "review_count": 5000},
        "embedding_metadata": {"tags": ["Hotel", "Accommodation", "Vrindavan", "ISKCON", "Budget", "Guesthouse"]}
    },
    {
        "id": 45, "name": "Hotel Sheela Agra", "category": "Hotel",
        "description": "Budget-friendly hotel near Taj Mahal with rooftop views and clean rooms.",
        "location": {"address": "Near East Gate, Taj Mahal, Agra", "city": "Agra", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.1721, "lng": 78.0450}},
        "operational_info": {"opening_hours": {"daily": "24 Hours"}, "avg_visit_duration_minutes": 720, "best_visit_time": ["Evening"], "peak_hours": [], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 1200, "per_night_low": 600, "per_night_moderate": 1500, "per_night_high": 3000},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.3, "festival_multiplier": 1.5, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Exploration", "Heritage"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": True},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 0},
        "ratings": {"overall_rating": 4.1, "review_count": 4000},
        "embedding_metadata": {"tags": ["Hotel", "Accommodation", "Agra", "Budget", "Taj Mahal View"]}
    },
    {
        "id": 46, "name": "Mathura Dharamshala", "category": "Hotel",
        "description": "Affordable dharamshala near Shri Krishna Janmabhoomi with basic facilities for pilgrims.",
        "location": {"address": "Near Janmabhoomi, Mathura", "city": "Mathura", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5040, "lng": 77.6740}},
        "operational_info": {"opening_hours": {"daily": "24 Hours"}, "avg_visit_duration_minutes": 720, "best_visit_time": ["Evening"], "peak_hours": [], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 400, "per_night_low": 300, "per_night_moderate": 600, "per_night_high": 1000},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.5, "festival_multiplier": 2.5, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Spiritual"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "Hinduism", "significance_level": 3, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 0},
        "ratings": {"overall_rating": 3.8, "review_count": 2500},
        "embedding_metadata": {"tags": ["Hotel", "Accommodation", "Mathura", "Dharamshala", "Budget", "Pilgrim"]}
    },
    # ─── ACCOMMODATION - Mid-range & Premium ───
    {
        "id": 47, "name": "The Gateway Hotel Agra", "category": "Hotel",
        "description": "Premium Taj Group hotel in Agra with pool, spa, and fine dining restaurant.",
        "location": {"address": "Fatehabad Road, Agra", "city": "Agra", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.1604, "lng": 78.0274}},
        "operational_info": {"opening_hours": {"daily": "24 Hours"}, "avg_visit_duration_minutes": 720, "best_visit_time": ["Evening"], "peak_hours": [], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 5000, "per_night_low": 3000, "per_night_moderate": 5000, "per_night_high": 10000},
        "crowd_data": {"base_crowd_level": "Low", "weekend_multiplier": 1.2, "festival_multiplier": 1.3, "seasonal_variation": {"Winter": "Medium", "Summer": "Low", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Exploration", "Heritage"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": True},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 0},
        "ratings": {"overall_rating": 4.5, "review_count": 8000},
        "embedding_metadata": {"tags": ["Hotel", "Accommodation", "Agra", "Premium", "Luxury", "Pool", "Spa"]}
    },
    {
        "id": 48, "name": "Nidhivan Sarovar Portico", "category": "Hotel",
        "description": "Comfortable mid-range hotel in Vrindavan with modern amenities and spiritual ambiance.",
        "location": {"address": "Chatikara Road, Vrindavan", "city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5670, "lng": 77.6830}},
        "operational_info": {"opening_hours": {"daily": "24 Hours"}, "avg_visit_duration_minutes": 720, "best_visit_time": ["Evening"], "peak_hours": [], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 3000, "per_night_low": 2000, "per_night_moderate": 3500, "per_night_high": 6000},
        "crowd_data": {"base_crowd_level": "Low", "weekend_multiplier": 1.2, "festival_multiplier": 1.4, "seasonal_variation": {"Winter": "Medium", "Summer": "Low", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Spiritual", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": True},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 0},
        "ratings": {"overall_rating": 4.2, "review_count": 3500},
        "embedding_metadata": {"tags": ["Hotel", "Accommodation", "Vrindavan", "Mid-Range", "Comfortable"]}
    },
    # ─── SHOPPING / MARKETS ───
    {
        "id": 49, "name": "Holi Gate Market Mathura", "category": "Market",
        "description": "Bustling market near Holi Gate famous for religious items, clothes, sweets, and local handicrafts.",
        "location": {"address": "Holi Gate, Mathura", "city": "Mathura", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5048, "lng": 77.6735}},
        "operational_info": {"opening_hours": {"daily": "09:00-21:00"}, "avg_visit_duration_minutes": 60, "best_visit_time": ["Evening"], "peak_hours": ["17:00-20:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 300},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.5, "festival_multiplier": 2.0, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Medium"}},
        "weather_sensitivity": {"is_indoor": False, "is_outdoor": True, "avoid_in_rain": True, "avoid_in_extreme_heat": True},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Shopping", "Exploration", "Food"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 1, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.1, "review_count": 5000},
        "embedding_metadata": {"tags": ["Market", "Shopping", "Mathura", "Culture", "Handicrafts"]}
    },
    {
        "id": 50, "name": "Loi Bazaar Vrindavan", "category": "Market",
        "description": "Colorful shopping street near Bankey Bihari with religious souvenirs, bangles, and flutes.",
        "location": {"address": "Near Bankey Bihari Temple, Vrindavan", "city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5710, "lng": 77.7010}},
        "operational_info": {"opening_hours": {"daily": "09:00-20:00"}, "avg_visit_duration_minutes": 45, "best_visit_time": ["Afternoon", "Evening"], "peak_hours": ["16:00-19:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 250},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.5, "festival_multiplier": 2.0, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": False, "is_outdoor": True, "avoid_in_rain": True, "avoid_in_extreme_heat": True},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Shopping", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 1, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": False, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.0, "review_count": 4000},
        "embedding_metadata": {"tags": ["Market", "Shopping", "Vrindavan", "Bangles", "Souvenirs"]}
    },
    {
        "id": 51, "name": "Sadar Bazaar Agra", "category": "Market",
        "description": "Main commercial market of Agra with marble crafts, leather goods, and Mughlai items.",
        "location": {"address": "Sadar Bazaar, Agra", "city": "Agra", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.1870, "lng": 78.0155}},
        "operational_info": {"opening_hours": {"daily": "10:00-21:00"}, "avg_visit_duration_minutes": 60, "best_visit_time": ["Evening"], "peak_hours": ["17:00-20:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 500},
        "crowd_data": {"base_crowd_level": "High", "weekend_multiplier": 1.4, "festival_multiplier": 1.6, "seasonal_variation": {"Winter": "High", "Summer": "Medium", "Monsoon": "Medium"}},
        "weather_sensitivity": {"is_indoor": False, "is_outdoor": True, "avoid_in_rain": True, "avoid_in_extreme_heat": True},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Shopping", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.0, "review_count": 6000},
        "embedding_metadata": {"tags": ["Market", "Shopping", "Agra", "Marble", "Handicrafts"]}
    },
    # ─── MORE VRINDAVAN FOOD ───
    {
        "id": 52, "name": "Baba Doodh Wala", "category": "Food Stall",
        "description": "Legendary milk and rabri shop in Vrindavan famous for fresh malai and kulfi.",
        "location": {"address": "Parikrama Marg, Vrindavan", "city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.5740, "lng": 77.6980}},
        "operational_info": {"opening_hours": {"daily": "06:00-20:00"}, "avg_visit_duration_minutes": 20, "best_visit_time": ["Morning", "Evening"], "peak_hours": ["17:00-19:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 60},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.3, "festival_multiplier": 1.6, "seasonal_variation": {"Winter": "Medium", "Summer": "High", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": False, "is_outdoor": True, "avoid_in_rain": True, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": False, "child_friendly": True, "recommended_for": ["Food", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": False, "parking": False, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": False, "market_nearby": True, "recommended_buffer_time_minutes": 5},
        "ratings": {"overall_rating": 4.5, "review_count": 7000},
        "embedding_metadata": {"tags": ["Food", "Milk", "Kulfi", "Vrindavan", "Street Food", "Famous"]}
    },
    {
        "id": 53, "name": "Brijwasi Royal Restaurant", "category": "Restaurant",
        "description": "Upscale vegetarian restaurant in Mathura with AC, thali meals, and Braj specialties.",
        "location": {"address": "Station Road, Mathura", "city": "Mathura", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.4900, "lng": 77.6780}},
        "operational_info": {"opening_hours": {"daily": "09:00-22:30"}, "avg_visit_duration_minutes": 60, "best_visit_time": ["Afternoon", "Evening"], "peak_hours": ["12:30-14:30", "19:30-21:30"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 350},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.3, "festival_multiplier": 1.5, "seasonal_variation": {"Winter": "Medium", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food", "Exploration"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.3, "review_count": 5500},
        "embedding_metadata": {"tags": ["Restaurant", "Food", "Mathura", "Vegetarian", "Thali", "AC"]}
    },
    {
        "id": 54, "name": "Pinch of Spice Agra", "category": "Restaurant",
        "description": "Popular family restaurant in Agra with North Indian, Mughlai, and Continental cuisine.",
        "location": {"address": "Fatehabad Road, Agra", "city": "Agra", "state": "Uttar Pradesh", "country": "India", "coordinates": {"lat": 27.1617, "lng": 78.0290}},
        "operational_info": {"opening_hours": {"daily": "11:00-23:00"}, "avg_visit_duration_minutes": 60, "best_visit_time": ["Afternoon", "Evening"], "peak_hours": ["13:00-15:00", "20:00-22:00"], "closed_on": []},
        "pricing": {"entry_fee": {"Indians": 0, "Foreigners": 0, "Children": 0}, "avg_additional_expense": 500},
        "crowd_data": {"base_crowd_level": "Medium", "weekend_multiplier": 1.4, "festival_multiplier": 1.5, "seasonal_variation": {"Winter": "Medium", "Summer": "Medium", "Monsoon": "Low"}},
        "weather_sensitivity": {"is_indoor": True, "is_outdoor": False, "avoid_in_rain": False, "avoid_in_extreme_heat": False},
        "visitor_profile_fit": {"senior_friendly": True, "wheelchair_accessible": True, "child_friendly": True, "recommended_for": ["Food"], "physical_intensity_level": "Low"},
        "facilities": {"restrooms": True, "parking": True, "food_available": True, "guided_tours": False, "locker_facility": False},
        "spiritual_metadata": {"religion": "None", "significance_level": 0, "ritual_time_specific": False},
        "nearby_context": {"transport_hub_nearby": True, "market_nearby": True, "recommended_buffer_time_minutes": 10},
        "ratings": {"overall_rating": 4.4, "review_count": 9000},
        "embedding_metadata": {"tags": ["Restaurant", "Food", "Agra", "Multi-Cuisine", "Family"]}
    }
]


def add_locations():
    with open("data/locations_v2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {loc["id"] for loc in data}
    added = 0

    for loc in NEW_LOCATIONS:
        if loc["id"] not in existing_ids:
            data.append(loc)
            added += 1
            print(f"  Added #{loc['id']}: {loc['name']} ({loc['category']}) [{loc['location']['city']}]")

    with open("data/locations_v2.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nTotal: {len(data)} locations ({added} new)")


if __name__ == "__main__":
    add_locations()
