import streamlit as st
import plotly.graph_objects as go
import hashlib
import json
import os
import random
import secrets
import math
import io
from datetime import date, timedelta
from urllib.parse import quote
from cities import CITIES, TRANSPORT_ROUTES
from fpdf import FPDF

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
        "screen": "wizard",
        "wizard_step": 1,
        "prefs": {},
        "results": None,
        "rng_seed": random.randint(0, 999999),
        "surprise_result": None,
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
    # User comfort is 1-100, city comfort is 1-5. Normalize user to 1-5 scale for comparison.
    user_comfort_raw = prefs.get("comfort", 50)
    user_comfort = 1 + (user_comfort_raw - 1) * 4 / 99  # map 1-100 to 1-5
    city_comfort = city_data.get("comfort", 3)
    if city_comfort >= user_comfort:
        score += 8
    else:
        score -= (user_comfort - city_comfort) * 5

    # ── Adventure level ──
    adventure = prefs.get("adventure", 50)
    if adventure >= 70 and any(t in city_tags for t in ["hiking", "wildlife", "culture"]):
        score += 5
    if adventure <= 30 and city_comfort >= 4:
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
    lang_comfort = prefs.get("language_comfort", 50)
    country = city_data.get("country", "")
    is_english = country in ENGLISH_COUNTRIES
    if lang_comfort <= 30 and not is_english:
        score -= 8
    elif lang_comfort >= 70 and not is_english:
        score += 3  # adventurous linguist bonus

    # ── NEW: Safety match (+/- 10) ──
    safety_prio = prefs.get("safety_priority", 50)
    city_safety = city_data.get("safety", 3)
    if safety_prio >= 70 and city_safety <= 2:
        score -= 10
    elif safety_prio >= 70 and city_safety >= 4:
        score += 8
    elif safety_prio <= 30:
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
    crowd_tolerance = prefs.get("crowd_tolerance", 50)
    city_crowd = city_data.get("crowd_level", 3)
    if crowd_tolerance <= 30 and city_crowd >= 4:
        score -= 8
    elif crowd_tolerance >= 70 and city_crowd >= 4:
        score += 3

    # ── NEW: Wifi needs (+/- 8) ──
    wifi_need = prefs.get("wifi_needs", 50)
    city_wifi = city_data.get("wifi", 3)
    if wifi_need >= 70 and city_wifi <= 2:
        score -= 8
    elif wifi_need >= 70 and city_wifi >= 4:
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
    immersion = prefs.get("cultural_immersion", 50)
    if immersion >= 70 and "culture" in city_tags:
        score += 5

    # ── NEW: Shopping importance (+5) ──
    shopping = prefs.get("shopping_importance", 50)
    if shopping >= 70 and "shopping" in city_tags:
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
    religious = prefs.get("religious_interest", 50)
    if religious >= 70 and "temples" in city_tags:
        score += 5

    # ── NEW: Coast vs mountain slider ──
    coast_mountain = prefs.get("coast_vs_mountain", 50)  # 1=coast, 100=mountain
    if coast_mountain <= 30 and city_terrain in ("coastal", "island"):
        score += 5
    elif coast_mountain >= 70 and city_terrain == "mountain":
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


# ── Travel Utility Functions ──────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two lat/lon points."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def get_transport_between(city_a, city_b):
    """Look up TRANSPORT_ROUTES for a city pair, fall back to distance-based estimate."""
    route = TRANSPORT_ROUTES.get((city_a, city_b)) or TRANSPORT_ROUTES.get((city_b, city_a))
    if route:
        return route
    # Fall back: estimate from distance
    data_a = CITIES.get(city_a, {})
    data_b = CITIES.get(city_b, {})
    if not data_a or not data_b:
        return {"mode": "flight", "name": "Flight", "duration": 3, "cost": 150, "notes": "Estimated"}
    dist = haversine(data_a["lat"], data_a["lon"], data_b["lat"], data_b["lon"])
    same_country = data_a.get("country") == data_b.get("country")
    if dist < 300 and same_country:
        return {"mode": "bus", "name": "Bus/Train", "duration": round(dist / 80, 1), "cost": round(dist * 0.08), "notes": "Estimated overland"}
    elif dist < 800:
        return {"mode": "train", "name": "Train/Bus", "duration": round(dist / 120, 1), "cost": round(dist * 0.1), "notes": "Estimated"}
    else:
        return {"mode": "flight", "name": "Flight", "duration": round(1.5 + dist / 800, 1), "cost": round(50 + dist * 0.06), "notes": "Estimated flight"}


def generate_flight_search_url(departure, destination, date_str):
    """Generate a Google Flights search URL."""
    return f"https://www.google.com/travel/flights?q=flights+from+{quote(departure)}+to+{quote(destination)}+on+{date_str}"


def generate_hotel_search_urls(city, country, checkin, checkout):
    """Generate Booking.com and Airbnb search URLs for a city."""
    booking_url = f"https://www.booking.com/searchresults.html?ss={quote(city + ', ' + country)}&checkin={checkin}&checkout={checkout}"
    airbnb_url = f"https://www.airbnb.com/s/{quote(city + '--' + country)}/homes?checkin={checkin}&checkout={checkout}"
    return {"booking": booking_url, "airbnb": airbnb_url}


def generate_packing_list(cities_data, trip_days, interests):
    """Generate a smart packing list based on destinations and activities."""
    weathers = set()
    terrains = set()
    has_beach = False
    has_hiking = False
    has_nightlife = False
    has_temples = False
    for c in cities_data:
        d = c.get("data", c)
        weathers.add(d.get("weather", "mild"))
        terrains.add(d.get("terrain", "urban"))
        if d.get("beach_type", "none") != "none":
            has_beach = True
    for tag in interests:
        if tag == "hiking":
            has_hiking = True
        if tag == "nightlife":
            has_nightlife = True
        if tag == "temples":
            has_temples = True

    packing = {
        "Essentials": [
            "Passport (+ copies)", "Travel insurance docs", "Phone + charger",
            "Power adapter", "Wallet / travel cards", "Medications",
            "Copies of reservations", "Pen (for customs forms)",
        ],
        "Clothing": [
            f"Underwear ({min(trip_days, 7)} pairs)",
            f"Socks ({min(trip_days, 7)} pairs)",
            f"T-shirts/tops ({min(trip_days, 5)})",
            "Pants/shorts (2-3)", "Light jacket or hoodie",
            "Sleepwear",
        ],
        "Toiletries": [
            "Toothbrush + toothpaste", "Deodorant", "Sunscreen",
            "Shampoo (travel size)", "Any prescriptions",
        ],
        "Tech": [
            "Phone + charger", "Portable battery pack",
            "Headphones", "Camera (optional)",
        ],
    }

    # Weather-based additions
    if "tropical" in weathers or "hot" in weathers:
        packing["Clothing"].extend(["Breathable shorts", "Sun hat", "Sandals"])
        packing["Essentials"].append("Insect repellent")
    if "cold" in weathers or "snowy" in weathers:
        packing["Clothing"].extend(["Warm coat", "Gloves", "Scarf", "Thermal base layer"])
    if "rainy" in weathers:
        packing["Essentials"].append("Compact umbrella or rain jacket")
    if any(w in weathers for w in ["mild", "warm", "temperate", "mediterranean"]):
        packing["Clothing"].append("Light layers for evening")

    # Activity-based
    if has_beach:
        packing.setdefault("Beach & Water", []).extend(["Swimsuit", "Quick-dry towel", "Reef-safe sunscreen", "Waterproof phone pouch"])
    if has_hiking:
        packing.setdefault("Hiking & Outdoors", []).extend(["Hiking shoes/boots", "Daypack", "Water bottle", "First aid kit", "Rain layer"])
    if has_nightlife:
        packing["Clothing"].append("One nice outfit for going out")
    if has_temples:
        packing["Clothing"].extend(["Modest clothing (covers shoulders/knees)", "Scarf or shawl"])

    # Trip length adjustments
    if trip_days > 14:
        packing["Essentials"].append("Laundry bag + travel detergent")

    return packing


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
    transport_legs = []  # transport info between cities
    day_counter = 1

    for i, city in enumerate(all_cities):
        city_data = city["data"]
        city_name = city["name"]
        structured = city_data.get("structured_activities", [])
        used = set()

        # Build activity pool — prefer structured activities with real details
        if structured:
            # Filter by user interest tags for relevance
            time_map = {"morning": "Morning", "afternoon": "Afternoon", "evening": "Evening", "full_day": "Morning"}
            tagged = [a for a in structured if any(t in a.get("tags", []) for t in user_tags)]
            untagged = [a for a in structured if a not in tagged]
            ordered = tagged + untagged  # relevant ones first
            pool = []
            for a in ordered:
                pool.append({
                    "activity": a["name"],
                    "address": a.get("address", ""),
                    "hours": a.get("hours", ""),
                    "cost": a.get("cost", ""),
                    "maps_url": a.get("maps_url", ""),
                    "description": a.get("description", ""),
                    "time_of_day": time_map.get(a.get("time_of_day", "morning"), "Morning"),
                    "structured": True,
                })
        else:
            # Fall back to template-based activities
            pool = []
            highlights = list(city_data.get("highlights", []))
            for h in highlights:
                pool.append({"activity": h, "structured": False})
            for tag in user_tags:
                if tag in city_data.get("tags", []):
                    for act in ACTIVITY_TEMPLATES.get(tag, []):
                        pool.append({"activity": act.format(city=city_name), "structured": False})
            pool.extend([
                {"activity": f"Explore {city_name}'s neighborhoods on foot", "structured": False},
                {"activity": f"Relax at a local café in {city_name}", "structured": False},
                {"activity": f"Free time to wander and discover {city_name}", "structured": False},
            ])

        for d in range(city["days_allocated"]):
            day_activities = []
            times = ["Morning", "Midday", "Afternoon", "Evening", "Night"][:activities_per_day]

            for t in times:
                picked = None
                for act in pool:
                    act_key = act["activity"]
                    if act_key not in used:
                        picked = dict(act)
                        picked["time"] = t
                        used.add(act_key)
                        break
                if not picked:
                    picked = {"time": t, "activity": f"Free time in {city_name}", "structured": False}
                day_activities.append(picked)

            title = f"Day {day_counter}: {city_name}"
            is_travel_day = False
            if d == 0 and i == 0:
                title += " — Arrival"
            elif d == 0 and i > 0:
                title += " — Travel Day"
                is_travel_day = True
            elif d == city["days_allocated"] - 1 and i == len(all_cities) - 1:
                title += " — Final Day"

            day_entry = {
                "day": day_counter,
                "title": title,
                "city": city_name,
                "country": city["country"],
                "activities": day_activities,
            }

            # Add transport info on travel days
            if is_travel_day and i > 0:
                prev_city = all_cities[i - 1]["name"]
                transport = get_transport_between(prev_city, city_name)
                day_entry["transport"] = {
                    "from": prev_city,
                    "to": city_name,
                    **transport,
                }
                transport_legs.append(day_entry["transport"])

            itinerary.append(day_entry)
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

    # Add transport costs to total
    transport_total = sum(t.get("cost", 0) for t in transport_legs)
    total_cost += transport_total * group_size

    return {
        "itinerary": itinerary,
        "cities": all_cities,
        "budget_breakdown": budget_breakdown,
        "total_cost": total_cost,
        "trip_days": trip_days,
        "transport_legs": transport_legs,
    }


