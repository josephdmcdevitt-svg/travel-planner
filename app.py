import streamlit as st
import plotly.graph_objects as go
import hashlib
import json
import os
import random
import secrets
import math
from datetime import date, timedelta
from cities import CITIES

# ── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Travel Planner", page_icon="🌍", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

INTEREST_OPTIONS = {
    "food": "🍜 Food & Street Eats",
    "temples": "🛕 Temples & History",
    "nightlife": "🍸 Nightlife & Bars",
    "beaches": "🏖️ Beaches & Islands",
    "hiking": "🥾 Hiking & Nature",
    "art": "🎨 Art & Museums",
    "shopping": "🛍️ Shopping & Markets",
    "architecture": "🏛️ Architecture",
    "wellness": "💆 Wellness & Spas",
    "wildlife": "🦁 Wildlife",
    "photography": "📸 Photography",
    "culture": "🏡 Local Culture & Homestays",
}

ACTIVITY_TEMPLATES = {
    "food": [
        "Street food walking tour in {city}",
        "Visit the famous local market",
        "Cooking class with a local chef",
        "Try the signature local dish",
        "Dinner at a top-rated local restaurant",
        "Morning coffee and pastry at a beloved café",
    ],
    "temples": [
        "Visit the historic temple complex",
        "Guided walking tour of the old quarter",
        "Explore ancient ruins and monuments",
        "Visit the national history museum",
        "Sunrise visit to the sacred site",
    ],
    "nightlife": [
        "Bar-hopping in the nightlife district",
        "Live music at a popular venue",
        "Rooftop cocktails with city views",
        "Night market exploration",
        "Evening pub crawl with locals",
    ],
    "beaches": [
        "Beach day — swimming and sunbathing",
        "Snorkeling or diving trip",
        "Sunset boat cruise along the coast",
        "Beachside seafood dinner",
        "Island-hopping day trip",
    ],
    "hiking": [
        "Morning hike to a scenic viewpoint",
        "Nature trail through the national park",
        "Guided eco-trek with a local guide",
        "Waterfall visit and swimming hole",
        "Sunrise trek to the summit",
    ],
    "art": [
        "Visit the main art museum",
        "Street art walking tour",
        "Gallery hopping in the art district",
        "Contemporary art exhibition",
        "Artisan workshop visit",
    ],
    "shopping": [
        "Explore the main bazaar and market",
        "Shopping in the artisan district",
        "Visit local craft workshops",
        "Vintage and antique shopping",
        "Pick up souvenirs at the central market",
    ],
    "architecture": [
        "Architecture walking tour of landmarks",
        "Visit the iconic cathedral or palace",
        "Explore the historic district on foot",
        "Guided tour of famous buildings",
        "Photograph the skyline from the best viewpoint",
    ],
    "wellness": [
        "Traditional spa treatment",
        "Morning yoga session",
        "Hot springs or thermal bath visit",
        "Meditation and mindfulness experience",
        "Wellness retreat half-day",
    ],
    "wildlife": [
        "Safari or wildlife spotting tour",
        "Visit the nature reserve",
        "Birdwatching excursion at dawn",
        "Marine wildlife boat trip",
        "Guided wildlife photography walk",
    ],
    "photography": [
        "Sunrise photography at the iconic viewpoint",
        "Photo walk through colorful neighborhoods",
        "Golden hour shoot at the scenic spot",
        "Night photography tour of illuminated landmarks",
        "Capture local life at the morning market",
    ],
    "culture": [
        "Homestay experience with a local family",
        "Traditional craft workshop",
        "Cultural performance or folk show",
        "Visit a local village or community",
        "Learn traditional dance or music",
    ],
}

DEPARTURE_HUBS = {
    "new york": "north_america", "los angeles": "north_america", "chicago": "north_america",
    "san francisco": "north_america", "miami": "north_america", "toronto": "north_america",
    "boston": "north_america", "seattle": "north_america", "denver": "north_america",
    "atlanta": "north_america", "dallas": "north_america", "houston": "north_america",
    "washington": "north_america", "vancouver": "north_america", "montreal": "north_america",
    "london": "europe", "paris": "europe", "berlin": "europe", "amsterdam": "europe",
    "madrid": "europe", "rome": "europe", "frankfurt": "europe", "munich": "europe",
    "sydney": "oceania", "melbourne": "oceania", "auckland": "oceania",
    "tokyo": "asia", "singapore": "asia", "hong kong": "asia", "bangkok": "asia",
    "seoul": "asia", "mumbai": "asia", "delhi": "asia", "beijing": "asia",
    "dubai": "middle_east", "doha": "middle_east", "abu dhabi": "middle_east",
    "sao paulo": "south_america", "buenos aires": "south_america", "lima": "south_america",
    "bogota": "south_america", "mexico city": "south_america",
    "cairo": "africa", "johannesburg": "africa", "nairobi": "africa",
    "cape town": "africa", "casablanca": "africa",
}

FLIGHT_HOURS = {
    ("north_america", "Asia"): 14, ("north_america", "Europe"): 8,
    ("north_america", "South America"): 7, ("north_america", "Africa"): 12,
    ("north_america", "Oceania"): 17,
    ("europe", "Asia"): 10, ("europe", "Europe"): 3,
    ("europe", "South America"): 11, ("europe", "Africa"): 6,
    ("europe", "Oceania"): 20,
    ("asia", "Asia"): 4, ("asia", "Europe"): 10,
    ("asia", "South America"): 18, ("asia", "Africa"): 12,
    ("asia", "Oceania"): 8,
    ("oceania", "Asia"): 8, ("oceania", "Europe"): 20,
    ("oceania", "South America"): 14, ("oceania", "Africa"): 14,
    ("oceania", "Oceania"): 3,
    ("south_america", "Asia"): 18, ("south_america", "Europe"): 11,
    ("south_america", "South America"): 4, ("south_america", "Africa"): 12,
    ("south_america", "Oceania"): 14,
    ("africa", "Asia"): 10, ("africa", "Europe"): 6,
    ("africa", "South America"): 12, ("africa", "Africa"): 4,
    ("africa", "Oceania"): 14,
    ("middle_east", "Asia"): 6, ("middle_east", "Europe"): 6,
    ("middle_east", "South America"): 16, ("middle_east", "Africa"): 6,
    ("middle_east", "Oceania"): 14,
}

# Experience keyword matches for must-have experiences scoring
EXPERIENCE_TAGS = {
    "scuba_diving": ["beaches", "wildlife"],
    "volcano": ["hiking"],
    "aurora": [],
    "safari": ["wildlife"],
    "wine_tasting": ["food"],
    "hot_air_balloon": ["photography"],
    "mountain_trekking": ["hiking"],
    "cooking_class": ["food", "culture"],
    "train_journey": ["culture", "photography"],
    "river_cruise": ["culture", "photography"],
    "festival": ["culture", "nightlife"],
    "ancient_ruins": ["temples", "architecture"],
}

# Cities known for specific experiences
EXPERIENCE_CITIES = {
    "scuba_diving": ["Raja Ampat", "Komodo", "Dahab", "Cairns", "Bali", "Palawan", "Ari Atoll", "Male",
                     "Zanzibar", "Crete", "Galapagos", "Bocas del Toro"],
    "volcano": ["Bali", "Cappadocia", "Sicily", "Bagan", "La Fortuna", "Pucon", "Atacama",
                 "Antigua", "Lake Atitlan", "Jeju", "Reykjavik", "Vik", "Rotorua"],
    "aurora": ["Tromso", "Lofoten", "Rovaniemi", "Reykjavik", "Vik", "Akureyri"],
    "safari": ["Kruger", "Serengeti", "Masai Mara", "Etosha", "Chobe", "Okavango Delta",
               "Chitwan", "Volcanoes NP", "Bwindi", "Arusha"],
    "wine_tasting": ["Bordeaux", "Mendoza", "Stellenbosch", "Santorini", "Tbilisi", "Porto",
                      "Cape Town", "Santiago", "Florence", "San Sebastian"],
    "hot_air_balloon": ["Cappadocia", "Bagan", "Luxor", "Masai Mara", "Serengeti", "Vang Vieng"],
    "mountain_trekking": ["Kathmandu", "Pokhara", "Torres del Paine", "Cusco", "Interlaken",
                           "Zermatt", "Sapa", "Ella", "Kazbegi", "Bariloche"],
    "cooking_class": ["Chiang Mai", "Hoi An", "Oaxaca", "Florence", "Bangkok", "Lima",
                       "Marrakech", "Bali", "Tokyo"],
    "train_journey": ["Ella", "Tokyo", "Kyoto", "Interlaken", "Bergen", "Cusco"],
    "river_cruise": ["Budapest", "Paris", "Cairo", "Hue", "Luang Prabang", "Amsterdam"],
    "festival": ["Rio de Janeiro", "Bangkok", "Chiang Mai", "Seville", "Munich", "Edinburgh",
                  "Venice", "Salvador", "Oaxaca", "Delhi"],
    "ancient_ruins": ["Cusco", "Siem Reap", "Petra", "Athens", "Rome", "Cairo", "Luxor",
                       "Ephesus", "Tikal", "Bagan", "Ayutthaya", "Yogyakarta"],
}

