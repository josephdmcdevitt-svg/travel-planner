#!/usr/bin/env python3
"""Builder script: adds 11 new fields to all 326 cities in cities.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from cities import CITIES

# ── Country-level defaults ──────────────────────────────────────────────────

LANGUAGE = {
    "Japan": "Japanese", "Thailand": "Thai", "Vietnam": "Vietnamese",
    "South Korea": "Korean", "Indonesia": "Bahasa Indonesian", "India": "Hindi/English",
    "Cambodia": "Khmer", "Philippines": "Filipino/English", "Malaysia": "Malay/English",
    "China": "Mandarin", "Taiwan": "Mandarin", "Sri Lanka": "Sinhala/English",
    "Nepal": "Nepali", "Myanmar": "Burmese", "Laos": "Lao",
    "Mongolia": "Mongolian", "Uzbekistan": "Uzbek", "Georgia": "Georgian",
    "Jordan": "Arabic", "Oman": "Arabic", "Maldives": "Dhivehi/English",
    "Bhutan": "Dzongkha", "France": "French", "Italy": "Italian",
    "Spain": "Spanish", "Portugal": "Portuguese", "Greece": "Greek",
    "Croatia": "Croatian", "Czech Republic": "Czech", "Netherlands": "Dutch",
    "Germany": "German", "Turkey": "Turkish", "United Kingdom": "English",
    "Switzerland": "German/French", "Austria": "German", "Hungary": "Hungarian",
    "Poland": "Polish", "Romania": "Romanian", "Bulgaria": "Bulgarian",
    "Montenegro": "Montenegrin", "Albania": "Albanian", "Slovenia": "Slovenian",
    "Estonia": "Estonian", "Latvia": "Latvian", "Lithuania": "Lithuanian",
    "Denmark": "Danish", "Sweden": "Swedish", "Norway": "Norwegian",
    "Finland": "Finnish", "Iceland": "Icelandic", "Ireland": "English",
    "Belgium": "French/Dutch", "Malta": "Maltese/English", "Cyprus": "Greek/Turkish",
    "Colombia": "Spanish", "Peru": "Spanish", "Argentina": "Spanish",
    "Brazil": "Portuguese", "Chile": "Spanish", "Ecuador": "Spanish",
    "Bolivia": "Spanish", "Uruguay": "Spanish", "Paraguay": "Spanish/Guarani",
    "Costa Rica": "Spanish", "Panama": "Spanish", "Guatemala": "Spanish",
    "Mexico": "Spanish", "Morocco": "Arabic/French", "South Africa": "English/Afrikaans",
    "Tanzania": "Swahili/English", "Kenya": "Swahili/English", "Egypt": "Arabic",
    "Ghana": "English/Twi", "Rwanda": "Kinyarwanda/English", "Ethiopia": "Amharic",
    "Namibia": "English/Afrikaans", "Botswana": "English/Setswana",
    "Senegal": "French/Wolof", "Madagascar": "Malagasy/French",
    "Mauritius": "English/French/Creole", "Tunisia": "Arabic/French",
    "Uganda": "English/Swahili", "Australia": "English", "New Zealand": "English",
}

SAFETY = {
    "Japan": 5, "South Korea": 5, "Taiwan": 5, "Bhutan": 5,
    "Oman": 5, "Iceland": 5, "Switzerland": 5, "Norway": 5, "Finland": 5,
    "Denmark": 5, "Sweden": 5, "New Zealand": 5, "Maldives": 4,
    "Australia": 4, "Austria": 4, "Netherlands": 4, "Germany": 4,
    "United Kingdom": 4, "Ireland": 4, "Belgium": 4, "Czech Republic": 4,
    "Slovenia": 4, "Estonia": 4, "Croatia": 4, "Portugal": 4,
    "Spain": 4, "France": 4, "Italy": 4, "Malta": 4, "Cyprus": 4,
    "Poland": 4, "Hungary": 4, "Georgia": 4, "Latvia": 4, "Lithuania": 4,
    "Malaysia": 4, "Thailand": 4, "Uruguay": 4, "Chile": 4, "Costa Rica": 4,
    "Greece": 4, "Romania": 3, "Bulgaria": 3, "Montenegro": 3, "Albania": 3,
    "Turkey": 3, "China": 4, "Vietnam": 3, "Cambodia": 3, "Philippines": 3,
    "Indonesia": 3, "Sri Lanka": 3, "Nepal": 3, "India": 3, "Jordan": 4,
    "Mongolia": 3, "Uzbekistan": 3, "Laos": 3, "Myanmar": 2, "Argentina": 3,
    "Brazil": 2, "Peru": 3, "Colombia": 3, "Ecuador": 3, "Bolivia": 3,
    "Paraguay": 3, "Panama": 3, "Guatemala": 3, "Mexico": 3,
    "Morocco": 3, "Egypt": 3, "Tunisia": 3, "South Africa": 2,
    "Tanzania": 3, "Kenya": 3, "Ghana": 3, "Rwanda": 4,
    "Ethiopia": 3, "Namibia": 3, "Botswana": 3, "Senegal": 3,
    "Madagascar": 2, "Mauritius": 4, "Uganda": 3,
}

WIFI = {
    "Japan": 5, "South Korea": 5, "Taiwan": 5, "Iceland": 5,
    "Estonia": 5, "Finland": 5, "Sweden": 5, "Denmark": 5, "Norway": 5,
    "Netherlands": 5, "United Kingdom": 5, "Germany": 5, "Switzerland": 5,
    "Australia": 4, "New Zealand": 4, "France": 4, "Italy": 4,
    "Spain": 4, "Portugal": 4, "Greece": 4, "Croatia": 4,
    "Czech Republic": 4, "Austria": 4, "Hungary": 4, "Poland": 4,
    "Turkey": 4, "Ireland": 4, "Belgium": 4, "Malta": 4, "Thailand": 4,
    "Malaysia": 4, "China": 4, "India": 3, "Romania": 4, "Slovenia": 4,
    "Latvia": 4, "Lithuania": 4, "Argentina": 4, "Chile": 4,
    "Colombia": 3, "Uruguay": 4, "Brazil": 3, "Costa Rica": 3,
    "Georgia": 4, "Maldives": 3, "Bulgaria": 3, "Montenegro": 3,
    "Albania": 3, "Cyprus": 3, "Vietnam": 3, "Philippines": 3,
    "Cambodia": 3, "Indonesia": 3, "Sri Lanka": 3, "Nepal": 2,
    "Mexico": 3, "Peru": 3, "Ecuador": 3, "Morocco": 3, "Egypt": 3,
    "Tunisia": 3, "Jordan": 3, "Oman": 4, "South Africa": 3,
    "Panama": 3, "Guatemala": 2, "Bhutan": 2, "Uzbekistan": 2,
    "Mongolia": 2, "Bolivia": 2, "Paraguay": 2, "Laos": 2, "Myanmar": 2,
    "Kenya": 3, "Tanzania": 2, "Ghana": 2, "Rwanda": 3,
    "Uganda": 2, "Senegal": 2, "Ethiopia": 2, "Madagascar": 1,
    "Namibia": 2, "Botswana": 2, "Mauritius": 3,
}

VEG_FRIENDLY = {
    "India": 5, "Taiwan": 4, "Thailand": 4, "Japan": 4,
    "United Kingdom": 4, "Netherlands": 4, "Germany": 4, "Italy": 4,
    "Australia": 4, "New Zealand": 4, "Sri Lanka": 4, "Israel": 4,
    "France": 3, "Spain": 3, "Portugal": 3, "Greece": 3, "Turkey": 3,
    "Indonesia": 3, "Malaysia": 3, "South Korea": 3, "China": 3,
    "Mexico": 3, "Peru": 3, "Switzerland": 4, "Austria": 3,
    "Czech Republic": 3, "Poland": 3, "Hungary": 3, "Croatia": 3,
    "Romania": 3, "Bulgaria": 3, "Belgium": 3, "Ireland": 3,
    "Denmark": 4, "Sweden": 4, "Norway": 3, "Finland": 3, "Iceland": 3,
    "Slovenia": 3, "Estonia": 3, "Latvia": 3, "Lithuania": 3,
    "Cyprus": 3, "Malta": 3, "Nepal": 4, "Maldives": 3, "Bhutan": 3,
    "Georgia": 3, "Colombia": 3, "Chile": 3, "Ecuador": 3, "Costa Rica": 3,
    "Panama": 3, "Guatemala": 3, "Uruguay": 2, "Brazil": 3,
    "Argentina": 2, "Bolivia": 2, "Paraguay": 2,
    "Vietnam": 3, "Philippines": 2, "Cambodia": 2, "Laos": 2,
    "Myanmar": 2, "Mongolia": 1, "Uzbekistan": 2, "Jordan": 3,
    "Oman": 3, "Morocco": 3, "Egypt": 3, "Tunisia": 3,
    "South Africa": 3, "Kenya": 2, "Tanzania": 2, "Ghana": 2,
    "Rwanda": 2, "Ethiopia": 3, "Namibia": 2, "Botswana": 2,
    "Senegal": 2, "Madagascar": 2, "Mauritius": 3, "Uganda": 2,
    "Montenegro": 2, "Albania": 2,
}

# ── City-specific data ──────────────────────────────────────────────────────

CITY_SIZE = {
    # Mega cities
    "Tokyo": "mega_city", "Delhi": "mega_city", "Mumbai": "mega_city",
    "Beijing": "mega_city", "Shanghai": "mega_city", "Bangkok": "mega_city",
    "Jakarta": "mega_city", "Seoul": "mega_city", "Cairo": "mega_city",
    "Mexico City": "mega_city", "Sao Paulo": "mega_city", "Istanbul": "mega_city",
    "London": "mega_city", "Paris": "mega_city", "Ho Chi Minh City": "mega_city",
    "Manila": "mega_city", "Kuala Lumpur": "mega_city", "Lima": "mega_city",
    "Buenos Aires": "mega_city", "Rio de Janeiro": "mega_city", "Bogota": "mega_city",
    # Large cities
    "Osaka": "large_city", "Taipei": "large_city", "Hong Kong": "large_city",
    "Hanoi": "large_city", "Singapore": "large_city", "Chengdu": "large_city",
    "Xi'an": "large_city", "Rome": "large_city", "Barcelona": "large_city",
    "Madrid": "large_city", "Berlin": "large_city", "Amsterdam": "large_city",
    "Prague": "large_city", "Budapest": "large_city", "Vienna": "large_city",
    "Athens": "large_city", "Lisbon": "large_city", "Warsaw": "large_city",
    "Bucharest": "large_city", "Sofia": "large_city", "Milan": "large_city",
    "Munich": "large_city", "Hamburg": "large_city", "Cologne": "large_city",
    "Naples": "large_city", "Seville": "large_city", "Lyon": "large_city",
    "Marseille": "large_city", "Dublin": "large_city", "Edinburgh": "large_city",
    "Brussels": "large_city", "Copenhagen": "large_city", "Stockholm": "large_city",
    "Oslo": "large_city", "Helsinki": "large_city", "Zurich": "large_city",
    "Santiago": "large_city", "Medellin": "large_city", "Nairobi": "large_city",
    "Johannesburg": "large_city", "Addis Ababa": "large_city", "Accra": "large_city",
    "Dakar": "large_city", "Kampala": "large_city", "Dar es Salaam": "large_city",
    "Sydney": "large_city", "Melbourne": "large_city", "Auckland": "large_city",
    "Krakow": "large_city", "Reykjavik": "large_city", "Salvador": "large_city",
    "Cartagena": "large_city", "Quito": "large_city", "Marrakech": "large_city",
    "Cape Town": "large_city", "Tirana": "large_city", "Riga": "large_city",
    "Vilnius": "large_city", "Tallinn": "large_city", "Rotterdam": "large_city",
    "Florence": "large_city", "Valencia": "large_city", "Malaga": "large_city",
    "Porto": "large_city", "Thessaloniki": "large_city", "Split": "large_city",
    "Zagreb": "large_city", "Gdansk": "large_city", "Wroclaw": "large_city",
    "Ljubljana": "large_city", "Tbilisi": "large_city", "Amman": "large_city",
    "Muscat": "large_city", "Colombo": "large_city", "Kathmandu": "large_city",
    "Yangon": "large_city", "Phnom Penh": "large_city", "Vientiane": "large_city",
    "Ulaanbaatar": "large_city", "Tashkent": "large_city",
    "Panama City": "large_city", "Montevideo": "large_city",
    "Asuncion": "large_city", "San Jose": "large_city", "La Paz": "large_city",
    "Antigua": "large_city", "Kigali": "large_city", "Tunis": "large_city",
    "Antananarivo": "large_city", "Windhoek": "large_city", "Perth": "large_city",
    "Wellington": "large_city", "Busan": "large_city", "Cebu": "large_city",
    "Da Nang": "large_city", "Chiang Mai": "large_city", "Jaipur": "large_city",
    "Durban": "large_city", "Nice": "large_city", "Antalya": "large_city",
    "Izmir": "large_city", "Fes": "large_city", "Gothenburg": "large_city",
    "Bergen": "large_city", "Dresden": "large_city", "Strasbourg": "large_city",
    "Bordeaux": "large_city", "Granada": "large_city", "Plovdiv": "large_city",
    "Kaohsiung": "large_city", "Penang": "large_city", "Salzburg": "large_city",
    "Innsbruck": "large_city", "Guilin": "large_city", "Sapporo": "large_city",
    "Nha Trang": "large_city", "Hiroshima": "large_city",
    # Small cities
    "Kyoto": "small_city", "Cusco": "small_city", "Dubrovnik": "small_city",
    "Bruges": "small_city", "Valparaiso": "small_city", "Arequipa": "small_city",
    "Chefchaouen": "small_city", "Essaouira": "small_city",
    "Bali": "small_city", "Yogyakarta": "small_city", "Lombok": "small_city",
    "Goa": "small_city", "Varanasi": "small_city", "Udaipur": "small_city",
    "Kandy": "small_city", "Galle": "small_city", "Pokhara": "small_city",
    "Siem Reap": "small_city", "Luang Prabang": "small_city",
    "Hoi An": "small_city", "Hue": "small_city", "Nara": "small_city",
    "Phuket": "small_city", "Krabi": "small_city", "Koh Samui": "small_city",
    "Santorini": "small_city", "Mykonos": "small_city", "Crete": "small_city",
    "Rhodes": "small_city", "Cappadocia": "small_city",
    "Cesky Krumlov": "small_town", "Brno": "small_city",
    "Bath": "small_city", "Liverpool": "small_city", "Galway": "small_city",
    "Cork": "small_city", "Ghent": "small_city", "Utrecht": "small_city",
    "Hvar": "small_town", "Kotor": "small_town", "Budva": "small_town",
    "Saranda": "small_town", "Berat": "small_town", "Bled": "small_town",
    "Piran": "small_town", "Tainan": "small_city", "Jiufen": "small_town",
    "Jeonju": "small_city", "Gyeongju": "small_city", "Jeju": "small_city",
    "Malacca": "small_city", "Langkawi": "small_town",
    "Samarkand": "small_city", "Bukhara": "small_city",
    "Batumi": "small_city", "Petra": "small_town", "Nizwa": "small_town",
    "Male": "small_city", "Thimphu": "small_city", "Paro": "small_town",
    "Zanzibar": "small_city", "Mombasa": "small_city", "Luxor": "small_city",
    "Aswan": "small_city", "Alexandria": "large_city", "Cape Coast": "small_town",
    "Stellenbosch": "small_town", "Swakopmund": "small_town",
    "Cairns": "small_city", "Byron Bay": "small_town",
    "Queenstown": "small_town", "Rotorua": "small_city",
    "Cuenca": "small_city", "Oaxaca": "small_city", "Merida": "small_city",
    "Guanajuato": "small_city", "San Cristobal": "small_town",
    "Tulum": "small_town", "Puerto Vallarta": "small_city",
    "Santa Marta": "small_city", "Salento": "village",
    "Mendoza": "small_city", "Bariloche": "small_town", "Salta": "small_city",
    "Florianopolis": "small_city", "Paraty": "small_town",
    "Pucon": "small_town", "Banos": "small_town", "Montanita": "village",
    "Sucre": "small_city", "Colonia": "small_town",
    "Punta del Este": "small_town", "Bocas del Toro": "small_town",
    "Lake Atitlan": "village", "Tikal": "village",
    "Brasov": "small_city", "Cluj-Napoca": "small_city", "Sibiu": "small_town",
    "Veliko Tarnovo": "small_town", "Tartu": "small_town",
    "Rovaniemi": "small_town", "Tromso": "small_town", "Lofoten": "village",
    "Vik": "village", "Akureyri": "small_town",
    "Valletta": "small_town", "Nicosia": "small_city", "Paphos": "small_town",
    "Sidi Bou Said": "village", "Djerba": "small_town",
    "Saint-Louis": "small_town", "Nosy Be": "small_town",
    "Port Louis": "small_city", "Grand Baie": "small_town",
    "Kerala": "small_city", "Rishikesh": "small_town", "Agra": "small_city",
    "Borneo": "small_town", "Kampot": "small_town",
    "Palawan": "small_town", "Siargao": "village", "Boracay": "small_town",
    "Ella": "village", "Sigiriya": "village", "Chitwan": "village",
    "Bagan": "village", "Mandalay": "small_city", "Inle Lake": "village",
    "Vang Vieng": "small_town", "Kazbegi": "village",
    "Wadi Rum": "village", "Ari Atoll": "village",
    "Amalfi Coast": "small_town", "Cinque Terre": "village", "Sicily": "small_city",
    "San Sebastian": "small_city", "Sintra": "small_town", "Madeira": "small_city",
    "Azores": "small_town", "Algarve": "small_town", "Plitvice": "village",
    "Highlands": "village", "Isle of Skye": "village",
    "Interlaken": "small_town", "Lucerne": "small_city", "Zermatt": "village",
    "Eger": "small_town",
    "Arusha": "small_city", "Lamu": "small_town",
    "Dahab": "small_town", "Merzouga": "village", "Kumasi": "small_city",
    "Maun": "small_town", "Milford Sound": "village",
    # Safari/Nature (no real city)
    "Gobi Desert": "village", "Komodo": "village", "Raja Ampat": "village",
    "Sun Moon Lake": "village", "Sacred Valley": "village",
    "Huacachina": "village", "Torres del Paine": "village",
    "Atacama": "small_town", "Galapagos": "village", "Uyuni": "small_town",
    "Copacabana": "small_town", "Monteverde": "village",
    "Manuel Antonio": "village", "La Fortuna": "small_town",
    "San Blas": "village", "Iguazu": "small_town",
    "Kruger": "village", "Serengeti": "village", "Masai Mara": "village",
    "Sossusvlei": "village", "Etosha": "village",
    "Okavango Delta": "village", "Chobe": "village",
    "Volcanoes NP": "village", "Bwindi": "village",
    "Ushuaia": "small_town", "El Calafate": "small_town",
    "Pai": "village",
    "Sapa": "small_town",
}

TERRAIN = {
    # Coastal
    "Nice": "coastal", "Marseille": "coastal", "Amalfi Coast": "coastal",
    "Cinque Terre": "coastal", "Barcelona": "coastal", "San Sebastian": "coastal",
    "Valencia": "coastal", "Malaga": "coastal", "Lisbon": "coastal",
    "Porto": "coastal", "Algarve": "coastal", "Dubrovnik": "coastal",
    "Split": "coastal", "Hvar": "coastal", "Kotor": "coastal",
    "Budva": "coastal", "Saranda": "coastal", "Piran": "coastal",
    "Antalya": "coastal", "Swakopmund": "coastal", "Essaouira": "coastal",
    "Mombasa": "coastal", "Lamu": "coastal", "Dahab": "coastal",
    "Alexandria": "coastal", "Durban": "coastal", "Dar es Salaam": "coastal",
    "Puerto Vallarta": "coastal", "Cartagena": "coastal", "Santa Marta": "coastal",
    "Valparaiso": "coastal", "Florianopolis": "coastal", "Salvador": "coastal",
    "Paraty": "coastal", "Montevideo": "coastal", "Sydney": "coastal",
    "Melbourne": "coastal", "Perth": "coastal", "Byron Bay": "coastal",
    "Auckland": "coastal", "Wellington": "coastal", "Cairns": "coastal",
    "Da Nang": "coastal", "Hoi An": "coastal", "Nha Trang": "coastal",
    "Nara": "flat", "Phuket": "coastal", "Krabi": "coastal",
    "Koh Samui": "island", "Punta del Este": "coastal",
    "Bocas del Toro": "island", "Cape Town": "coastal",
    "Rio de Janeiro": "coastal", "Goa": "coastal", "Colombo": "coastal",
    "Galle": "coastal", "Muscat": "coastal",  "Batumi": "coastal",
    "Gdansk": "coastal", "Accra": "coastal", "Cape Coast": "coastal",
    "Dakar": "coastal", "Port Louis": "coastal", "Grand Baie": "coastal",
    "Montanita": "coastal", "Tulum": "coastal", "Ushuaia": "coastal",
    "Djerba": "island",
    # Islands
    "Bali": "island", "Lombok": "island", "Komodo": "island",
    "Raja Ampat": "island", "Langkawi": "island", "Borneo": "island",
    "Palawan": "island", "Siargao": "island", "Boracay": "island",
    "Jeju": "island", "Male": "island", "Ari Atoll": "island",
    "Santorini": "island", "Mykonos": "island", "Crete": "island",
    "Rhodes": "island", "Sicily": "island", "Madeira": "island",
    "Azores": "island", "Zanzibar": "island", "Nosy Be": "island",
    "San Blas": "island", "Galapagos": "island", "Vik": "island",
    "Valletta": "island", "Paphos": "island", "Nicosia": "island",
    "Sidi Bou Said": "coastal",
    # Mountains
    "Kathmandu": "mountain", "Pokhara": "mountain", "Sapa": "mountain",
    "Hakone": "mountain", "Interlaken": "mountain", "Zermatt": "mountain",
    "Lucerne": "mountain", "Innsbruck": "mountain", "Salzburg": "mountain",
    "Bled": "mountain", "Kazbegi": "mountain", "Cappadocia": "mountain",
    "Ella": "mountain", "Sigiriya": "mountain", "Cusco": "mountain",
    "Sacred Valley": "mountain", "Arequipa": "mountain",
    "Torres del Paine": "mountain", "Atacama": "desert",
    "Bariloche": "mountain", "El Calafate": "mountain",
    "Pucon": "mountain", "Salento": "mountain", "Banos": "mountain",
    "Chefchaouen": "mountain", "Highlands": "mountain",
    "Isle of Skye": "mountain", "Lofoten": "coastal",
    "Tromso": "coastal", "Bergen": "coastal",
    "Queenstown": "mountain", "Milford Sound": "mountain",
    "La Paz": "mountain", "Salta": "mountain",
    "Brasov": "mountain", "Plitvice": "mountain",
    "Rovaniemi": "flat", "Pai": "mountain", "Kandy": "mountain",
    "Thimphu": "mountain", "Paro": "mountain", "Chitwan": "jungle",
    "Monteverde": "jungle", "Manuel Antonio": "coastal",
    "La Fortuna": "jungle", "Tikal": "jungle",
    "Lake Atitlan": "mountain", "Bagan": "flat",
    "Mandalay": "flat", "Inle Lake": "mountain",
    "Vang Vieng": "mountain", "Luang Prabang": "mountain",
    "Rishikesh": "mountain", "Udaipur": "flat",
    "Kerala": "coastal", "Volcanoes NP": "mountain",
    "Bwindi": "jungle", "Arusha": "mountain",
    "Merzouga": "desert", "Sossusvlei": "desert",
    "Gobi Desert": "desert", "Wadi Rum": "desert",
    "Huacachina": "desert", "San Cristobal": "mountain",
    "Guanajuato": "mountain", "Oaxaca": "mountain",
    "Mendoza": "mountain",
    # Jungle
    "Borneo": "jungle", "Komodo": "island",
    # Flat/urban (default for most big cities)
}

BEACH_TYPE = {
    "Phuket": "party", "Koh Samui": "mixed", "Mykonos": "party",
    "Goa": "party", "Boracay": "party", "Nha Trang": "party",
    "Hvar": "party", "Budva": "party", "Montanita": "party",
    "Bocas del Toro": "party",
    "Raja Ampat": "secluded", "San Blas": "secluded", "Palawan": "secluded",
    "Siargao": "secluded", "Lamu": "secluded", "Dahab": "secluded",
    "Ari Atoll": "secluded", "Male": "secluded",
    "Langkawi": "family", "Nice": "family", "Amalfi Coast": "family",
    "Algarve": "family", "Byron Bay": "family", "Paphos": "family",
    "Rhodes": "family", "Crete": "family", "Durban": "family",
    "Djerba": "family", "Grand Baie": "family", "Manuel Antonio": "family",
    "Bali": "mixed", "Krabi": "mixed", "Santorini": "mixed",
    "Tulum": "mixed", "Da Nang": "mixed", "Zanzibar": "mixed",
    "Puerto Vallarta": "mixed", "Nosy Be": "secluded",
    "Essaouira": "secluded", "Vik": "secluded", "Saranda": "secluded",
    "Lombok": "secluded", "Punta del Este": "mixed",
    "Florianopolis": "mixed", "Cebu": "mixed", "Hoi An": "family",
    "Antalya": "family", "Barcelona": "mixed", "San Sebastian": "family",
    "Valencia": "mixed", "Malaga": "mixed", "Cape Coast": "secluded",
    "Mombasa": "mixed", "Swakopmund": "secluded",
    "Cartagena": "mixed", "Santa Marta": "secluded",
    "Salvador": "mixed", "Paraty": "secluded",
    "Galapagos": "secluded", "Colombo": "mixed", "Galle": "family",
    "Piran": "family", "Gdansk": "family", "Valletta": "mixed",
    "Cape Town": "mixed", "Rio de Janeiro": "party",
    "Sydney": "mixed", "Perth": "family", "Cairns": "family",
    "Auckland": "family", "Accra": "mixed", "Dakar": "mixed",
    "Batumi": "mixed", "Kotor": "secluded",
    "Azores": "secluded", "Madeira": "secluded", "Sicily": "mixed",
    "Cinque Terre": "secluded",
}

# ── Descriptions ────────────────────────────────────────────────────────────

DESCRIPTIONS = {
    "Tokyo": "Japan's electric capital blending ancient temples with futuristic technology and world-class cuisine",
    "Kyoto": "The cultural heart of Japan, home to thousands of temples, traditional geisha districts, and serene bamboo groves",
    "Osaka": "Japan's kitchen — a vibrant city famous for incredible street food, energetic nightlife, and warm locals",
    "Hiroshima": "A city reborn as a symbol of peace, offering profound history alongside lush parks and island escapes",
    "Nara": "An ancient capital where friendly deer roam freely among magnificent temples and manicured gardens",
    "Hakone": "A mountain resort town with volcanic hot springs, serene lakes, and iconic views of Mount Fuji",
    "Sapporo": "Hokkaido's capital known for its famous snow festival, craft beer scene, and fresh seafood",
    "Bangkok": "Thailand's intoxicating capital where golden temples, chaotic markets, and sizzling street food converge",
    "Chiang Mai": "A laid-back cultural hub surrounded by mountains, night markets, and hundreds of ancient temples",
    "Phuket": "Thailand's largest island with buzzing beaches, turquoise waters, and vibrant nightlife",
    "Krabi": "Dramatic limestone cliffs, crystal-clear water, and some of Thailand's most stunning beaches",
    "Pai": "A bohemian mountain village with hot springs, canyons, and a chilled-out backpacker vibe",
    "Koh Samui": "A tropical island paradise with palm-fringed beaches, luxury resorts, and lively beach bars",
    "Ayutthaya": "The magnificent ruins of Thailand's ancient capital, a UNESCO World Heritage city surrounded by rivers",
    "Hanoi": "Vietnam's charming capital with a maze-like Old Quarter, legendary street food, and French colonial flair",
    "Ho Chi Minh City": "Vietnam's bustling southern hub with war history, French architecture, and electric nightlife",
    "Da Nang": "A coastal city with stunning beaches, the iconic Dragon Bridge, and a gateway to ancient ruins",
    "Hoi An": "A magical lantern-lit ancient town with tailor shops, incredible food, and golden beaches nearby",
    "Nha Trang": "Vietnam's beach party capital with turquoise water, fresh seafood, and vibrant nightlife",
    "Sapa": "Misty mountain terraces and colorful hill tribe villages in Vietnam's far north",
    "Hue": "Vietnam's imperial city with a magnificent citadel, royal tombs, and river-side charm",
    "Seoul": "South Korea's high-tech capital where K-pop culture meets ancient palaces and incredible street food",
    "Busan": "Korea's coastal gem with colorful villages, stunning beaches, and famous fish markets",
    "Jeju": "A volcanic island paradise with dramatic hiking, pristine beaches, and unique local culture",
    "Gyeongju": "The museum without walls — Korea's ancient capital filled with tombs, temples, and pagodas",
    "Jeonju": "Korea's food capital, famous for bibimbap and a beautifully preserved traditional village",
    "Bali": "Indonesia's Island of the Gods with rice terraces, surf breaks, temples, and spiritual retreats",
    "Yogyakarta": "Java's cultural soul with the magnificent Borobudur temple and vibrant arts scene",
    "Jakarta": "Indonesia's massive, chaotic capital with great food, nightlife, and island escapes nearby",
    "Lombok": "Bali's less-touristy neighbor with a towering volcano, paradise beaches, and the Gili Islands",
    "Komodo": "Home of the legendary Komodo dragons, pink sand beaches, and world-class diving",
    "Raja Ampat": "The crown jewel of marine biodiversity — remote islands with the planet's best coral reefs",
    "Delhi": "India's sprawling capital where Mughal monuments, chaotic bazaars, and diverse cuisines collide",
    "Jaipur": "The Pink City of Rajasthan with stunning forts, colorful bazaars, and royal heritage",
    "Mumbai": "India's city of dreams — Bollywood, colonial grandeur, and the country's best street food",
    "Goa": "India's beach paradise with golden sands, Portuguese heritage, and legendary parties",
    "Varanasi": "The world's oldest living city, where sacred rituals unfold along the holy Ganges",
    "Udaipur": "The City of Lakes — a romantic Rajasthani gem with floating palaces and sunset views",
    "Kerala": "God's Own Country with tranquil backwaters, spice plantations, and Ayurvedic wellness",
    "Rishikesh": "The yoga capital of the world, nestled in the Himalayas along the sacred Ganges",
    "Agra": "Home of the Taj Mahal — one of the world's most iconic monuments of love",
    "Siem Reap": "Gateway to the awe-inspiring Angkor Wat temple complex, Cambodia's crown jewel",
    "Phnom Penh": "Cambodia's capital blending royal palaces, sobering history, and a thriving riverside scene",
    "Kampot": "A quiet riverside town known for world-famous pepper, French architecture, and cave explorations",
    "Manila": "The Philippines' vibrant capital with historic Intramuros, wild nightlife, and incredible food",
    "Cebu": "An island hub with whale sharks, stunning waterfalls, and a mix of history and beach vibes",
    "Palawan": "One of the world's most beautiful islands with underground rivers and crystal lagoons",
    "Siargao": "The Philippines' surf capital with a laid-back island vibe and stunning natural pools",
    "Boracay": "A tiny island famous for its powdery White Beach and vibrant party scene",
    "Kuala Lumpur": "Malaysia's modern capital where towering skyscrapers meet bustling street food markets",
    "Penang": "A UNESCO heritage island with the best street food in Southeast Asia and colorful street art",
    "Langkawi": "A duty-free island paradise with sky bridges, mangroves, and beautiful beaches",
    "Malacca": "A charming historic port city with Dutch-Portuguese heritage and famous Jonker Street",
    "Borneo": "A wild jungle island home to orangutans, Mount Kinabalu, and incredible biodiversity",
    "Beijing": "China's imperial capital with the Great Wall, Forbidden City, and centuries of dynastic grandeur",
    "Shanghai": "China's dazzling modern metropolis where Art Deco meets futuristic skylines on the Bund",
    "Xi'an": "Home of the Terracotta Warriors and the starting point of the ancient Silk Road",
    "Chengdu": "The home of giant pandas and fiery Sichuan cuisine in a laid-back, tea-loving city",
    "Guilin": "Otherworldly karst landscapes along the Li River — one of China's most photographed regions",
    "Hong Kong": "A dazzling East-meets-West metropolis of harbor views, dim sum, and neon-lit streets",
    "Taipei": "A food lover's paradise with incredible night markets, hot springs, and lush mountain trails",
    "Kaohsiung": "Taiwan's sunny southern port city with great seafood, temples, and a vibrant arts scene",
    "Tainan": "Taiwan's oldest city and culinary capital, packed with temples and traditional street food",
    "Jiufen": "A hillside village of narrow alleys and tea houses that inspired the world of Spirited Away",
    "Sun Moon Lake": "Taiwan's most scenic lake surrounded by temples, cycling paths, and misty mountains",
    "Colombo": "Sri Lanka's energetic capital with colonial charm, colorful temples, and bustling markets",
    "Kandy": "The hill country gem housing the sacred Temple of the Tooth amid lush botanical gardens",
    "Ella": "A tiny mountain village with epic train rides, misty hikes, and the famous Nine Arches Bridge",
    "Galle": "A UNESCO-listed Dutch fort town on Sri Lanka's southern coast with beautiful beaches",
    "Sigiriya": "An ancient rock fortress rising from the jungle — Sri Lanka's most dramatic landmark",
    "Kathmandu": "Nepal's vibrant capital where ancient stupas, bustling bazaars, and Himalayan culture meet",
    "Pokhara": "The gateway to the Annapurna trek with a serene lakeside setting and paragliding paradise",
    "Chitwan": "A subtropical jungle park where you can spot rhinos and tigers on safari",
    "Yangon": "Myanmar's largest city crowned by the golden Shwedagon Pagoda, a spiritual wonder",
    "Bagan": "An ancient plain dotted with over 2,000 temples — best seen by hot air balloon at sunrise",
    "Mandalay": "Myanmar's cultural capital with royal palaces, monastery-filled hills, and the iconic U Bein Bridge",
    "Inle Lake": "A magical lake where fishermen row with one leg among floating gardens and stilt villages",
    "Luang Prabang": "A UNESCO gem where saffron-robed monks collect alms at dawn beside French colonial streets",
    "Vientiane": "The world's most laid-back capital, with riverside temples and a slow-paced charm",
    "Vang Vieng": "A riverside adventure town with limestone caves, blue lagoons, and stunning karst scenery",
    "Ulaanbaatar": "Mongolia's capital — a gateway to vast steppes, nomadic culture, and the Gobi Desert",
    "Gobi Desert": "One of Earth's last great wildernesses with towering dunes, dinosaur fossils, and nomad camps",
    "Samarkand": "A Silk Road jewel with turquoise-tiled mosques and some of Central Asia's grandest architecture",
    "Bukhara": "An ancient Silk Road oasis city with stunning madrasas, trading domes, and centuries of history",
    "Tashkent": "Uzbekistan's modern capital blending Soviet-era architecture with vibrant bazaars",
    "Tbilisi": "Georgia's enchanting capital with cobblestone streets, sulfur baths, natural wine, and eclectic nightlife",
    "Batumi": "A lively Black Sea resort town with bold modern architecture and charming old streets",
    "Kazbegi": "A remote mountain village with jaw-dropping views of Mount Kazbek and the iconic Gergeti Church",
    "Amman": "Jordan's welcoming capital with Roman ruins, incredible food, and a growing arts scene",
    "Petra": "The Rose City — an ancient wonder carved into pink sandstone cliffs by the Nabataeans",
    "Wadi Rum": "The Valley of the Moon — a vast desert of red sand, rock arches, and Bedouin camps",
    "Muscat": "Oman's elegant capital with grand mosques, mountain-backed coastlines, and warm hospitality",
    "Nizwa": "A historic oasis town with a massive fort, traditional goat markets, and mountain treks",
    "Male": "The Maldives' tiny island capital — gateway to overwater bungalows and coral-reef paradise",
    "Ari Atoll": "A remote Maldivian paradise with whale shark encounters and pristine coral reefs",
    "Thimphu": "Bhutan's unique capital where traditional Buddhist culture thrives in the shadow of Himalayas",
    "Paro": "Home of the legendary Tiger's Nest monastery perched on a Himalayan cliff face",
    "Paris": "The City of Light — timeless romance, world-class art, and legendary cuisine",
    "Nice": "The sparkling jewel of the French Riviera with azure waters, vibrant markets, and promenades",
    "Lyon": "France's gastronomic capital with Renaissance architecture and a thriving food scene",
    "Marseille": "France's oldest city with a gritty charm, stunning calanques, and vibrant Mediterranean energy",
    "Bordeaux": "World wine capital with elegant architecture, riverside charm, and exceptional gastronomy",
    "Strasbourg": "A Franco-German gem with a fairy-tale old town, soaring cathedral, and legendary Christmas markets",
    "Rome": "The Eternal City where ancient ruins, Renaissance art, and la dolce vita come together",
    "Florence": "The birthplace of the Renaissance — a living museum of art, architecture, and Tuscan cuisine",
    "Venice": "A floating city of canals, gondolas, and centuries of artistic and architectural splendor",
    "Amalfi Coast": "Italy's most dramatic coastline with pastel villages clinging to cliffs above azure waters",
    "Milan": "Italy's fashion and design capital with world-class shopping, art treasures, and sleek nightlife",
    "Cinque Terre": "Five colorful fishing villages connected by coastal hiking trails along the Italian Riviera",
    "Naples": "The birthplace of pizza, a chaotic city of underground ruins and passionate culture",
    "Sicily": "Italy's largest island with Greek temples, active volcanoes, and some of the country's best food",
    "Barcelona": "Gaudi's playground — a vibrant Mediterranean city of art, beaches, tapas, and nightlife",
    "Madrid": "Spain's elegant capital with world-class museums, tapas culture, and legendary nightlife",
    "Seville": "The soul of Andalusia with flamenco, Moorish palaces, and intoxicating orange-blossom scent",
    "Granada": "Home of the Alhambra — a Moorish masterpiece nestled below the snow-capped Sierra Nevada",
    "San Sebastian": "The culinary capital of Spain with stunning beaches and world-renowned pintxos bars",
    "Valencia": "A Mediterranean city of futuristic architecture, paella birthplace, and golden beaches",
    "Malaga": "A sun-soaked coastal city with Picasso heritage, great beaches, and vibrant food scene",
    "Lisbon": "Portugal's sun-drenched capital of pastel-colored neighborhoods, fado music, and pasteis de nata",
    "Porto": "A riverside city of port wine cellars, azulejo tiles, and breathtaking bridges",
    "Algarve": "Portugal's southern coast with dramatic sea caves, golden cliffs, and family-friendly beaches",
    "Sintra": "A fairy-tale town of whimsical palaces and enchanted gardens in the misty hills near Lisbon",
    "Madeira": "A lush Atlantic island of levada walks, dramatic cliffs, and year-round mild weather",
    "Azores": "Remote volcanic islands in the mid-Atlantic with hot springs, whale watching, and crater lakes",
    "Athens": "The cradle of Western civilization, crowned by the Acropolis and alive with modern Greek energy",
    "Santorini": "The iconic Greek island of blue-domed churches, caldera sunsets, and volcanic beaches",
    "Thessaloniki": "Greece's vibrant second city with Byzantine heritage, great food, and waterfront nightlife",
    "Crete": "Greece's largest island with ancient palaces, dramatic gorges, and beautiful beaches",
    "Mykonos": "The glamorous Greek island of whitewashed alleys, legendary parties, and turquoise waters",
    "Rhodes": "A medieval island fortress with beautiful beaches, ancient ruins, and a lively old town",
    "Dubrovnik": "The Pearl of the Adriatic — a stunning walled city of marble streets and Game of Thrones fame",
    "Split": "A living ancient Roman palace turned vibrant Croatian city on the Dalmatian coast",
    "Zagreb": "Croatia's underrated capital with a thriving café culture, quirky museums, and Art Nouveau charm",
    "Hvar": "A sun-drenched Croatian island with lavender fields, hidden coves, and chic summer nightlife",
    "Plitvice": "A cascade of 16 terraced lakes connected by waterfalls in one of Europe's most beautiful parks",
    "Prague": "The City of a Hundred Spires — fairy-tale architecture, craft beer, and enchanting old town",
    "Cesky Krumlov": "A fairy-tale town wrapped around a river bend with a stunning medieval castle",
    "Brno": "Czech Republic's second city with underground tunnels, creative culture, and great nightlife",
    "Amsterdam": "A canal-laced city of world-class museums, cycling culture, and legendary tolerance",
    "Rotterdam": "Europe's architecture capital with futuristic buildings, great food halls, and creative energy",
    "Utrecht": "A charming Dutch canal city with unique wharf cellars turned cafés and restaurants",
    "Berlin": "A city of creative reinvention with world-class clubs, street art, Cold War history, and diversity",
    "Munich": "Bavaria's cosmopolitan capital with beer gardens, Alpine proximity, and cultural riches",
    "Hamburg": "Germany's maritime metropolis with a legendary harbor, Reeperbahn nightlife, and great music",
    "Cologne": "A vibrant Rhine city dominated by its magnificent Gothic cathedral and Carnival traditions",
    "Dresden": "The Florence of the Elbe — a Baroque masterpiece reborn from wartime devastation",
    "Istanbul": "Where East meets West — a city of grand mosques, bustling bazaars, and Bosphorus views",
    "Cappadocia": "A surreal landscape of fairy chimneys, cave hotels, and sunrise hot air balloon rides",
    "Antalya": "Turkey's turquoise coast resort capital with a charming old town and nearby ancient ruins",
    "Izmir": "Turkey's laid-back Aegean city with a vibrant waterfront, great bazaars, and nearby ruins",
    "Ephesus": "One of the best-preserved ancient cities in the world, a monument to Greek and Roman grandeur",
    "London": "A global capital of culture, history, theater, and some of the world's greatest museums",
    "Edinburgh": "Scotland's dramatic capital with a hilltop castle, literary heritage, and world-famous festivals",
    "Bath": "An elegant Georgian city built around ancient Roman baths and natural hot springs",
    "Liverpool": "The birthplace of the Beatles with a proud maritime heritage and thriving cultural scene",
    "Highlands": "Scotland's wild and majestic landscape of lochs, glens, castles, and endless moors",
    "Isle of Skye": "A rugged Scottish island of otherworldly landscapes, fairy pools, and dramatic sea cliffs",
    "Zurich": "Switzerland's cosmopolitan lakeside city with a charming old town and Alpine panoramas",
    "Interlaken": "The adventure capital of Switzerland, set between two lakes with stunning Alpine peaks",
    "Lucerne": "A picture-perfect Swiss city with a medieval bridge, lakeside setting, and mountain excursions",
    "Zermatt": "A car-free Alpine village with world-class skiing and iconic Matterhorn views",
    "Vienna": "The imperial city of Mozart, grand palaces, Viennese cafés, and classical music",
    "Salzburg": "Mozart's birthplace — a Baroque gem nestled among Alpine peaks with Sound of Music charm",
    "Innsbruck": "A compact Alpine city with world-class skiing, Habsburg architecture, and mountain views",
    "Budapest": "A grand European capital split by the Danube, with thermal baths, ruin bars, and Art Nouveau",
    "Eger": "A charming Hungarian town with a historic castle, thermal baths, and the Valley of Beautiful Women",
    "Krakow": "Poland's cultural jewel with a stunning medieval square, Jewish heritage, and vibrant nightlife",
    "Warsaw": "Poland's resilient capital, meticulously rebuilt after WWII with a buzzing modern food scene",
    "Gdansk": "A Baltic port city with colorful waterfront architecture, amber markets, and WWII history",
    "Wroclaw": "The Venice of Poland — a charming city of bridges, islands, and hidden dwarf statues",
    "Bucharest": "Romania's lively capital with a massive palace, vibrant nightlife, and Art Nouveau streets",
    "Brasov": "A picturesque Transylvanian city at the foot of the Carpathians near Dracula's castle",
    "Cluj-Napoca": "Romania's youthful cultural capital with a thriving arts and music festival scene",
    "Sibiu": "A beautifully preserved Transylvanian gem with colorful squares and medieval fortifications",
    "Sofia": "Bulgaria's affordable capital with ancient ruins, mountain backdrop, and a growing food scene",
    "Plovdiv": "One of Europe's oldest cities with a Roman amphitheater and vibrant arts district",
    "Veliko Tarnovo": "Bulgaria's medieval capital perched dramatically on three hills above a winding river",
    "Kotor": "A medieval walled town at the head of a spectacular fjord-like bay in Montenegro",
    "Budva": "Montenegro's premier beach town with a charming old town and lively summer nightlife",
    "Tirana": "Albania's colorful, fast-changing capital with quirky museums and an emerging food scene",
    "Saranda": "Albania's Riviera gem with crystal waters, ancient ruins, and unspoiled Mediterranean charm",
    "Berat": "The City of a Thousand Windows — an Ottoman-era treasure clinging to a hillside in Albania",
    "Ljubljana": "Slovenia's fairy-tale capital with a castle-topped hill, emerald river, and café-lined streets",
    "Bled": "A postcard-perfect Alpine lake with a tiny island church and a cliffside medieval castle",
    "Piran": "A charming Venetian-style town on the Slovenian coast with narrow alleys and seafood",
    "Tallinn": "A perfectly preserved medieval Old Town meets cutting-edge digital culture in Estonia's capital",
    "Tartu": "Estonia's intellectual heart — a charming university town with bohemian energy",
    "Riga": "Latvia's capital with the finest Art Nouveau architecture in Europe and a vibrant old town",
    "Vilnius": "Lithuania's Baroque capital with a bohemian soul and one of Europe's largest old towns",
    "Copenhagen": "Scandinavia's coolest capital with world-leading food, design, and cycling culture",
    "Stockholm": "Sweden's stunning capital spread across 14 islands with incredible museums and Nordic design",
    "Gothenburg": "Sweden's friendly west coast city with a great food scene, archipelago, and theme parks",
    "Oslo": "Norway's green capital surrounded by fjords and forests with world-class art museums",
    "Bergen": "Norway's gateway to the fjords with colorful wooden wharf houses and mountain hiking",
    "Tromso": "The gateway to the Arctic — Northern Lights, midnight sun, and whale watching in Norway",
    "Lofoten": "Norway's dramatic Arctic archipelago of fishing villages, peaks, and Northern Lights",
    "Helsinki": "Finland's design capital on the Baltic Sea with saunas, architecture, and island hopping",
    "Rovaniemi": "The official hometown of Santa Claus on the Arctic Circle, with Northern Lights and huskies",
    "Reykjavik": "The world's northernmost capital with hot springs, Northern Lights, and raw natural beauty",
    "Vik": "Iceland's southernmost village with a legendary black sand beach and dramatic sea stacks",
    "Akureyri": "The capital of North Iceland with whale watching, waterfalls, and midnight sun",
    "Dublin": "Ireland's literary capital with legendary pubs, Georgian architecture, and warm hospitality",
    "Galway": "Ireland's bohemian west coast city with live music, colorful streets, and wild Atlantic views",
    "Cork": "Ireland's foodie capital with a famous English Market and gateway to Blarney Castle",
    "Brussels": "The heart of Europe with Art Nouveau splendor, chocolate shops, and world-famous waffles",
    "Bruges": "A medieval masterpiece of canals, cobblestones, and chocolate in the heart of Flanders",
    "Ghent": "A vibrant Flemish city with a stunning medieval skyline and one of Europe's best food scenes",
    "Valletta": "One of Europe's smallest capitals, packed with Baroque architecture and Mediterranean charm",
    "Nicosia": "The world's last divided capital, where Greek and Turkish cultures meet across a border",
    "Paphos": "Cyprus's sun-drenched coast with ancient mosaics, mythological sites, and clear waters",
    "Bogota": "Colombia's high-altitude capital with world-class street art, museums, and Andean cuisine",
    "Medellin": "The City of Eternal Spring — once infamous, now a beacon of innovation and creativity",
    "Cartagena": "A Caribbean fairy tale of colonial walls, cobblestone plazas, and salsa-filled nights",
    "Santa Marta": "Colombia's oldest city with Caribbean beaches and the gateway to the Lost City trek",
    "Salento": "A colorful Coffee Country village surrounded by towering wax palms in the Cocora Valley",
    "Lima": "South America's gastronomic capital with world-class ceviche and a vibrant colonial center",
    "Cusco": "The ancient Inca capital and gateway to Machu Picchu, high in the Peruvian Andes",
    "Arequipa": "The White City built of volcanic stone with the spectacular Colca Canyon nearby",
    "Sacred Valley": "The heartland of the Inca Empire with terraces, markets, and mountain-framed villages",
    "Huacachina": "A desert oasis surrounded by massive sand dunes — Peru's adventure playground",
    "Buenos Aires": "The Paris of South America with tango, incredible steak, and passionate nightlife",
    "Mendoza": "Argentina's wine country capital set dramatically against the Andes mountain backdrop",
    "Bariloche": "Argentina's Alpine-style lake district with chocolate shops, hiking, and Patagonian views",
    "Salta": "A colonial gem in Argentina's northwest with colorful landscapes and indigenous culture",
    "Ushuaia": "The End of the World — Earth's southernmost city and gateway to Antarctica",
    "El Calafate": "Gateway to the spectacular Perito Moreno Glacier in Argentine Patagonia",
    "Rio de Janeiro": "Brazil's Marvelous City with iconic beaches, Carnival, samba, and Christ the Redeemer",
    "Sao Paulo": "South America's largest city with an incredible food scene, nightlife, and street art",
    "Salvador": "The heart of Afro-Brazilian culture with colorful colonial streets and infectious rhythms",
    "Florianopolis": "A Brazilian island city with 42 beaches, world-class surfing, and vibrant nightlife",
    "Iguazu": "One of the world's most spectacular waterfalls straddling the Brazil-Argentina border",
    "Paraty": "A perfectly preserved colonial town between mountains and sea on Brazil's Gold Coast",
    "Santiago": "Chile's cosmopolitan capital nestled between the Andes and the coast with great wine",
    "Valparaiso": "Chile's bohemian port city with colorful street art, funiculars, and Pacific views",
    "Torres del Paine": "Patagonia's crown jewel — towering granite peaks, glaciers, and pristine wilderness",
    "Atacama": "The world's driest desert with otherworldly landscapes, geysers, and pristine stargazing",
    "Pucon": "Chile's adventure capital with a snow-capped volcano, hot springs, and lakeside charm",
    "Quito": "Ecuador's high-altitude capital with the best-preserved colonial center in South America",
    "Cuenca": "A UNESCO gem of colonial churches, flower markets, and Panama hat workshops in Ecuador",
    "Galapagos": "Evolution's living laboratory — a volcanic archipelago of fearless wildlife and pristine waters",
    "Banos": "Ecuador's adventure gateway with the famous Swing at the End of the World and hot springs",
    "Montanita": "Ecuador's surf and party town on the Pacific coast with yoga and beach vibes",
    "La Paz": "The world's highest capital set in a dramatic Andean valley with chaotic markets and cable cars",
    "Uyuni": "Home of the world's largest salt flat — a surreal white expanse and photographer's dream",
    "Sucre": "Bolivia's constitutional capital — a quiet colonial city known as the White City",
    "Copacabana": "A lakeside pilgrimage town on the shores of Lake Titicaca with Isla del Sol nearby",
    "Montevideo": "Uruguay's laid-back capital with a beautiful riverfront promenade and great steak culture",
    "Colonia": "A charming UNESCO colonial outpost across the river from Buenos Aires",
    "Punta del Este": "South America's glitziest beach resort with art, surf, and summer nightlife",
    "Asuncion": "Paraguay's quiet capital on the river with colonial history and a vibrant street food scene",
    "San Jose": "Costa Rica's often-overlooked capital with interesting museums and a vibrant market",
    "Monteverde": "A cloud forest wonderland with hanging bridges, zip lines, and incredible biodiversity",
    "Manuel Antonio": "A national park paradise with white sand beaches, monkey-filled forests, and easy trails",
    "La Fortuna": "A jungle town at the base of Arenal Volcano with hot springs and waterfall hikes",
    "Panama City": "A modern skyline meets colonial charm at the crossroads of the Americas",
    "Bocas del Toro": "A Caribbean archipelago of colorful wooden houses, reef snorkeling, and island parties",
    "San Blas": "Pristine island paradise managed by the indigenous Guna people with unmatched seclusion",
    "Antigua": "Guatemala's colonial crown jewel with cobblestone streets, volcanoes, and coffee plantations",
    "Lake Atitlan": "A breathtaking volcanic lake ringed by Mayan villages and towering volcanoes",
    "Tikal": "The jungle-shrouded ruins of an ancient Mayan superpower rising above the treetops",
    "Mexico City": "One of the world's greatest cities with ancient ruins, world-class food, and incredible art",
    "Oaxaca": "Mexico's culinary and cultural capital with mezcal, mole, ancient ruins, and textile arts",
    "Tulum": "Mayan cliff-top ruins overlooking Caribbean waters, with cenotes and bohemian beach clubs",
    "San Cristobal": "A highland colonial town in Chiapas surrounded by indigenous Mayan villages and canyons",
    "Guanajuato": "A kaleidoscope of color built into a canyon with underground streets and vibrant culture",
    "Puerto Vallarta": "A Pacific beach resort with a charming old town, whale watching, and great food",
    "Merida": "The gateway to the Yucatan's Mayan wonders with cenotes, haciendas, and warm hospitality",
    "Marrakech": "Morocco's sensory overload — a swirl of spices, souks, snake charmers, and stunning riads",
    "Fes": "The world's largest car-free urban area with a medieval medina and centuries-old leather tanneries",
    "Chefchaouen": "Morocco's famous Blue City nestled in the Rif Mountains with a serene, photogenic medina",
    "Essaouira": "A windswept Atlantic port town with a bohemian vibe, fresh seafood, and art galleries",
    "Merzouga": "The gateway to Morocco's Sahara Desert with towering sand dunes and starlit desert camps",
    "Cape Town": "One of the world's most beautiful cities with Table Mountain, wine lands, and Cape Point",
    "Johannesburg": "South Africa's largest city with powerful history, vibrant arts, and township culture",
    "Durban": "A warm Indian Ocean city with great surfing, Zulu culture, and spicy curry heritage",
    "Stellenbosch": "South Africa's wine country gem with oak-lined streets and world-class estates",
    "Kruger": "Africa's premier safari destination with the Big Five in vast bushveld landscapes",
    "Dar es Salaam": "Tanzania's largest city and gateway to Zanzibar with bustling markets and beaches",
    "Zanzibar": "A spice island paradise with Stone Town's winding alleys, pristine beaches, and rich history",
    "Arusha": "The safari capital of Tanzania and gateway to Kilimanjaro and the Serengeti",
    "Serengeti": "Africa's most iconic safari — endless plains, the Great Migration, and balloon rides at dawn",
    "Nairobi": "Kenya's dynamic capital with wildlife parks within city limits and a thriving food scene",
    "Mombasa": "Kenya's coastal gateway with Indian Ocean beaches, Swahili culture, and historic forts",
    "Masai Mara": "Kenya's legendary wildlife reserve — home to the Great Migration and Maasai culture",
    "Lamu": "A car-free Swahili island of narrow alleys, dhow sailing, and centuries of coastal culture",
    "Cairo": "The city of a thousand minarets where the Pyramids of Giza meet a chaotic modern metropolis",
    "Luxor": "The world's greatest open-air museum with temples and tombs of ancient Egyptian pharaohs",
    "Aswan": "A laid-back Nile city with Nubian villages, felucca sailing, and the gateway to Abu Simbel",
    "Dahab": "A chilled-out Red Sea dive town with world-class snorkeling and a Sinai Desert backdrop",
    "Alexandria": "Egypt's Mediterranean jewel with a legendary library, coastal charm, and cosmopolitan heritage",
    "Accra": "Ghana's vibrant capital with lively markets, Atlantic beaches, and a thriving arts scene",
    "Cape Coast": "A historic Ghanaian town with slave fort heritage and canopy walks through the rainforest",
    "Kumasi": "The Ashanti Kingdom's cultural hub with the largest open-air market in West Africa",
    "Kigali": "Africa's cleanest city — Rwanda's modern capital with a powerful genocide memorial",
    "Volcanoes NP": "One of the last places on Earth to see mountain gorillas in their misty forest home",
    "Addis Ababa": "Ethiopia's high-altitude capital with unique cuisine, ancient coffee culture, and jazz",
    "Lalibela": "Home of Ethiopia's incredible rock-hewn churches — the Jerusalem of Africa",
    "Gondar": "The Camelot of Africa with a royal fortress complex and gateway to the Simien Mountains",
    "Windhoek": "Namibia's small, clean capital with German colonial heritage and African energy",
    "Sossusvlei": "The world's tallest sand dunes in a surreal red desert landscape of Namibia",
    "Swakopmund": "A quirky German colonial town where the desert meets the Atlantic in Namibia",
    "Etosha": "A vast salt pan surrounded by waterholes that draw incredible concentrations of African wildlife",
    "Maun": "The gateway to the Okavango Delta — Botswana's safari launch pad",
    "Okavango Delta": "One of Earth's last great wetland wildernesses — a labyrinth of channels and islands",
    "Chobe": "Botswana's elephant capital with incredible river safaris and massive wildlife concentrations",
    "Dakar": "Senegal's vibrant Atlantic capital with a thriving music scene, art, and West African cuisine",
    "Saint-Louis": "A faded colonial island town with jazz heritage and dramatic Saharan landscapes nearby",
    "Antananarivo": "Madagascar's hilltop capital and gateway to lemurs, baobabs, and unique wildlife",
    "Nosy Be": "Madagascar's tropical island paradise with lemurs, snorkeling, and untouched beaches",
    "Port Louis": "Mauritius's multicultural capital with a bustling waterfront and vibrant market",
    "Grand Baie": "Mauritius's premier beach resort area with catamaran cruises and underwater wonders",
    "Tunis": "Tunisia's capital blending Arab medina culture with French colonial elegance and Roman ruins",
    "Sidi Bou Said": "A picture-perfect blue-and-white cliff-top village overlooking the Mediterranean",
    "Djerba": "A Mediterranean island of ancient synagogues, colorful souks, and flamingo-dotted lagoons",
    "Kampala": "Uganda's hilly capital with a vibrant market scene and gateway to gorilla trekking",
    "Bwindi": "An impenetrable forest sheltering half the world's remaining mountain gorillas",
    "Sydney": "Australia's harbor city with the iconic Opera House, Bondi Beach, and a dynamic food scene",
    "Melbourne": "Australia's cultural capital with world-class coffee, street art laneways, and diverse food",
    "Cairns": "The gateway to the Great Barrier Reef and the ancient Daintree Rainforest in tropical Australia",
    "Perth": "Australia's sunniest city with beautiful beaches, wine regions, and adorable quokkas nearby",
    "Byron Bay": "Australia's bohemian beach town with surfing, yoga, and a laid-back creative spirit",
    "Auckland": "New Zealand's City of Sails with island hopping, volcanic hikes, and Polynesian culture",
    "Queenstown": "The adventure capital of the world with bungee jumping, fjords, and Alpine scenery",
    "Wellington": "New Zealand's compact capital with a thriving food and craft beer scene and hillside views",
    "Rotorua": "A geothermal wonderland of bubbling mud pools, geysers, and rich Maori culture",
    "Milford Sound": "A breathtaking fjord of towering cliffs, cascading waterfalls, and misty rainforest",
}

# ── Festivals ───────────────────────────────────────────────────────────────

FESTIVALS = {
    "Tokyo": ["Cherry Blossom Season (Mar-Apr)", "Sanja Matsuri (May)"],
    "Kyoto": ["Gion Matsuri (Jul)", "Aoi Matsuri (May)"],
    "Osaka": ["Tenjin Matsuri (Jul)", "Osaka Marathon (Nov)"],
    "Sapporo": ["Sapporo Snow Festival (Feb)"],
    "Bangkok": ["Songkran Water Festival (Apr)", "Loy Krathong (Nov)"],
    "Chiang Mai": ["Yi Peng Lantern Festival (Nov)", "Songkran (Apr)"],
    "Seoul": ["Cherry Blossom Festival (Apr)", "Seoul Lantern Festival (Nov)"],
    "Bali": ["Nyepi Day of Silence (Mar)", "Galungan Festival"],
    "Delhi": ["Diwali Festival of Lights (Oct-Nov)", "Holi Festival (Mar)"],
    "Mumbai": ["Ganesh Chaturthi (Aug-Sep)", "Diwali (Oct-Nov)"],
    "Varanasi": ["Dev Deepawali (Nov)", "Ganga Aarti (Daily)"],
    "Jaipur": ["Jaipur Literature Festival (Jan)", "Elephant Festival (Mar)"],
    "Hoi An": ["Full Moon Lantern Festival (Monthly)"],
    "Rio de Janeiro": ["Carnival (Feb-Mar)", "New Year's Eve at Copacabana"],
    "Salvador": ["Salvador Carnival (Feb-Mar)"],
    "Buenos Aires": ["Tango Festival (Aug)", "Carnival (Feb)"],
    "Cusco": ["Inti Raymi Festival of the Sun (Jun)"],
    "Oaxaca": ["Day of the Dead (Nov)", "Guelaguetza (Jul)"],
    "Mexico City": ["Day of the Dead (Nov)", "Independence Day (Sep)"],
    "Seville": ["Feria de Abril (Apr)", "Semana Santa (Mar-Apr)"],
    "Barcelona": ["La Merce Festival (Sep)", "Sant Jordi Day (Apr)"],
    "Venice": ["Venice Carnival (Feb)", "Venice Film Festival (Sep)"],
    "Munich": ["Oktoberfest (Sep-Oct)"],
    "Edinburgh": ["Edinburgh Fringe Festival (Aug)", "Hogmanay New Year (Dec)"],
    "Nice": ["Nice Carnival (Feb)"],
    "Dublin": ["St. Patrick's Festival (Mar)"],
    "Istanbul": ["Istanbul Tulip Festival (Apr)"],
    "Marrakech": ["Marrakech International Film Festival (Dec)"],
    "Cape Town": ["Cape Town Jazz Festival (Mar)"],
    "Nairobi": ["Lamu Cultural Festival (Nov)"],
    "Reykjavik": ["Iceland Airwaves Music Festival (Nov)"],
    "Tromso": ["Northern Lights Season (Sep-Mar)"],
    "Rovaniemi": ["Northern Lights Season (Sep-Mar)", "Midnight Sun (Jun-Jul)"],
    "Paris": ["Bastille Day (Jul 14)", "Nuit Blanche (Oct)"],
    "London": ["Notting Hill Carnival (Aug)", "Bonfire Night (Nov)"],
    "Berlin": ["Berlinale Film Festival (Feb)", "Karneval der Kulturen (May)"],
    "Amsterdam": ["King's Day (Apr 27)", "Amsterdam Light Festival (Dec-Jan)"],
    "Prague": ["Prague Spring Music Festival (May-Jun)"],
    "Budapest": ["Sziget Festival (Aug)", "Budapest Wine Festival (Sep)"],
    "Cologne": ["Cologne Carnival (Feb)"],
    "Copenhagen": ["Roskilde Festival (Jun-Jul)"],
    "Stockholm": ["Midsummer (Jun)"],
    "Lisbon": ["Santos Populares (Jun)", "Rock in Rio Lisboa (Jun)"],
    "Porto": ["Sao Joao Festival (Jun)"],
    "Athens": ["Athens Epidaurus Festival (Jun-Aug)"],
    "Dubrovnik": ["Dubrovnik Summer Festival (Jul-Aug)"],
    "Krakow": ["Wianki Midsummer Festival (Jun)"],
    "Galway": ["Galway International Arts Festival (Jul)"],
    "Zanzibar": ["Zanzibar International Film Festival (Jul)"],
    "Luang Prabang": ["Pi Mai Lao New Year (Apr)"],
    "Antigua": ["Semana Santa Holy Week (Mar-Apr)"],
    "Cartagena": ["Hay Festival Cartagena (Jan)"],
    "La Paz": ["Gran Poder Festival (May-Jun)"],
    "Santiago": ["Fiestas Patrias (Sep)"],
    "Medellin": ["Feria de las Flores (Aug)"],
    "Lima": ["Mistura Food Festival (Sep)"],
    "Tulum": ["Day of the Dead (Nov)"],
    "Merida": ["Hanal Pixan Day of the Dead (Nov)"],
    "Guanajuato": ["Festival Cervantino (Oct)"],
    "Granada": ["Corpus Christi (Jun)"],
    "Valencia": ["Las Fallas (Mar)"],
    "Thessaloniki": ["Thessaloniki Film Festival (Nov)"],
    "Split": ["Ultra Europe Music Festival (Jul)"],
    "Florence": ["Scoppio del Carro Easter (Apr)"],
    "Strasbourg": ["Christmas Market (Nov-Dec)"],
    "Bruges": ["Bruges Beer Festival (Feb)"],
    "Ghent": ["Gentse Feesten (Jul)"],
    "Tallinn": ["Tallinn Music Week (May)"],
    "Riga": ["Riga City Festival (Aug)"],
    "Vilnius": ["Vilnius Film Festival (Mar)"],
    "Helsinki": ["Helsinki Festival (Aug)"],
    "Bergen": ["Bergen International Festival (May-Jun)"],
    "Oslo": ["Constitution Day (May 17)"],
    "Agra": ["Taj Mahotsav (Feb)"],
    "Fes": ["Fes Festival of World Sacred Music (Jun)"],
    "Addis Ababa": ["Timkat Epiphany (Jan)", "Meskel Finding of the True Cross (Sep)"],
    "Lalibela": ["Genna Ethiopian Christmas (Jan)"],
    "Cairo": ["Cairo International Film Festival (Nov)"],
    "Taipei": ["Lantern Festival (Feb)", "Dragon Boat Festival (Jun)"],
    "Hong Kong": ["Chinese New Year (Jan-Feb)", "Mid-Autumn Festival (Sep)"],
    "Singapore": ["Chinese New Year (Jan-Feb)"],
    "Paro": ["Paro Tsechu (Mar-Apr)"],
}

# ── best_for ────────────────────────────────────────────────────────────────

def infer_best_for(name, data):
    tags = data.get("tags", [])
    cost = data.get("cost", 100)
    comfort = data.get("comfort", 3)
    best = []

    # Honeymoon
    if comfort >= 4 and any(t in tags for t in ["beaches", "wellness", "photography"]):
        best.append("honeymoon")
    if name in ["Santorini", "Maldives", "Male", "Ari Atoll", "Amalfi Coast", "Bali",
                 "Koh Samui", "Paris", "Venice", "Zanzibar", "Bora Bora", "Punta del Este"]:
        if "honeymoon" not in best:
            best.append("honeymoon")

    # Bucket list
    if name in ["Tokyo", "Machu Picchu", "Cusco", "Petra", "Bagan", "Angkor Wat",
                 "Siem Reap", "Galapagos", "Serengeti", "Masai Mara", "Torres del Paine",
                 "Iguazu", "Cappadocia", "Santorini", "Iceland", "Reykjavik", "Vik",
                 "Cairo", "Rome", "Paris", "Rio de Janeiro", "Uyuni", "Great Wall",
                 "Beijing", "Komodo", "Raja Ampat", "Tromso", "Lofoten", "Milford Sound",
                 "Atacama", "Sossusvlei", "Volcanoes NP", "Bwindi", "Kruger",
                 "Okavango Delta", "Chobe", "Lalibela", "El Calafate"]:
        best.append("bucket_list")

    # Digital nomad
    if cost <= 60 and comfort >= 3 and any(t in tags for t in ["food", "nightlife", "culture"]):
        best.append("digital_nomad")
    if name in ["Bali", "Chiang Mai", "Lisbon", "Medellin", "Tbilisi", "Bangkok",
                 "Ho Chi Minh City", "Budapest", "Prague", "Mexico City", "Tulum",
                 "Da Nang", "Hoi An", "Bogota", "Oaxaca"]:
        if "digital_nomad" not in best:
            best.append("digital_nomad")

    # Family
    if comfort >= 4 and cost <= 150:
        best.append("family")

    # Bachelor/ette
    if "nightlife" in tags and comfort >= 4:
        best.append("bachelor_ette")

    # Gap year
    if cost <= 50:
        best.append("gap_year")

    # Retirement
    if comfort >= 4 and cost <= 100 and any(t in tags for t in ["culture", "food", "wellness"]):
        best.append("retirement")

    # Just for fun (most places)
    best.append("just_for_fun")

    return best[:5]  # Cap at 5


# ── Crowd level inference ───────────────────────────────────────────────────

HIGH_TOURISM = {
    "Paris", "London", "Rome", "Barcelona", "Venice", "Amsterdam", "Prague",
    "Tokyo", "Bangkok", "Bali", "Dubai", "New York", "Istanbul",
    "Santorini", "Mykonos", "Dubrovnik", "Florence", "Milan", "Phuket",
    "Marrakech", "Cairo", "Cusco", "Rio de Janeiro", "Sydney", "Hong Kong",
    "Singapore", "Machu Picchu", "Amalfi Coast", "Hvar",
}

def infer_crowd(name, data):
    if name in HIGH_TOURISM:
        return 5
    size = CITY_SIZE.get(name, "small_city")
    if size == "mega_city":
        return 5
    if size == "large_city":
        return 4
    if size == "small_city":
        return 3
    if size == "small_town":
        return 2
    return 1  # village


# ── Build enriched dict ─────────────────────────────────────────────────────

def enrich():
    enriched = {}
    for name, data in CITIES.items():
        country = data["country"]
        tags = data.get("tags", [])
        d = dict(data)  # copy

        d["description"] = DESCRIPTIONS.get(name, f"A captivating destination in {country} with unique culture and attractions")
        d["language"] = LANGUAGE.get(country, "Local language")
        d["safety"] = SAFETY.get(country, 3)
        d["wifi"] = WIFI.get(country, 3)
        d["vegetarian_friendly"] = VEG_FRIENDLY.get(country, 3)
        d["crowd_level"] = infer_crowd(name, data)
        d["city_size"] = CITY_SIZE.get(name, "small_city")

        # Beach type
        if name in BEACH_TYPE:
            d["beach_type"] = BEACH_TYPE[name]
        elif "beaches" in tags:
            d["beach_type"] = "mixed"
        else:
            d["beach_type"] = None

        # Terrain
        if name in TERRAIN:
            d["terrain"] = TERRAIN[name]
        elif "beaches" in tags or "island" in str(tags):
            d["terrain"] = "coastal"
        elif "hiking" in tags and data.get("weather") == "cold":
            d["terrain"] = "mountain"
        else:
            d["terrain"] = "flat"

        d["festivals"] = FESTIVALS.get(name, [])
        d["best_for"] = infer_best_for(name, data)

        enriched[name] = d
    return enriched


def write_cities_file(enriched):
    lines = ["CITIES = {\n"]
    for name, d in enriched.items():
        lines.append(f'    "{name}": {{\n')
        # Original fields first
        lines.append(f'        "country": {repr(d["country"])}, "region": {repr(d["region"])}, '
                     f'"lat": {d["lat"]}, "lon": {d["lon"]}, "cost": {d["cost"]},\n')
        lines.append(f'        "months": {d["months"]}, '
                     f'"tags": {d["tags"]},\n')
        lines.append(f'        "comfort": {d["comfort"]}, "weather": {repr(d["weather"])}, '
                     f'"highlights": {d["highlights"]},\n')
        # New fields
        lines.append(f'        "description": {repr(d["description"])},\n')
        lines.append(f'        "language": {repr(d["language"])}, "safety": {d["safety"]}, '
                     f'"wifi": {d["wifi"]}, "vegetarian_friendly": {d["vegetarian_friendly"]},\n')
        lines.append(f'        "crowd_level": {d["crowd_level"]}, '
                     f'"city_size": {repr(d["city_size"])},\n')
        lines.append(f'        "beach_type": {repr(d["beach_type"])}, '
                     f'"terrain": {repr(d["terrain"])},\n')
        lines.append(f'        "festivals": {d["festivals"]},\n')
        lines.append(f'        "best_for": {d["best_for"]},\n')
        lines.append(f'    }},\n')
    lines.append("}\n")

    outpath = os.path.join(os.path.dirname(__file__), "cities.py")
    with open(outpath, "w") as f:
        f.writelines(lines)
    print(f"Wrote enriched cities.py with {len(enriched)} cities")


if __name__ == "__main__":
    enriched = enrich()
    write_cities_file(enriched)