def build_single_city_itinerary(city_name, city_data, trip_days=10):
    """Build a sample itinerary for a single city, reusing build_itinerary()."""
    recommended = [{
        "country": city_data["country"],
        "region": city_data["region"],
        "score": 100,
        "cities": [{"name": city_name, "data": city_data, "score": 100}],
    }]
    prefs = {
        "days": trip_days,
        "interests": city_data.get("tags", [])[:5],
        "group": "Solo",
        "pace": "Moderate",
        "budget": 3000,
        "departure_city": "",
    }
    return build_itinerary(recommended, prefs)


# Fun facts for cities (fallback generates from description)
CITY_FUN_FACTS = {
    "Tokyo": "Tokyo has more Michelin-starred restaurants than any other city in the world.",
    "Kyoto": "Kyoto has over 2,000 temples and shrines — more than you could visit in a lifetime.",
    "Osaka": "Osaka is called 'Japan's Kitchen' — locals greet each other with 'have you eaten yet?'",
    "Hiroshima": "Hiroshima rebuilt itself from total devastation and is now a UNESCO City of Peace.",
    "Nara": "Over 1,200 wild deer roam freely through Nara — they're considered sacred messengers of the gods.",
    "Hakone": "On clear days, Hakone offers picture-perfect views of Mount Fuji reflected in Lake Ashi.",
    "Sapporo": "Sapporo's Snow Festival attracts over 2 million visitors to see massive snow and ice sculptures.",
    "Bangkok": "Bangkok's full ceremonial name is 168 letters long — the longest city name in the world.",
    "Chiang Mai": "Chiang Mai has over 300 Buddhist temples within the city and surrounding area.",
    "Bali": "Bali has more than 20,000 temples — there's at least one in every home and village.",
    "Seoul": "Seoul's subway system is one of the most advanced in the world, with heated seats and free wifi.",
    "Delhi": "Delhi's Qutub Minar is the tallest brick minaret in the world at 73 meters.",
    "Hanoi": "Hanoi's Old Quarter streets are named after the goods historically sold on them.",
    "Ho Chi Minh City": "Over 5 million motorbikes navigate Ho Chi Minh City's streets every day.",
    "Paris": "The Eiffel Tower was supposed to be temporary — it was meant to be dismantled after 20 years.",
    "Rome": "Rome's Trevi Fountain collects about $1.5 million in coins every year, donated to charity.",
    "Florence": "Florence's Duomo was the largest dome in the world for over 500 years.",
    "Barcelona": "Gaudi's Sagrada Familia has been under construction since 1882 — over 140 years.",
    "London": "The London Underground is the oldest subway system in the world, opened in 1863.",
    "Istanbul": "Istanbul is the only city in the world that spans two continents — Europe and Asia.",
    "Marrakech": "Marrakech's Jemaa el-Fnaa square transforms every night into an open-air restaurant for thousands.",
    "Cape Town": "Table Mountain is one of the oldest mountains on Earth — roughly 600 million years old.",
    "Cusco": "Cusco sits at 3,400m elevation — it takes a day or two to adjust to the thin air.",
    "Mexico City": "Mexico City is slowly sinking — it's built on a drained lakebed and sinks up to 50cm per year.",
    "Sydney": "Sydney Harbour Bridge is nicknamed 'The Coathanger' by locals due to its arch shape.",
    "Rio de Janeiro": "Christ the Redeemer's arms stretch 28 meters wide — like giving the city a giant hug.",
    "Buenos Aires": "Buenos Aires has the widest avenue in the world — 9 de Julio Avenue has 16 lanes.",
    "Santorini": "Santorini is actually the rim of a massive volcanic caldera that erupted 3,600 years ago.",
    "Amsterdam": "Amsterdam has more bicycles than people — roughly 881,000 bikes for 821,000 residents.",
    "Prague": "Prague Castle is the largest ancient castle complex in the world at 70,000 square meters.",
    "Budapest": "Budapest has the largest thermal water cave system in the world beneath the city.",
    "Lisbon": "Lisbon is one of the oldest cities in Europe — older than Rome by several centuries.",
    "Berlin": "Berlin has more bridges than Venice — roughly 960 compared to Venice's 400.",
    "Dubrovnik": "Dubrovnik's city walls are nearly 2km long and up to 25 meters high.",
    "Medellin": "Medellin went from one of the most dangerous cities to winning 'Most Innovative City' in 2013.",
    "Petra": "Petra was lost to the Western world for nearly 500 years until rediscovered in 1812.",
    "Reykjavik": "Reykjavik is powered almost entirely by geothermal energy from underground hot springs.",
    "Singapore": "Singapore is both a city AND a country — one of only three city-states in the world.",
    "Hong Kong": "Hong Kong has more skyscrapers than any other city on Earth — over 480.",
    "Dubai": "Dubai's Burj Khalifa is so tall that you can watch the sunset twice — once from the base and again from the top.",
    "Machu Picchu": "Machu Picchu was built without mortar — the stones fit together so tightly that a knife blade can't fit between them.",
    "Venice": "Venice is built on 118 small islands connected by over 400 bridges.",
    "Cappadocia": "Cappadocia's underground cities could shelter up to 20,000 people and their livestock.",
    "Galapagos": "The Galapagos tortoise can live over 175 years — the longest of any vertebrate.",
    "Zanzibar": "Zanzibar was once the world's largest producer of cloves — you can still smell them in the air.",
    "Siem Reap": "Angkor Wat is the largest religious monument ever built — it covers 162.6 hectares.",
    "Luang Prabang": "Every morning at dawn, hundreds of monks walk the streets collecting alms in an unbroken tradition.",
    "Varanasi": "Varanasi is believed to be one of the oldest continuously inhabited cities, possibly 5,000 years old.",
    "Queenstown": "Queenstown is the birthplace of commercial bungee jumping — it started here in 1988.",
    "Bruges": "Bruges has an underground pipeline that carries beer 3km from the brewery to the bottling plant.",
    "Tbilisi": "Georgia is one of the oldest winemaking regions on Earth — they've been making wine for 8,000 years.",
    "Uyuni": "Bolivia's Salar de Uyuni is so flat that it's used to calibrate satellites from space.",
    "Atacama": "Parts of the Atacama Desert haven't seen rain in over 500 years.",
    "Torres del Paine": "The granite towers of Torres del Paine took 12 million years to form.",
    "Chefchaouen": "Nobody knows for sure why Chefchaouen is painted blue — theories range from mosquito repellent to spiritual tradition.",
    "Hoi An": "On the 14th day of each lunar month, Hoi An turns off its electric lights and glows with lanterns only.",
    "Bagan": "Bagan once had over 10,000 temples — about 2,200 still survive across the ancient plain.",
    "Fes": "The tanneries of Fes have been operating the same way for nearly 1,000 years.",
    "Jaipur": "Jaipur was painted pink in 1876 to welcome Prince Albert — and the color stuck.",
    "Udaipur": "Udaipur's Lake Palace appears to float on the water and was used as a James Bond filming location.",
    "Krakow": "A trumpet call plays from Krakow's St. Mary's Church tower every hour — and stops mid-note, honoring a 13th-century watchman shot by invaders.",
    "Valletta": "Valletta is the smallest national capital in the EU — you can walk across it in about 15 minutes.",
    "Colombo": "Sri Lanka is one of the world's largest tea producers — try a cup of fresh Ceylon tea.",
    "Kathmandu": "Kathmandu Valley has 7 UNESCO World Heritage Sites in an area smaller than most cities.",
    "La Paz": "La Paz has the highest commercial airport in the world at over 4,000 meters elevation.",
    "Oaxaca": "Oaxaca has more varieties of mole sauce than anywhere else — at least 7 distinct types.",
    "Tulum": "Tulum's cliff-top Mayan ruins are one of the last cities built by the Maya, dating to around 1200 AD.",
    "Rotorua": "Rotorua smells like sulfur due to its geothermal activity — locals call it 'Sulphur City.'",
    "Serengeti": "The Great Migration sees over 1.5 million wildebeest cross the Serengeti every year.",
    "Cairo": "The Great Pyramid of Giza was the tallest man-made structure for over 3,800 years.",
    "Luxor": "Luxor contains roughly one-third of all the world's ancient monuments.",
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
    .detail-panel {
        background: white; border-radius: 16px; padding: 28px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07); margin-top: 16px;
    }
    .detail-panel h3 { color: #1a1a2e; font-size: 1.5rem; margin-bottom: 4px; }
    .detail-panel h4 { color: #4361ee; font-size: 1.05rem; margin: 18px 0 8px; font-weight: 600; }
    .neighborhood-item {
        background: #f0f4ff; border-radius: 10px; padding: 10px 14px;
        margin-bottom: 6px; font-size: 0.92rem; color: #333;
        border-left: 3px solid #4361ee;
    }
    .activity-rank {
        display: flex; align-items: center; padding: 6px 0;
        border-bottom: 1px solid #f0f0f0; font-size: 0.92rem;
    }
    .activity-number {
        background: #4361ee; color: white; border-radius: 50%;
        width: 24px; height: 24px; display: inline-flex;
        align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 700; margin-right: 10px; flex-shrink: 0;
    }
    .food-drink-item {
        display: inline-block; background: #fff3e0; color: #e65100;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem;
        margin: 3px 4px; font-weight: 500;
    }
    .drink-item {
        display: inline-block; background: #e8f5e9; color: #2e7d32;
        padding: 4px 12px; border-radius: 20px; font-size: 0.82rem;
        margin: 3px 4px; font-weight: 500;
    }
    .cost-stat {
        background: #f8f9fa; border-radius: 12px; padding: 14px;
        text-align: center;
    }
    .cost-stat .val { font-size: 1.4rem; font-weight: 700; color: #4361ee; }
    .cost-stat .lbl { font-size: 0.78rem; color: #888; }
    .visa-badge {
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        font-size: 0.82rem; font-weight: 600; margin: 2px 4px;
    }
    .visa-free { background: #d4edda; color: #155724; }
    .visa-arrival { background: #fff3cd; color: #856404; }
    .visa-evisa { background: #ffe0b2; color: #e65100; }
    .visa-embassy { background: #f8d7da; color: #721c24; }
    .transport-card {
        background: linear-gradient(135deg, #f0f4ff, #e8f4f8); border-radius: 12px;
        padding: 14px 18px; margin: 8px 0; border-left: 4px solid #2ec4b6;
        display: flex; align-items: center; gap: 12px;
    }
    .transport-icon { font-size: 1.5rem; }
    .transport-details { flex: 1; }
    .transport-details .route { font-weight: 600; color: #1a1a2e; font-size: 0.95rem; }
    .transport-details .info { color: #666; font-size: 0.85rem; }
    .practical-card {
        background: white; border-radius: 12px; padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 12px;
    }
    .practical-card h4 { color: #1a1a2e; margin: 0 0 10px; font-size: 1.1rem; }
    .practical-item {
        display: flex; justify-content: space-between; padding: 6px 0;
        border-bottom: 1px solid #f0f0f0; font-size: 0.9rem;
    }
    .practical-item .label { color: #888; font-weight: 500; }
    .practical-item .value { color: #333; font-weight: 600; }
    .packing-category {
        background: #f8f9fa; border-radius: 12px; padding: 16px;
        margin-bottom: 12px;
    }
    .packing-category h4 { color: #4361ee; margin: 0 0 10px; font-size: 1rem; }
    .activity-details {
        background: #f8f9fa; border-radius: 10px; padding: 10px 14px;
        margin: 4px 0; border-left: 3px solid #4361ee;
    }
    .activity-details .act-name { font-weight: 600; color: #1a1a2e; font-size: 0.92rem; }
    .activity-details .act-meta { color: #666; font-size: 0.8rem; margin-top: 2px; }
    .maps-link {
        color: #4361ee; text-decoration: none; font-size: 0.8rem; font-weight: 500;
    }
    .maps-link:hover { text-decoration: underline; }
    .search-link-btn {
        display: inline-block; padding: 6px 16px; border-radius: 8px;
        font-size: 0.85rem; font-weight: 600; text-decoration: none;
        margin: 4px 6px 4px 0;
    }
    .flight-link { background: #e3f2fd; color: #1565c0; }
    .hotel-link { background: #fff3e0; color: #e65100; }
    .airbnb-link { background: #fce4ec; color: #c62828; }
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
        '<div class="nav-bar">'
        '<span class="nav-title">🌍 Travel Planner</span></div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("🗺️ Skip to Explore Map", key="explore_bypass"):
            st.session_state.screen = "explore"
            st.rerun()
    with c3:
        if st.button("🧰 Tools", key="to_tools_wizard"):
            st.session_state.screen = "tools"
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
        budget = st.slider("Total budget (USD)", 500, 50000, prefs.get("budget", 3000), step=250,
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
        adventure = st.slider("Adventure level", 1, 100, prefs.get("adventure", 50),
                              help="1 = Very relaxed, stick to tourist areas · 100 = Off the beaten path, thrill-seeking")
        adv_label = "Very chill" if adventure <= 20 else "Easygoing" if adventure <= 40 else "Balanced" if adventure <= 60 else "Adventurous" if adventure <= 80 else "Full send"
        st.caption(f"You selected: **{adv_label}**")

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

        religious = st.slider("Interest in religious/spiritual sites", 1, 100,
                              prefs.get("religious_interest", 50),
                              help="1 = Not interested · 100 = Very interested")

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

        comfort = st.slider("Accommodation preference", 1, 100, prefs.get("comfort", 50),
                            help="1 = Hostels & basic guesthouses · 100 = Luxury hotels & resorts")
        comfort_label = "Hostels & dorms" if comfort <= 20 else "Budget guesthouses" if comfort <= 40 else "Nice hotels" if comfort <= 60 else "Boutique / upper-mid" if comfort <= 80 else "Luxury resorts"
        st.caption(f"You selected: **{comfort_label}**")

        transport = st.radio("Transport preference",
                             ["Local buses & trains", "Mix of local and private", "Private / taxi"],
                             index=["Local buses & trains", "Mix of local and private", "Private / taxi"]
                             .index(prefs.get("transport", "Mix of local and private")),
                             horizontal=True)

        food_adventure = st.slider("Food adventurousness", 1, 100, prefs.get("food_adventure", 50),
                                   help="1 = Familiar food only · 100 = I'll eat anything from a street cart")
        food_label = "Stick to what I know" if food_adventure <= 20 else "Mildly curious" if food_adventure <= 40 else "Open to trying things" if food_adventure <= 60 else "Adventurous eater" if food_adventure <= 80 else "Feed me anything"
        st.caption(f"You selected: **{food_label}**")

        dietary_options = ["vegetarian", "vegan", "halal", "kosher", "gluten_free"]
        dietary_labels = {"vegetarian": "Vegetarian", "vegan": "Vegan", "halal": "Halal",
                          "kosher": "Kosher", "gluten_free": "Gluten-free"}
        saved_dietary = prefs.get("dietary_restrictions", [])
        dietary = st.multiselect("Dietary restrictions",
                                  options=dietary_options,
                                  format_func=lambda x: dietary_labels[x],
                                  default=saved_dietary)

        wifi = st.slider("Internet / wifi needs", 1, 100, prefs.get("wifi_needs", 50),
                         help="1 = Don't need it · 100 = Must have reliable wifi")

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

        coast_mountain = st.slider("Coast vs Mountain", 1, 100, prefs.get("coast_vs_mountain", 50),
                                   help="1 = Prefer coast & beaches · 100 = Prefer mountains & highlands")
        cm_label = "Coast lover" if coast_mountain <= 20 else "Leaning coastal" if coast_mountain <= 40 else "Both are great" if coast_mountain <= 60 else "Leaning mountains" if coast_mountain <= 80 else "Mountain lover"
        st.caption(f"You selected: **{cm_label}**")

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

        lang_comfort = st.slider("Language barrier comfort", 1, 100,
                                 prefs.get("language_comfort", 50),
                                 help="1 = Only go where English is spoken · 100 = Love learning new languages")

        immersion = st.slider("Cultural immersion level", 1, 100,
                              prefs.get("cultural_immersion", 50),
                              help="1 = Tourist-friendly spots · 100 = Live like a local")

        night_options = ["not_important", "nice_to_have", "important", "essential"]
        night_labels = {"not_important": "Not important", "nice_to_have": "Nice to have",
                        "important": "Important", "essential": "Essential"}
        saved_night = prefs.get("nightlife_importance", "nice_to_have")
        nightlife = st.radio("Nightlife importance",
                             options=night_options,
                             format_func=lambda x: night_labels[x],
                             index=night_options.index(saved_night),
                             horizontal=True)

        crowd_tolerance = st.slider("Crowd / tourist tolerance", 1, 100,
                                    prefs.get("crowd_tolerance", 50),
                                    help="1 = Avoid crowds at all costs · 100 = Don't mind tourist hotspots")

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

        safety = st.slider("Safety priority", 1, 100, prefs.get("safety_priority", 50),
                           help="1 = I'm comfortable anywhere · 100 = Safety is my top priority")

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

        shopping = st.slider("Shopping importance", 1, 100, prefs.get("shopping_importance", 50),
                             help="1 = Not interested · 100 = Shopping is a big part of my trip")

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


# ── City Detail View ──────────────────────────────────────────────────────────
def render_city_detail(city_name, city_data, context="explore", prefs=None, trip_days=None):
    """Render a rich detail panel for a city. Used by both explore and results screens."""
    country = city_data.get("country", "")
    desc = city_data.get("description", "A great destination")
    safety = city_data.get("safety", 3)
    language = city_data.get("language", "Local")
    uber = city_data.get("uber_cost", 8)
    airbnb = city_data.get("airbnb_cost", 60)
    neighborhoods = city_data.get("neighborhoods", [])
    activities = city_data.get("top_activities", [])
    local_food = city_data.get("local_food", [])
    local_drink = city_data.get("local_drink", [])
    things = city_data.get("things_to_do", [])
    best_months_nums = city_data.get("months", [])
    festivals = city_data.get("festivals", [])
    cost_pp = city_data.get("cost", 100)

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    best_months = ", ".join(month_names[m - 1] for m in best_months_nums)
    safety_stars = "★" * safety + "☆" * (5 - safety)

    st.markdown(f'<div class="detail-panel">', unsafe_allow_html=True)

    # Header
    st.markdown(f'<h3>📍 {city_name}, {country}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#555;margin-top:0;">{desc}</p>', unsafe_allow_html=True)

    # Quick stats row
    st.markdown(
        f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin:12px 0;">'
        f'<div class="cost-stat"><div class="val">{safety_stars}</div><div class="lbl">Safety</div></div>'
        f'<div class="cost-stat"><div class="val">{language}</div><div class="lbl">Language</div></div>'
        f'<div class="cost-stat"><div class="val">${uber}</div><div class="lbl">Avg Uber Ride</div></div>'
        f'<div class="cost-stat"><div class="val">${airbnb}/n</div><div class="lbl">Avg Airbnb</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Neighborhoods
    if neighborhoods:
        st.markdown('<h4>🏘️ Top Neighborhoods</h4>', unsafe_allow_html=True)
        for i, n in enumerate(neighborhoods, 1):
            st.markdown(f'<div class="neighborhood-item"><strong>{i}.</strong> {n}</div>', unsafe_allow_html=True)

    # Top 10 Activities
    if activities:
        st.markdown('<h4>🏆 Top 10 Activities</h4>', unsafe_allow_html=True)
        acts_html = ""
        for i, a in enumerate(activities[:10], 1):
            acts_html += f'<div class="activity-rank"><span class="activity-number">{i}</span> {a}</div>'
        st.markdown(acts_html, unsafe_allow_html=True)

    # Things to Do
    if things:
        st.markdown('<h4>📋 Things To Do</h4>', unsafe_allow_html=True)
        for t in things:
            st.markdown(f'- {t}')

    # Cost summary
    st.markdown('<h4>💰 Cost Summary</h4>', unsafe_allow_html=True)
    daily_total = cost_pp + uber + (airbnb if airbnb else 0)
    st.markdown(
        f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">'
        f'<div class="cost-stat"><div class="val">${cost_pp}</div><div class="lbl">Daily Budget / Person</div></div>'
        f'<div class="cost-stat"><div class="val">${uber}</div><div class="lbl">Avg Uber Ride</div></div>'
        f'<div class="cost-stat"><div class="val">${airbnb}</div><div class="lbl">Airbnb / Night</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Local Flavors spotlight + fun fact
    st.markdown('<h4>🍽️ Local Flavors</h4>', unsafe_allow_html=True)
    flavors_html = ""
    for f in local_food:
        flavors_html += f'<span class="food-drink-item">{f}</span>'
    for d in local_drink:
        flavors_html += f'<span class="drink-item">{d}</span>'
    st.markdown(f'<div style="margin-bottom:12px;">{flavors_html}</div>', unsafe_allow_html=True)

    # Fun fact
    fun_fact = CITY_FUN_FACTS.get(city_name)
    if not fun_fact:
        fun_fact = f"{city_name} is a unique destination in {country} — explore it and make your own discoveries."
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#f0f4ff,#e8eeff);border-radius:12px;'
        f'padding:14px 18px;margin:10px 0;border-left:4px solid #4361ee;">'
        f'<strong>🎲 Fun Fact:</strong> {fun_fact}</div>',
        unsafe_allow_html=True,
    )

    # Best months
    st.markdown(f'<div style="margin:8px 0;color:#555;"><strong>📅 Best months to visit:</strong> {best_months}</div>',
                unsafe_allow_html=True)

    # Sample itinerary (explore context only)
    if context == "explore":
        st.markdown('<h4>📅 Sample 10-Day Itinerary</h4>', unsafe_allow_html=True)
        sample = build_single_city_itinerary(city_name, city_data, trip_days=10)
        for day in sample["itinerary"]:
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
        st.markdown(
            f'<div style="background:#f0f4ff;border-radius:12px;padding:16px;margin-top:12px;">'
            f'<strong>Estimated 10-day budget (solo):</strong> '
            f'~<strong style="color:#4361ee;font-size:1.2rem;">${sample["total_cost"]:,}</strong>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Results-only section: why recommended + budget estimate
    if context == "results" and prefs:
        st.markdown('<h4>🎯 Why We Recommended This City</h4>', unsafe_allow_html=True)
        _render_match_breakdown(city_name, city_data, prefs)

        if trip_days:
            group_size = {"Solo": 1, "Couple": 2, "Group": 4, "Family": 4}.get(prefs.get("group", "Solo"), 2)
            est_total = (cost_pp + airbnb) * trip_days + uber * trip_days * 0.5
            est_group = est_total * group_size
            st.markdown(
                f'<div style="background:#f0f4ff;border-radius:12px;padding:16px;margin-top:12px;">'
                f'<strong>Trip Budget Estimate ({trip_days} days, {group_size} people):</strong> '
                f'~<strong style="color:#4361ee;font-size:1.2rem;">${est_group:,.0f}</strong> total '
                f'(${est_total:,.0f} per person)'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)


def _render_match_breakdown(city_name, city_data, prefs):
    """Show human-readable reasons why this city was recommended."""
    reasons = []
    city_tags = city_data.get("tags", [])
    user_tags = prefs.get("interests", [])

    # Interest matches
    matches = set(user_tags) & set(city_tags)
    if matches:
        labels = [INTEREST_OPTIONS.get(t, t).split(" ", 1)[-1] for t in matches]
        reasons.append(f"Matches your interests: {', '.join(labels)}")

    # Budget fit
    trip_days = prefs.get("days", 10)
    group_size = {"Solo": 1, "Couple": 2, "Group": 4, "Family": 4}.get(prefs.get("group", "Solo"), 2)
    daily_budget = (prefs.get("budget", 3000) * 0.70) / max(trip_days, 1) / max(group_size, 1)
    city_cost = city_data.get("cost", 100)
    if city_cost <= daily_budget:
        reasons.append(f"Fits your budget (${city_cost}/day vs ${daily_budget:.0f}/day available)")
    elif city_cost <= daily_budget * 1.2:
        reasons.append(f"Close to budget (${city_cost}/day, slightly above ${daily_budget:.0f}/day)")

    # Weather match
    travel_month = prefs.get("travel_month")
    if travel_month and travel_month in city_data.get("months", []):
        month_name = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][travel_month - 1]
        reasons.append(f"Great weather in {month_name}")

    # Safety
    if prefs.get("safety_priority", 50) >= 70 and city_data.get("safety", 3) >= 4:
        reasons.append(f"High safety rating ({city_data['safety']}/5)")

    # Must-have experiences
    for exp in prefs.get("must_have_experiences", []):
        if city_name in EXPERIENCE_CITIES.get(exp, []):
            reasons.append(f"Top destination for {exp.replace('_', ' ')}")

    if not reasons:
        reasons.append("Strong overall match for your travel preferences")

    for r in reasons:
        st.markdown(f'✅ {r}')


# ── Explore Map Screen ─────────────────────────────────────────────────────────
def explore_screen():
    st.markdown(
        '<div class="nav-bar">'
        '<span class="nav-title">🌍 Explore the World</span></div>',
        unsafe_allow_html=True,
    )

    nc1, nc2, nc3 = st.columns([1, 1, 1])
    with nc1:
        if st.button("← Back to Wizard", key="back_to_wizard_explore"):
            st.session_state.screen = "wizard"
            st.rerun()
    with nc2:
        if st.button("🧰 Tools", key="to_tools_explore"):
            st.session_state.screen = "tools"
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
        render_city_detail(selected_city, data, context="explore")

        # ── Quick-plan section ────────────────────────────────────────────
        st.markdown("---")
        st.markdown(f"### ✈️ Plan a Trip to {selected_city}")

        qp1, qp2 = st.columns(2)
        with qp1:
            departure_city = st.text_input(
                "Departure city",
                value=st.session_state.get("explore_departure", ""),
                placeholder="e.g. New York, London, Tokyo…",
                key="explore_departure_input",
            )
        with qp2:
            trip_days = st.number_input(
                "Trip length (days)", min_value=3, max_value=30, value=10,
                key="explore_trip_days",
            )

        # Auto multi-country for 10+ days
        multi_country = trip_days > 10

        if st.button(
            f"🗺️ Plan a {trip_days}-day trip to {selected_city}!",
            key="plan_trip_explore",
            type="primary",
        ):
            # Build default preferences
            quick_prefs = {
                "days": trip_days,
                "budget": 3000,
                "group": "Solo",
                "pace": "Moderate",
                "interests": data.get("tags", [])[:5],
                "departure_city": departure_city.strip(),
                "region_pref": [data["region"]],
                "multi_country": multi_country,
                "safety_priority": 50,
                "travel_month": None,
                "must_have_experiences": [],
            }
            st.session_state.prefs = quick_prefs

            # Build recommended list — single city or multi via recommend()
            if multi_country:
                # Use the full recommend engine so it picks nearby countries
                recommended = recommend(quick_prefs)
                # Make sure our selected city is included
                found = False
                for grp in recommended:
                    for c in grp["cities"]:
                        if c["name"] == selected_city:
                            found = True
                            break
                if not found and recommended:
                    recommended[0]["cities"].insert(0, {
                        "name": selected_city,
                        "data": data,
                        "score": 100,
                    })
            else:
                recommended = [{
                    "country": data["country"],
                    "region": data["region"],
                    "score": 100,
                    "cities": [{"name": selected_city, "data": data, "score": 100}],
                }]

            results = build_itinerary(recommended, quick_prefs)
            results["recommended"] = recommended
            st.session_state.results = results
            st.session_state.screen = "results"
            st.rerun()


# ── PDF Export ─────────────────────────────────────────────────────────────────
def _pdf_safe(text):
    """Strip non-latin1 characters for PDF rendering."""
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " ",
        "\u2022": "*", "\u2192": "->", "\u2190": "<-",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def generate_pdf_itinerary(results, prefs):
    """Generate a PDF itinerary using fpdf2."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Title Page ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 40, "", ln=True)
    pdf.cell(0, 15, "Your Travel Itinerary", ln=True, align="C")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(100, 100, 100)
    dep_city = prefs.get("departure_city", "New York")
    cities_str = " > ".join(c["name"] for c in results["cities"])
    pdf.cell(0, 10, _pdf_safe(f"From {dep_city}"), ln=True, align="C")
    pdf.cell(0, 8, _pdf_safe(cities_str), ln=True, align="C")
    pdf.cell(0, 8, f'{results["trip_days"]} days | Est. ${results["total_cost"]:,}', ln=True, align="C")
    start_date = prefs.get("start_date", date.today() + timedelta(days=30))
    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)
    end_date = start_date + timedelta(days=results["trip_days"])
    pdf.cell(0, 8, f'{start_date.strftime("%B %d, %Y")} - {end_date.strftime("%B %d, %Y")}', ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    # ── Trip Overview ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Trip Overview", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.ln(4)

    recommended = results.get("recommended", [])
    for country_info in recommended:
        country = country_info["country"]
        sample = country_info["cities"][0]["data"]
        visa = sample.get("visa_status", "unknown").replace("_", " ").title()
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, _pdf_safe(f"{country} - {visa}"), ln=True)
        pdf.set_font("Helvetica", "", 10)
        for city in country_info["cities"]:
            alloc = next((c["days_allocated"] for c in results["cities"] if c["name"] == city["name"]), "?")
            pdf.cell(0, 7, _pdf_safe(f"  {city['name']} - {alloc} days (~${city['data']['cost']}/day pp)"), ln=True)
        pdf.ln(3)

    # ── Day-by-Day ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Day-by-Day Itinerary", ln=True)
    pdf.ln(4)

    for day in results["itinerary"]:
        if "transport" in day:
            t = day["transport"]
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 7, _pdf_safe(f"  >> {t.get('name', t['mode'])} from {t['from']} to {t['to']} "
                     f"(~{t.get('duration', '?')}h, ~${t.get('cost', '?')})"), ln=True)
            pdf.set_text_color(0, 0, 0)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 9, _pdf_safe(day["title"]), ln=True)
        pdf.set_font("Helvetica", "", 10)

        for a in day["activities"]:
            activity_text = a.get("activity", "")
            if a.get("structured"):
                line = f"  {a['time']}: {activity_text}"
                if a.get("address"):
                    line += f" [{a['address']}]"
                if a.get("cost"):
                    line += f" ({a['cost']})"
            else:
                line = f"  {a['time']}: {activity_text}"
            safe_line = _pdf_safe(line)
            if len(safe_line) > 120:
                safe_line = safe_line[:117] + "..."
            pdf.cell(0, 6, safe_line, ln=True)
        pdf.ln(3)

        if pdf.get_y() > 250:
            pdf.add_page()

    # ── Budget ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Budget Breakdown", ln=True)
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    group_size = {"Solo": 1, "Couple": 2, "Group": 4, "Family": 4}.get(prefs.get("group", "Solo"), 2)
    pdf.cell(0, 7, f"Group size: {group_size} | Budget: ${prefs.get('budget', 3000):,} | "
             f"Estimated: ${results['total_cost']:,}", ln=True)
    pdf.ln(4)

    for item in results["budget_breakdown"]:
        pdf.cell(0, 7, _pdf_safe(f"  {item['city']} ({item['country']}): {item['days']}d x "
                 f"${item['daily_pp']}/pp = ${item['total']:,}"), ln=True)

    transport_legs = results.get("transport_legs", [])
    if transport_legs:
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Transport Costs", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for leg in transport_legs:
            pdf.cell(0, 7, _pdf_safe(f"  {leg['from']} -> {leg['to']}: {leg.get('name', '')} ~${leg.get('cost', 0)} pp"), ln=True)

    # ── Practical Info ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Practical Info", ln=True)
    pdf.ln(4)

    seen_countries = set()
    for country_info in recommended:
        country = country_info["country"]
        if country in seen_countries:
            continue
        seen_countries.add(country)
        sample = country_info["cities"][0]["data"]

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, country, ln=True)
        pdf.set_font("Helvetica", "", 10)
        info_items = [
            f"Visa: {sample.get('visa_status', '?').replace('_', ' ').title()} (max {sample.get('visa_max_stay', '?')} days)",
            f"Currency: {sample.get('currency_name', '?')} ({sample.get('currency', '?')}) {sample.get('currency_symbol', '')}",
            f"Power: {sample.get('plug_type', '?')}",
            f"Tipping: {sample.get('tipping', '?')}",
            f"Emergency: {sample.get('emergency_number', '?')}",
            f"SIM: {sample.get('sim_info', '?')}",
            f"Tap Water: {sample.get('tap_water', '?')}",
            f"Dress Code: {sample.get('dress_code', '?')}",
        ]
        for info in info_items:
            pdf.cell(0, 6, _pdf_safe(f"  {info}"), ln=True)
        pdf.ln(4)

    # ── Packing List ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Packing List", ln=True)
    pdf.ln(4)

    packing = generate_packing_list(results["cities"], results["trip_days"], prefs.get("interests", []))
    for category, items in packing.items():
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, _pdf_safe(category), ln=True)
        pdf.set_font("Helvetica", "", 10)
        for item in items:
            pdf.cell(0, 6, _pdf_safe(f"  [ ] {item}"), ln=True)
        pdf.ln(3)

    return pdf.output()


# ── Results Screen ─────────────────────────────────────────────────────────────
def results_screen():
    results = st.session_state.results
    prefs = st.session_state.prefs
    recommended = results["recommended"]

    st.markdown(
        '<div class="nav-bar">'
        '<span class="nav-title">🌍 Travel Planner — Your Trip</span></div>',
        unsafe_allow_html=True,
    )

    nc1, nc2, nc3, nc4, nc5 = st.columns([1, 1, 1, 1, 1])
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
        if st.button("🗺️ Explore Map", key="to_explore_from_results"):
            st.session_state.screen = "explore"
            st.rerun()
    with nc4:
        if st.button("🧰 Tools", key="to_tools_results"):
            st.session_state.screen = "tools"
            st.rerun()
    with nc5:
        pdf_bytes = generate_pdf_itinerary(results, prefs)
        st.download_button(
            label="📄 Download PDF",
            data=pdf_bytes,
            file_name="travel_itinerary.pdf",
            mime="application/pdf",
            key="download_pdf",
        )

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
    tab_overview, tab_itinerary, tab_map, tab_budget, tab_practical, tab_packing = st.tabs(
        ["📋 Overview", "📅 Day-by-Day", "🗺️ Route Map", "💰 Budget", "🌐 Practical Info", "🧳 Packing List"]
    )

    # ── Overview Tab ──
    with tab_overview:
        # Flight search links at top
        dep_city = prefs.get("departure_city", "New York")
        start_date = prefs.get("start_date", date.today() + timedelta(days=30))
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        end_date = start_date + timedelta(days=results["trip_days"])
        first_dest = results["cities"][0]["name"] if results["cities"] else ""
        last_dest = results["cities"][-1]["name"] if results["cities"] else ""

        outbound_url = generate_flight_search_url(dep_city, first_dest, start_date.isoformat())
        return_url = generate_flight_search_url(last_dest, dep_city, end_date.isoformat())

        st.markdown(
            f'<div style="background:#f0f4ff;border-radius:12px;padding:16px;margin-bottom:16px;">'
            f'<strong>✈️ Search Flights</strong><br>'
            f'<a href="{outbound_url}" target="_blank" class="search-link-btn flight-link">'
            f'Outbound: {dep_city} → {first_dest} ({start_date.strftime("%b %d")})</a>'
            f'<a href="{return_url}" target="_blank" class="search-link-btn flight-link">'
            f'Return: {last_dest} → {dep_city} ({end_date.strftime("%b %d")})</a>'
            f'</div>',
            unsafe_allow_html=True,
        )

        for country_info in recommended:
            reason = generate_country_reason(country_info, prefs)

            # Visa badge
            sample_city = country_info["cities"][0]["data"]
            visa_status = sample_city.get("visa_status", "unknown")
            visa_max = sample_city.get("visa_max_stay", 0)
            visa_notes = sample_city.get("visa_notes", "")
            visa_class = {"visa_free": "visa-free", "visa_on_arrival": "visa-arrival",
                          "e_visa": "visa-evisa", "embassy_visa": "visa-embassy"}.get(visa_status, "visa-evisa")
            visa_label = {"visa_free": "Visa Free", "visa_on_arrival": "Visa on Arrival",
                          "e_visa": "E-Visa Required", "embassy_visa": "Embassy Visa"}.get(visa_status, visa_status.replace("_", " ").title())
            visa_html = f'<span class="visa-badge {visa_class}">{visa_label}'
            if visa_max:
                visa_html += f' · {visa_max} days'
            visa_html += '</span>'

            st.markdown(f'<div class="result-card">'
                        f'<div class="country-header">🇺🇳 {country_info["country"]} {visa_html}</div>'
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

                    # Hotel search links
                    city_start = start_date
                    city_end = start_date + timedelta(days=alloc if isinstance(alloc, int) else 3)
                    hotel_urls = generate_hotel_search_urls(city["name"], country_info["country"],
                                                           city_start.isoformat(), city_end.isoformat())
                    hotel_html = (
                        f'<a href="{hotel_urls["booking"]}" target="_blank" class="search-link-btn hotel-link">Hotels</a>'
                        f'<a href="{hotel_urls["airbnb"]}" target="_blank" class="search-link-btn airbnb-link">Airbnb</a>'
                    )

                    st.markdown(
                        f'<div style="background:#f8f9fa;border-radius:12px;padding:16px;">'
                        f'<strong style="font-size:1.1rem;">{city["name"]}</strong><br>'
                        f'<span style="color:#888;font-size:0.85rem;">{alloc} days · ~${city["data"]["cost"]}/day pp</span><br>'
                        f'<div style="margin:8px 0;">{tags_html}</div>'
                        f'<span style="color:#666;font-size:0.82rem;">{highlights}</span><br>'
                        f'<span style="color:#999;font-size:0.78rem;font-style:italic;">{desc}</span><br>'
                        f'<div style="margin-top:8px;">{hotel_html}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown('</div>', unsafe_allow_html=True)

            # Expandable detail view for each city in this country
            for city in country_info["cities"]:
                city_days = next((c["days_allocated"] for c in results["cities"] if c["name"] == city["name"]), None)
                with st.expander(f"📖 See full details for {city['name']}"):
                    render_city_detail(city["name"], city["data"], context="results", prefs=prefs, trip_days=city_days)

    # ── Itinerary Tab ──
    with tab_itinerary:
        st.markdown(f"### Your {results['trip_days']}-Day Itinerary")
        current_city = None
        for day in results["itinerary"]:
            # Transport card between cities
            if "transport" in day:
                t = day["transport"]
                mode_icon = {"flight": "✈️", "train": "🚆", "bus": "🚌", "ferry": "⛴️"}.get(t["mode"], "🚐")
                cost_str = f"~${t['cost']}" if t.get("cost") else ""
                dur_str = f"{t['duration']}h" if t.get("duration") else ""
                st.markdown(
                    f'<div class="transport-card">'
                    f'<span class="transport-icon">{mode_icon}</span>'
                    f'<div class="transport-details">'
                    f'<div class="route">{t["from"]} → {t["to"]}</div>'
                    f'<div class="info">{t.get("name", t["mode"].title())} · {dur_str} · {cost_str}</div>'
                    f'<div class="info" style="font-size:0.8rem;color:#999;">{t.get("notes", "")}</div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

            if day["city"] != current_city:
                current_city = day["city"]
                st.markdown(f"---")
                st.markdown(f"#### 📍 {current_city}, {day['country']}")

            acts_html = ""
            for a in day["activities"]:
                if a.get("structured"):
                    # Rich activity card with address, hours, cost, maps link
                    meta_parts = []
                    if a.get("address"):
                        meta_parts.append(f"📍 {a['address']}")
                    if a.get("hours"):
                        meta_parts.append(f"🕐 {a['hours']}")
                    if a.get("cost"):
                        meta_parts.append(f"💰 {a['cost']}")
                    meta_str = " · ".join(meta_parts)
                    maps_html = ""
                    if a.get("maps_url"):
                        maps_html = f' · <a href="{a["maps_url"]}" target="_blank" class="maps-link">📍 Open in Maps</a>'
                    desc_html = ""
                    if a.get("description"):
                        desc_html = f'<div style="color:#888;font-size:0.78rem;margin-top:2px;">{a["description"]}</div>'
                    acts_html += (
                        f'<div class="activity-details">'
                        f'<span class="activity-time">{a["time"]}</span>'
                        f'<span class="act-name">{a["activity"]}</span>'
                        f'<div class="act-meta">{meta_str}{maps_html}</div>'
                        f'{desc_html}'
                        f'</div>'
                    )
                else:
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
        # Add transport costs if any
        transport_legs = results.get("transport_legs", [])
        if transport_legs:
            st.markdown("#### Transport Between Cities")
            for leg in transport_legs:
                mode_icon = {"flight": "✈️", "train": "🚆", "bus": "🚌", "ferry": "⛴️"}.get(leg["mode"], "🚐")
                st.markdown(
                    f'{mode_icon} **{leg["from"]} → {leg["to"]}** — {leg.get("name", "")} · '
                    f'~${leg.get("cost", 0)} pp · {leg.get("duration", "?")}h'
                )
            transport_total = sum(t.get("cost", 0) for t in transport_legs)
            st.markdown(f"**Transport subtotal:** ${transport_total * group_size:,} ({group_size}p)")
            st.markdown("")

        st.caption("Estimates are for mid-range travel and cover accommodation, food, activities, and local transport. "
                   "International flights are not included.")

    # ── Practical Info Tab ──
    with tab_practical:
        st.markdown("### Practical Travel Info")
        st.markdown("*Essential info for US passport holders*")
        st.markdown("")

        seen_countries = set()
        for country_info in recommended:
            country = country_info["country"]
            if country in seen_countries:
                continue
            seen_countries.add(country)

            sample = country_info["cities"][0]["data"]

            # Visa info
            visa_status = sample.get("visa_status", "unknown")
            visa_class = {"visa_free": "visa-free", "visa_on_arrival": "visa-arrival",
                          "e_visa": "visa-evisa", "embassy_visa": "visa-embassy"}.get(visa_status, "visa-evisa")
            visa_label = {"visa_free": "Visa Free", "visa_on_arrival": "Visa on Arrival",
                          "e_visa": "E-Visa Required", "embassy_visa": "Embassy Visa"}.get(visa_status, "Unknown")

            st.markdown(f'<div class="practical-card">'
                        f'<h4>🇺🇳 {country} <span class="visa-badge {visa_class}">{visa_label}</span></h4>',
                        unsafe_allow_html=True)

            items = [
                ("Visa", f'{visa_label} · Max {sample.get("visa_max_stay", "?")} days · {sample.get("visa_notes", "")}'),
                ("Currency", f'{sample.get("currency_name", "?")} ({sample.get("currency", "?")}) {sample.get("currency_symbol", "")}'),
                ("Power Plugs", sample.get("plug_type", "?")),
                ("Tipping", sample.get("tipping", "?")),
                ("Emergency", sample.get("emergency_number", "?")),
                ("SIM Card", sample.get("sim_info", "?")),
                ("Tap Water", sample.get("tap_water", "?")),
                ("Dress Code", sample.get("dress_code", "?")),
            ]
            for label, value in items:
                st.markdown(
                    f'<div class="practical-item"><span class="label">{label}</span>'
                    f'<span class="value">{value}</span></div>',
                    unsafe_allow_html=True,
                )

            st.markdown('</div>', unsafe_allow_html=True)

    # ── Packing List Tab ──
    with tab_packing:
        st.markdown("### Smart Packing List")
        st.markdown("*Customized for your destinations and activities*")
        st.markdown("")

        user_interests = prefs.get("interests", [])
        packing = generate_packing_list(results["cities"], results["trip_days"], user_interests)

        for category, items in packing.items():
            st.markdown(f'<div class="packing-category"><h4>{category}</h4>', unsafe_allow_html=True)
            for item in items:
                st.checkbox(item, key=f"pack_{category}_{item}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")
        st.caption("This list is generated based on your destinations' weather, terrain, and your selected interests.")


# ── Tools Screen ──────────────────────────────────────────────────────────────
def tools_screen():
    st.markdown(
        '<div class="nav-bar">'
        '<span class="nav-title">🧰 Travel Tools</span></div>',
        unsafe_allow_html=True,
    )

    nc1, nc2, nc3 = st.columns([1, 1, 1])
    with nc1:
        if st.button("← Back to Wizard", key="back_to_wizard_tools"):
            st.session_state.screen = "wizard"
            st.rerun()
    with nc2:
        if st.button("🗺️ Explore Map", key="to_explore_tools"):
            st.session_state.screen = "explore"
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs([
        "⚖️ Compare Cities",
        "🏆 Top Cities",
        "💰 Budget Calculator",
        "🎲 Surprise Me",
    ])

    # ── Tab 1: Compare Cities ─────────────────────────────────────────────────
    with tab1:
        st.subheader("⚖️ Compare Cities Side-by-Side")
        city_names = sorted(CITIES.keys())
        selected = st.multiselect(
            "Pick 2–3 cities to compare",
            city_names,
            max_selections=3,
            key="compare_cities_select",
        )

        if len(selected) < 2:
            st.info("Select at least 2 cities to compare.")
        else:
            cols = st.columns(len(selected))
            month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

            for i, city_name in enumerate(selected):
                d = CITIES[city_name]
                with cols[i]:
                    safety_stars = "★" * d.get("safety", 3) + "☆" * (5 - d.get("safety", 3))
                    best_months = ", ".join(month_names[m - 1] for m in d.get("months", []))
                    tags_html = "".join(
                        f'<span class="city-tag">{INTEREST_OPTIONS.get(t, t)}</span>'
                        for t in d.get("tags", [])
                    )
                    food_html = "".join(f'<span class="food-drink-item">{f}</span>' for f in d.get("local_food", []))
                    drink_html = "".join(f'<span class="drink-item">{dr}</span>' for dr in d.get("local_drink", []))

                    st.markdown(
                        f'<div class="detail-panel">'
                        f'<h3>📍 {city_name}</h3>'
                        f'<p style="color:#666;margin-top:0;">{d["country"]} · {d["region"]}</p>'
                        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;">'
                        f'<div class="cost-stat"><div class="val">${d["cost"]}</div><div class="lbl">Cost / Day</div></div>'
                        f'<div class="cost-stat"><div class="val">{safety_stars}</div><div class="lbl">Safety</div></div>'
                        f'<div class="cost-stat"><div class="val">${d.get("airbnb_cost", 60)}/n</div><div class="lbl">Airbnb</div></div>'
                        f'<div class="cost-stat"><div class="val">${d.get("uber_cost", 8)}</div><div class="lbl">Avg Uber</div></div>'
                        f'</div>'
                        f'<p><strong>Language:</strong> {d.get("language", "Local")}</p>'
                        f'<p><strong>Best Months:</strong> {best_months}</p>'
                        f'<div style="margin:8px 0;">{tags_html}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    # Top 5 activities
                    st.markdown('<h4>Top Activities</h4>', unsafe_allow_html=True)
                    for j, a in enumerate(d.get("top_activities", [])[:5], 1):
                        st.markdown(
                            f'<div class="activity-rank">'
                            f'<span class="activity-number">{j}</span> {a}</div>',
                            unsafe_allow_html=True,
                        )

                    # Food & drink
                    st.markdown(
                        f'<div style="margin:12px 0;">{food_html}{drink_html}</div>',
                        unsafe_allow_html=True,
                    )

            # Winner summary
            st.markdown("---")
            st.markdown("### 🏅 Quick Comparison")
            comparison = [(n, CITIES[n]) for n in selected]
            cheapest = min(comparison, key=lambda x: x[1]["cost"])
            safest = max(comparison, key=lambda x: x[1].get("safety", 3))
            best_airbnb = min(comparison, key=lambda x: x[1].get("airbnb_cost", 60))
            best_uber = min(comparison, key=lambda x: x[1].get("uber_cost", 8))

            wc1, wc2, wc3, wc4 = st.columns(4)
            with wc1:
                st.markdown(
                    f'<div class="metric-box"><div class="metric-val">{cheapest[0]}</div>'
                    f'<div class="metric-lbl">💸 Cheapest (${cheapest[1]["cost"]}/day)</div></div>',
                    unsafe_allow_html=True,
                )
            with wc2:
                st.markdown(
                    f'<div class="metric-box"><div class="metric-val">{safest[0]}</div>'
                    f'<div class="metric-lbl">🛡️ Safest ({safest[1].get("safety", 3)}/5)</div></div>',
                    unsafe_allow_html=True,
                )
            with wc3:
                st.markdown(
                    f'<div class="metric-box"><div class="metric-val">{best_airbnb[0]}</div>'
                    f'<div class="metric-lbl">🏠 Best Airbnb (${best_airbnb[1].get("airbnb_cost", 60)}/n)</div></div>',
                    unsafe_allow_html=True,
                )
            with wc4:
                st.markdown(
                    f'<div class="metric-box"><div class="metric-val">{best_uber[0]}</div>'
                    f'<div class="metric-lbl">🚗 Cheapest Uber (${best_uber[1].get("uber_cost", 8)})</div></div>',
                    unsafe_allow_html=True,
                )

    # ── Tab 2: Top Cities By Category ─────────────────────────────────────────
    with tab2:
        st.subheader("🏆 Top 10 Cities By Category")

        categories = {
            "💸 Cheapest": {
                "sort": lambda n, d: d["cost"],
                "reverse": False,
                "stat": lambda d: f"${d['cost']}/day",
            },
            "💎 Most Expensive": {
                "sort": lambda n, d: d["cost"],
                "reverse": True,
                "stat": lambda d: f"${d['cost']}/day",
            },
            "🛡️ Safest": {
                "sort": lambda n, d: d.get("safety", 3),
                "reverse": True,
                "stat": lambda d: f"{d.get('safety', 3)}/5 safety",
            },
            "🍜 Best Food Scene": {
                "sort": lambda n, d: len(d.get("local_food", [])) * 3 + len(d.get("local_drink", [])),
                "reverse": True,
                "stat": lambda d: f"{len(d.get('local_food', []))} dishes · ${d['cost']}/day",
                "filter": lambda n, d: "food" in d.get("tags", []),
            },
            "🍸 Best Nightlife": {
                "sort": lambda n, d: -d["cost"],
                "reverse": False,
                "stat": lambda d: f"${d['cost']}/day",
                "filter": lambda n, d: "nightlife" in d.get("tags", []),
            },
            "🏖️ Best for Beaches": {
                "sort": lambda n, d: -d["cost"],
                "reverse": False,
                "stat": lambda d: f"${d['cost']}/day · {d.get('beach_type', 'beach')}",
                "filter": lambda n, d: "beaches" in d.get("tags", []),
            },
            "🥾 Best for Hiking": {
                "sort": lambda n, d: -d["cost"],
                "reverse": False,
                "stat": lambda d: f"${d['cost']}/day · {d.get('terrain', 'varied')}",
                "filter": lambda n, d: "hiking" in d.get("tags", []),
            },
            "🏛️ Best for Culture": {
                "sort": lambda n, d: sum(1 for t in d.get("tags", []) if t in ("culture", "temples", "art", "architecture")) * 10 - d["cost"] * 0.05,
                "reverse": True,
                "stat": lambda d: f"${d['cost']}/day",
                "filter": lambda n, d: any(t in d.get("tags", []) for t in ("culture", "temples", "art", "architecture")),
            },
            "🎒 Best for Solo Travel": {
                "sort": lambda n, d: d.get("safety", 3) * 10 + d.get("wifi", 3) * 5 - d["cost"] * 0.1,
                "reverse": True,
                "stat": lambda d: f"${d['cost']}/day · Safety {d.get('safety', 3)}/5",
            },
            "💕 Best for Honeymoon": {
                "sort": lambda n, d: d.get("safety", 3) + d.get("comfort", 3),
                "reverse": True,
                "stat": lambda d: f"${d['cost']}/day · Comfort {d.get('comfort', 3)}/5",
                "filter": lambda n, d: "honeymoon" in d.get("best_for", []),
            },
        }

        category = st.selectbox("Pick a category", list(categories.keys()), key="top_category_select")
        config = categories[category]

        candidates = list(CITIES.items())
        if "filter" in config:
            candidates = [(n, d) for n, d in candidates if config["filter"](n, d)]

        ranked = sorted(candidates, key=lambda x: config["sort"](x[0], x[1]), reverse=config["reverse"])[:10]

        for rank, (city_name, city_data) in enumerate(ranked, 1):
            stat_text = config["stat"](city_data)
            region_color = REGION_COLORS.get(city_data["region"], "#888")
            st.markdown(
                f'<div class="activity-rank" style="padding:12px 8px;margin-bottom:4px;">'
                f'<span class="activity-number" style="width:32px;height:32px;font-size:1rem;">{rank}</span>'
                f'<span style="flex:1;">'
                f'<strong>{city_name}</strong>, {city_data["country"]}'
                f'<span style="color:{region_color};margin-left:8px;font-size:0.8rem;">● {city_data["region"]}</span>'
                f'</span>'
                f'<span style="color:#4361ee;font-weight:600;">{stat_text}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Tab 3: Budget Calculator ──────────────────────────────────────────────
    with tab3:
        st.subheader("💰 Trip Budget Calculator")

        bc1, bc2, bc3 = st.columns(3)
        with bc1:
            calc_city = st.selectbox("City", sorted(CITIES.keys()), key="budget_calc_city")
        with bc2:
            calc_days = st.number_input("Trip Length (days)", 3, 30, 7, key="budget_calc_days")
        with bc3:
            calc_group = st.radio(
                "Group Size",
                ["Solo", "Couple", "Group (4)", "Family (4)"],
                key="budget_calc_group",
                horizontal=True,
            )

        group_map = {"Solo": 1, "Couple": 2, "Group (4)": 4, "Family (4)": 4}
        group_size = group_map[calc_group]

        cd = CITIES[calc_city]
        cost_pp = cd["cost"]
        airbnb = cd.get("airbnb_cost", 60)
        uber = cd.get("uber_cost", 8)

        airbnb_units = 1 if group_size <= 2 else 2
        airbnb_total = airbnb * calc_days * airbnb_units
        food_total = cost_pp * calc_days * group_size
        uber_total = uber * calc_days * 2
        if group_size > 2:
            uber_total = uber_total * 2
        grand_total = airbnb_total + food_total + uber_total
        per_person = grand_total / group_size

        st.markdown("")
        st.markdown(
            f'<div class="budget-card">'
            f'<div class="budget-label">{calc_city} · {calc_days} days · {group_size} {"person" if group_size == 1 else "people"}</div>'
            f'<div class="budget-amount">${grand_total:,.0f}</div>'
            f'<div class="budget-label">Estimated Total</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        b1, b2, b3, b4 = st.columns(4)
        with b1:
            st.markdown(
                f'<div class="cost-stat"><div class="val">${airbnb_total:,.0f}</div>'
                f'<div class="lbl">🏠 Accommodation<br>{airbnb_units} Airbnb × {calc_days}n</div></div>',
                unsafe_allow_html=True,
            )
        with b2:
            st.markdown(
                f'<div class="cost-stat"><div class="val">${food_total:,.0f}</div>'
                f'<div class="lbl">🍽️ Food & Activities<br>${cost_pp}/day × {group_size}pp</div></div>',
                unsafe_allow_html=True,
            )
        with b3:
            st.markdown(
                f'<div class="cost-stat"><div class="val">${uber_total:,.0f}</div>'
                f'<div class="lbl">🚗 Transport<br>~2 rides/day</div></div>',
                unsafe_allow_html=True,
            )
        with b4:
            st.markdown(
                f'<div class="cost-stat"><div class="val">${per_person:,.0f}</div>'
                f'<div class="lbl">👤 Per Person<br>total ÷ {group_size}</div></div>',
                unsafe_allow_html=True,
            )

    # ── Tab 4: Surprise Me ────────────────────────────────────────────────────
    with tab4:
        st.subheader("🎲 Surprise Me!")
        st.markdown("Not sure where to go? Let us pick a random destination for you!")

        s1, s2 = st.columns(2)
        with s1:
            region_options = ["Any Region"] + list(REGION_COLORS.keys())
            surprise_region = st.selectbox("Region", region_options, key="surprise_region")
        with s2:
            budget_tier = st.radio(
                "Budget Range",
                ["Budget (< $50/day)", "Mid-Range ($50–$120/day)", "Luxury ($120+/day)"],
                key="surprise_budget",
                horizontal=True,
            )

        label_to_key = {v: k for k, v in INTEREST_OPTIONS.items()}
        surprise_interests = st.multiselect(
            "Interests (optional — leave empty for any)",
            list(INTEREST_OPTIONS.values()),
            key="surprise_interests",
        )
        interest_keys = [label_to_key[l] for l in surprise_interests if l in label_to_key]

        if st.button("🎲 Surprise Me!", type="primary", key="surprise_btn"):
            candidates = []
            for name, data in CITIES.items():
                if surprise_region != "Any Region" and data["region"] != surprise_region:
                    continue
                cost = data["cost"]
                if budget_tier.startswith("Budget") and cost >= 50:
                    continue
                if budget_tier.startswith("Mid") and (cost < 50 or cost > 120):
                    continue
                if budget_tier.startswith("Luxury") and cost < 120:
                    continue
                if interest_keys and not any(t in data.get("tags", []) for t in interest_keys):
                    continue
                candidates.append((name, data))

            if candidates:
                st.session_state.surprise_result = random.choice(candidates)
            else:
                st.session_state.surprise_result = None
                st.warning("No cities match those filters. Try broadening your criteria!")

        result = st.session_state.get("surprise_result")
        if result:
            city_name, city_data = result
            st.markdown("")
            st.success(f"Your surprise destination: **{city_name}, {city_data['country']}**!")
            render_city_detail(city_name, city_data, context="explore")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    init_state()

    if st.session_state.screen == "wizard":
        wizard_screen()
    elif st.session_state.screen == "results":
        results_screen()
    elif st.session_state.screen == "explore":
        explore_screen()
    elif st.session_state.screen == "tools":
        tools_screen()
    else:
        wizard_screen()


main()
