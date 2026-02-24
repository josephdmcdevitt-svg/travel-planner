#!/usr/bin/env python3
"""Builder script: adds 7 new detail fields to all 326 cities in cities.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from cities import CITIES

# ── Country-level Uber costs (USD per typical ride) ──────────────────────────
COUNTRY_UBER_COST = {
    "Japan": 15, "Thailand": 4, "Vietnam": 3, "South Korea": 8, "Indonesia": 3,
    "India": 3, "Cambodia": 4, "Philippines": 3, "Malaysia": 4, "China": 5,
    "Taiwan": 6, "Sri Lanka": 3, "Nepal": 3, "Myanmar": 3, "Laos": 4,
    "Mongolia": 4, "Uzbekistan": 3, "Georgia": 3, "Jordan": 6, "Oman": 8,
    "Maldives": 10, "Bhutan": 8, "France": 15, "Italy": 12, "Spain": 10,
    "Portugal": 8, "Greece": 7, "Croatia": 8, "Czech Republic": 6,
    "Netherlands": 12, "Germany": 12, "Turkey": 4, "United Kingdom": 15,
    "Switzerland": 25, "Austria": 12, "Hungary": 5, "Poland": 5,
    "Romania": 4, "Bulgaria": 3, "Montenegro": 5, "Albania": 3,
    "Slovenia": 8, "Estonia": 6, "Latvia": 5, "Lithuania": 5,
    "Denmark": 18, "Sweden": 16, "Norway": 20, "Finland": 15, "Iceland": 22,
    "Ireland": 12, "Belgium": 12, "Malta": 8, "Cyprus": 8,
    "Colombia": 3, "Peru": 4, "Argentina": 4, "Brazil": 5, "Chile": 6,
    "Ecuador": 3, "Bolivia": 3, "Uruguay": 8, "Paraguay": 3,
    "Costa Rica": 5, "Panama": 5, "Guatemala": 4, "Mexico": 4,
    "Morocco": 3, "South Africa": 5, "Tanzania": 5, "Kenya": 5, "Egypt": 3,
    "Ghana": 4, "Rwanda": 4, "Ethiopia": 3, "Namibia": 8, "Botswana": 8,
    "Senegal": 4, "Madagascar": 3, "Mauritius": 6, "Tunisia": 3, "Uganda": 4,
    "Australia": 15, "New Zealand": 14,
}

CITY_UBER_OVERRIDE = {
    "Tokyo": 18, "Singapore": 10, "Hong Kong": 8, "Seoul": 10,
    "London": 18, "Paris": 18, "Zurich": 30, "Zermatt": 35,
    "New York": 20, "Dubai": 8, "Oslo": 22, "Reykjavik": 25,
    "Sydney": 18, "Melbourne": 16, "Copenhagen": 20, "Stockholm": 18,
    "Amsterdam": 15, "Munich": 14, "Rome": 14, "Barcelona": 12,
    "Istanbul": 3, "Bangkok": 3, "Bali": 2, "Hanoi": 2,
    "Ho Chi Minh City": 2, "Chiang Mai": 3, "Siem Reap": 3,
    "Buenos Aires": 3, "Mexico City": 3, "Lima": 3, "Bogota": 2,
    "Cairo": 2, "Marrakech": 2, "Cape Town": 4, "Nairobi": 4,
    "Queenstown": 18, "Interlaken": 28, "Lucerne": 28,
    "Male": 5, "Ari Atoll": 15, "Ushuaia": 8, "Galapagos": 12,
}

# ── Country-level Airbnb costs (USD per night, whole place) ──────────────────
COUNTRY_AIRBNB_COST = {
    "Japan": 120, "Thailand": 40, "Vietnam": 35, "South Korea": 80, "Indonesia": 45,
    "India": 30, "Cambodia": 30, "Philippines": 35, "Malaysia": 40, "China": 50,
    "Taiwan": 60, "Sri Lanka": 35, "Nepal": 25, "Myanmar": 35, "Laos": 30,
    "Mongolia": 35, "Uzbekistan": 25, "Georgia": 35, "Jordan": 60, "Oman": 80,
    "Maldives": 200, "Bhutan": 100, "France": 120, "Italy": 110, "Spain": 90,
    "Portugal": 80, "Greece": 80, "Croatia": 80, "Czech Republic": 70,
    "Netherlands": 130, "Germany": 100, "Turkey": 50, "United Kingdom": 130,
    "Switzerland": 180, "Austria": 100, "Hungary": 60, "Poland": 55,
    "Romania": 45, "Bulgaria": 40, "Montenegro": 55, "Albania": 40,
    "Slovenia": 70, "Estonia": 60, "Latvia": 50, "Lithuania": 50,
    "Denmark": 140, "Sweden": 120, "Norway": 150, "Finland": 110, "Iceland": 160,
    "Ireland": 120, "Belgium": 100, "Malta": 80, "Cyprus": 70,
    "Colombia": 40, "Peru": 40, "Argentina": 45, "Brazil": 50, "Chile": 55,
    "Ecuador": 35, "Bolivia": 25, "Uruguay": 60, "Paraguay": 30,
    "Costa Rica": 60, "Panama": 55, "Guatemala": 35, "Mexico": 50,
    "Morocco": 40, "South Africa": 50, "Tanzania": 50, "Kenya": 50, "Egypt": 35,
    "Ghana": 40, "Rwanda": 50, "Ethiopia": 35, "Namibia": 60, "Botswana": 70,
    "Senegal": 45, "Madagascar": 35, "Mauritius": 80, "Tunisia": 40, "Uganda": 40,
    "Australia": 140, "New Zealand": 130,
}

CITY_AIRBNB_OVERRIDE = {
    "Tokyo": 130, "Kyoto": 140, "Hakone": 180, "Singapore": 150, "Hong Kong": 140,
    "Seoul": 90, "Bali": 55, "London": 160, "Paris": 150, "Amsterdam": 160,
    "Barcelona": 120, "Rome": 130, "Venice": 180, "Florence": 130,
    "Amalfi Coast": 200, "Santorini": 180, "Mykonos": 190, "Dubrovnik": 120,
    "Prague": 80, "Zurich": 200, "Interlaken": 190, "Zermatt": 220,
    "Reykjavik": 180, "Copenhagen": 160, "Stockholm": 140, "Oslo": 170,
    "Sydney": 160, "Melbourne": 140, "Queenstown": 160, "Male": 120,
    "Ari Atoll": 350, "Cape Town": 70, "Marrakech": 50, "Lisbon": 100,
    "Budapest": 65, "Istanbul": 55, "Bangkok": 45, "Chiang Mai": 30,
    "Hanoi": 30, "Ho Chi Minh City": 35, "Mexico City": 45, "Tulum": 90,
    "Cusco": 35, "Buenos Aires": 40, "Rio de Janeiro": 60, "Lima": 45,
    "Ushuaia": 80, "Galapagos": 120, "Torres del Paine": 100,
}

# ── Country-level food ───────────────────────────────────────────────────────
COUNTRY_FOOD = {
    "Japan": ["Ramen", "Sushi", "Tempura", "Yakitori", "Okonomiyaki"],
    "Thailand": ["Pad Thai", "Green Curry", "Som Tum Papaya Salad", "Mango Sticky Rice"],
    "Vietnam": ["Pho", "Banh Mi", "Bun Cha", "Spring Rolls"],
    "South Korea": ["Bibimbap", "Korean BBQ", "Kimchi Jjigae", "Tteokbokki"],
    "Indonesia": ["Nasi Goreng", "Satay", "Rendang", "Gado-Gado"],
    "India": ["Butter Chicken", "Biryani", "Dosa", "Samosa", "Thali"],
    "Cambodia": ["Fish Amok", "Lok Lak", "Num Banh Chok"],
    "Philippines": ["Adobo", "Sinigang", "Lechon", "Lumpia"],
    "Malaysia": ["Nasi Lemak", "Char Kway Teow", "Laksa", "Roti Canai"],
    "China": ["Peking Duck", "Dim Sum", "Kung Pao Chicken", "Hotpot"],
    "Taiwan": ["Beef Noodle Soup", "Bubble Tea", "Gua Bao", "Oyster Omelette"],
    "Sri Lanka": ["Rice and Curry", "Hoppers", "Kottu Roti", "Pol Sambol"],
    "Nepal": ["Dal Bhat", "Momo Dumplings", "Sel Roti"],
    "Myanmar": ["Mohinga Fish Soup", "Shan Noodles", "Tea Leaf Salad"],
    "Laos": ["Laap Minced Meat Salad", "Khao Piak Sen Noodles", "Sticky Rice"],
    "Mongolia": ["Buuz Dumplings", "Khuushuur Fried Pastry", "Airag Fermented Mare's Milk"],
    "Uzbekistan": ["Plov Rice Pilaf", "Shashlik Kebabs", "Samsa Pastry"],
    "Georgia": ["Khachapuri Cheese Bread", "Khinkali Dumplings", "Churchkhela"],
    "Jordan": ["Mansaf", "Falafel", "Hummus", "Kunafa"],
    "Oman": ["Shuwa Slow-Roasted Lamb", "Harees", "Omani Halwa"],
    "Maldives": ["Mas Huni Tuna Salad", "Garudhiya Fish Broth", "Hedhikaa Snacks"],
    "Bhutan": ["Ema Datshi Chili Cheese", "Phaksha Paa Pork", "Red Rice"],
    "France": ["Croissant", "Coq au Vin", "Croque Monsieur", "Ratatouille"],
    "Italy": ["Pasta Carbonara", "Pizza Margherita", "Risotto", "Gelato"],
    "Spain": ["Paella", "Tapas", "Jamon Iberico", "Churros"],
    "Portugal": ["Pasteis de Nata", "Bacalhau Cod", "Francesinha", "Sardines"],
    "Greece": ["Moussaka", "Souvlaki", "Spanakopita", "Baklava"],
    "Croatia": ["Cevapi", "Peka", "Black Risotto", "Strukli"],
    "Czech Republic": ["Svickova", "Trdelnik", "Goulash", "Knedliky Dumplings"],
    "Netherlands": ["Stroopwafel", "Bitterballen", "Herring", "Poffertjes"],
    "Germany": ["Bratwurst", "Schnitzel", "Pretzel", "Currywurst"],
    "Turkey": ["Kebab", "Baklava", "Pide", "Manti Dumplings", "Lahmacun"],
    "United Kingdom": ["Fish and Chips", "Full English Breakfast", "Roast Dinner", "Scones"],
    "Switzerland": ["Fondue", "Raclette", "Rosti", "Swiss Chocolate"],
    "Austria": ["Wiener Schnitzel", "Sachertorte", "Kaiserschmarrn", "Apfelstrudel"],
    "Hungary": ["Goulash", "Langos", "Chimney Cake", "Chicken Paprikash"],
    "Poland": ["Pierogi", "Zurek Soup", "Bigos", "Zapiekanka"],
    "Romania": ["Sarmale Cabbage Rolls", "Mici Grilled Rolls", "Mamaliga"],
    "Bulgaria": ["Shopska Salad", "Banitsa", "Kebapche"],
    "Montenegro": ["Njeguski Steak", "Cevapi", "Kacamak"],
    "Albania": ["Byrek", "Tave Kosi", "Qofte"],
    "Slovenia": ["Potica Nut Roll", "Idrijski Zlikrofi", "Jota Stew"],
    "Estonia": ["Black Bread", "Verivorst Blood Sausage", "Kama"],
    "Latvia": ["Grey Peas with Bacon", "Piradzini", "Rupjmaizes Kartojums"],
    "Lithuania": ["Cepelinai Potato Dumplings", "Saltibarsciai Cold Beet Soup", "Kibinai"],
    "Denmark": ["Smorrebrod Open Sandwich", "Danish Pastry", "Frikadeller Meatballs"],
    "Sweden": ["Swedish Meatballs", "Smorgasbord", "Kanelbullar Cinnamon Bun"],
    "Norway": ["Brunost Brown Cheese", "Rakfisk", "Farikal Lamb Stew"],
    "Finland": ["Karelian Pie", "Salmon Soup", "Reindeer Stew"],
    "Iceland": ["Lamb Soup", "Skyr", "Plokkfiskur Fish Stew", "Hot Dog"],
    "Ireland": ["Irish Stew", "Soda Bread", "Boxty", "Colcannon"],
    "Belgium": ["Belgian Waffles", "Moules-Frites", "Speculoos", "Stoofvlees Stew"],
    "Malta": ["Pastizzi", "Rabbit Stew", "Ftira Bread"],
    "Cyprus": ["Halloumi", "Souvlaki", "Meze Platter", "Kleftiko"],
    "Colombia": ["Bandeja Paisa", "Arepas", "Empanadas", "Ajiaco Soup"],
    "Peru": ["Ceviche", "Lomo Saltado", "Causa", "Anticuchos"],
    "Argentina": ["Asado Steak", "Empanadas", "Choripan", "Dulce de Leche"],
    "Brazil": ["Feijoada", "Pao de Queijo", "Acai Bowl", "Coxinha"],
    "Chile": ["Empanadas", "Pastel de Choclo", "Curanto", "Cazuela"],
    "Ecuador": ["Ceviche", "Llapingachos Potato Cakes", "Encebollado Fish Soup"],
    "Bolivia": ["Salteñas", "Pique Macho", "Anticuchos"],
    "Uruguay": ["Chivito Sandwich", "Asado", "Dulce de Leche"],
    "Paraguay": ["Sopa Paraguaya Corn Bread", "Chipa Cheese Bread", "Asado"],
    "Costa Rica": ["Gallo Pinto", "Casado", "Ceviche", "Plantains"],
    "Panama": ["Sancocho Stew", "Ceviche", "Carimañolas", "Hojaldras"],
    "Guatemala": ["Pepian Stew", "Tamales", "Kak'ik Turkey Soup"],
    "Mexico": ["Tacos al Pastor", "Mole", "Tamales", "Guacamole", "Elote"],
    "Morocco": ["Tagine", "Couscous", "Pastilla", "Harira Soup"],
    "South Africa": ["Braai", "Biltong", "Bobotie", "Bunny Chow"],
    "Tanzania": ["Ugali", "Nyama Choma Grilled Meat", "Zanzibar Pizza"],
    "Kenya": ["Nyama Choma", "Ugali", "Sukuma Wiki", "Mandazi"],
    "Egypt": ["Koshari", "Ful Medames", "Molokhia", "Shawarma"],
    "Ghana": ["Jollof Rice", "Banku and Tilapia", "Kelewele Fried Plantain"],
    "Rwanda": ["Brochettes", "Ugali", "Isombe Cassava Leaves"],
    "Ethiopia": ["Injera with Wat", "Doro Wat Chicken Stew", "Kitfo"],
    "Namibia": ["Biltong", "Braai", "Potjiekos Stew"],
    "Botswana": ["Seswaa Pounded Meat", "Vetkoek", "Morogo Wild Greens"],
    "Senegal": ["Thieboudienne Fish Rice", "Yassa Chicken", "Mafe Peanut Stew"],
    "Madagascar": ["Romazava Stew", "Ravitoto Cassava Leaves", "Zebu Steak"],
    "Mauritius": ["Dholl Puri", "Alouda", "Gateau Piment Chili Cakes"],
    "Tunisia": ["Brik Pastry", "Couscous", "Lablabi Chickpea Soup"],
    "Uganda": ["Rolex Egg Wrap", "Matoke Plantain Stew", "Luwombo"],
    "Australia": ["Meat Pie", "Barramundi", "Lamington", "Vegemite Toast"],
    "New Zealand": ["Lamb Roast", "Hangi Earth Oven", "Pavlova", "Pies"],
}

# ── Country-level drinks ─────────────────────────────────────────────────────
COUNTRY_DRINK = {
    "Japan": ["Sake", "Japanese Whisky Highball", "Matcha"],
    "Thailand": ["Thai Iced Tea", "Chang Beer", "Fresh Coconut Water"],
    "Vietnam": ["Vietnamese Iced Coffee", "Bia Hoi Draft Beer", "Fresh Sugarcane Juice"],
    "South Korea": ["Soju", "Makgeolli Rice Wine", "Korean Banana Milk"],
    "Indonesia": ["Bali Kopi Coffee", "Es Teler Iced Drink", "Jamu Herbal Tonic"],
    "India": ["Masala Chai", "Lassi", "Nimbu Pani Lemonade"],
    "Cambodia": ["Angkor Beer", "Fresh Coconut", "Sugar Palm Juice"],
    "Philippines": ["San Miguel Beer", "Calamansi Juice", "Lambanog Coconut Wine"],
    "Malaysia": ["Teh Tarik Pulled Tea", "White Coffee", "Fresh Fruit Juice"],
    "China": ["Chinese Tea", "Baijiu Liquor", "Tsingtao Beer"],
    "Taiwan": ["Bubble Tea", "Oolong Tea", "Taiwan Beer"],
    "Sri Lanka": ["Ceylon Tea", "Arrack", "King Coconut Water"],
    "Nepal": ["Nepali Milk Tea", "Tongba Millet Beer", "Raksi"],
    "Myanmar": ["Myanmar Beer", "Lahpet Yei Tea", "Sugar Cane Juice"],
    "Laos": ["Beerlao", "Lao Lao Rice Whisky", "Fresh Fruit Shakes"],
    "Mongolia": ["Airag Fermented Mare's Milk", "Suutei Tsai Milk Tea"],
    "Uzbekistan": ["Green Tea", "Ayran Yogurt Drink", "Kompot"],
    "Georgia": ["Georgian Wine", "Chacha Grape Brandy", "Lemonade"],
    "Jordan": ["Arabic Coffee", "Fresh Mint Tea", "Tamar Hindi"],
    "Oman": ["Kahwa Omani Coffee", "Laban Buttermilk"],
    "Maldives": ["Fresh Coconut Water", "Raa Palm Toddy"],
    "Bhutan": ["Butter Tea", "Ara Rice Wine"],
    "France": ["Wine", "Espresso", "Pastis"],
    "Italy": ["Espresso", "Aperol Spritz", "Limoncello"],
    "Spain": ["Sangria", "Tinto de Verano", "Cava"],
    "Portugal": ["Port Wine", "Ginjinha Cherry Liqueur", "Passionfruit Caipirinha"],
    "Greece": ["Ouzo", "Frappe Coffee", "Tsipouro"],
    "Croatia": ["Rakija", "Gemist Wine Spritzer", "Ozujsko Beer"],
    "Czech Republic": ["Pilsner Beer", "Becherovka", "Slivovice"],
    "Netherlands": ["Heineken Beer", "Genever Gin", "Chocomel"],
    "Germany": ["German Beer", "Riesling Wine", "Apfelschorle"],
    "Turkey": ["Turkish Tea", "Turkish Coffee", "Ayran"],
    "United Kingdom": ["Pub Ale", "Gin and Tonic", "Pimm's"],
    "Switzerland": ["Swiss Wine", "Rivella", "Hot Chocolate"],
    "Austria": ["Viennese Coffee", "Gruner Veltliner Wine", "Schnapps"],
    "Hungary": ["Unicum", "Tokaji Wine", "Palinka"],
    "Poland": ["Vodka", "Piwo Beer", "Kompot"],
    "Romania": ["Tuica Plum Brandy", "Romanian Wine", "Ciorbă"],
    "Bulgaria": ["Rakia", "Bulgarian Wine", "Boza"],
    "Montenegro": ["Rakija", "Vranac Wine", "Niksicko Beer"],
    "Albania": ["Raki", "Albanian Wine", "Dhalle Yogurt"],
    "Slovenia": ["Lasko Beer", "Slovenian Wine", "Borovnicke Blueberry Liqueur"],
    "Estonia": ["Vana Tallinn Liqueur", "Craft Beer", "Kali Kvass"],
    "Latvia": ["Riga Black Balsam", "Latvian Beer"],
    "Lithuania": ["Lithuanian Beer", "Midus Mead", "Gira Kvass"],
    "Denmark": ["Carlsberg Beer", "Aquavit", "Glogg"],
    "Sweden": ["Swedish Craft Beer", "Glogg", "Snaps Aquavit"],
    "Norway": ["Aquavit", "Norwegian Craft Beer", "Glogg"],
    "Finland": ["Lonkero Long Drink", "Sahti Beer", "Glogi"],
    "Iceland": ["Brennivin", "Icelandic Craft Beer", "Skyr Smoothie"],
    "Ireland": ["Guinness", "Irish Whiskey", "Irish Coffee"],
    "Belgium": ["Belgian Trappist Beer", "Kriek Cherry Beer", "Jenever"],
    "Malta": ["Cisk Beer", "Kinnie Soda", "Maltese Wine"],
    "Cyprus": ["Commandaria Wine", "Zivania", "KEO Beer"],
    "Colombia": ["Aguardiente", "Colombian Coffee", "Lulada Fruit Drink"],
    "Peru": ["Pisco Sour", "Chicha Morada", "Inca Kola"],
    "Argentina": ["Malbec Wine", "Mate", "Fernet con Coca"],
    "Brazil": ["Caipirinha", "Guarana Soda", "Acai Juice"],
    "Chile": ["Chilean Wine", "Pisco Sour", "Mote con Huesillo"],
    "Ecuador": ["Canelazo Hot Drink", "Pilsener Beer", "Fresh Fruit Juice"],
    "Bolivia": ["Singani Brandy", "Api Corn Drink", "Coca Tea"],
    "Uruguay": ["Mate", "Tannat Wine", "Medio y Medio"],
    "Paraguay": ["Terere Cold Mate", "Cana", "Mosto Sugarcane Juice"],
    "Costa Rica": ["Imperial Beer", "Guaro Sour", "Agua Dulce"],
    "Panama": ["Seco Herrerano", "Balboa Beer", "Chicheme Corn Drink"],
    "Guatemala": ["Guatemalan Coffee", "Gallo Beer", "Horchata"],
    "Mexico": ["Mezcal", "Margarita", "Horchata", "Michelada"],
    "Morocco": ["Mint Tea", "Fresh Orange Juice", "Avocado Smoothie"],
    "South Africa": ["Pinotage Wine", "Amarula", "Rooibos Tea"],
    "Tanzania": ["Kilimanjaro Beer", "Dawa Cocktail", "Sugar Cane Juice"],
    "Kenya": ["Tusker Beer", "Dawa Cocktail", "Kenyan Tea"],
    "Egypt": ["Hibiscus Tea", "Turkish Coffee", "Fresh Juice"],
    "Ghana": ["Star Beer", "Sobolo Hibiscus Drink", "Palm Wine"],
    "Rwanda": ["Inyange Juice", "Urwagwa Banana Wine", "Rwandan Coffee"],
    "Ethiopia": ["Ethiopian Coffee Ceremony", "Tej Honey Wine", "Tella Beer"],
    "Namibia": ["Windhoek Lager", "Amarula", "Rooibos Tea"],
    "Botswana": ["Chibuku Shake Shake Beer", "Ginger Beer"],
    "Senegal": ["Cafe Touba Spiced Coffee", "Bissap Hibiscus", "Bouye Baobab"],
    "Madagascar": ["THB Beer", "Ranonapango Rice Water", "Rum Arrangé"],
    "Mauritius": ["Phoenix Beer", "Alouda", "Mauritius Rum"],
    "Tunisia": ["Mint Tea", "Boukha Fig Spirit", "Fresh Orange Juice"],
    "Uganda": ["Nile Beer", "Rolex (egg wrap)", "Ugandan Coffee"],
    "Australia": ["Flat White Coffee", "Australian Wine", "VB Beer"],
    "New Zealand": ["Sauvignon Blanc", "Flat White Coffee", "L&P Soda"],
}

# ── City-specific detail data ────────────────────────────────────────────────
# Cities not in this dict will use smart fallback generation
CITY_DETAILS = {
    # ═══ JAPAN ═══
    "Tokyo": {
        "neighborhoods": ["Shinjuku — neon nightlife hub with izakayas and karaoke", "Shibuya — trendy shopping, youth culture, and the famous crossing", "Asakusa — historic temples, rickshaws, and old-Tokyo street food"],
        "top_activities": ["Explore Tsukiji Outer Market at dawn for fresh sushi", "Walk through Meiji Shrine's forested path in Harajuku", "Experience the sensory overload of Shibuya Crossing", "Wander the electric streets of Akihabara", "Ride to the top of Tokyo Skytree for panoramic views", "People-watch in Yoyogi Park on a Sunday", "Shop the fashion boutiques of Omotesando", "Take a day trip to teamLab Borderless digital art museum", "Bar-hop through Golden Gai's tiny themed bars", "Soak in an onsen (hot spring bath) in the city"],
        "local_food": ["Ramen", "Sushi", "Tempura", "Yakitori", "Okonomiyaki"],
        "local_drink": ["Sake", "Japanese Whisky Highball", "Matcha Latte"],
        "things_to_do": ["Walk Shibuya Crossing at night under the neon lights", "Take a sushi-making class", "Visit the Imperial Palace gardens", "Explore Harajuku's Takeshita Street", "Ride the bullet train to nearby Kamakura", "Catch a sumo practice session", "Try a themed cafe experience"],
    },
    "Kyoto": {
        "neighborhoods": ["Gion — geisha district with traditional tea houses", "Higashiyama — hillside temples and stone-paved lanes", "Arashiyama — bamboo groves and riverside scenery"],
        "top_activities": ["Walk through the thousands of torii gates at Fushimi Inari", "Visit the golden Kinkaku-ji temple at sunrise", "Stroll through the magical Arashiyama Bamboo Grove", "Explore the rock garden at Ryoan-ji", "Take a traditional tea ceremony class", "Wander Gion at dusk hoping to spot a geisha", "Cycle along the Philosopher's Path in spring", "Visit Nijo Castle and its nightingale floors", "Try kaiseki multi-course dining", "Hike the Fushimi Inari trail to the summit"],
        "local_food": ["Kaiseki Multi-Course Dinner", "Yudofu Tofu Hot Pot", "Matcha Sweets", "Kyoto Pickles"],
        "local_drink": ["Matcha", "Sake", "Kyoto Craft Beer"],
        "things_to_do": ["Rent a kimono and explore the temple district", "Take a cooking class for Japanese home-style food", "Visit Nishiki Market for local street food", "See the cherry blossoms or fall foliage (seasonal)", "Stay overnight in a traditional ryokan", "Attend a calligraphy or ikebana workshop"],
    },
    "Osaka": {
        "neighborhoods": ["Dotonbori — neon-lit food street with canal views", "Shinsekai — retro district with the Tsutenkaku Tower", "Namba — entertainment hub with theaters and arcades"],
        "top_activities": ["Eat your way through Dotonbori's street food stalls", "Visit Osaka Castle and its surrounding park", "Explore the retro Shinsekai district", "Try takoyaki from a famous street vendor", "Shop the underground malls of Namba", "Watch a comedy show at a local theater", "Visit the Osaka Aquarium Kaiyukan", "Stroll through Kuromon Market for fresh seafood", "Take a sake tasting tour", "Experience Osaka's legendary nightlife in Namba"],
        "local_food": ["Takoyaki Octopus Balls", "Okonomiyaki Savory Pancake", "Kushikatsu Deep-Fried Skewers", "Gyoza"],
        "local_drink": ["Sake", "Asahi Beer", "Chuhai Cocktail"],
        "things_to_do": ["Take a street food walking tour in Dotonbori", "Visit Universal Studios Japan", "Explore the Umeda Sky Building observation deck", "Day trip to Nara to feed the deer", "Try a takoyaki cooking class", "Wander the nightlife in Amerikamura"],
    },
    # ═══ THAILAND ═══
    "Bangkok": {
        "neighborhoods": ["Khao San Road — legendary backpacker strip and nightlife", "Silom — business district with rooftop bars and night markets", "Chinatown (Yaowarat) — street food paradise after dark"],
        "top_activities": ["Visit the Grand Palace and Wat Phra Kaew", "Explore Wat Pho and the Reclining Buddha", "Eat street food in Chinatown after dark", "Take a longtail boat through the canals", "Shop at the massive Chatuchak Weekend Market", "Sip cocktails at a rooftop bar overlooking the skyline", "Get a traditional Thai massage", "Visit Wat Arun at sunset", "Ride the Sky Train to explore different neighborhoods", "Take a Thai cooking class near a local market"],
        "local_food": ["Pad Thai", "Green Curry", "Som Tum Papaya Salad", "Mango Sticky Rice", "Tom Yum Soup"],
        "local_drink": ["Thai Iced Tea", "Chang Beer", "Fresh Coconut Water"],
        "things_to_do": ["Take a street food tour through Yaowarat (Chinatown)", "Visit the Jim Thompson House museum", "Cruise the Chao Phraya River at sunset", "Haggle at Chatuchak for unique souvenirs", "Get a Thai massage on Khao San Road", "Explore the Flower Market early morning"],
    },
    "Chiang Mai": {
        "neighborhoods": ["Old City — temples, cafes, and boutique guesthouses inside the moat", "Nimmanhaemin — trendy street with cafes, co-working, and galleries", "Night Bazaar Area — lively evening markets and food stalls"],
        "top_activities": ["Hike to Doi Suthep Temple for panoramic views", "Take a Thai cooking class at a local farm", "Visit an ethical elephant sanctuary", "Explore the Old City's ancient temples on foot", "Browse the Sunday Walking Street market", "Take a Muay Thai boxing class", "Visit the Royal Flora garden", "Try a traditional khantoke dinner", "Explore the trendy Nimmanhaemin Road cafes", "Hike Doi Inthanon, Thailand's highest peak"],
        "local_food": ["Khao Soi Curry Noodles", "Sai Oua Northern Sausage", "Pad Thai", "Sticky Rice and Laab"],
        "local_drink": ["Thai Iced Tea", "Local Craft Beer", "Fresh Mango Shake"],
        "things_to_do": ["Visit an ethical elephant sanctuary for a half-day", "Take a full-day cooking class", "Hike to the top of Doi Suthep at sunrise", "Explore the Saturday or Sunday night markets", "Get a traditional Thai massage at a temple", "Visit a local coffee farm"],
    },
    # ═══ VIETNAM ═══
    "Hanoi": {
        "neighborhoods": ["Old Quarter — maze of 36 ancient streets and street food vendors", "French Quarter — colonial architecture and wide boulevards", "West Lake — upscale lakeside dining and cafes"],
        "top_activities": ["Walk through the chaotic Old Quarter at morning rush", "Taste the legendary street food on every corner", "Visit Ho Chi Minh Mausoleum and the One Pillar Pagoda", "Watch a water puppet show", "Sip egg coffee at a hidden cafe", "Explore the Temple of Literature", "Take a cyclo ride through the Old Quarter", "Stroll around Hoan Kiem Lake at sunset", "Visit the Vietnam Museum of Ethnology", "Take a street food walking tour with a local"],
        "local_food": ["Pho Bo Beef Noodle Soup", "Bun Cha Grilled Pork Noodles", "Banh Mi Sandwich", "Egg Coffee"],
        "local_drink": ["Vietnamese Iced Coffee", "Bia Hoi Fresh Draft Beer", "Egg Coffee"],
        "things_to_do": ["Take a street food tour through the Old Quarter", "Sip egg coffee at Cafe Giang", "Cruise Ha Long Bay on a day or overnight trip", "Walk around Hoan Kiem Lake in the evening", "Visit the Train Street neighborhood", "Take a cooking class"],
    },
    "Ho Chi Minh City": {
        "neighborhoods": ["District 1 — colonial landmarks and rooftop bars", "Binh Thanh — local street food and coffee culture", "District 4 — authentic Saigon street food alleys"],
        "top_activities": ["Explore the War Remnants Museum", "Eat pho from a street-side stall at dawn", "Tour the Cu Chi Tunnels outside the city", "Wander through Ben Thanh Market", "Sip coffee at a vintage cafe in a French colonial building", "Visit Notre-Dame Cathedral and the Central Post Office", "Ride a motorbike through the city at night", "Try banh mi from the most famous street cart", "Explore the Mekong Delta on a day trip", "Bar-hop along Bui Vien Walking Street"],
        "local_food": ["Pho", "Banh Mi", "Com Tam Broken Rice", "Banh Xeo Crepe"],
        "local_drink": ["Vietnamese Iced Coffee", "Fresh Beer", "Sugarcane Juice"],
        "things_to_do": ["Take a motorbike food tour at night", "Visit Cu Chi Tunnels for a half-day trip", "Explore the bustling Ben Thanh Market", "Take a day trip to the Mekong Delta", "Visit the Jade Emperor Pagoda", "Try street food in District 4"],
    },
    # ═══ SOUTH KOREA ═══
    "Seoul": {
        "neighborhoods": ["Hongdae — indie music, street performers, and youth culture", "Gangnam — upscale shopping and K-pop agencies", "Insadong — traditional tea houses and art galleries"],
        "top_activities": ["Explore Gyeongbokgung Palace in a rented hanbok", "Walk the Bukchon Hanok Village of traditional houses", "Shop and eat in the Myeongdong district", "Hike Namsan Mountain to N Seoul Tower", "Explore the vibrant Hongdae nightlife", "Visit the DMZ on a guided tour", "Eat Korean BBQ in Gangnam", "Stroll along the Cheonggyecheon Stream", "Browse Insadong's galleries and tea houses", "Experience a jjimjilbang (Korean spa)"],
        "local_food": ["Korean BBQ", "Bibimbap", "Tteokbokki", "Kimchi Jjigae", "Fried Chicken"],
        "local_drink": ["Soju", "Makgeolli Rice Wine", "Korean Banana Milk"],
        "things_to_do": ["Rent a hanbok and explore Gyeongbokgung Palace", "Take a DMZ tour to the border", "Experience a Korean BBQ dinner", "Hike Bukhansan National Park", "Visit a K-pop themed cafe or shop", "Try street food at Gwangjang Market"],
    },
    # ═══ INDONESIA ═══
    "Bali": {
        "neighborhoods": ["Ubud — rice terraces, yoga studios, and art galleries", "Seminyak — trendy beach clubs, boutiques, and restaurants", "Canggu — surf culture, coworking spaces, and sunset bars"],
        "top_activities": ["Watch sunrise from the top of Mount Batur", "Walk through the Tegallalang Rice Terraces", "Visit the Sacred Monkey Forest in Ubud", "Surf the waves at Canggu or Uluwatu", "Explore the Tirta Empul water temple", "Attend a traditional Balinese dance performance", "Relax at a luxury day spa", "Visit the Uluwatu Temple at sunset", "Take a Balinese cooking class", "Snorkel at Nusa Penida island"],
        "local_food": ["Nasi Goreng", "Babi Guling Roast Suckling Pig", "Satay", "Lawar"],
        "local_drink": ["Bali Kopi Coffee", "Bintang Beer", "Fresh Coconut Water"],
        "things_to_do": ["Hike Mount Batur for sunrise", "Take a yoga class in Ubud", "Visit the rice terraces at Tegallalang", "Day trip to Nusa Penida for snorkeling", "Get a Balinese spa treatment", "Take a surfing lesson in Canggu", "Visit Tanah Lot temple at sunset"],
    },
    # ═══ INDIA ═══
    "Delhi": {
        "neighborhoods": ["Old Delhi — Mughal-era chaos of bazaars and spice markets", "New Delhi — wide boulevards, Lutyens architecture, and government", "Hauz Khas — trendy village with cafes, galleries, and nightlife"],
        "top_activities": ["Explore the Red Fort and Jama Masjid in Old Delhi", "Visit the stunning Humayun's Tomb", "Walk through Chandni Chowk market for street food", "See the Qutub Minar and surrounding ruins", "Tour the Lotus Temple", "Explore the vibrant Hauz Khas Village", "Visit the India Gate and Rajpath", "Take a cycle-rickshaw ride through Old Delhi", "Explore the National Museum", "Try a street food crawl through Chandni Chowk"],
        "local_food": ["Chole Bhature", "Butter Chicken", "Parantha from Paranthe Wali Gali", "Chaat"],
        "local_drink": ["Masala Chai", "Lassi", "Fresh Lime Soda"],
        "things_to_do": ["Take a street food tour through Old Delhi", "Visit Humayun's Tomb at golden hour", "Shop for spices in Chandni Chowk", "Try a cooking class for North Indian food", "Day trip to the Taj Mahal in Agra", "Explore Lodhi Art District's street murals"],
    },
    # ═══ FRANCE ═══
    "Paris": {
        "neighborhoods": ["Le Marais — historic quarter with galleries, cafes, and boutiques", "Montmartre — hilltop village with Sacre-Coeur and street artists", "Saint-Germain-des-Pres — literary cafes and chic shopping"],
        "top_activities": ["Visit the Louvre Museum and see the Mona Lisa", "Climb the Eiffel Tower at sunset", "Stroll along the Seine and browse the bookstalls", "Explore Montmartre and Sacre-Coeur Basilica", "Visit Musee d'Orsay for Impressionist masterpieces", "Walk through the Luxembourg Gardens", "Shop the Champs-Elysees", "Visit Notre-Dame Cathedral (exterior)", "Explore the catacombs beneath the city", "People-watch from a sidewalk cafe with an espresso"],
        "local_food": ["Croissant", "Croque Monsieur", "Duck Confit", "Escargot", "Crepes"],
        "local_drink": ["Wine", "Espresso", "Kir Royale"],
        "things_to_do": ["Take a patisserie or cooking class", "Cruise the Seine River at sunset", "Visit Versailles on a day trip", "Explore the Marche des Enfants Rouges food market", "Picnic with cheese and wine by the Eiffel Tower", "Browse the flea markets at Clignancourt"],
    },
    # ═══ ITALY ═══
    "Rome": {
        "neighborhoods": ["Trastevere — cobblestone charm with trattorias and nightlife", "Centro Storico — Pantheon, piazzas, and gelato shops", "Testaccio — working-class food scene and nightlife"],
        "top_activities": ["Explore the Colosseum and Roman Forum", "Throw a coin in the Trevi Fountain", "Visit the Vatican Museums and Sistine Chapel", "Wander the Pantheon and surrounding piazzas", "Eat carbonara in Trastevere", "Walk the Spanish Steps and Via Condotti", "Explore the Borghese Gallery and gardens", "Take a gelato tour of the best artisan shops", "Visit Castel Sant'Angelo along the Tiber", "Watch sunset from Pincio Terrace"],
        "local_food": ["Pasta Carbonara", "Cacio e Pepe", "Supplì Rice Balls", "Pizza al Taglio", "Gelato"],
        "local_drink": ["Espresso", "Aperol Spritz", "Negroni"],
        "things_to_do": ["Take a pasta-making class", "Explore the Vatican Museums early morning", "Eat in Testaccio's authentic trattorias", "Day trip to Pompeii or Tivoli", "Stroll through Villa Borghese gardens", "Try a gelato tasting tour"],
    },
    "Florence": {
        "neighborhoods": ["Oltrarno — artisan workshops and hidden trattorias", "Duomo Area — iconic cathedral and Renaissance landmarks", "San Lorenzo — leather market and central food hall"],
        "top_activities": ["Climb to the top of Brunelleschi's Dome", "See Michelangelo's David at the Accademia", "Walk across the Ponte Vecchio at sunset", "Visit the Uffizi Gallery for Renaissance masterpieces", "Explore the Boboli Gardens", "Eat a Florentine steak at a local trattoria", "Shop for leather goods at San Lorenzo Market", "Visit the Palazzo Pitti", "Take a cooking class in the Tuscan countryside", "Watch sunset from Piazzale Michelangelo"],
        "local_food": ["Bistecca alla Fiorentina", "Ribollita Bread Soup", "Lampredotto Tripe Sandwich", "Cantucci Biscotti"],
        "local_drink": ["Chianti Wine", "Aperol Spritz", "Negroni"],
        "things_to_do": ["Take a Tuscan cooking class", "Day trip to Siena or San Gimignano", "Visit Mercato Centrale for local food", "Explore the Oltrarno artisan district", "Wine tasting in the Chianti hills", "Hike to Piazzale Michelangelo for sunset views"],
    },
    # ═══ SPAIN ═══
    "Barcelona": {
        "neighborhoods": ["Gothic Quarter — medieval streets and hidden plazas", "El Born — trendy bars, galleries, and Picasso Museum", "Gracia — bohemian village feel with local tapas bars"],
        "top_activities": ["Visit Gaudi's Sagrada Familia basilica", "Wander through Park Guell's colorful mosaics", "Stroll Las Ramblas from top to bottom", "Explore the Gothic Quarter's winding alleys", "Relax on Barceloneta Beach", "Visit the Picasso Museum in El Born", "Eat tapas at La Boqueria market", "Tour Casa Batllo and Casa Mila", "Watch sunset from the Bunkers del Carmel viewpoint", "Catch a flamenco show in a small tablao"],
        "local_food": ["Tapas", "Paella", "Pa amb Tomaquet", "Patatas Bravas", "Jamon Iberico"],
        "local_drink": ["Sangria", "Cava", "Vermouth"],
        "things_to_do": ["Take a tapas and wine walking tour", "Visit La Boqueria market in the morning", "Day trip to Montserrat monastery", "Explore the Gracia neighborhood at night", "Take a paella cooking class", "Watch FC Barcelona at Camp Nou (match day)"],
    },
    # ═══ GREECE ═══
    "Santorini": {
        "neighborhoods": ["Oia — iconic blue domes and legendary sunset views", "Fira — clifftop capital with shops, bars, and caldera views", "Imerovigli — quiet luxury perched at the highest point"],
        "top_activities": ["Watch the sunset from Oia's castle ruins", "Hike the caldera trail from Fira to Oia", "Visit the Red Beach and Akrotiri ruins", "Take a catamaran cruise around the caldera", "Wine-taste at a volcanic vineyard", "Swim in the hot springs near the volcano", "Explore the ancient ruins of Akrotiri", "Photograph the blue-domed churches", "Eat fresh seafood overlooking the caldera", "Relax at a cliffside infinity pool"],
        "local_food": ["Tomatokeftedes Tomato Fritters", "Fava Bean Puree", "Fresh Grilled Octopus", "Gyros"],
        "local_drink": ["Assyrtiko Wine", "Ouzo", "Frappe Coffee"],
        "things_to_do": ["Book a sunset catamaran cruise", "Hike the Fira-to-Oia trail", "Visit a volcanic winery", "Explore the ancient city of Akrotiri", "Swim at Perissa Black Sand Beach", "Take a photography tour of the villages"],
    },
    # ═══ UNITED KINGDOM ═══
    "London": {
        "neighborhoods": ["Shoreditch — street art, vintage shops, and creative nightlife", "South Bank — Thames-side culture with galleries and food markets", "Soho — theater district, eclectic dining, and cocktail bars"],
        "top_activities": ["Visit the British Museum's world-class collection", "Walk along the South Bank from Westminster to Tower Bridge", "See a show in the West End theater district", "Explore the Tower of London and Crown Jewels", "Stroll through Hyde Park and Kensington Gardens", "Visit Tate Modern art gallery", "Shop at Borough Market for artisan food", "Tour Buckingham Palace and watch the changing of the guard", "Explore the street food at Camden Market", "Take a ride on the London Eye"],
        "local_food": ["Fish and Chips", "Full English Breakfast", "Sunday Roast", "Pies"],
        "local_drink": ["Pub Ale", "Gin and Tonic", "Pimm's Cup"],
        "things_to_do": ["Explore Borough Market for lunch", "Take a walking tour of street art in Shoreditch", "See a West End musical or play", "Visit free museums — British Museum, Tate, National Gallery", "Walk through Notting Hill and Portobello Road Market", "Catch sunset from Primrose Hill"],
    },
    # ═══ TURKEY ═══
    "Istanbul": {
        "neighborhoods": ["Sultanahmet — Hagia Sophia, Blue Mosque, and Topkapi Palace", "Beyoglu — Istiklal Street, rooftop bars, and art galleries", "Kadikoy — Asian side local food scene and vintage markets"],
        "top_activities": ["Visit the Hagia Sophia mosque-museum", "Explore the Blue Mosque and Hippodrome", "Haggle in the Grand Bazaar", "Cruise the Bosphorus between Europe and Asia", "Eat a Turkish breakfast spread by the water", "Visit the underground Basilica Cistern", "Explore Topkapi Palace and its harem", "Walk Istiklal Street and ride the historic tram", "Try a traditional hammam (Turkish bath)", "Eat fresh fish sandwiches at Eminonu pier"],
        "local_food": ["Kebab", "Baklava", "Lahmacun", "Borek", "Simit Sesame Bread"],
        "local_drink": ["Turkish Tea", "Turkish Coffee", "Raki"],
        "things_to_do": ["Take a Bosphorus ferry cruise at sunset", "Get a traditional Turkish bath experience", "Shop for ceramics and spices at the Grand Bazaar", "Eat breakfast in Kadikoy on the Asian side", "Take a cooking class for Turkish cuisine", "Visit the Spice Bazaar"],
    },
    # ═══ MOROCCO ═══
    "Marrakech": {
        "neighborhoods": ["Medina — winding souks, riads, and sensory overload", "Gueliz — modern district with cafes and galleries", "Kasbah — royal palaces and the Saadian Tombs"],
        "top_activities": ["Get lost in the maze-like souks of the Medina", "Watch the spectacle of Jemaa el-Fnaa square at night", "Visit the stunning Bahia Palace", "Explore the Jardin Majorelle and YSL Museum", "Take a cooking class in a riad", "Haggle for handcrafted goods in the souks", "Visit the Saadian Tombs", "Relax at a traditional hammam", "Day trip to the Atlas Mountains", "Ride a camel at sunset near the Palmeraie"],
        "local_food": ["Tagine", "Couscous", "Pastilla Pigeon Pie", "Harira Soup", "Msemen Flatbread"],
        "local_drink": ["Mint Tea", "Fresh Orange Juice", "Avocado Smoothie"],
        "things_to_do": ["Take a riad-based cooking class", "Explore the souks with a local guide", "Day trip to the Atlas Mountains and Berber villages", "Relax at a traditional hammam spa", "Ride a hot air balloon at sunrise over the desert", "Visit the Jardin Majorelle"],
    },
    # ═══ SOUTH AFRICA ═══
    "Cape Town": {
        "neighborhoods": ["Bo-Kaap — colorful houses and Cape Malay cuisine", "Woodstock — street art, breweries, and creative spaces", "Camps Bay — beachfront bars and sunset views"],
        "top_activities": ["Hike or cable car up Table Mountain", "Visit the penguins at Boulders Beach", "Drive the stunning Chapman's Peak coastal road", "Explore the V&A Waterfront", "Tour the Stellenbosch winelands", "Visit Robben Island museum", "Walk through the colorful Bo-Kaap neighborhood", "Surf or swim at Muizenberg Beach", "Take a food tour through the city center", "Watch sunset from Signal Hill or Lion's Head"],
        "local_food": ["Braai Grilled Meat", "Bobotie", "Cape Malay Curry", "Biltong"],
        "local_drink": ["Pinotage Wine", "Amarula", "Rooibos Tea"],
        "things_to_do": ["Hike Lion's Head for sunrise or sunset", "Take a wine tour through Stellenbosch", "Visit Robben Island and Mandela's cell", "Explore Bo-Kaap on a food tour", "Drive the Cape Peninsula to Cape Point", "Visit Kirstenbosch Botanical Garden"],
    },
    # ═══ PERU ═══
    "Cusco": {
        "neighborhoods": ["San Blas — artsy hilltop quarter with studios and cafes", "Plaza de Armas — central square with colonial churches", "San Pedro — local market and street food scene"],
        "top_activities": ["Visit the magnificent Machu Picchu", "Explore the Sacsayhuaman fortress above the city", "Wander the San Pedro Market for local food", "Walk the cobblestoned San Blas artisan quarter", "Visit the Qorikancha Temple of the Sun", "Hike the Rainbow Mountain", "Take a cooking class for Peruvian cuisine", "Explore the Sacred Valley on a day trip", "Try cuy (guinea pig) at a local restaurant", "Watch a traditional dance performance in the plaza"],
        "local_food": ["Ceviche", "Lomo Saltado", "Cuy (Guinea Pig)", "Alpaca Steak", "Causa"],
        "local_drink": ["Pisco Sour", "Chicha Morada", "Coca Tea"],
        "things_to_do": ["Day trip to Machu Picchu by train", "Hike Rainbow Mountain for stunning views", "Explore the Sacred Valley and Ollantaytambo", "Shop for textiles at San Pedro Market", "Take a Peruvian cooking class", "Visit Moray circular terraces and Maras salt mines"],
    },
    # ═══ MEXICO ═══
    "Mexico City": {
        "neighborhoods": ["Roma Norte — tree-lined streets, cafes, and art galleries", "Condesa — art deco architecture, parks, and hip restaurants", "Coyoacan — colorful colonial quarter and Frida Kahlo's house"],
        "top_activities": ["Visit the Frida Kahlo Museum in Coyoacan", "Explore the ancient ruins of Teotihuacan", "Eat tacos al pastor from a street stand", "Visit the stunning Palacio de Bellas Artes", "Walk through Chapultepec Park and castle", "Explore the murals of Diego Rivera", "Stroll the trendy Roma and Condesa neighborhoods", "Visit the Anthropology Museum", "Eat at one of the world's best restaurants", "Take a boat ride on the canals of Xochimilco"],
        "local_food": ["Tacos al Pastor", "Mole", "Tamales", "Tlacoyos", "Churros"],
        "local_drink": ["Mezcal", "Pulque", "Mexican Hot Chocolate"],
        "things_to_do": ["Take a street food crawl through Roma Norte", "Day trip to the Teotihuacan pyramids", "Visit Frida Kahlo Museum and Coyoacan", "Explore Chapultepec Castle for city views", "Float the canals of Xochimilco on a trajinera", "Try a mezcal tasting experience"],
    },
    # ═══ AUSTRALIA ═══
    "Sydney": {
        "neighborhoods": ["The Rocks — historic cobblestones and weekend markets", "Surry Hills — trendy dining, coffee, and boutique shops", "Manly — beachside village a ferry ride from the city"],
        "top_activities": ["Walk across the Sydney Harbour Bridge", "See a performance at the Sydney Opera House", "Surf or swim at Bondi Beach", "Walk the Bondi to Coogee coastal trail", "Explore the Royal Botanic Garden", "Take a ferry to Manly Beach", "Visit Taronga Zoo with harbor views", "Eat fresh seafood at the Sydney Fish Market", "Explore The Rocks' weekend markets and pubs", "Watch sunset from Mrs Macquarie's Chair"],
        "local_food": ["Barramundi", "Meat Pie", "Avocado Toast", "Lamington"],
        "local_drink": ["Flat White Coffee", "Australian Shiraz", "VB Beer"],
        "things_to_do": ["Walk the Bondi to Coogee coastal trail", "Take a ferry to Manly for the day", "Visit the Opera House and take a backstage tour", "Explore the food stalls at The Rocks Market", "Day trip to the Blue Mountains", "Surf at Bondi Beach"],
    },
    # ═══ BRAZIL ═══
    "Rio de Janeiro": {
        "neighborhoods": ["Copacabana — legendary beach strip and nightlife", "Santa Teresa — hilltop bohemian quarter with art studios", "Lapa — samba clubs and street party scene"],
        "top_activities": ["Visit Christ the Redeemer atop Corcovado", "Take the cable car up Sugarloaf Mountain", "Relax on Copacabana or Ipanema Beach", "Hike through Tijuca National Forest", "Watch a samba show in Lapa", "Catch sunset at Arpoador rock between the beaches", "Explore the colorful Selaron Steps", "Visit the Museum of Tomorrow", "Eat at a traditional churrascaria", "Experience a Carnival street party (seasonal)"],
        "local_food": ["Feijoada", "Acai Bowl", "Pao de Queijo Cheese Bread", "Coxinha"],
        "local_drink": ["Caipirinha", "Guarana Soda", "Chopp Draft Beer"],
        "things_to_do": ["Hike to the top of Two Brothers Mountain", "Take a samba lesson in Lapa", "Visit the iconic Selaron Steps", "Watch sunset at Arpoador Rock", "Explore the street art of Santa Teresa", "Eat acai on the beach"],
    },
    # ═══ ARGENTINA ═══
    "Buenos Aires": {
        "neighborhoods": ["San Telmo — antique markets, tango halls, and cobblestones", "Palermo Soho — trendy bars, street art, and designer shops", "La Boca — colorful Caminito street and football culture"],
        "top_activities": ["Watch a live tango show in San Telmo", "Explore the colorful La Boca neighborhood", "Eat a world-class steak at a traditional parrilla", "Browse the San Telmo Sunday antique market", "Visit the Recoleta Cemetery and Eva Peron's grave", "Stroll the parks and bars of Palermo", "Take a tango class", "Visit the MALBA modern art museum", "Eat empanadas and drink Malbec", "Explore the Mataderos gaucho fair"],
        "local_food": ["Asado Steak", "Empanadas", "Choripan", "Provoleta Grilled Cheese"],
        "local_drink": ["Malbec Wine", "Mate", "Fernet con Coca"],
        "things_to_do": ["Take a tango lesson and see a milonga", "Eat at a traditional parrilla steakhouse", "Browse the San Telmo Sunday market", "Day trip to Tigre Delta", "Explore Palermo Soho's street art and bars", "Visit Recoleta Cemetery"],
    },
    # ═══ COLOMBIA ═══
    "Medellin": {
        "neighborhoods": ["El Poblado — upscale restaurants, rooftop bars, and nightlife", "Laureles — local neighborhood with cafes and sports bars", "Comuna 13 — world-famous street art and outdoor escalators"],
        "top_activities": ["Take the outdoor escalators through Comuna 13 street art", "Ride the cable car over the city for stunning views", "Visit the Botero sculptures in Plaza Botero", "Explore the Arvi Nature Park by metrocable", "Eat bandeja paisa at a local restaurant", "Visit a coffee farm in the nearby countryside", "Walk the Parque Lleras nightlife district", "Explore the Medellin Botanical Garden", "Take a dance class in salsa or reggaeton", "Visit the Memory Museum"],
        "local_food": ["Bandeja Paisa", "Arepas", "Empanadas", "Patacones Fried Plantain"],
        "local_drink": ["Aguardiente", "Colombian Coffee", "Lulada Fruit Drink"],
        "things_to_do": ["Walk the Comuna 13 street art graffiti tour", "Take a coffee farm day trip", "Ride the Metrocable over the city", "Experience the nightlife in El Poblado", "Visit the Botero sculptures downtown", "Take a salsa dance class"],
    },
    # ═══ GERMANY ═══
    "Berlin": {
        "neighborhoods": ["Kreuzberg — multicultural food scene and legendary nightlife", "Mitte — museums, galleries, and historic landmarks", "Friedrichshain — street art, flea markets, and warehouse clubs"],
        "top_activities": ["Visit the Berlin Wall Memorial and East Side Gallery", "Explore Museum Island's world-class museums", "Walk through the Brandenburg Gate", "Tour the Reichstag building and glass dome", "Explore the street food scene at Markthalle Neun", "Visit the Holocaust Memorial", "Wander the flea markets at Mauerpark on Sundays", "Experience Berlin's legendary club scene", "Explore the Tiergarten park", "Visit the Topography of Terror museum"],
        "local_food": ["Currywurst", "Doner Kebab", "Schnitzel", "Berliner Donut"],
        "local_drink": ["German Craft Beer", "Berliner Weisse", "Club Mate"],
        "things_to_do": ["Explore the East Side Gallery street art", "Browse the Mauerpark flea market on Sunday", "Take a Cold War history walking tour", "Eat doner kebab at a legendary stand", "Visit Tempelhofer Feld former airport park", "Experience the nightlife at a warehouse club"],
    },
    # ═══ NETHERLANDS ═══
    "Amsterdam": {
        "neighborhoods": ["Jordaan — canal-side charm with cafes and galleries", "De Pijp — multicultural food at Albert Cuyp Market", "NDSM Wharf — industrial-chic art and food district"],
        "top_activities": ["Visit the Anne Frank House", "Explore the Rijksmuseum and see The Night Watch", "Take a canal boat tour through the city", "Visit the Van Gogh Museum", "Cycle through Vondelpark", "Explore the Albert Cuyp street market", "Walk the Red Light District", "Visit the Heineken Experience", "Stroll the Nine Streets shopping area", "Explore the NDSM creative district by ferry"],
        "local_food": ["Stroopwafel", "Bitterballen", "Herring Sandwich", "Dutch Pancakes"],
        "local_drink": ["Heineken Beer", "Genever Gin", "Dutch Jenever"],
        "things_to_do": ["Rent a bike and cycle the canal ring", "Visit the Anne Frank House (book ahead)", "Take a canal cruise at sunset", "Explore the Jordaan's hidden cafes", "Visit the floating flower market", "Try Dutch cheese at a local cheese shop"],
    },
    # ═══ PORTUGAL ═══
    "Lisbon": {
        "neighborhoods": ["Alfama — winding alleys, fado bars, and Castelo de Sao Jorge", "Bairro Alto — nightlife, rooftop bars, and bohemian vibes", "Belem — monuments, pasteis de nata, and waterfront parks"],
        "top_activities": ["Ride the iconic Tram 28 through Alfama", "Eat a warm pastel de nata at Pasteis de Belem", "Explore the hilltop Castelo de Sao Jorge", "Listen to live fado in an Alfama tavern", "Visit the Jeronimos Monastery in Belem", "Walk through the LX Factory creative space", "Watch sunset from Miradouro da Graca", "Explore the Time Out Market food hall", "Visit the Oceanario aquarium", "Ride the Santa Justa Elevator for city views"],
        "local_food": ["Pasteis de Nata Custard Tart", "Bacalhau a Bras Cod", "Bifana Pork Sandwich", "Sardines"],
        "local_drink": ["Port Wine", "Ginjinha Cherry Liqueur", "Vinho Verde"],
        "things_to_do": ["Eat pasteis de nata at Pasteis de Belem", "Take a fado music tour in Alfama", "Day trip to Sintra's fairy-tale palaces", "Ride Tram 28 through the old neighborhoods", "Explore the LX Factory for shopping and food", "Watch sunset from a miradouro viewpoint"],
    },
    # ═══ CZECH REPUBLIC ═══
    "Prague": {
        "neighborhoods": ["Stare Mesto — Old Town Square, Astronomical Clock, and Gothic churches", "Mala Strana — cobblestone streets, Baroque palaces, and riverside cafes", "Vinohrady — leafy residential area with wine bars and brunch spots"],
        "top_activities": ["Walk across the Charles Bridge at sunrise", "Watch the Astronomical Clock perform on the hour", "Visit Prague Castle, the largest ancient castle complex", "Explore the Jewish Quarter and its synagogues", "Drink Czech pilsner in a traditional beer hall", "Stroll through the Wallenstein Garden", "Visit the Lennon Wall in Mala Strana", "Take a river cruise on the Vltava", "Explore the Letna Park beer garden", "Visit the Dancing House"],
        "local_food": ["Svickova Marinated Beef", "Trdelnik Chimney Cake", "Smoked Meats", "Goulash"],
        "local_drink": ["Pilsner Beer", "Becherovka Liqueur", "Czech Wine"],
        "things_to_do": ["Take a craft beer tasting tour", "Walk Charles Bridge at sunrise before the crowds", "Visit Kutna Hora bone church on a day trip", "Explore Prague Castle and St. Vitus Cathedral", "Drink at a traditional Czech beer hall", "Walk the Petrin Hill for panoramic views"],
    },
    # ═══ HUNGARY ═══
    "Budapest": {
        "neighborhoods": ["Jewish Quarter — ruin bars, street art, and nightlife", "Castle District — Buda hilltop with Fisherman's Bastion", "Downtown Pest — grand boulevards, baths, and the Parliament"],
        "top_activities": ["Soak in the Szechenyi Thermal Baths", "Visit the stunning Hungarian Parliament Building", "Explore the ruin bars of the Jewish Quarter", "Walk along the Danube and see the Shoes memorial", "Visit Fisherman's Bastion for panoramic views", "Explore the Great Market Hall", "Relax in the Gellert Baths", "Take a Danube river cruise at night", "Visit the Hospital in the Rock", "Eat langos at the Central Market"],
        "local_food": ["Goulash Soup", "Langos Fried Dough", "Chimney Cake", "Chicken Paprikash"],
        "local_drink": ["Unicum Herbal Liqueur", "Tokaji Wine", "Palinka Fruit Brandy"],
        "things_to_do": ["Spend a morning at Szechenyi Baths", "Bar-hop through the ruin bars", "Take a Danube evening cruise", "Explore the Great Market Hall for local food", "Hike up Gellert Hill for sunset", "Take a day trip to the Danube Bend"],
    },
}

# ── Neighborhood templates for fallback generation ───────────────────────────
NEIGHBORHOOD_TEMPLATES = {
    "mega_city": [
        "{city} Old Quarter — historic heart with markets and street food",
        "Central Business District — modern skyline, malls, and rooftop bars",
        "Cultural Quarter — museums, galleries, and performing arts",
    ],
    "large_city": [
        "Old Town — historic center with traditional architecture and local cafes",
        "Market District — bustling stalls, local food, and artisan goods",
        "Waterfront Area — riverside or lakeside promenade with dining",
    ],
    "small_city": [
        "Historic Center — main square, churches, and winding streets",
        "Local Market Area — food stalls, local crafts, and everyday life",
        "Scenic Quarter — viewpoints, parks, and quieter streets",
    ],
    "small_town": [
        "Town Center — main plaza with cafes and local shops",
        "Old Quarter — charming alleys and traditional buildings",
        "Outskirts — nature walks and panoramic viewpoints",
    ],
    "village": [
        "Village Center — small plaza with local gathering spots",
        "Nature Area — trails and scenic viewpoints nearby",
        "Riverside or Lakeside — waterfront paths and relaxation spots",
    ],
}

ACTIVITY_TAG_TEMPLATES = {
    "food": [
        "Take a street food walking tour",
        "Try the signature local dish at a top-rated spot",
        "Visit the famous local market for fresh produce",
        "Take a cooking class with a local chef",
        "Eat breakfast at a beloved local cafe",
    ],
    "temples": [
        "Visit the most famous temple or religious site",
        "Take a guided walking tour of the historic quarter",
        "Explore ancient ruins and monuments",
        "Watch a traditional ceremony or ritual",
        "Visit the local history museum",
    ],
    "nightlife": [
        "Bar-hop through the main nightlife district",
        "Catch live music at a popular local venue",
        "Sip cocktails at a rooftop bar",
        "Join an evening pub crawl",
        "Experience the local club scene",
    ],
    "beaches": [
        "Spend a day at the best beach",
        "Go snorkeling or diving at a top spot",
        "Take a sunset boat cruise",
        "Eat fresh seafood by the water",
        "Explore hidden coves and beaches",
    ],
    "hiking": [
        "Hike to the best scenic viewpoint",
        "Trek through a national park or nature reserve",
        "Take a guided nature walk",
        "Visit a waterfall or swimming hole",
        "Catch sunrise from a summit or high point",
    ],
    "art": [
        "Visit the main art museum or gallery",
        "Take a street art walking tour",
        "Explore the local art and gallery district",
        "Visit an artisan workshop",
        "Attend a cultural performance or exhibition",
    ],
    "shopping": [
        "Explore the main market or bazaar",
        "Shop in the artisan district for handmade goods",
        "Visit local craft workshops",
        "Browse vintage and antique shops",
        "Pick up unique souvenirs",
    ],
    "architecture": [
        "Take an architecture walking tour",
        "Visit the most iconic landmark building",
        "Explore the historic district on foot",
        "Photograph the skyline from the best viewpoint",
        "Visit a famous church, palace, or fort",
    ],
    "wellness": [
        "Book a traditional spa treatment",
        "Try a morning yoga or meditation session",
        "Visit hot springs or thermal baths",
        "Enjoy a wellness retreat experience",
        "Relax at a peaceful garden or park",
    ],
    "wildlife": [
        "Go on a wildlife spotting tour or safari",
        "Visit the nature reserve or sanctuary",
        "Try a birdwatching excursion",
        "Take a marine or river wildlife trip",
        "Go on a guided photography walk in nature",
    ],
    "photography": [
        "Catch sunrise at the most iconic viewpoint",
        "Take a photo walk through colorful neighborhoods",
        "Shoot golden hour at the scenic landmark",
        "Capture night scenes of illuminated landmarks",
        "Photograph local life at the morning market",
    ],
    "culture": [
        "Visit a local family or homestay experience",
        "Attend a traditional performance or folk show",
        "Take a traditional craft workshop",
        "Explore a local village or community",
        "Learn a traditional dance or art form",
    ],
}


def generate_fallback(name, data):
    """Generate detail data for cities not in CITY_DETAILS."""
    country = data["country"]
    tags = data.get("tags", [])
    highlights = data.get("highlights", [])
    city_size = data.get("city_size", "small_city")
    terrain = data.get("terrain", "flat")
    description = data.get("description", "")

    # Neighborhoods
    templates = NEIGHBORHOOD_TEMPLATES.get(city_size, NEIGHBORHOOD_TEMPLATES["small_city"])
    neighborhoods = []
    for t in templates:
        neighborhoods.append(t.replace("{city}", name))
    # Customize first neighborhood based on terrain
    if terrain in ("coastal", "island") and city_size not in ("mega_city",):
        neighborhoods[0] = f"Waterfront — beach area, promenade, and seaside dining"
    elif terrain == "mountain":
        neighborhoods[0] = f"Valley Center — town hub surrounded by mountain scenery"

    # Top activities from tags (pick from templates)
    activities = []
    for tag in tags:
        tag_acts = ACTIVITY_TAG_TEMPLATES.get(tag, [])
        for act in tag_acts:
            a = f"{act} in {name}" if "the" not in act.lower()[:5] else act
            if a not in activities:
                activities.append(a)
            if len(activities) >= 10:
                break
        if len(activities) >= 10:
            break
    # Fill from highlights
    for h in highlights:
        act = f"Visit {h}"
        if act not in activities and len(activities) < 10:
            activities.append(act)
    # Pad if needed
    generic = [
        f"Explore {name}'s main streets and neighborhoods",
        f"Try local street food in {name}",
        f"Take photos at the most scenic viewpoint",
        f"Visit the local market or shops",
        f"Relax at a cafe and people-watch",
        f"Walk through the historic center",
        f"Chat with locals and learn about the culture",
        f"Watch sunset from the best spot in town",
        f"Book a guided tour of {name}",
        f"Try a local experience or workshop",
    ]
    for g in generic:
        if len(activities) >= 10:
            break
        if g not in activities:
            activities.append(g)
    activities = activities[:10]

    # Food and drink from country defaults
    local_food = list(COUNTRY_FOOD.get(country, ["Local specialties", "Street food", "Traditional dishes"]))[:5]
    local_drink = list(COUNTRY_DRINK.get(country, ["Local beer", "Traditional tea"]))[:3]

    # Things to do (from highlights + generic)
    things = []
    for h in highlights[:4]:
        things.append(f"Visit {h}")
    things_generic = [
        f"Take a walking tour of {name}",
        f"Explore the local food scene",
        f"Visit the main viewpoint for panoramic photos",
        f"Shop for local crafts and souvenirs",
        f"Try a local cooking or cultural class",
        f"Day trip to a nearby attraction",
        f"Relax and soak in the local atmosphere",
    ]
    for t in things_generic:
        if len(things) >= 7:
            break
        if t not in things:
            things.append(t)
    things = things[:7]

    return {
        "neighborhoods": neighborhoods,
        "top_activities": activities,
        "local_food": local_food,
        "local_drink": local_drink,
        "things_to_do": things,
    }


# ── Enrich function ──────────────────────────────────────────────────────────
def enrich():
    """Copy all 21 existing fields and add 7 new detail fields."""
    enriched = {}
    for name, data in CITIES.items():
        d = dict(data)  # copy existing 21 fields
        country = data["country"]

        # Get city-specific details or fallback
        if name in CITY_DETAILS:
            details = CITY_DETAILS[name]
        else:
            details = generate_fallback(name, data)

        d["neighborhoods"] = details["neighborhoods"]
        d["top_activities"] = details["top_activities"]
        d["local_food"] = details["local_food"]
        d["local_drink"] = details["local_drink"]
        d["things_to_do"] = details["things_to_do"]

        # Uber cost
        d["uber_cost"] = CITY_UBER_OVERRIDE.get(name, COUNTRY_UBER_COST.get(country, 8))

        # Airbnb cost
        d["airbnb_cost"] = CITY_AIRBNB_OVERRIDE.get(name, COUNTRY_AIRBNB_COST.get(country, 60))

        enriched[name] = d
    return enriched


# ── Write cities.py ──────────────────────────────────────────────────────────
def write_cities_file(enriched):
    lines = ["CITIES = {\n"]
    for name, d in enriched.items():
        lines.append(f'    "{name}": {{\n')
        # Original 21 fields
        lines.append(f'        "country": {repr(d["country"])}, "region": {repr(d["region"])}, '
                     f'"lat": {d["lat"]}, "lon": {d["lon"]}, "cost": {d["cost"]},\n')
        lines.append(f'        "months": {d["months"]}, '
                     f'"tags": {d["tags"]},\n')
        lines.append(f'        "comfort": {d["comfort"]}, "weather": {repr(d["weather"])}, '
                     f'"highlights": {d["highlights"]},\n')
        lines.append(f'        "description": {repr(d["description"])},\n')
        lines.append(f'        "language": {repr(d["language"])}, "safety": {d["safety"]}, '
                     f'"wifi": {d["wifi"]}, "vegetarian_friendly": {d["vegetarian_friendly"]},\n')
        lines.append(f'        "crowd_level": {d["crowd_level"]}, '
                     f'"city_size": {repr(d["city_size"])},\n')
        lines.append(f'        "beach_type": {repr(d["beach_type"])}, '
                     f'"terrain": {repr(d["terrain"])},\n')
        lines.append(f'        "festivals": {d["festivals"]},\n')
        lines.append(f'        "best_for": {d["best_for"]},\n')
        # New 7 fields
        lines.append(f'        "neighborhoods": {d["neighborhoods"]},\n')
        lines.append(f'        "top_activities": {d["top_activities"]},\n')
        lines.append(f'        "local_food": {d["local_food"]},\n')
        lines.append(f'        "local_drink": {d["local_drink"]},\n')
        lines.append(f'        "things_to_do": {d["things_to_do"]},\n')
        lines.append(f'        "uber_cost": {d["uber_cost"]},\n')
        lines.append(f'        "airbnb_cost": {d["airbnb_cost"]},\n')
        lines.append(f'    }},\n')
    lines.append("}\n")

    outpath = os.path.join(os.path.dirname(__file__), "cities.py")
    with open(outpath, "w") as f:
        f.writelines(lines)
    print(f"Wrote enriched cities.py with {len(enriched)} cities ({sum(len(d) for d in enriched.values())} total fields)")


if __name__ == "__main__":
    enriched = enrich()
    write_cities_file(enriched)
    # Verify
    missing = [n for n, d in enriched.items() if not d.get("neighborhoods") or not d.get("top_activities")]
    if missing:
        print(f"WARNING: {len(missing)} cities missing detail data: {missing[:5]}...")
    else:
        print("All cities have complete detail data!")