# Region colors for explore map
REGION_COLORS = {
    "Asia": "#e74c3c",
    "Europe": "#3498db",
    "South America": "#2ecc71",
    "Africa": "#e67e22",
    "Oceania": "#9b59b6",
}


# ── Auth Functions ─────────────────────────────────────────────────────────────
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()


def create_account(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    salt = secrets.token_hex(16)
    users[username] = {"salt": salt, "hash": hash_password(password, salt), "saved_trips": []}
    save_users(users)
    return True, "Account created!"


def login(username, password):
    users = load_users()
    if username not in users:
        return False, "Username not found"
    user = users[username]
    if hash_password(password, user["salt"]) == user["hash"]:
        return True, "Welcome back!"
    return False, "Incorrect password"


def save_trip_for_user(username, trip_data):
    users = load_users()
    if username in users:
        users[username].setdefault("saved_trips", []).append(trip_data)
        save_users(users)


# ── Session State ──────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "logged_in": False,
        "username": "",
        "screen": "login",
        "wizard_step": 1,
        "prefs": {},
        "results": None,
        "rng_seed": random.randint(0, 999999),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Matching Algorithm ─────────────────────────────────────────────────────────
def get_departure_region(city_name):
    city_lower = city_name.strip().lower()
    for hub, region in DEPARTURE_HUBS.items():
        if hub in city_lower or city_lower in hub:
            return region
    return "north_america"


def get_flight_hours(departure_region, dest_region):
    return FLIGHT_HOURS.get((departure_region, dest_region), 10)


# English-speaking countries for language scoring
ENGLISH_COUNTRIES = {
    "United Kingdom", "Ireland", "Australia", "New Zealand", "South Africa",
    "Ghana", "Kenya", "Tanzania", "Uganda", "Rwanda", "Namibia", "Botswana",
    "Mauritius", "Philippines", "India", "Malaysia", "Malta",
}


def score_city(city_name, city_data, prefs):
    score = 0.0
    city_tags = city_data.get("tags", [])

    # ── Interest match (biggest factor) ──
    user_tags = prefs.get("interests", [])
    matching_tags = len(set(user_tags) & set(city_tags))
    score += matching_tags * 15

    # ── Budget fit ──
    trip_days = prefs.get("days", 10)
    group_size = {"Solo": 1, "Couple": 2, "Group": 4, "Family": 4}.get(prefs.get("group", "Solo"), 2)
    total_budget = prefs.get("budget", 3000)
    daily_budget_pp = (total_budget * 0.70) / max(trip_days, 1) / max(group_size, 1)
    city_cost = city_data.get("cost", 100)

    if city_cost <= daily_budget_pp:
        score += 25
    elif city_cost <= daily_budget_pp * 1.2:
        score += 10
    else:
        score -= (city_cost - daily_budget_pp) * 0.3

    # ── Weather / season match ──
    travel_month = prefs.get("travel_month", None)
    if travel_month and travel_month in city_data.get("months", []):
        score += 15
    elif travel_month:
        score -= 5

    # ── Weather preference ──
    weather_pref = prefs.get("weather_pref", "any")
    city_weather = city_data.get("weather", "temperate")
    if weather_pref == "warm_only" and city_weather in ("tropical", "hot_dry", "warm", "mild"):
        score += 10
    elif weather_pref == "warm_only" and city_weather in ("cold", "temperate"):
        score -= 15
    if weather_pref == "no_rain" and city_weather == "tropical":
        score -= 10

    # ── Comfort match ──
    user_comfort = prefs.get("comfort", 3)
    city_comfort = city_data.get("comfort", 3)
    if city_comfort >= user_comfort:
        score += 8
    else:
        score -= (user_comfort - city_comfort) * 5

    # ── Adventure level ──
    adventure = prefs.get("adventure", 3)
    if adventure >= 4 and any(t in city_tags for t in ["hiking", "wildlife", "culture"]):
        score += 5
    if adventure <= 2 and city_comfort >= 4:
        score += 5

    # ── Flight penalty / jet lag ──
    dep_region = get_departure_region(prefs.get("departure_city", "New York"))
    hours = get_flight_hours(dep_region, city_data.get("region", "Asia"))

    if prefs.get("no_long_flights", False):
        if hours > 10:
            score -= 20
        elif hours > 8:
            score -= 10

    jet_lag = prefs.get("jet_lag_tolerance", "doesnt_bother")
    if jet_lag == "minimize" and hours > 6:
        score -= hours * 1.5
    elif jet_lag == "prefer_few" and hours > 10:
        score -= 8

    # ── NEW: Trip purpose match (+10) ──
    purpose = prefs.get("trip_purpose", "just_for_fun")
    best_for = city_data.get("best_for", [])
    if purpose in best_for:
        score += 10

    # ── NEW: Language comfort (+/- 8) ──
    lang_comfort = prefs.get("language_comfort", 3)
    country = city_data.get("country", "")
    is_english = country in ENGLISH_COUNTRIES
    if lang_comfort <= 2 and not is_english:
        score -= 8
    elif lang_comfort >= 4 and not is_english:
        score += 3  # adventurous linguist bonus

    # ── NEW: Safety match (+/- 10) ──
    safety_prio = prefs.get("safety_priority", 3)
    city_safety = city_data.get("safety", 3)
    if safety_prio >= 4 and city_safety <= 2:
        score -= 10
    elif safety_prio >= 4 and city_safety >= 4:
        score += 8
    elif safety_prio <= 2:
        score += 2  # doesn't care, slight bonus for adventurous places

    # ── NEW: City size preference (+/- 8) ──
    size_pref = prefs.get("city_size_pref", "mix")
    city_size = city_data.get("city_size", "small_city")
    size_map = {"big_cities": ["mega_city", "large_city"],
                "small_mid": ["small_city", "small_town"],
                "small_towns": ["small_town", "village"]}
    if size_pref != "mix" and size_pref in size_map:
        if city_size in size_map[size_pref]:
            score += 8
        else:
            score -= 8

    # ── NEW: Terrain / landscape match (+10) ──
    landscape_prefs = prefs.get("landscape_prefs", [])
    city_terrain = city_data.get("terrain", "flat")
    terrain_map = {
        "beaches_coast": ["coastal", "island"],
        "mountains": ["mountain"],
        "jungle": ["jungle"],
        "desert": ["desert"],
        "islands": ["island"],
    }
    for lp in landscape_prefs:
        if city_terrain in terrain_map.get(lp, []):
            score += 10
            break

    # ── NEW: Beach type match (+/- 6) ──
    beach_pref = prefs.get("beach_type_pref", "no_preference")
    city_beach = city_data.get("beach_type", None)
    if beach_pref != "no_preference" and city_beach:
        if city_beach == beach_pref:
            score += 6
        elif city_beach != "mixed":
            score -= 3

    # ── NEW: Nightlife importance (+/- 6) ──
    nightlife = prefs.get("nightlife_importance", "nice_to_have")
    has_nightlife = "nightlife" in city_tags
    if nightlife == "essential" and has_nightlife:
        score += 6
    elif nightlife == "essential" and not has_nightlife:
        score -= 6
    elif nightlife == "not_important" and not has_nightlife:
        score += 2

    # ── NEW: Crowd tolerance (+/- 8) ──
    crowd_tolerance = prefs.get("crowd_tolerance", 3)
    city_crowd = city_data.get("crowd_level", 3)
    if crowd_tolerance <= 2 and city_crowd >= 4:
        score -= 8
    elif crowd_tolerance >= 4 and city_crowd >= 4:
        score += 3

    # ── NEW: Wifi needs (+/- 8) ──
    wifi_need = prefs.get("wifi_needs", 3)
    city_wifi = city_data.get("wifi", 3)
    if wifi_need >= 4 and city_wifi <= 2:
        score -= 8
    elif wifi_need >= 4 and city_wifi >= 4:
        score += 5

    # ── NEW: Vegetarian / dietary (+/- 5) ──
    dietary = prefs.get("dietary_restrictions", [])
    veg_score = city_data.get("vegetarian_friendly", 3)
    if any(d in dietary for d in ["vegetarian", "vegan"]):
        if veg_score >= 4:
            score += 5
        elif veg_score <= 2:
            score -= 5

    # ── NEW: Photography priority (+5) ──
    photo = prefs.get("photography_priority", "casual")
    if photo in ("enthusiast", "dedicated") and "photography" in city_tags:
        score += 5

    # ── NEW: Cultural immersion (+5) ──
    immersion = prefs.get("cultural_immersion", 3)
    if immersion >= 4 and "culture" in city_tags:
        score += 5

    # ── NEW: Shopping importance (+5) ──
    shopping = prefs.get("shopping_importance", 3)
    if shopping >= 4 and "shopping" in city_tags:
        score += 5

    # ── NEW: Fitness / hiking match (+/- 5) ──
    fitness = prefs.get("fitness_level", "moderate")
    if fitness == "low" and "hiking" in city_tags and city_comfort <= 2:
        score -= 5
    elif fitness == "high" and "hiking" in city_tags:
        score += 5

    # ── NEW: Must-have experiences (+12 each) ──
    must_haves = prefs.get("must_have_experiences", [])
    for exp in must_haves:
        if city_name in EXPERIENCE_CITIES.get(exp, []):
            score += 12
        else:
            exp_tags = EXPERIENCE_TAGS.get(exp, [])
            if any(t in city_tags for t in exp_tags):
                score += 4

    # ── NEW: Festival interest ──
    fest_interest = prefs.get("festival_interest", "if_one_happens")
    city_festivals = city_data.get("festivals", [])
    if fest_interest == "plan_around" and city_festivals:
        score += 8
    elif fest_interest == "not_interested":
        pass  # no effect

    # ── NEW: Religious site interest ──
    religious = prefs.get("religious_interest", 3)
    if religious >= 4 and "temples" in city_tags:
        score += 5

    # ── NEW: Coast vs mountain slider ──
    coast_mountain = prefs.get("coast_vs_mountain", 3)  # 1=coast, 5=mountain
    if coast_mountain <= 2 and city_terrain in ("coastal", "island"):
        score += 5
    elif coast_mountain >= 4 and city_terrain == "mountain":
        score += 5

    return score


def recommend(prefs):
    rng = random.Random(st.session_state.rng_seed)

    # Score all cities
    scored = []
    for name, data in CITIES.items():
        s = score_city(name, data, prefs)
        s += rng.uniform(-5, 5)
        scored.append((name, data, s))

    scored.sort(key=lambda x: -x[2])

    # Group by country
    country_cities = {}
    for name, data, s in scored:
        c = data["country"]
        country_cities.setdefault(c, []).append((name, data, s))

    # Score countries by average of top 3 cities
    country_scores = {}
    for country, cities in country_cities.items():
        top = cities[:3]
        country_scores[country] = sum(s for _, _, s in top) / len(top)

    # Pick top countries based on trip length
    trip_days = prefs.get("days", 10)
    multi_country = prefs.get("multi_country", False)

    if multi_country:
        num_countries = max(2, min(4, trip_days // 5))
    elif trip_days <= 7:
        num_countries = 1
    elif trip_days <= 14:
        num_countries = 2
    else:
        num_countries = 3

    # Sort countries by score
    sorted_countries = sorted(country_scores, key=lambda c: -country_scores[c])

    if multi_country and num_countries >= 2:
        # Pick the best country first, then nearby countries
        best_country = sorted_countries[0]
        best_region = country_cities[best_country][0][1]["region"]
        top_countries = [best_country]

        for c in sorted_countries[1:]:
            if len(top_countries) >= num_countries:
                break
            c_region = country_cities[c][0][1]["region"]
            # Prefer same region or adjacent (proximity filter)
            if c_region == best_region:
                top_countries.append(c)
            elif c not in top_countries:
                # Allow cross-region if score is high enough
                if country_scores[c] > country_scores[best_country] * 0.6:
                    top_countries.append(c)

        # If we still need more, just take top scorers
        if len(top_countries) < num_countries:
            for c in sorted_countries:
                if c not in top_countries:
                    top_countries.append(c)
                if len(top_countries) >= num_countries:
                    break
    else:
        top_countries = sorted_countries[:num_countries]

    # Pick 2-3 cities per country
    result = []
    for country in top_countries:
        cities = country_cities[country]
        num_cities = min(3, max(2, trip_days // (num_countries * 3)))
        picked = cities[:num_cities]
        result.append({
            "country": country,
            "region": picked[0][1]["region"],
            "score": country_scores[country],
            "cities": [{"name": n, "data": d, "score": s} for n, d, s in picked],
        })

    return result


def build_itinerary(recommended, prefs):
    trip_days = prefs.get("days", 10)
    user_tags = prefs.get("interests", [])
    group_size = {"Solo": 1, "Couple": 2, "Group": 4, "Family": 4}.get(prefs.get("group", "Solo"), 2)
    pace = prefs.get("pace", "Moderate")

    all_cities = []
    for country_info in recommended:
        for city_info in country_info["cities"]:
            richness = len(set(user_tags) & set(city_info["data"].get("tags", [])))
            all_cities.append({**city_info, "richness": max(richness, 1), "country": country_info["country"]})

    total_richness = sum(c["richness"] for c in all_cities)
    travel_days = len(all_cities) - 1
    available_days = trip_days - travel_days

    for city in all_cities:
        raw_days = (city["richness"] / max(total_richness, 1)) * available_days
        city["days_allocated"] = max(1, round(raw_days))

    allocated = sum(c["days_allocated"] for c in all_cities) + travel_days
    diff = trip_days - allocated
    if diff > 0:
        all_cities[0]["days_allocated"] += diff
    elif diff < 0:
        for c in reversed(all_cities):
            can_remove = c["days_allocated"] - 1
            remove = min(can_remove, -diff)
            c["days_allocated"] -= remove
            diff += remove
            if diff >= 0:
                break

    activities_per_day = {"Relaxed": 3, "Moderate": 4, "Packed": 5}.get(pace, 4)
    itinerary = []
    day_counter = 1

    for i, city in enumerate(all_cities):
        city_data = city["data"]
        city_name = city["name"]
        highlights = list(city_data.get("highlights", []))
        used = set()

        pool = []
        for h in highlights:
            pool.append(h)

        for tag in user_tags:
            if tag in city_data.get("tags", []):
                for act in ACTIVITY_TEMPLATES.get(tag, []):
                    pool.append(act.format(city=city_name))

        pool.extend([
            f"Explore {city_name}'s neighborhoods on foot",
            f"Relax at a local café in {city_name}",
            f"Free time to wander and discover {city_name}",
        ])

        for d in range(city["days_allocated"]):
            day_activities = []
            times = ["Morning", "Midday", "Afternoon", "Evening", "Night"][:activities_per_day]

            for t in times:
                picked = None
                for act in pool:
                    if act not in used:
                        picked = act
                        used.add(act)
                        break
                if not picked:
                    picked = f"Free time in {city_name}"
                day_activities.append({"time": t, "activity": picked})

            title = f"Day {day_counter}: {city_name}"
            if d == 0 and i == 0:
                title += " — Arrival"
            elif d == 0 and i > 0:
                title += " — Travel Day"
            elif d == city["days_allocated"] - 1 and i == len(all_cities) - 1:
                title += " — Final Day"

            itinerary.append({
                "day": day_counter,
                "title": title,
                "city": city_name,
                "country": city["country"],
                "activities": day_activities,
            })
            day_counter += 1

    total_cost = 0
    budget_breakdown = []
    for city in all_cities:
        city_total = city["data"]["cost"] * city["days_allocated"] * group_size
        total_cost += city_total
        budget_breakdown.append({
            "city": city["name"],
            "country": city["country"],
            "days": city["days_allocated"],
            "daily_pp": city["data"]["cost"],
            "total": city_total,
        })

    return {
        "itinerary": itinerary,
        "cities": all_cities,
        "budget_breakdown": budget_breakdown,
        "total_cost": total_cost,
        "trip_days": trip_days,
    }


def generate_country_reason(country_info, prefs):
    user_tags = prefs.get("interests", [])
    city_names = [c["name"] for c in country_info["cities"]]
    all_tags = set()
    for c in country_info["cities"]:
        all_tags.update(set(c["data"].get("tags", [])) & set(user_tags))

    tag_labels = [INTEREST_OPTIONS.get(t, t).split(" ", 1)[-1] for t in all_tags]
    tag_str = ", ".join(tag_labels[:4]) if tag_labels else "your travel preferences"

    return (
        f"{country_info['country']} is a great match for your love of {tag_str}. "
        f"With cities like {', '.join(city_names)}, you'll have an unforgettable trip."
    )


# ── CSS ────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    .login-box {
        max-width: 420px; margin: 60px auto; padding: 40px;
        background: white; border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    }
    .login-title { text-align: center; font-size: 2rem; font-weight: 700; color: #1a1a2e; margin-bottom: 4px; }
    .login-sub { text-align: center; color: #666; margin-bottom: 24px; font-size: 0.95rem; }
    .wizard-header { text-align: center; padding: 20px 0 10px; }
    .wizard-title { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin-bottom: 4px; }
    .wizard-sub { color: #666; font-size: 1rem; }
    .step-indicator { display: flex; justify-content: center; gap: 8px; margin: 20px 0 30px; flex-wrap: wrap; }
    .step-dot {
        width: 36px; height: 36px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center; font-weight: 600;
        font-size: 0.8rem; transition: all 0.3s;
    }
    .step-active { background: #4361ee; color: white; }
    .step-done { background: #2ec4b6; color: white; }
    .step-pending { background: #e9ecef; color: #999; }
    .result-card {
        background: white; border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06); margin-bottom: 16px;
    }
    .country-header { font-size: 1.4rem; font-weight: 700; color: #1a1a2e; margin-bottom: 8px; }
    .city-tag {
        display: inline-block; background: #e8f4f8; color: #1a7f8f;
        padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;
        margin: 2px 4px; font-weight: 500;
    }
    .day-card {
        background: #f8f9fa; border-radius: 12px; padding: 16px;
        margin-bottom: 10px; border-left: 4px solid #4361ee;
    }
    .day-title { font-weight: 700; font-size: 1.05rem; color: #1a1a2e; margin-bottom: 8px; }
    .activity-item { padding: 4px 0; color: #444; font-size: 0.92rem; }
    .activity-time { font-weight: 600; color: #4361ee; min-width: 80px; display: inline-block; }
    .budget-card {
        background: linear-gradient(135deg, #4361ee, #3a56d4);
        border-radius: 16px; padding: 24px; color: white; text-align: center;
    }
    .budget-amount { font-size: 2.2rem; font-weight: 700; }
    .budget-label { font-size: 0.9rem; opacity: 0.85; }
    .metric-box {
        background: white; border-radius: 12px; padding: 18px; text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .metric-val { font-size: 1.8rem; font-weight: 700; color: #4361ee; }
    .metric-lbl { font-size: 0.85rem; color: #888; }
    .interest-grid { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }
    .nav-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 24px; border-bottom: 1px solid #eee; margin-bottom: 20px;
    }
    .nav-title { font-size: 1.3rem; font-weight: 700; color: #1a1a2e; }
    .nav-user { color: #666; font-size: 0.9rem; }
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    .explore-card {
        background: white; border-radius: 16px; padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06); margin-top: 16px;
    }
    </style>""", unsafe_allow_html=True)


# ── Login Screen ───────────────────────────────────────────────────────────────
def login_screen():
    st.markdown("")
    st.markdown("")
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-title">🌍 Travel Planner</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Discover your perfect trip</div>', unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username", key="login_user")
                password = st.text_input("Password", type="password", key="login_pass")
                submitted = st.form_submit_button("Log In", use_container_width=True, type="primary")
                if submitted:
                    if username and password:
                        ok, msg = login(username, password)
                        if ok:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.screen = "wizard"
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please enter username and password")

        with tab_signup:
            with st.form("signup_form"):
                new_user = st.text_input("Choose a username", key="signup_user")
                new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
                new_pass2 = st.text_input("Confirm password", type="password", key="signup_pass2")
                submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
                if submitted:
                    if not new_user or not new_pass:
                        st.warning("Please fill in all fields")
                    elif len(new_pass) < 4:
                        st.warning("Password must be at least 4 characters")
                    elif new_pass != new_pass2:
                        st.error("Passwords don't match")
                    else:
                        ok, msg = create_account(new_user, new_pass)
                        if ok:
                            st.success(msg + " You can now log in.")
                        else:
                            st.error(msg)


# ── Wizard Screen ──────────────────────────────────────────────────────────────
def show_step_indicator(current):
    labels = ["Basics", "Style", "Interests", "Experiences", "Comfort",
              "Destination", "Social", "Safety", "Dealbreakers"]
    dots = ""
    for i, label in enumerate(labels):
        step_num = i + 1
        if step_num < current:
            cls = "step-done"
        elif step_num == current:
            cls = "step-active"
        else:
            cls = "step-pending"
        dots += f'<div class="step-dot {cls}" title="{label}">{step_num}</div>'
    st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)


def wizard_screen():
    # Nav bar
    st.markdown(
        f'<div class="nav-bar">'
        f'<span class="nav-title">🌍 Travel Planner</span>'
        f'<span class="nav-user">👤 {st.session_state.username}</span></div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("🗺️ Skip to Explore Map", key="explore_bypass"):
            st.session_state.screen = "explore"
            st.rerun()
    with c3:
        if st.button("Log Out", key="logout_wizard"):
            st.session_state.logged_in = False
            st.session_state.screen = "login"
            st.session_state.wizard_step = 1
            st.session_state.prefs = {}
            st.rerun()

    step = st.session_state.wizard_step
    prefs = st.session_state.prefs

    st.markdown('<div class="wizard-header"><div class="wizard-title">Plan Your Dream Trip</div>'
                '<div class="wizard-sub">Answer a few questions and we\'ll build your perfect itinerary</div></div>',
                unsafe_allow_html=True)
    show_step_indicator(step)

    # ── Step 1: Trip Basics ──
    if step == 1:
        st.subheader("✈️ Trip Basics")
        budget = st.slider("Total budget (USD)", 500, 25000, prefs.get("budget", 3000), step=250,
                           help="Your total trip budget including accommodation, food, activities, and local transport")
        days = st.slider("Trip length (days)", 3, 60, prefs.get("days", 10))
        departure = st.text_input("Departure city", value=prefs.get("departure_city", ""),
                                  placeholder="e.g. New York, London, Sydney")

        st.markdown("**Travel dates**")
        dc1, dc2 = st.columns(2)
        with dc1:
            default_start = date.today() + timedelta(days=60)
            try:
                saved_start = date.fromisoformat(prefs["start_date"]) if "start_date" in prefs else default_start
            except (ValueError, TypeError):
                saved_start = default_start
            start_date = st.date_input("Start date", value=saved_start)
        with dc2:
            default_end = start_date + timedelta(days=days)
            end_date = st.date_input("End date", value=default_end)

        multi_country = st.toggle("I want to visit multiple countries", value=prefs.get("multi_country", False))

        st.markdown("")
        _, rc = st.columns([3, 1])
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next1"):
                if not departure:
                    st.warning("Please enter a departure city")
                else:
                    prefs.update({
                        "budget": budget, "days": days, "departure_city": departure,
                        "start_date": start_date.isoformat(), "end_date": end_date.isoformat(),
                        "travel_month": start_date.month, "multi_country": multi_country,
                    })
                    st.session_state.wizard_step = 2
                    st.rerun()

    # ── Step 2: Travel Style ──
    elif step == 2:
        st.subheader("🧭 Travel Style")
        adventure = st.slider("Adventure level", 1, 5, prefs.get("adventure", 3),
                              help="1 = Very relaxed, stick to tourist areas · 5 = Off the beaten path, thrill-seeking")
        labels = {1: "Very chill", 2: "Easygoing", 3: "Balanced", 4: "Adventurous", 5: "Full send"}
        st.caption(f"You selected: **{labels[adventure]}**")

        pace = st.radio("Trip pace", ["Relaxed", "Moderate", "Packed"],
                        index=["Relaxed", "Moderate", "Packed"].index(prefs.get("pace", "Moderate")),
                        horizontal=True,
                        help="Relaxed = 2-3 activities/day · Moderate = 3-4 · Packed = 5+")

        group = st.radio("Who's traveling?", ["Solo", "Couple", "Group", "Family"],
                         index=["Solo", "Couple", "Group", "Family"].index(prefs.get("group", "Solo")),
                         horizontal=True)

        purpose_options = ["just_for_fun", "honeymoon", "bachelor_ette", "gap_year",
                           "retirement", "bucket_list", "digital_nomad", "family"]
        purpose_labels = {
            "just_for_fun": "Just for fun", "honeymoon": "Honeymoon",
            "bachelor_ette": "Bachelor/ette trip", "gap_year": "Gap year",
            "retirement": "Retirement trip", "bucket_list": "Bucket list",
            "digital_nomad": "Digital nomad", "family": "Family vacation",
        }
        saved_purpose = prefs.get("trip_purpose", "just_for_fun")
        purpose = st.selectbox("Trip purpose",
                               options=purpose_options,
                               format_func=lambda x: purpose_labels[x],
                               index=purpose_options.index(saved_purpose))

        exp_options = ["first_international", "a_few_trips", "seasoned"]
        exp_labels = {"first_international": "First international trip",
                      "a_few_trips": "A few trips under my belt",
                      "seasoned": "Seasoned traveler"}
        saved_exp = prefs.get("travel_experience", "a_few_trips")
        experience = st.radio("Travel experience",
                              options=exp_options,
                              format_func=lambda x: exp_labels[x],
                              index=exp_options.index(saved_exp),
                              horizontal=True)

        st.markdown("")
        lc, rc = st.columns([1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back2"):
                st.session_state.wizard_step = 1
                st.rerun()
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next2"):
                prefs.update({"adventure": adventure, "pace": pace, "group": group,
                              "trip_purpose": purpose, "travel_experience": experience})
                st.session_state.wizard_step = 3
                st.rerun()

    # ── Step 3: Interests ──
    elif step == 3:
        st.subheader("❤️ What do you love?")
        st.caption("Pick as many as you want — we'll match destinations to your interests")

        saved = prefs.get("interests", [])
        selected = []
        cols = st.columns(3)
        for i, (tag, label) in enumerate(INTEREST_OPTIONS.items()):
            with cols[i % 3]:
                if st.checkbox(label, value=tag in saved, key=f"int_{tag}"):
                    selected.append(tag)

        st.markdown("")
        lc, rc = st.columns([1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back3"):
                st.session_state.wizard_step = 2
                st.rerun()
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next3"):
                if not selected:
                    st.warning("Pick at least one interest!")
                else:
                    prefs["interests"] = selected
                    st.session_state.wizard_step = 4
                    st.rerun()

    # ── Step 4: Must-Have Experiences (NEW) ──
    elif step == 4:
        st.subheader("🌟 Must-Have Experiences")
        st.caption("Any bucket-list experiences you want on this trip?")

        exp_options_map = {
            "scuba_diving": "🤿 Scuba diving / snorkeling",
            "volcano": "🌋 Visit a volcano",
            "aurora": "🌌 See the Northern Lights",
            "safari": "🦒 Go on safari",
            "wine_tasting": "🍷 Wine tasting",
            "hot_air_balloon": "🎈 Hot air balloon ride",
            "mountain_trekking": "🏔️ Mountain trekking",
            "cooking_class": "👨‍🍳 Cooking class",
            "train_journey": "🚂 Scenic train journey",
            "river_cruise": "🚢 River cruise",
            "festival": "🎉 Attend a festival",
            "ancient_ruins": "🏛️ Explore ancient ruins",
        }
        saved_exp = prefs.get("must_have_experiences", [])
        must_haves = st.multiselect("Must-have experiences",
                                     options=list(exp_options_map.keys()),
                                     format_func=lambda x: exp_options_map[x],
                                     default=saved_exp)

        fest_options = ["not_interested", "if_one_happens", "plan_around"]
        fest_labels = {"not_interested": "Not interested in festivals",
                       "if_one_happens": "If one happens to be on, great!",
                       "plan_around": "I'd plan my trip around a festival"}
        saved_fest = prefs.get("festival_interest", "if_one_happens")
        festival = st.radio("Festival interest",
                            options=fest_options,
                            format_func=lambda x: fest_labels[x],
                            index=fest_options.index(saved_fest),
                            horizontal=True)

        religious = st.slider("Interest in religious/spiritual sites", 1, 5,
                              prefs.get("religious_interest", 3),
                              help="1 = Not interested · 5 = Very interested")

        st.markdown("")
        lc, rc = st.columns([1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back4"):
                st.session_state.wizard_step = 3
                st.rerun()
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next4"):
                prefs.update({"must_have_experiences": must_haves,
                              "festival_interest": festival,
                              "religious_interest": religious})
                st.session_state.wizard_step = 5
                st.rerun()

    # ── Step 5: Comfort & Accommodation ──
    elif step == 5:
        st.subheader("🛏️ Comfort & Accommodation")

        comfort = st.slider("Accommodation preference", 1, 5, prefs.get("comfort", 3),
                            help="1 = Hostels & basic guesthouses · 5 = Luxury hotels & resorts")
        comfort_labels = {1: "Hostels & dorms", 2: "Budget guesthouses", 3: "Nice hotels",
                          4: "Boutique / upper-mid", 5: "Luxury resorts"}
        st.caption(f"You selected: **{comfort_labels[comfort]}**")

        transport = st.radio("Transport preference",
                             ["Local buses & trains", "Mix of local and private", "Private / taxi"],
                             index=["Local buses & trains", "Mix of local and private", "Private / taxi"]
                             .index(prefs.get("transport", "Mix of local and private")),
                             horizontal=True)

        food_adventure = st.slider("Food adventurousness", 1, 5, prefs.get("food_adventure", 3),
                                   help="1 = Familiar food only · 5 = I'll eat anything from a street cart")
        food_labels = {1: "Stick to what I know", 2: "Mildly curious", 3: "Open to trying things",
                       4: "Adventurous eater", 5: "Feed me anything"}
        st.caption(f"You selected: **{food_labels[food_adventure]}**")

        dietary_options = ["vegetarian", "vegan", "halal", "kosher", "gluten_free"]
        dietary_labels = {"vegetarian": "Vegetarian", "vegan": "Vegan", "halal": "Halal",
                          "kosher": "Kosher", "gluten_free": "Gluten-free"}
        saved_dietary = prefs.get("dietary_restrictions", [])
        dietary = st.multiselect("Dietary restrictions",
                                  options=dietary_options,
                                  format_func=lambda x: dietary_labels[x],
                                  default=saved_dietary)

        wifi = st.slider("Internet / wifi needs", 1, 5, prefs.get("wifi_needs", 3),
                         help="1 = Don't need it · 5 = Must have reliable wifi")

        fitness_options = ["low", "moderate", "high"]
        fitness_labels = {"low": "Low — prefer minimal walking", "moderate": "Moderate — can handle some hikes",
                          "high": "High — love challenging treks"}
        saved_fitness = prefs.get("fitness_level", "moderate")
        fitness = st.radio("Physical fitness level",
                           options=fitness_options,
                           format_func=lambda x: fitness_labels[x],
                           index=fitness_options.index(saved_fitness),
                           horizontal=True)

        st.markdown("")
        lc, rc = st.columns([1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back5"):
                st.session_state.wizard_step = 4
                st.rerun()
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next5"):
                prefs.update({"comfort": comfort, "transport": transport,
                              "food_adventure": food_adventure, "dietary_restrictions": dietary,
                              "wifi_needs": wifi, "fitness_level": fitness})
                st.session_state.wizard_step = 6
                st.rerun()

    # ── Step 6: Destination Preferences (NEW) ──
    elif step == 6:
        st.subheader("🏞️ Destination Preferences")

        size_options = ["big_cities", "small_mid", "small_towns", "mix"]
        size_labels = {"big_cities": "Big cities", "small_mid": "Small-mid cities",
                       "small_towns": "Small towns & villages", "mix": "Mix of everything"}
        saved_size = prefs.get("city_size_pref", "mix")
        city_size = st.radio("City size preference",
                             options=size_options,
                             format_func=lambda x: size_labels[x],
                             index=size_options.index(saved_size),
                             horizontal=True)

        landscape_options = ["beaches_coast", "mountains", "jungle", "desert", "islands"]
        landscape_labels = {"beaches_coast": "🏖️ Beaches & coast", "mountains": "⛰️ Mountains",
                            "jungle": "🌴 Jungle / rainforest", "desert": "🏜️ Desert",
                            "islands": "🏝️ Islands"}
        saved_landscape = prefs.get("landscape_prefs", [])
        landscape = st.multiselect("Landscape preferences",
                                    options=landscape_options,
                                    format_func=lambda x: landscape_labels[x],
                                    default=saved_landscape)

        beach_pref = "no_preference"
        if "beaches_coast" in landscape or "islands" in landscape:
            beach_options = ["party", "secluded", "family", "no_preference"]
            beach_labels = {"party": "Party beaches", "secluded": "Secluded / quiet",
                            "family": "Family-friendly", "no_preference": "No preference"}
            saved_beach = prefs.get("beach_type_pref", "no_preference")
            beach_pref = st.radio("Beach type",
                                  options=beach_options,
                                  format_func=lambda x: beach_labels[x],
                                  index=beach_options.index(saved_beach),
                                  horizontal=True)

        coast_mountain = st.slider("Coast vs Mountain", 1, 5, prefs.get("coast_vs_mountain", 3),
                                   help="1 = Prefer coast & beaches · 5 = Prefer mountains & highlands")
        cm_labels = {1: "Coast lover", 2: "Leaning coastal", 3: "Both are great",
                     4: "Leaning mountains", 5: "Mountain lover"}
        st.caption(f"You selected: **{cm_labels[coast_mountain]}**")

        st.markdown("")
        lc, rc = st.columns([1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back6"):
                st.session_state.wizard_step = 5
                st.rerun()
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next6"):
                prefs.update({"city_size_pref": city_size, "landscape_prefs": landscape,
                              "beach_type_pref": beach_pref, "coast_vs_mountain": coast_mountain})
                st.session_state.wizard_step = 7
                st.rerun()

    # ── Step 7: Social & Cultural (NEW) ──
    elif step == 7:
        st.subheader("🤝 Social & Cultural")

        lang_comfort = st.slider("Language barrier comfort", 1, 5,
                                 prefs.get("language_comfort", 3),
                                 help="1 = Only go where English is spoken · 5 = Love learning new languages")

        immersion = st.slider("Cultural immersion level", 1, 5,
                              prefs.get("cultural_immersion", 3),
                              help="1 = Tourist-friendly spots · 5 = Live like a local")

        night_options = ["not_important", "nice_to_have", "important", "essential"]
        night_labels = {"not_important": "Not important", "nice_to_have": "Nice to have",
                        "important": "Important", "essential": "Essential"}
        saved_night = prefs.get("nightlife_importance", "nice_to_have")
        nightlife = st.radio("Nightlife importance",
                             options=night_options,
                             format_func=lambda x: night_labels[x],
                             index=night_options.index(saved_night),
                             horizontal=True)

        crowd_tolerance = st.slider("Crowd / tourist tolerance", 1, 5,
                                    prefs.get("crowd_tolerance", 3),
                                    help="1 = Avoid crowds at all costs · 5 = Don't mind tourist hotspots")

        photo_options = ["casual", "enthusiast", "dedicated"]
        photo_labels = {"casual": "Casual — phone snaps", "enthusiast": "Enthusiast — good photos matter",
                        "dedicated": "Dedicated — photography drives my trips"}
        saved_photo = prefs.get("photography_priority", "casual")
        photo = st.radio("Photography priority",
                         options=photo_options,
                         format_func=lambda x: photo_labels[x],
                         index=photo_options.index(saved_photo),
                         horizontal=True)

        st.markdown("")
        lc, rc = st.columns([1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back7"):
                st.session_state.wizard_step = 6
                st.rerun()
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next7"):
                prefs.update({"language_comfort": lang_comfort, "cultural_immersion": immersion,
                              "nightlife_importance": nightlife, "crowd_tolerance": crowd_tolerance,
                              "photography_priority": photo})
                st.session_state.wizard_step = 8
                st.rerun()

    # ── Step 8: Safety & Logistics (NEW) ──
    elif step == 8:
        st.subheader("🔒 Safety & Logistics")

        safety = st.slider("Safety priority", 1, 5, prefs.get("safety_priority", 3),
                           help="1 = I'm comfortable anywhere · 5 = Safety is my top priority")

        jet_options = ["doesnt_bother", "prefer_few", "minimize"]
        jet_labels = {"doesnt_bother": "Doesn't bother me",
                      "prefer_few": "Prefer just a few hours",
                      "minimize": "Minimize jet lag"}
        saved_jet = prefs.get("jet_lag_tolerance", "doesnt_bother")
        jet_lag = st.radio("Jet lag tolerance",
                           options=jet_options,
                           format_func=lambda x: jet_labels[x],
                           index=jet_options.index(saved_jet),
                           horizontal=True)

        shopping = st.slider("Shopping importance", 1, 5, prefs.get("shopping_importance", 3),
                             help="1 = Not interested · 5 = Shopping is a big part of my trip")

        st.markdown("")
        lc, rc = st.columns([1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back8"):
                st.session_state.wizard_step = 7
                st.rerun()
        with rc:
            if st.button("Next →", use_container_width=True, type="primary", key="next8"):
                prefs.update({"safety_priority": safety, "jet_lag_tolerance": jet_lag,
                              "shopping_importance": shopping})
                st.session_state.wizard_step = 9
                st.rerun()

    # ── Step 9: Dealbreakers ──
    elif step == 9:
        st.subheader("⚠️ Dealbreakers")
        st.caption("Any hard requirements? We'll filter out destinations that don't fit.")

        no_long_flights = st.checkbox("Avoid very long flights (10+ hours)",
                                      value=prefs.get("no_long_flights", False))

        weather_pref = st.radio("Weather preference",
                                ["Any weather is fine", "Warm destinations only", "Avoid rainy season"],
                                index=["any", "warm_only", "no_rain"]
                                .index(prefs.get("weather_pref", "any")),
                                horizontal=True)
        weather_map = {"Any weather is fine": "any", "Warm destinations only": "warm_only",
                       "Avoid rainy season": "no_rain"}

        region_pref = st.multiselect("Preferred regions (leave empty for all)",
                                     ["Asia", "Europe", "South America", "Africa", "Oceania"],
                                     default=prefs.get("region_pref", []))

        st.markdown("")
        st.markdown("---")
        lc, mc, rc = st.columns([1, 1, 1])
        with lc:
            if st.button("← Back", use_container_width=True, key="back9"):
                st.session_state.wizard_step = 8
                st.rerun()
        with rc:
            if st.button("🌍 Generate My Trip!", use_container_width=True, type="primary", key="generate"):
                prefs.update({
                    "no_long_flights": no_long_flights,
                    "weather_pref": weather_map[weather_pref],
                    "region_pref": region_pref,
                })
                # Filter by region if specified
                global CITIES
                filtered_cities = CITIES
                if region_pref:
                    filtered_cities = {k: v for k, v in CITIES.items() if v["region"] in region_pref}

                original = CITIES
                CITIES = filtered_cities if filtered_cities else original

                recommended = recommend(prefs)
                CITIES = original

                if not recommended:
                    st.error("No destinations matched your criteria. Try adjusting your preferences.")
                else:
                    result = build_itinerary(recommended, prefs)
                    result["recommended"] = recommended
                    st.session_state.results = result
                    st.session_state.screen = "results"
                    st.rerun()


# ── Explore Map Screen ─────────────────────────────────────────────────────────
def explore_screen():
    st.markdown(
        f'<div class="nav-bar">'
        f'<span class="nav-title">🌍 Explore the World</span>'
        f'<span class="nav-user">👤 {st.session_state.username}</span></div>',
        unsafe_allow_html=True,
    )

    nc1, nc2, nc3 = st.columns([1, 1, 1])
    with nc1:
        if st.button("← Back to Wizard", key="back_to_wizard_explore"):
            st.session_state.screen = "wizard"
            st.rerun()
    with nc3:
        if st.button("🚪 Log Out", key="logout_explore"):
            st.session_state.logged_in = False
            st.session_state.screen = "login"
            st.session_state.wizard_step = 1
            st.session_state.prefs = {}
            st.rerun()

    # Build map data by region
    fig = go.Figure()

    for region, color in REGION_COLORS.items():
        region_cities = {k: v for k, v in CITIES.items() if v["region"] == region}
        if not region_cities:
            continue

        lats = [v["lat"] for v in region_cities.values()]
        lons = [v["lon"] for v in region_cities.values()]
        names = list(region_cities.keys())
        hover_texts = []
        for name, data in region_cities.items():
            desc = data.get("description", "")[:80]
            best_months = ", ".join(
                ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][m - 1]
                for m in data.get("months", [])[:4]
            )
            tags_str = ", ".join(
                INTEREST_OPTIONS.get(t, t).split(" ", 1)[-1]
                for t in data.get("tags", [])[:4]
            )
            highlights = " · ".join(data.get("highlights", [])[:3])
            hover_texts.append(
                f"<b>{name}</b>, {data['country']}<br>"
                f"${data['cost']}/day · Best: {best_months}<br>"
                f"{tags_str}<br>"
                f"{highlights}<br>"
                f"<i>{desc}...</i>"
            )

        fig.add_trace(go.Scattergeo(
            lat=lats, lon=lons,
            mode="markers",
            marker=dict(size=8, color=color, opacity=0.8,
                        line=dict(width=0.5, color="white")),
            text=hover_texts,
            hoverinfo="text",
            name=region,
        ))

    fig.update_layout(
        geo=dict(
            showframe=False, showcoastlines=True,
            coastlinecolor="rgba(0,0,0,0.2)",
            showland=True, landcolor="rgba(243,243,243,1)",
            showocean=True, oceancolor="rgba(218,232,245,1)",
            showlakes=True, lakecolor="rgba(218,232,245,1)",
            projection_type="natural earth",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True)

    # City selector
    st.markdown("### City Details")
    city_names = sorted(CITIES.keys())
    selected_city = st.selectbox("Select a city to learn more", city_names, key="explore_city_select")

    if selected_city:
        data = CITIES[selected_city]
        desc = data.get("description", "A great destination")
        tags_html = "".join(
            f'<span class="city-tag">{INTEREST_OPTIONS.get(t, t).split(" ", 1)[-1]}</span>'
            for t in data.get("tags", [])[:8]
        )
        highlights = " · ".join(data.get("highlights", [])[:5])
        best_months = ", ".join(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][m - 1]
            for m in data.get("months", [])
        )
        festivals = data.get("festivals", [])
        fest_str = " · ".join(festivals) if festivals else "No major festivals listed"
        best_for_labels = {
            "honeymoon": "Honeymoon", "bucket_list": "Bucket list",
            "digital_nomad": "Digital nomad", "family": "Family",
            "bachelor_ette": "Bachelor/ette", "gap_year": "Gap year",
            "retirement": "Retirement", "just_for_fun": "Just for fun",
        }
        best_for = ", ".join(best_for_labels.get(b, b) for b in data.get("best_for", []))

        st.markdown(
            f'<div class="explore-card">'
            f'<div style="font-size:1.3rem;font-weight:700;color:#1a1a2e;">'
            f'{selected_city}, {data["country"]}</div>'
            f'<p style="color:#555;margin:8px 0;">{desc}</p>'
            f'<div style="margin:8px 0;">{tags_html}</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0;">'
            f'<div><strong>Cost:</strong> ${data["cost"]}/day per person</div>'
            f'<div><strong>Safety:</strong> {"⭐" * data.get("safety", 3)}</div>'
            f'<div><strong>Wifi:</strong> {"📶" * data.get("wifi", 3)}</div>'
            f'<div><strong>Language:</strong> {data.get("language", "Local")}</div>'
            f'<div><strong>Best months:</strong> {best_months}</div>'
            f'<div><strong>Terrain:</strong> {data.get("terrain", "flat").replace("_", " ").title()}</div>'
            f'</div>'
            f'<p><strong>Highlights:</strong> {highlights}</p>'
            f'<p><strong>Festivals:</strong> {fest_str}</p>'
            f'<p><strong>Best for:</strong> {best_for}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if st.button(f"🗺️ Plan a trip to {selected_city}!", key="plan_trip_explore", type="primary"):
            st.session_state.prefs["region_pref"] = [data["region"]]
            st.session_state.screen = "wizard"
            st.session_state.wizard_step = 1
            st.rerun()


# ── Results Screen ─────────────────────────────────────────────────────────────
def results_screen():
    results = st.session_state.results
    prefs = st.session_state.prefs
    recommended = results["recommended"]

    st.markdown(
        f'<div class="nav-bar">'
        f'<span class="nav-title">🌍 Travel Planner — Your Trip</span>'
        f'<span class="nav-user">👤 {st.session_state.username}</span></div>',
        unsafe_allow_html=True,
    )

    nc1, nc2, nc3, nc4 = st.columns([1, 1, 1, 1])
    with nc1:
        if st.button("← Edit Preferences", key="back_to_wizard"):
            st.session_state.screen = "wizard"
            st.rerun()
    with nc2:
        if st.button("🔄 Regenerate", key="regen"):
            st.session_state.rng_seed = random.randint(0, 999999)
            filtered_cities = CITIES
            region_pref = prefs.get("region_pref", [])
            if region_pref:
                filtered_cities = {k: v for k, v in CITIES.items() if v["region"] in region_pref}
            original = CITIES
            use_cities = filtered_cities if filtered_cities else original
            old_cities = globals()["CITIES"]
            globals()["CITIES"] = use_cities
            new_rec = recommend(prefs)
            globals()["CITIES"] = old_cities
            if new_rec:
                new_result = build_itinerary(new_rec, prefs)
                new_result["recommended"] = new_rec
                st.session_state.results = new_result
            st.rerun()
    with nc3:
        if st.button("💾 Save Trip", key="save_trip"):
            save_trip_for_user(st.session_state.username, {
                "prefs": prefs,
                "results": {
                    "countries": [r["country"] for r in recommended],
                    "cities": [c["name"] for ci in recommended for c in ci["cities"]],
                    "total_cost": results["total_cost"],
                    "trip_days": results["trip_days"],
                },
            })
            st.success("Trip saved!")
    with nc4:
        if st.button("🚪 Log Out", key="logout_results"):
            st.session_state.logged_in = False
            st.session_state.screen = "login"
            st.session_state.wizard_step = 1
            st.session_state.prefs = {}
            st.session_state.results = None
            st.rerun()

    st.markdown("")

    # ── Top metrics ──
    group_size = {"Solo": 1, "Couple": 2, "Group": 4, "Family": 4}.get(prefs.get("group", "Solo"), 2)
    total_cities = sum(len(c["cities"]) for c in recommended)

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{len(recommended)}</div>'
                    f'<div class="metric-lbl">Countries</div></div>', unsafe_allow_html=True)
    with mc2:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{total_cities}</div>'
                    f'<div class="metric-lbl">Cities</div></div>', unsafe_allow_html=True)
    with mc3:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{results["trip_days"]}</div>'
                    f'<div class="metric-lbl">Days</div></div>', unsafe_allow_html=True)
    with mc4:
        st.markdown(f'<div class="metric-box"><div class="metric-val">${results["total_cost"]:,}</div>'
                    f'<div class="metric-lbl">Est. Cost ({group_size}p)</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # ── Tabs ──
    tab_overview, tab_itinerary, tab_map, tab_budget = st.tabs(
        ["📋 Overview", "📅 Day-by-Day Itinerary", "🗺️ Route Map", "💰 Budget Breakdown"]
    )

    # ── Overview Tab ──
    with tab_overview:
        for country_info in recommended:
            reason = generate_country_reason(country_info, prefs)
            st.markdown(f'<div class="result-card">'
                        f'<div class="country-header">🇺🇳 {country_info["country"]}</div>'
                        f'<p style="color:#555;margin-bottom:12px;">{reason}</p>',
                        unsafe_allow_html=True)

            cols = st.columns(len(country_info["cities"]))
            for j, city in enumerate(country_info["cities"]):
                with cols[j]:
                    tags_html = "".join(
                        f'<span class="city-tag">{INTEREST_OPTIONS.get(t, t).split(" ", 1)[-1]}</span>'
                        for t in city["data"].get("tags", [])[:6]
                    )
                    highlights = " · ".join(city["data"].get("highlights", [])[:4])
                    desc = city["data"].get("description", "")[:100]
                    alloc = next((c["days_allocated"] for c in results["cities"] if c["name"] == city["name"]), "?")
                    st.markdown(
                        f'<div style="background:#f8f9fa;border-radius:12px;padding:16px;">'
                        f'<strong style="font-size:1.1rem;">{city["name"]}</strong><br>'
                        f'<span style="color:#888;font-size:0.85rem;">{alloc} days · ~${city["data"]["cost"]}/day pp</span><br>'
                        f'<div style="margin:8px 0;">{tags_html}</div>'
                        f'<span style="color:#666;font-size:0.82rem;">{highlights}</span><br>'
                        f'<span style="color:#999;font-size:0.78rem;font-style:italic;">{desc}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown('</div>', unsafe_allow_html=True)

    # ── Itinerary Tab ──
    with tab_itinerary:
        st.markdown(f"### Your {results['trip_days']}-Day Itinerary")
        current_city = None
        for day in results["itinerary"]:
            if day["city"] != current_city:
                current_city = day["city"]
                st.markdown(f"---")
                st.markdown(f"#### 📍 {current_city}, {day['country']}")

            acts_html = ""
            for a in day["activities"]:
                acts_html += (
                    f'<div class="activity-item">'
                    f'<span class="activity-time">{a["time"]}</span> {a["activity"]}'
                    f'</div>'
                )

            st.markdown(
                f'<div class="day-card">'
                f'<div class="day-title">{day["title"]}</div>'
                f'{acts_html}</div>',
                unsafe_allow_html=True,
            )

    # ── Map Tab (Animated Scattergeo) ──
    with tab_map:
        cities_list = results["cities"]
        dep_city = prefs.get("departure_city", "New York")
        dep_region = get_departure_region(dep_city)

        # Try to get departure lat/lon from hubs or default
        dep_lat, dep_lon = 40.71, -74.01  # NYC default
        dep_lookup = dep_city.strip().lower()
        for cname, cdata in CITIES.items():
            if cname.lower() == dep_lookup:
                dep_lat, dep_lon = cdata["lat"], cdata["lon"]
                break

        # Build frames for animation
        all_lats = [dep_lat] + [c["data"]["lat"] for c in cities_list]
        all_lons = [dep_lon] + [c["data"]["lon"] for c in cities_list]
        all_names = [f"🌟 {dep_city} (Departure)"] + [c["name"] for c in cities_list]
        all_countries = ["Departure"] + [c["country"] for c in cities_list]
        all_days = [0] + [c["days_allocated"] for c in cities_list]

        frames = []
        for step_idx in range(1, len(all_lats) + 1):
            # Markers up to this step
            marker_lats = all_lats[:step_idx]
            marker_lons = all_lons[:step_idx]
            marker_names = all_names[:step_idx]
            marker_sizes = []
            marker_colors = []
            for k in range(step_idx):
                if k == 0:
                    marker_sizes.append(16)
                    marker_colors.append("#FFD700")  # gold star for departure
                else:
                    marker_sizes.append(max(10, all_days[k] * 5))
                    marker_colors.append("#4361ee")

            hover_texts = []
            for k in range(step_idx):
                if k == 0:
                    hover_texts.append(f"🌟 {dep_city} (Departure)")
                else:
                    hover_texts.append(f"{all_names[k]} ({all_countries[k]})<br>{all_days[k]} days")

            frame_data = [
                go.Scattergeo(
                    lat=marker_lats, lon=marker_lons,
                    mode="markers+text",
                    marker=dict(size=marker_sizes, color=marker_colors,
                                opacity=0.9, symbol=["star" if k == 0 else "circle" for k in range(step_idx)],
                                line=dict(width=1, color="white")),
                    text=marker_names,
                    textposition="top center",
                    textfont=dict(size=10, color="#1a1a2e"),
                    hovertext=hover_texts,
                    hoverinfo="text",
                    showlegend=False,
                )
            ]

            # Lines up to this step
            if step_idx >= 2:
                for seg in range(step_idx - 1):
                    c1_country = all_countries[seg]
                    c2_country = all_countries[seg + 1]
                    same_country = (c1_country == c2_country and c1_country != "Departure")

                    frame_data.append(go.Scattergeo(
                        lat=[all_lats[seg], all_lats[seg + 1]],
                        lon=[all_lons[seg], all_lons[seg + 1]],
                        mode="lines",
                        line=dict(
                            width=2.5 if not same_country else 2,
                            color="#3498db" if not same_country else "#2ec4b6",
                            dash="dash" if not same_country else "solid",
                        ),
                        showlegend=False,
                        hoverinfo="skip",
                    ))

            frames.append(go.Frame(data=frame_data, name=str(step_idx)))

        # Initial figure (just departure)
        fig = go.Figure(
            data=frames[0].data if frames else [],
            frames=frames,
        )

        # Animation controls
        fig.update_layout(
            geo=dict(
                showframe=False, showcoastlines=True,
                coastlinecolor="rgba(0,0,0,0.15)",
                showland=True, landcolor="rgba(243,243,243,1)",
                showocean=True, oceancolor="rgba(218,232,245,1)",
                projection_type="natural earth",
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            height=550,
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "y": 1.05, "x": 0.5, "xanchor": "center",
                "buttons": [
                    {
                        "label": "▶ Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": 1000, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 500},
                        }],
                    },
                    {
                        "label": "⏸ Pause",
                        "method": "animate",
                        "args": [[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        }],
                    },
                ],
            }],
            sliders=[{
                "active": 0,
                "steps": [
                    {"args": [[str(i + 1)], {"frame": {"duration": 500, "redraw": True},
                                             "mode": "immediate",
                                             "transition": {"duration": 300}}],
                     "label": all_names[i].replace("🌟 ", "")[:15] if i < len(all_names) else "",
                     "method": "animate"}
                    for i in range(len(frames))
                ],
                "x": 0.05, "len": 0.9,
                "currentvalue": {"prefix": "Stop: ", "visible": True, "xanchor": "center"},
                "transition": {"duration": 300},
            }],
        )

        st.plotly_chart(fig, use_container_width=True)

        # Route summary with flight vs overland indicators
        st.markdown("**Your route:**")
        route_parts = []
        prev_country = "Departure"
        for c in cities_list:
            icon = "✈️" if c["country"] != prev_country else "🚌"
            route_parts.append(f"{icon} **{c['name']}** ({c['days_allocated']}d)")
            prev_country = c["country"]
        st.markdown(" → ".join(route_parts))

        st.caption("✈️ = flight between countries · 🚌 = overland within country")

    # ── Budget Tab ──
    with tab_budget:
        st.markdown("### Budget Breakdown")
        budget = prefs.get("budget", 3000)
        total = results["total_cost"]

        bc1, bc2, bc3 = st.columns(3)
        with bc1:
            st.markdown(f'<div class="budget-card"><div class="budget-amount">${budget:,}</div>'
                        f'<div class="budget-label">Your Budget</div></div>', unsafe_allow_html=True)
        with bc2:
            st.markdown(f'<div class="budget-card" style="background:linear-gradient(135deg,#2ec4b6,#20a89d);">'
                        f'<div class="budget-amount">${total:,}</div>'
                        f'<div class="budget-label">Estimated Cost</div></div>', unsafe_allow_html=True)
        with bc3:
            remaining = budget - total
            color = "linear-gradient(135deg,#28a745,#20913c)" if remaining >= 0 else "linear-gradient(135deg,#dc3545,#c82333)"
            st.markdown(f'<div class="budget-card" style="background:{color};">'
                        f'<div class="budget-amount">${remaining:,}</div>'
                        f'<div class="budget-label">{"Remaining" if remaining >= 0 else "Over Budget"}</div></div>',
                        unsafe_allow_html=True)

        st.markdown("")
        st.markdown("#### Cost per City")
        for item in results["budget_breakdown"]:
            pct = (item["total"] / max(total, 1)) * 100
            st.markdown(
                f'<div style="display:flex;align-items:center;margin-bottom:8px;">'
                f'<div style="width:160px;font-weight:600;">{item["city"]}</div>'
                f'<div style="flex:1;background:#e9ecef;border-radius:8px;height:28px;margin:0 12px;">'
                f'<div style="background:#4361ee;width:{pct:.0f}%;height:100%;border-radius:8px;'
                f'display:flex;align-items:center;padding-left:8px;color:white;font-size:0.8rem;font-weight:600;">'
                f'${item["total"]:,}</div></div>'
                f'<div style="width:120px;color:#666;font-size:0.85rem;">'
                f'{item["days"]}d × ${item["daily_pp"]}/pp</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("")
        st.caption("Estimates are for mid-range travel and cover accommodation, food, activities, and local transport. "
                   "International flights are not included.")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    init_state()

    if not st.session_state.logged_in:
        login_screen()
    elif st.session_state.screen == "wizard":
        wizard_screen()
    elif st.session_state.screen == "results":
        results_screen()
    elif st.session_state.screen == "explore":
        explore_screen()
    else:
        login_screen()


main()
