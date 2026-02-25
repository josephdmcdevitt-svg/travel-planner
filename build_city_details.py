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

# ── Visa requirements for US passport holders ──────────────────────────────
COUNTRY_VISA = {
    "Japan": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Thailand": {"status": "visa_free", "max_stay": 30, "notes": "30 days visa-free by air, 15 by land. 60-day tourist visa available"},
    "Vietnam": {"status": "e_visa", "max_stay": 90, "notes": "E-visa required (~$25). Apply at evisa.xuatnhapcanh.gov.vn"},
    "South Korea": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free. K-ETA registration required before travel"},
    "Indonesia": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($35). Extendable once for 30 more days"},
    "India": {"status": "e_visa", "max_stay": 90, "notes": "E-visa required (~$25). Apply at indianvisaonline.gov.in"},
    "Cambodia": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($30) or e-visa available"},
    "Philippines": {"status": "visa_free", "max_stay": 30, "notes": "30 days visa-free, extendable to 59 days at immigration"},
    "Malaysia": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "China": {"status": "visa_free", "max_stay": 15, "notes": "15-day visa-free transit for many cities. Regular visa required for longer stays"},
    "Taiwan": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Sri Lanka": {"status": "e_visa", "max_stay": 30, "notes": "ETA required (~$50). Apply at eta.gov.lk"},
    "Nepal": {"status": "visa_on_arrival", "max_stay": 90, "notes": "Visa on arrival ($30 for 15 days, $50 for 30 days, $125 for 90 days)"},
    "Myanmar": {"status": "e_visa", "max_stay": 28, "notes": "E-visa required ($50). Apply at evisa.moip.gov.mm"},
    "Laos": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($35-42 depending on entry point)"},
    "Mongolia": {"status": "visa_free", "max_stay": 30, "notes": "30 days visa-free for tourism"},
    "Uzbekistan": {"status": "visa_free", "max_stay": 30, "notes": "30 days visa-free for tourism"},
    "Georgia": {"status": "visa_free", "max_stay": 365, "notes": "1 year visa-free for tourism"},
    "Jordan": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($56). Free with Jordan Pass ($70+, includes Petra)"},
    "Oman": {"status": "e_visa", "max_stay": 30, "notes": "E-visa required (~$20). Apply at evisa.rop.gov.om"},
    "Maldives": {"status": "visa_on_arrival", "max_stay": 30, "notes": "30-day visa on arrival, free of charge"},
    "Bhutan": {"status": "e_visa", "max_stay": 30, "notes": "Visa required + $100/day Sustainable Development Fee. Apply through licensed tour operator"},
    "France": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Italy": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Spain": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Portugal": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Greece": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Croatia": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Czech Republic": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Netherlands": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Germany": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Turkey": {"status": "e_visa", "max_stay": 90, "notes": "E-visa required ($50). Apply at evisa.gov.tr"},
    "United Kingdom": {"status": "visa_free", "max_stay": 180, "notes": "6 months visa-free for tourism"},
    "Switzerland": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Austria": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Hungary": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Poland": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Romania": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period"},
    "Bulgaria": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period"},
    "Montenegro": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Albania": {"status": "visa_free", "max_stay": 365, "notes": "1 year visa-free for tourism"},
    "Slovenia": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Estonia": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Latvia": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Lithuania": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Denmark": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Sweden": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Norway": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Finland": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Iceland": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Ireland": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Belgium": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Malta": {"status": "visa_free", "max_stay": 90, "notes": "90 days in any 180-day period (Schengen Area)"},
    "Cyprus": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Colombia": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free, extendable once for 90 more days"},
    "Peru": {"status": "visa_free", "max_stay": 183, "notes": "183 days visa-free for tourism"},
    "Argentina": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Brazil": {"status": "e_visa", "max_stay": 90, "notes": "E-visa required. Apply at vfrb.com.br"},
    "Chile": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Ecuador": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Bolivia": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($160). Reciprocity fee required"},
    "Uruguay": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Paraguay": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Costa Rica": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Panama": {"status": "visa_free", "max_stay": 180, "notes": "180 days visa-free for tourism"},
    "Guatemala": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism (CA-4 region)"},
    "Mexico": {"status": "visa_free", "max_stay": 180, "notes": "180 days visa-free for tourism"},
    "Morocco": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "South Africa": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Tanzania": {"status": "e_visa", "max_stay": 90, "notes": "E-visa required ($50). Apply at visa.immigration.go.tz"},
    "Kenya": {"status": "e_visa", "max_stay": 90, "notes": "ETA required ($30). Apply at etakenya.go.ke"},
    "Egypt": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($25) or e-visa available"},
    "Ghana": {"status": "e_visa", "max_stay": 30, "notes": "Visa required. Apply at ghana.gov.gh"},
    "Rwanda": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($30) or e-visa available"},
    "Ethiopia": {"status": "e_visa", "max_stay": 90, "notes": "E-visa required ($82). Apply at evisa.gov.et"},
    "Namibia": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Botswana": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Senegal": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Madagascar": {"status": "visa_on_arrival", "max_stay": 30, "notes": "Visa on arrival ($37). Apply at airport"},
    "Mauritius": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Tunisia": {"status": "visa_free", "max_stay": 90, "notes": "90 days visa-free for tourism"},
    "Uganda": {"status": "e_visa", "max_stay": 90, "notes": "E-visa required ($50). Apply at visas.immigration.go.ug"},
    "Australia": {"status": "e_visa", "max_stay": 90, "notes": "ETA required ($20). Apply through Australian ETA app"},
    "New Zealand": {"status": "e_visa", "max_stay": 90, "notes": "NZeTA required ($12-17). Apply through NZ Immigration app"},
}

# ── Country-level practical information ─────────────────────────────────────
COUNTRY_PRACTICAL = {
    "Japan": {"currency": "JPY", "currency_symbol": "¥", "currency_name": "Japanese Yen", "plug_type": "Type A (US-style, no adapter needed)", "tipping": "No tipping — it can be considered rude", "emergency": "110 (police), 119 (fire/ambulance)", "sim_info": "Buy tourist SIM at airport or rent pocket wifi", "tap_water": "Safe to drink", "dress_code": "Remove shoes entering homes/some restaurants. Cover up at temples."},
    "Thailand": {"currency": "THB", "currency_symbol": "฿", "currency_name": "Thai Baht", "plug_type": "Type A/B/C (US plugs usually work)", "tipping": "Not expected but appreciated, 20-50 THB for good service", "emergency": "191 (police), 1669 (ambulance)", "sim_info": "Cheap tourist SIMs at 7-Eleven or airport. AIS or DTAC recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover shoulders and knees at temples. Remove shoes before entering."},
    "Vietnam": {"currency": "VND", "currency_symbol": "₫", "currency_name": "Vietnamese Dong", "plug_type": "Type A/C (US plugs usually work)", "tipping": "Not expected, small tips appreciated at restaurants", "emergency": "113 (police), 115 (ambulance)", "sim_info": "Very cheap SIMs at airport. Viettel or Mobifone recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover shoulders and knees at temples and pagodas"},
    "South Korea": {"currency": "KRW", "currency_symbol": "₩", "currency_name": "South Korean Won", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "No tipping culture", "emergency": "112 (police), 119 (fire/ambulance)", "sim_info": "Rent pocket wifi or buy SIM at airport. KT or SK Telecom", "tap_water": "Safe to drink", "dress_code": "No special requirements. Remove shoes indoors."},
    "Indonesia": {"currency": "IDR", "currency_symbol": "Rp", "currency_name": "Indonesian Rupiah", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants if no service charge. Small tips for drivers", "emergency": "110 (police), 118 (ambulance)", "sim_info": "Buy SIM at airport. Telkomsel recommended for best coverage", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover up at temples. Sarong required at Balinese temples."},
    "India": {"currency": "INR", "currency_symbol": "₹", "currency_name": "Indian Rupee", "plug_type": "Type C/D/M (adapter needed for US plugs)", "tipping": "10-15% at restaurants, small tips for service staff", "emergency": "100 (police), 102 (ambulance)", "sim_info": "Buy SIM with passport at airport. Jio or Airtel recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover shoulders and knees at temples. Remove shoes."},
    "Cambodia": {"currency": "USD/KHR", "currency_symbol": "$/៛", "currency_name": "US Dollar widely used / Cambodian Riel", "plug_type": "Type A/C (US plugs usually work)", "tipping": "Not expected, $1-2 appreciated", "emergency": "117 (police), 119 (ambulance)", "sim_info": "Cheap SIMs at airport. Smart or Cellcard recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover shoulders and knees at temples (Angkor Wat strictly enforced)"},
    "Philippines": {"currency": "PHP", "currency_symbol": "₱", "currency_name": "Philippine Peso", "plug_type": "Type A/B (US plugs work)", "tipping": "10% at restaurants if no service charge", "emergency": "911", "sim_info": "Buy SIM at airport. Globe or Smart recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements. Casual dress accepted."},
    "Malaysia": {"currency": "MYR", "currency_symbol": "RM", "currency_name": "Malaysian Ringgit", "plug_type": "Type G (UK-style, adapter needed)", "tipping": "Not expected, service charge usually included", "emergency": "999", "sim_info": "Buy SIM at airport. Maxis or Digi recommended", "tap_water": "Generally safe but locals drink bottled", "dress_code": "Cover up at mosques. Remove shoes before entering."},
    "China": {"currency": "CNY", "currency_symbol": "¥", "currency_name": "Chinese Yuan", "plug_type": "Type A/C/I (US plugs often work)", "tipping": "No tipping culture", "emergency": "110 (police), 120 (ambulance)", "sim_info": "Buy SIM at airport. VPN needed for Google/social media", "tap_water": "Not safe — drink bottled or boiled water", "dress_code": "No special requirements"},
    "Taiwan": {"currency": "TWD", "currency_symbol": "NT$", "currency_name": "New Taiwan Dollar", "plug_type": "Type A/B (US plugs work)", "tipping": "No tipping culture", "emergency": "110 (police), 119 (ambulance)", "sim_info": "Buy SIM at airport. Chunghwa Telecom recommended", "tap_water": "Safe but locals prefer bottled", "dress_code": "No special requirements"},
    "Sri Lanka": {"currency": "LKR", "currency_symbol": "Rs", "currency_name": "Sri Lankan Rupee", "plug_type": "Type D/G (adapter needed)", "tipping": "10% at restaurants appreciated", "emergency": "119 (police), 110 (ambulance)", "sim_info": "Buy SIM at airport. Dialog recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover shoulders and knees at temples. Remove shoes."},
    "Nepal": {"currency": "NPR", "currency_symbol": "Rs", "currency_name": "Nepalese Rupee", "plug_type": "Type C/D (adapter needed)", "tipping": "10% at restaurants, tips for trekking guides", "emergency": "100 (police), 102 (ambulance)", "sim_info": "Buy SIM in Kathmandu. Ncell recommended", "tap_water": "Not safe — drink bottled or purified water", "dress_code": "Cover up at temples. Remove shoes before entering."},
    "Myanmar": {"currency": "MMK", "currency_symbol": "K", "currency_name": "Myanmar Kyat", "plug_type": "Type C/D/F/G (adapter needed)", "tipping": "Not expected, small tips appreciated", "emergency": "199 (police), 192 (ambulance)", "sim_info": "Buy SIM at airport. MPT or Telenor recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover shoulders and knees at temples. Remove shoes."},
    "Laos": {"currency": "LAK", "currency_symbol": "₭", "currency_name": "Lao Kip", "plug_type": "Type A/B/C (US plugs often work)", "tipping": "Not expected", "emergency": "191 (police), 195 (ambulance)", "sim_info": "Buy SIM in town. Unitel recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover up at temples"},
    "Mongolia": {"currency": "MNT", "currency_symbol": "₮", "currency_name": "Mongolian Tugrik", "plug_type": "Type C/E (adapter needed)", "tipping": "Not traditional, 10% at tourist restaurants", "emergency": "102 (police), 103 (ambulance)", "sim_info": "Buy SIM in Ulaanbaatar. Mobicom recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements"},
    "Uzbekistan": {"currency": "UZS", "currency_symbol": "сўм", "currency_name": "Uzbekistani Som", "plug_type": "Type C/F (adapter needed)", "tipping": "5-10% at restaurants appreciated", "emergency": "102 (police), 103 (ambulance)", "sim_info": "Buy SIM at airport. Ucell or Beeline recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Cover up at mosques and religious sites"},
    "Georgia": {"currency": "GEL", "currency_symbol": "₾", "currency_name": "Georgian Lari", "plug_type": "Type C/F (adapter needed)", "tipping": "10% at restaurants appreciated", "emergency": "112", "sim_info": "Buy SIM at airport. Magti recommended", "tap_water": "Safe in cities, bottled in rural areas", "dress_code": "Cover up at churches and monasteries"},
    "Jordan": {"currency": "JOD", "currency_symbol": "JD", "currency_name": "Jordanian Dinar", "plug_type": "Type B/C/D/G (adapter needed)", "tipping": "10% at restaurants, small tips for service", "emergency": "911", "sim_info": "Buy SIM at airport. Zain recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing recommended, especially at religious sites"},
    "Oman": {"currency": "OMR", "currency_symbol": "OMR", "currency_name": "Omani Rial", "plug_type": "Type G (UK-style, adapter needed)", "tipping": "10% at restaurants if no service charge", "emergency": "9999", "sim_info": "Buy SIM at airport. Omantel recommended", "tap_water": "Safe to drink", "dress_code": "Modest clothing, cover shoulders and knees. Headscarf at mosques for women."},
    "Maldives": {"currency": "MVR", "currency_symbol": "Rf", "currency_name": "Maldivian Rufiyaa (USD widely accepted)", "plug_type": "Type G (UK-style, adapter needed)", "tipping": "10% service charge usually included at resorts", "emergency": "119 (police), 102 (ambulance)", "sim_info": "Buy SIM at Male airport. Dhiraagu recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Bikinis only at resorts. Modest clothing on local islands."},
    "Bhutan": {"currency": "BTN", "currency_symbol": "Nu", "currency_name": "Bhutanese Ngultrum (Indian Rupee accepted)", "plug_type": "Type D/F/G (adapter needed)", "tipping": "Tips for guides and drivers expected ($5-10/day)", "emergency": "113 (police), 112 (ambulance)", "sim_info": "Buy SIM in Thimphu. TashiCell recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing. Formal dress required at dzongs (fortresses)."},
    "France": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/E (adapter needed for US plugs)", "tipping": "Service included, round up or leave 5-10% for great service", "emergency": "112 or 17 (police), 15 (medical)", "sim_info": "Buy SIM at tabac or phone shop. Orange or SFR recommended", "tap_water": "Safe to drink", "dress_code": "Smart casual. Cover up at churches."},
    "Italy": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F/L (adapter needed for US plugs)", "tipping": "Coperto (cover charge) usually included. Round up for good service", "emergency": "112 or 113 (police), 118 (ambulance)", "sim_info": "Buy SIM at phone shop. TIM or Vodafone recommended", "tap_water": "Safe to drink", "dress_code": "Cover shoulders and knees at churches (strictly enforced at Vatican)"},
    "Spain": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "Not expected, round up or leave small change", "emergency": "112", "sim_info": "Buy SIM at phone shop. Vodafone or Orange recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements. Cover up at churches."},
    "Portugal": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "5-10% at restaurants appreciated", "emergency": "112", "sim_info": "Buy SIM at phone shop. MEO or Vodafone recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Greece": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "5-10% at restaurants. Round up for taxis", "emergency": "112 or 100 (police), 166 (ambulance)", "sim_info": "Buy SIM at phone shop. Cosmote recommended", "tap_water": "Safe in cities, bottled on islands", "dress_code": "Cover shoulders and knees at churches and monasteries"},
    "Croatia": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants appreciated", "emergency": "112", "sim_info": "Buy SIM at phone shop. A1 or T-Mobile recommended", "tap_water": "Safe to drink", "dress_code": "Cover up at churches"},
    "Czech Republic": {"currency": "CZK", "currency_symbol": "Kč", "currency_name": "Czech Koruna", "plug_type": "Type C/E (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "112 or 158 (police), 155 (ambulance)", "sim_info": "Buy SIM at phone shop. O2 or Vodafone recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Netherlands": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "Round up or 5-10% at restaurants", "emergency": "112", "sim_info": "Buy SIM at phone shop. KPN or Vodafone recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Germany": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "5-10% at restaurants, round up for taxis", "emergency": "112 or 110 (police)", "sim_info": "Buy SIM at phone shop. O2 or Telekom recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Turkey": {"currency": "TRY", "currency_symbol": "₺", "currency_name": "Turkish Lira", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10-15% at restaurants", "emergency": "112 or 155 (police), 112 (ambulance)", "sim_info": "Buy SIM at airport. Turkcell recommended", "tap_water": "Not recommended — drink bottled water", "dress_code": "Cover shoulders and knees at mosques. Headscarf for women at mosques."},
    "United Kingdom": {"currency": "GBP", "currency_symbol": "£", "currency_name": "British Pound", "plug_type": "Type G (UK-style, adapter needed for US plugs)", "tipping": "10-15% at restaurants if no service charge", "emergency": "999 or 112", "sim_info": "Buy SIM at phone shop. EE or Three recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Switzerland": {"currency": "CHF", "currency_symbol": "CHF", "currency_name": "Swiss Franc", "plug_type": "Type J (adapter needed for US plugs)", "tipping": "Service included. Round up for good service", "emergency": "112 or 117 (police), 144 (ambulance)", "sim_info": "Buy SIM at phone shop. Swisscom recommended. Very expensive.", "tap_water": "Safe to drink — excellent quality", "dress_code": "No special requirements"},
    "Austria": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "5-10% at restaurants", "emergency": "112 or 133 (police), 144 (ambulance)", "sim_info": "Buy SIM at phone shop. A1 or Magenta recommended", "tap_water": "Safe to drink — excellent quality", "dress_code": "No special requirements"},
    "Hungary": {"currency": "HUF", "currency_symbol": "Ft", "currency_name": "Hungarian Forint", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10-15% at restaurants", "emergency": "112 or 107 (police), 104 (ambulance)", "sim_info": "Buy SIM at phone shop. Telekom or Vodafone recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Poland": {"currency": "PLN", "currency_symbol": "zł", "currency_name": "Polish Zloty", "plug_type": "Type C/E (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "112 or 997 (police), 999 (ambulance)", "sim_info": "Buy SIM at phone shop. Orange or Play recommended", "tap_water": "Safe to drink", "dress_code": "Cover up at churches"},
    "Romania": {"currency": "RON", "currency_symbol": "lei", "currency_name": "Romanian Leu", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "112", "sim_info": "Buy SIM at phone shop. Orange or Vodafone recommended", "tap_water": "Safe to drink in cities", "dress_code": "Cover up at monasteries and churches"},
    "Bulgaria": {"currency": "BGN", "currency_symbol": "лв", "currency_name": "Bulgarian Lev", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "112", "sim_info": "Buy SIM at phone shop. A1 recommended", "tap_water": "Safe to drink", "dress_code": "Cover up at churches and monasteries"},
    "Montenegro": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "112", "sim_info": "Buy SIM at phone shop. Crnogorski Telekom recommended", "tap_water": "Safe to drink", "dress_code": "Cover up at monasteries"},
    "Albania": {"currency": "ALL", "currency_symbol": "L", "currency_name": "Albanian Lek", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants appreciated", "emergency": "112 or 129 (police), 127 (ambulance)", "sim_info": "Buy SIM at phone shop. Vodafone Albania recommended", "tap_water": "Not recommended — drink bottled water", "dress_code": "Cover up at mosques and churches"},
    "Slovenia": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "112", "sim_info": "Buy SIM at phone shop. A1 recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Estonia": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants appreciated", "emergency": "112", "sim_info": "Buy SIM at phone shop. Telia recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Latvia": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants appreciated", "emergency": "112", "sim_info": "Buy SIM at phone shop. LMT recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Lithuania": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "10% at restaurants appreciated", "emergency": "112", "sim_info": "Buy SIM at phone shop. Telia recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Denmark": {"currency": "DKK", "currency_symbol": "kr", "currency_name": "Danish Krone", "plug_type": "Type C/K (adapter needed for US plugs)", "tipping": "Service included. Round up for great service", "emergency": "112", "sim_info": "Buy SIM at phone shop. TDC or Telenor recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Sweden": {"currency": "SEK", "currency_symbol": "kr", "currency_name": "Swedish Krona", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "Service included. Round up at restaurants", "emergency": "112", "sim_info": "Buy SIM at phone shop. Telia or Tele2 recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Norway": {"currency": "NOK", "currency_symbol": "kr", "currency_name": "Norwegian Krone", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "Service included. Round up for great service", "emergency": "112", "sim_info": "Buy SIM at phone shop. Telenor recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Finland": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "Service included. Round up for great service", "emergency": "112", "sim_info": "Buy SIM at phone shop. DNA or Elisa recommended", "tap_water": "Safe to drink — excellent quality", "dress_code": "No special requirements"},
    "Iceland": {"currency": "ISK", "currency_symbol": "kr", "currency_name": "Icelandic Krona", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "Service included. Not expected", "emergency": "112", "sim_info": "Buy SIM at airport. Siminn recommended", "tap_water": "Safe to drink — some of the purest in the world", "dress_code": "Dress warmly in layers. No special cultural requirements."},
    "Ireland": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type G (UK-style, adapter needed for US plugs)", "tipping": "10% at restaurants. Not expected in pubs", "emergency": "112 or 999", "sim_info": "Buy SIM at phone shop. Three or Vodafone recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Belgium": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type C/E (adapter needed for US plugs)", "tipping": "Service included. Round up for great service", "emergency": "112 or 101 (police), 100 (ambulance)", "sim_info": "Buy SIM at phone shop. Proximus recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Malta": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type G (UK-style, adapter needed for US plugs)", "tipping": "10% at restaurants if no service charge", "emergency": "112", "sim_info": "Buy SIM at phone shop. GO or Melita recommended", "tap_water": "Safe but tastes mineral-heavy, locals prefer bottled", "dress_code": "Cover up at churches"},
    "Cyprus": {"currency": "EUR", "currency_symbol": "€", "currency_name": "Euro", "plug_type": "Type G (UK-style, adapter needed for US plugs)", "tipping": "10% at restaurants if no service charge", "emergency": "112 or 199 (police), 199 (ambulance)", "sim_info": "Buy SIM at phone shop. MTN or Cyta recommended", "tap_water": "Safe to drink", "dress_code": "Cover up at churches and monasteries"},
    "Colombia": {"currency": "COP", "currency_symbol": "$", "currency_name": "Colombian Peso", "plug_type": "Type A/B (US plugs work)", "tipping": "10% at restaurants (often added automatically)", "emergency": "123", "sim_info": "Buy SIM at airport. Claro or Movistar recommended", "tap_water": "Safe in major cities like Bogota and Medellin", "dress_code": "No special requirements"},
    "Peru": {"currency": "PEN", "currency_symbol": "S/.", "currency_name": "Peruvian Sol", "plug_type": "Type A/B/C (US plugs usually work)", "tipping": "10% at restaurants appreciated", "emergency": "105 (police), 116 (ambulance)", "sim_info": "Buy SIM at airport. Claro or Movistar recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements. Dress warm for altitude."},
    "Argentina": {"currency": "ARS", "currency_symbol": "$", "currency_name": "Argentine Peso", "plug_type": "Type C/I (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "911", "sim_info": "Buy SIM at phone shop. Personal or Movistar recommended", "tap_water": "Safe in Buenos Aires, bottled elsewhere", "dress_code": "No special requirements"},
    "Brazil": {"currency": "BRL", "currency_symbol": "R$", "currency_name": "Brazilian Real", "plug_type": "Type N (adapter needed for US plugs)", "tipping": "10% service charge usually included", "emergency": "190 (police), 192 (ambulance)", "sim_info": "Buy SIM at phone shop with passport. Claro or Vivo recommended", "tap_water": "Not recommended — drink bottled or filtered water", "dress_code": "No special requirements. Beach culture is casual."},
    "Chile": {"currency": "CLP", "currency_symbol": "$", "currency_name": "Chilean Peso", "plug_type": "Type C/L (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "133 (police), 131 (ambulance)", "sim_info": "Buy SIM at phone shop. Entel or Movistar recommended", "tap_water": "Safe to drink in Santiago and major cities", "dress_code": "No special requirements"},
    "Ecuador": {"currency": "USD", "currency_symbol": "$", "currency_name": "US Dollar", "plug_type": "Type A/B (US plugs work)", "tipping": "10% at restaurants", "emergency": "911", "sim_info": "Buy SIM at phone shop. Claro recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements"},
    "Bolivia": {"currency": "BOB", "currency_symbol": "Bs", "currency_name": "Bolivian Boliviano", "plug_type": "Type A/C (US plugs usually work)", "tipping": "5-10% at restaurants appreciated", "emergency": "110 (police), 118 (ambulance)", "sim_info": "Buy SIM in city. Entel or Tigo recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements. Dress warm for altitude."},
    "Uruguay": {"currency": "UYU", "currency_symbol": "$U", "currency_name": "Uruguayan Peso", "plug_type": "Type C/F/I/L (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "911", "sim_info": "Buy SIM at phone shop. Antel recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements"},
    "Paraguay": {"currency": "PYG", "currency_symbol": "₲", "currency_name": "Paraguayan Guarani", "plug_type": "Type C (adapter needed for US plugs)", "tipping": "10% at restaurants appreciated", "emergency": "911", "sim_info": "Buy SIM at phone shop. Tigo recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements"},
    "Costa Rica": {"currency": "CRC", "currency_symbol": "₡", "currency_name": "Costa Rican Colon (USD widely accepted)", "plug_type": "Type A/B (US plugs work)", "tipping": "10% service charge included, extra tip appreciated", "emergency": "911", "sim_info": "Buy SIM at airport. Kolbi recommended", "tap_water": "Safe to drink in most areas", "dress_code": "No special requirements"},
    "Panama": {"currency": "USD/PAB", "currency_symbol": "$", "currency_name": "US Dollar / Panamanian Balboa", "plug_type": "Type A/B (US plugs work)", "tipping": "10-15% at restaurants", "emergency": "911", "sim_info": "Buy SIM at phone shop. Claro recommended", "tap_water": "Safe in Panama City, bottled elsewhere", "dress_code": "No special requirements"},
    "Guatemala": {"currency": "GTQ", "currency_symbol": "Q", "currency_name": "Guatemalan Quetzal", "plug_type": "Type A/B (US plugs work)", "tipping": "10% at restaurants", "emergency": "110 (police), 123 (ambulance)", "sim_info": "Buy SIM at phone shop. Tigo recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements. Modest at churches."},
    "Mexico": {"currency": "MXN", "currency_symbol": "$", "currency_name": "Mexican Peso", "plug_type": "Type A/B (US plugs work)", "tipping": "15-20% at restaurants (similar to US)", "emergency": "911", "sim_info": "Buy SIM at airport. Telcel recommended for best coverage", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements"},
    "Morocco": {"currency": "MAD", "currency_symbol": "MAD", "currency_name": "Moroccan Dirham", "plug_type": "Type C/E (adapter needed for US plugs)", "tipping": "10% at restaurants. Small tips for guides and porters", "emergency": "19 (police), 15 (ambulance)", "sim_info": "Buy SIM at airport. Maroc Telecom recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing recommended. Cover shoulders and knees, especially in medinas."},
    "South Africa": {"currency": "ZAR", "currency_symbol": "R", "currency_name": "South African Rand", "plug_type": "Type M/N (adapter needed for US plugs)", "tipping": "10-15% at restaurants", "emergency": "10111 (police), 10177 (ambulance)", "sim_info": "Buy SIM at airport. Vodacom or MTN recommended", "tap_water": "Safe in Cape Town and major cities", "dress_code": "No special requirements"},
    "Tanzania": {"currency": "TZS", "currency_symbol": "TSh", "currency_name": "Tanzanian Shilling", "plug_type": "Type D/G (adapter needed)", "tipping": "10% at restaurants. $5-10/day for safari guides", "emergency": "112 or 114 (police), 114 (ambulance)", "sim_info": "Buy SIM at airport. Vodacom recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing on Zanzibar (Muslim culture). Cover up away from beach."},
    "Kenya": {"currency": "KES", "currency_symbol": "KSh", "currency_name": "Kenyan Shilling", "plug_type": "Type G (UK-style, adapter needed)", "tipping": "10% at restaurants. Tips for safari guides", "emergency": "999 or 112", "sim_info": "Buy SIM at airport. Safaricom recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "No special requirements. Modest at coast (Muslim areas)."},
    "Egypt": {"currency": "EGP", "currency_symbol": "E£", "currency_name": "Egyptian Pound", "plug_type": "Type C/F (adapter needed for US plugs)", "tipping": "Baksheesh expected everywhere. 10-15% at restaurants", "emergency": "122 (police), 123 (ambulance)", "sim_info": "Buy SIM at airport. Vodafone Egypt recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing recommended. Cover shoulders and knees at mosques."},
    "Ghana": {"currency": "GHS", "currency_symbol": "GH₵", "currency_name": "Ghanaian Cedi", "plug_type": "Type D/G (adapter needed)", "tipping": "10% at restaurants appreciated", "emergency": "191 (police), 193 (ambulance)", "sim_info": "Buy SIM at phone shop. MTN recommended", "tap_water": "Not safe — drink bottled or sachet water", "dress_code": "No special requirements. Modest at religious sites."},
    "Rwanda": {"currency": "RWF", "currency_symbol": "FRw", "currency_name": "Rwandan Franc", "plug_type": "Type C/J (adapter needed)", "tipping": "10% at restaurants appreciated", "emergency": "112", "sim_info": "Buy SIM at airport. MTN Rwanda recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing recommended. Plastic bags are banned."},
    "Ethiopia": {"currency": "ETB", "currency_symbol": "Br", "currency_name": "Ethiopian Birr", "plug_type": "Type C/E/F (adapter needed)", "tipping": "10% at restaurants", "emergency": "911", "sim_info": "Buy SIM from Ethio Telecom (only provider)", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing at churches. Remove shoes at Ethiopian Orthodox churches."},
    "Namibia": {"currency": "NAD", "currency_symbol": "N$", "currency_name": "Namibian Dollar (South African Rand also accepted)", "plug_type": "Type D/M (adapter needed)", "tipping": "10-15% at restaurants", "emergency": "10111 (police)", "sim_info": "Buy SIM at phone shop. MTC recommended", "tap_water": "Safe in Windhoek, bottled elsewhere", "dress_code": "No special requirements"},
    "Botswana": {"currency": "BWP", "currency_symbol": "P", "currency_name": "Botswana Pula", "plug_type": "Type D/G/M (adapter needed)", "tipping": "10% at restaurants. Tips for safari guides ($10-20/day)", "emergency": "999 (police), 997 (ambulance)", "sim_info": "Buy SIM at phone shop. Mascom recommended", "tap_water": "Safe in cities, bottled in rural areas", "dress_code": "No special requirements"},
    "Senegal": {"currency": "XOF", "currency_symbol": "CFA", "currency_name": "West African CFA Franc", "plug_type": "Type C/D/E/K (adapter needed)", "tipping": "10% at restaurants appreciated", "emergency": "17 (police), 18 (fire)", "sim_info": "Buy SIM at phone shop. Orange Senegal recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing recommended. Cover up in Muslim areas."},
    "Madagascar": {"currency": "MGA", "currency_symbol": "Ar", "currency_name": "Malagasy Ariary", "plug_type": "Type C/D/E/J/K (adapter needed)", "tipping": "10% at restaurants appreciated", "emergency": "117 (police), 118 (ambulance)", "sim_info": "Buy SIM in Antananarivo. Airtel recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing in rural areas. Respect local fady (taboos)."},
    "Mauritius": {"currency": "MUR", "currency_symbol": "Rs", "currency_name": "Mauritian Rupee", "plug_type": "Type C/G (adapter needed)", "tipping": "10% at restaurants if no service charge", "emergency": "999 (police), 114 (ambulance)", "sim_info": "Buy SIM at airport. Emtel or MyT recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements. Beach casual widely accepted."},
    "Tunisia": {"currency": "TND", "currency_symbol": "DT", "currency_name": "Tunisian Dinar", "plug_type": "Type C/E (adapter needed for US plugs)", "tipping": "10% at restaurants", "emergency": "197 (police), 190 (ambulance)", "sim_info": "Buy SIM at phone shop. Ooredoo recommended", "tap_water": "Safe in cities, bottled preferred", "dress_code": "Modest clothing recommended. Cover up at mosques."},
    "Uganda": {"currency": "UGX", "currency_symbol": "USh", "currency_name": "Ugandan Shilling", "plug_type": "Type G (UK-style, adapter needed)", "tipping": "10% at restaurants appreciated", "emergency": "999", "sim_info": "Buy SIM at phone shop. MTN Uganda recommended", "tap_water": "Not safe — drink bottled water", "dress_code": "Modest clothing recommended"},
    "Australia": {"currency": "AUD", "currency_symbol": "A$", "currency_name": "Australian Dollar", "plug_type": "Type I (adapter needed for US plugs)", "tipping": "Not expected but 10% appreciated for great service", "emergency": "000", "sim_info": "Buy SIM at airport. Telstra recommended for best coverage", "tap_water": "Safe to drink", "dress_code": "No special requirements. Very casual culture."},
    "New Zealand": {"currency": "NZD", "currency_symbol": "NZ$", "currency_name": "New Zealand Dollar", "plug_type": "Type I (adapter needed for US plugs)", "tipping": "Not expected but appreciated", "emergency": "111", "sim_info": "Buy SIM at airport. Spark or Vodafone recommended", "tap_water": "Safe to drink", "dress_code": "No special requirements. Very casual culture."},
}

# ── Inter-city transport routes ─────────────────────────────────────────────
TRANSPORT_ROUTES = {
    # Japan
    ("Tokyo", "Kyoto"): {"mode": "train", "name": "Shinkansen Bullet Train", "duration": 2.25, "cost": 120, "notes": "Covered by Japan Rail Pass. Nozomi is fastest but not JR Pass eligible."},
    ("Tokyo", "Osaka"): {"mode": "train", "name": "Shinkansen Bullet Train", "duration": 2.5, "cost": 130, "notes": "Covered by Japan Rail Pass"},
    ("Kyoto", "Osaka"): {"mode": "train", "name": "JR Special Rapid", "duration": 0.5, "cost": 8, "notes": "Very frequent trains, no reservation needed"},
    ("Tokyo", "Hiroshima"): {"mode": "train", "name": "Shinkansen Bullet Train", "duration": 4.0, "cost": 180, "notes": "Covered by Japan Rail Pass"},
    ("Tokyo", "Hakone"): {"mode": "train", "name": "Odakyu Romance Car", "duration": 1.5, "cost": 15, "notes": "Scenic ride. Hakone Free Pass recommended."},
    ("Osaka", "Hiroshima"): {"mode": "train", "name": "Shinkansen Bullet Train", "duration": 1.5, "cost": 90, "notes": "Covered by Japan Rail Pass"},
    ("Kyoto", "Nara"): {"mode": "train", "name": "JR Nara Line", "duration": 0.75, "cost": 7, "notes": "Easy day trip from Kyoto"},
    # Thailand
    ("Bangkok", "Chiang Mai"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.25, "cost": 40, "notes": "Multiple daily flights. Overnight train also available (~12h, $20-60)"},
    ("Bangkok", "Phuket"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.5, "cost": 45, "notes": "Multiple daily flights"},
    ("Bangkok", "Krabi"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.25, "cost": 40, "notes": "Multiple daily flights"},
    ("Chiang Mai", "Pai"): {"mode": "bus", "name": "Minivan", "duration": 3.0, "cost": 8, "notes": "Winding mountain road, 762 curves. Take motion sickness pills."},
    # Vietnam
    ("Hanoi", "Ho Chi Minh City"): {"mode": "flight", "name": "Domestic Flight", "duration": 2.0, "cost": 50, "notes": "Reunification Express train is scenic but 30+ hours"},
    ("Hanoi", "Da Nang"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.25, "cost": 35, "notes": "Train also available (~15h, $25-40)"},
    ("Da Nang", "Hoi An"): {"mode": "bus", "name": "Taxi/Grab", "duration": 0.75, "cost": 12, "notes": "Short ride, use Grab app"},
    ("Hanoi", "Sapa"): {"mode": "bus", "name": "Sleeper Bus", "duration": 5.5, "cost": 15, "notes": "Overnight bus or train to Lao Cai + transfer"},
    # Europe
    ("Paris", "London"): {"mode": "train", "name": "Eurostar", "duration": 2.25, "cost": 80, "notes": "High-speed train through Channel Tunnel. Book early for best fares."},
    ("Paris", "Amsterdam"): {"mode": "train", "name": "Thalys", "duration": 3.25, "cost": 60, "notes": "High-speed train, book early"},
    ("Paris", "Barcelona"): {"mode": "train", "name": "TGV", "duration": 6.5, "cost": 70, "notes": "High-speed train via Perpignan. Flights also available (~2h, $50+)"},
    ("Rome", "Florence"): {"mode": "train", "name": "Frecciarossa", "duration": 1.5, "cost": 30, "notes": "High-speed train, very frequent"},
    ("Rome", "Venice"): {"mode": "train", "name": "Frecciarossa", "duration": 3.75, "cost": 45, "notes": "High-speed train"},
    ("Berlin", "Prague"): {"mode": "train", "name": "EuroCity", "duration": 4.5, "cost": 25, "notes": "Scenic route through Saxon Switzerland"},
    ("Prague", "Budapest"): {"mode": "train", "name": "EuroCity", "duration": 7.0, "cost": 30, "notes": "Direct train or bus (~6.5h, $20)"},
    ("Budapest", "Vienna"): {"mode": "train", "name": "Railjet", "duration": 2.5, "cost": 20, "notes": "Very frequent. Flixbus also available (~2.5h, $12)"},
    ("Amsterdam", "Berlin"): {"mode": "train", "name": "ICE", "duration": 6.0, "cost": 40, "notes": "Direct train. Flixbus also available (~8h, $20)"},
    ("Barcelona", "Lisbon"): {"mode": "flight", "name": "Flight", "duration": 1.5, "cost": 50, "notes": "No good train connection. Fly or overnight bus (~10h)"},
    ("London", "Edinburgh"): {"mode": "train", "name": "LNER", "duration": 4.5, "cost": 50, "notes": "Direct train from King's Cross. Book early."},
    ("Istanbul", "Cappadocia"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.25, "cost": 35, "notes": "Fly to Kayseri or Nevsehir airport"},
    # South America
    ("Buenos Aires", "Rio de Janeiro"): {"mode": "flight", "name": "Flight", "duration": 3.0, "cost": 120, "notes": "Direct flights available"},
    ("Lima", "Cusco"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.25, "cost": 60, "notes": "Acclimatize slowly — Cusco is at 3,400m altitude"},
    ("Bogota", "Medellin"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.0, "cost": 35, "notes": "Multiple daily flights. Bus also available (~9h, $15)"},
    # Southeast Asia cross-border
    ("Bangkok", "Siem Reap"): {"mode": "flight", "name": "Flight", "duration": 1.0, "cost": 60, "notes": "Direct flights. Bus via border also possible (~8h)"},
    ("Bangkok", "Hanoi"): {"mode": "flight", "name": "Flight", "duration": 2.0, "cost": 80, "notes": "Direct flights"},
    ("Bali", "Bangkok"): {"mode": "flight", "name": "Flight", "duration": 4.0, "cost": 100, "notes": "Direct or 1-stop flights"},
    ("Seoul", "Tokyo"): {"mode": "flight", "name": "Flight", "duration": 2.5, "cost": 100, "notes": "Very frequent flights. Budget airlines available."},
    # Other
    ("Marrakech", "Fez"): {"mode": "train", "name": "ONCF Train", "duration": 7.0, "cost": 25, "notes": "First class recommended"},
    ("Cape Town", "Johannesburg"): {"mode": "flight", "name": "Domestic Flight", "duration": 2.0, "cost": 80, "notes": "Multiple daily flights"},
    ("Sydney", "Melbourne"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.5, "cost": 60, "notes": "Very frequent flights. Drive also popular (~9h along coast)"},
    ("Delhi", "Agra"): {"mode": "train", "name": "Gatimaan Express", "duration": 1.75, "cost": 10, "notes": "India's fastest train. Book ahead."},
    ("Mexico City", "Oaxaca"): {"mode": "flight", "name": "Domestic Flight", "duration": 1.0, "cost": 50, "notes": "Bus also available (~6.5h, $25)"},
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

# ── Structured activities for hand-crafted cities ────────────────────────────
# Each activity has: name, address, hours, cost, tags, time_of_day, description
# maps_url is auto-generated in enrich() from name + city
CITY_STRUCTURED_ACTIVITIES = {
    "Tokyo": [
        {"name": "Senso-ji Temple", "address": "2-3-1 Asakusa, Taito City", "hours": "6am-5pm", "cost": "Free", "tags": ["temples", "culture"], "time_of_day": "Morning", "description": "Tokyo's oldest temple with the iconic Kaminarimon thunder gate"},
        {"name": "Tsukiji Outer Market", "address": "4-16-2 Tsukiji, Chuo City", "hours": "5am-2pm", "cost": "$10-20", "tags": ["food", "shopping"], "time_of_day": "Morning", "description": "Fresh sushi, tamagoyaki, and seafood stalls"},
        {"name": "Meiji Shrine", "address": "1-1 Yoyogikamizonocho, Shibuya", "hours": "Dawn-dusk", "cost": "Free", "tags": ["temples", "culture"], "time_of_day": "Morning", "description": "Serene Shinto shrine in a forested grove near Harajuku"},
        {"name": "Shibuya Crossing", "address": "Shibuya Station, Shibuya", "hours": "24/7", "cost": "Free", "tags": ["photography", "culture"], "time_of_day": "Evening", "description": "The world's busiest pedestrian crossing — best viewed from Shibuya Sky"},
        {"name": "teamLab Borderless", "address": "Azabudai Hills, Minato City", "hours": "10am-9pm", "cost": "$30", "tags": ["art", "photography"], "time_of_day": "Afternoon", "description": "Immersive digital art museum with flowing, borderless installations"},
        {"name": "Tokyo Skytree", "address": "1-1-2 Oshiage, Sumida City", "hours": "10am-9pm", "cost": "$20-30", "tags": ["architecture", "photography"], "time_of_day": "Afternoon", "description": "634m broadcasting tower with panoramic observation decks"},
        {"name": "Golden Gai", "address": "1 Kabukicho, Shinjuku", "hours": "8pm-late", "cost": "$5-15/drink", "tags": ["nightlife", "culture"], "time_of_day": "Night", "description": "Tiny themed bars crammed into narrow alleys — each seats 5-10 people"},
        {"name": "Akihabara Electric Town", "address": "Akihabara, Chiyoda City", "hours": "10am-9pm", "cost": "Free to browse", "tags": ["shopping", "culture"], "time_of_day": "Afternoon", "description": "Anime, manga, electronics, and gaming mecca"},
        {"name": "Yoyogi Park", "address": "2-1 Yoyogikamizonocho, Shibuya", "hours": "24/7", "cost": "Free", "tags": ["culture", "photography"], "time_of_day": "Morning", "description": "Massive park where Tokyoites relax, perform, and cosplay on weekends"},
        {"name": "Omoide Yokocho (Memory Lane)", "address": "1 Nishishinjuku, Shinjuku", "hours": "5pm-midnight", "cost": "$5-15", "tags": ["food", "nightlife"], "time_of_day": "Evening", "description": "Atmospheric alley of tiny yakitori stalls under the train tracks"},
    ],
    "Kyoto": [
        {"name": "Fushimi Inari Shrine", "address": "68 Fukakusa Yabunouchicho, Fushimi", "hours": "24/7", "cost": "Free", "tags": ["temples", "hiking", "photography"], "time_of_day": "Morning", "description": "Thousands of vermillion torii gates winding up the mountain"},
        {"name": "Kinkaku-ji (Golden Pavilion)", "address": "1 Kinkakujicho, Kita Ward", "hours": "9am-5pm", "cost": "$4", "tags": ["temples", "photography"], "time_of_day": "Morning", "description": "Gold-leaf covered Zen temple reflected in a mirror pond"},
        {"name": "Arashiyama Bamboo Grove", "address": "Sagaogurayama, Ukyo Ward", "hours": "24/7", "cost": "Free", "tags": ["photography", "hiking"], "time_of_day": "Morning", "description": "Towering bamboo stalks creating an ethereal green tunnel"},
        {"name": "Nishiki Market", "address": "Nishikikoji St, Nakagyo Ward", "hours": "9am-6pm", "cost": "$5-15 for tastings", "tags": ["food", "shopping"], "time_of_day": "Midday", "description": "Five blocks of food stalls and specialty shops — Kyoto's kitchen"},
        {"name": "Gion District", "address": "Gionmachi, Higashiyama Ward", "hours": "Best at dusk", "cost": "Free", "tags": ["culture", "photography"], "time_of_day": "Evening", "description": "Geisha district with traditional wooden machiya and tea houses"},
        {"name": "Ryoan-ji Rock Garden", "address": "13 Ryoanji Goryonoshitacho, Ukyo", "hours": "8am-5pm", "cost": "$5", "tags": ["temples", "wellness"], "time_of_day": "Morning", "description": "Japan's most famous Zen rock garden — 15 stones in raked gravel"},
        {"name": "Philosopher's Path", "address": "Shishigatani, Sakyo Ward", "hours": "24/7", "cost": "Free", "tags": ["hiking", "photography"], "time_of_day": "Afternoon", "description": "2km canal-side walking path lined with cherry trees and temples"},
        {"name": "Nijo Castle", "address": "541 Nijojocho, Nakagyo Ward", "hours": "8:45am-5pm", "cost": "$10", "tags": ["temples", "architecture"], "time_of_day": "Afternoon", "description": "Shogun's castle with nightingale floors that chirp when walked on"},
        {"name": "Tea Ceremony Experience", "address": "Various locations in Gion", "hours": "By reservation", "cost": "$30-50", "tags": ["culture", "wellness"], "time_of_day": "Afternoon", "description": "Traditional matcha ceremony in an authentic tea house"},
        {"name": "Pontocho Alley", "address": "Pontocho, Nakagyo Ward", "hours": "5pm-late", "cost": "$20-50/meal", "tags": ["food", "nightlife"], "time_of_day": "Evening", "description": "Narrow lantern-lit alley along the Kamo River with restaurants"},
    ],
    "Bangkok": [
        {"name": "Grand Palace & Wat Phra Kaew", "address": "Na Phra Lan Rd, Phra Nakhon", "hours": "8:30am-3:30pm", "cost": "$16", "tags": ["temples", "architecture"], "time_of_day": "Morning", "description": "Thailand's most sacred temple and former royal residence"},
        {"name": "Wat Pho (Reclining Buddha)", "address": "2 Sanam Chai Rd, Phra Nakhon", "hours": "8am-6:30pm", "cost": "$7", "tags": ["temples", "wellness"], "time_of_day": "Morning", "description": "Massive 46m gold reclining Buddha and birthplace of Thai massage"},
        {"name": "Chatuchak Weekend Market", "address": "Kamphaeng Phet 2 Rd, Chatuchak", "hours": "Sat-Sun 9am-6pm", "cost": "Free entry", "tags": ["shopping", "food"], "time_of_day": "Morning", "description": "15,000+ stalls across 35 acres — one of world's largest markets"},
        {"name": "Chinatown (Yaowarat)", "address": "Yaowarat Rd, Samphanthawong", "hours": "Best after 6pm", "cost": "$3-10", "tags": ["food", "culture"], "time_of_day": "Evening", "description": "Bangkok's best street food comes alive after dark"},
        {"name": "Wat Arun", "address": "158 Wang Doem Rd, Bangkok Yai", "hours": "8am-6pm", "cost": "$2", "tags": ["temples", "photography"], "time_of_day": "Afternoon", "description": "Temple of Dawn with stunning porcelain-decorated spire on the river"},
        {"name": "Jim Thompson House", "address": "6 Soi Kasemsan 2, Pathum Wan", "hours": "10am-6pm", "cost": "$8", "tags": ["art", "culture"], "time_of_day": "Afternoon", "description": "Traditional Thai houses filled with Southeast Asian art collection"},
        {"name": "Khao San Road", "address": "Khao San Rd, Phra Nakhon", "hours": "Best after 8pm", "cost": "Free to walk", "tags": ["nightlife", "food"], "time_of_day": "Night", "description": "Legendary backpacker street with bars, food, and energy"},
        {"name": "Thai Cooking Class", "address": "Various (Silom, Khao San area)", "hours": "Morning or afternoon sessions", "cost": "$30-50", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Learn to cook pad thai, green curry, and mango sticky rice"},
        {"name": "Rooftop Bar at Lebua", "address": "1055 Silom Rd, Bang Rak", "hours": "5pm-1am", "cost": "$15-25/drink", "tags": ["nightlife", "photography"], "time_of_day": "Evening", "description": "Sky Bar on the 63rd floor — famous from The Hangover II"},
        {"name": "Chao Phraya River Cruise", "address": "Various piers along the river", "hours": "Sunset cruises 5-7pm", "cost": "$15-40", "tags": ["photography", "culture"], "time_of_day": "Evening", "description": "Cruise past temples, the Grand Palace, and Wat Arun at sunset"},
    ],
    "Paris": [
        {"name": "Louvre Museum", "address": "Rue de Rivoli, 1st arr.", "hours": "9am-6pm (closed Tue)", "cost": "$19", "tags": ["art", "architecture"], "time_of_day": "Morning", "description": "World's largest art museum — home of the Mona Lisa"},
        {"name": "Eiffel Tower", "address": "Champ de Mars, 7th arr.", "hours": "9:30am-11:45pm", "cost": "$18-29", "tags": ["architecture", "photography"], "time_of_day": "Evening", "description": "Paris's iconic iron tower — best visited at sunset"},
        {"name": "Musee d'Orsay", "address": "1 Rue de la Legion d'Honneur, 7th arr.", "hours": "9:30am-6pm (closed Mon)", "cost": "$16", "tags": ["art"], "time_of_day": "Afternoon", "description": "Impressionist masterpieces by Monet, Renoir, and Van Gogh"},
        {"name": "Montmartre & Sacre-Coeur", "address": "35 Rue du Chevalier de la Barre, 18th arr.", "hours": "6am-10:30pm", "cost": "Free", "tags": ["architecture", "photography", "culture"], "time_of_day": "Morning", "description": "Hilltop basilica with stunning city views and artist-filled streets"},
        {"name": "Notre-Dame Cathedral", "address": "6 Parvis Notre-Dame, 4th arr.", "hours": "8am-6:45pm", "cost": "Free", "tags": ["architecture", "temples"], "time_of_day": "Morning", "description": "Gothic masterpiece on the Seine — reopened after restoration"},
        {"name": "Luxembourg Gardens", "address": "Rue de Medicis, 6th arr.", "hours": "Dawn-dusk", "cost": "Free", "tags": ["wellness", "photography"], "time_of_day": "Afternoon", "description": "Elegant 25-hectare garden with fountains, sculptures, and chairs"},
        {"name": "Le Marais Food Tour", "address": "Le Marais, 3rd/4th arr.", "hours": "Morning departures", "cost": "$80-100", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Taste falafel, pastries, cheese, and wine in Paris's trendiest quarter"},
        {"name": "Seine River Cruise", "address": "Port de la Bourdonnais, 7th arr.", "hours": "Various, sunset best", "cost": "$15-20", "tags": ["photography"], "time_of_day": "Evening", "description": "Glide past illuminated landmarks from the river"},
        {"name": "Paris Catacombs", "address": "1 Ave du Colonel Henri Rol-Tanguy, 14th arr.", "hours": "10am-8pm (closed Mon)", "cost": "$15", "tags": ["culture"], "time_of_day": "Afternoon", "description": "Underground ossuary holding the remains of 6 million people"},
        {"name": "Cafe de Flore", "address": "172 Blvd Saint-Germain, 6th arr.", "hours": "7am-1:30am", "cost": "$8-15", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Legendary literary cafe — Hemingway, Sartre, and de Beauvoir's haunt"},
    ],
    "Rome": [
        {"name": "Colosseum & Roman Forum", "address": "Piazza del Colosseo, 1", "hours": "9am-7pm", "cost": "$18", "tags": ["temples", "architecture"], "time_of_day": "Morning", "description": "Ancient gladiatorial arena and the heart of the Roman Empire"},
        {"name": "Vatican Museums & Sistine Chapel", "address": "Viale Vaticano", "hours": "8am-6pm (closed Sun except last Sun)", "cost": "$20", "tags": ["art", "architecture", "temples"], "time_of_day": "Morning", "description": "Michelangelo's ceiling, Raphael's rooms, and 7km of galleries"},
        {"name": "Trevi Fountain", "address": "Piazza di Trevi", "hours": "24/7 (best early morning)", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "Baroque masterpiece — throw a coin to ensure your return to Rome"},
        {"name": "Pantheon", "address": "Piazza della Rotonda", "hours": "9am-7pm", "cost": "$6", "tags": ["architecture", "temples"], "time_of_day": "Afternoon", "description": "2,000-year-old temple with the world's largest unreinforced concrete dome"},
        {"name": "Trastevere Neighborhood", "address": "Trastevere, across the Tiber", "hours": "Best in evening", "cost": "$15-30/meal", "tags": ["food", "nightlife", "culture"], "time_of_day": "Evening", "description": "Cobblestone charm with trattorias, wine bars, and nightlife"},
        {"name": "Borghese Gallery", "address": "Piazzale Scipione Borghese 5", "hours": "9am-7pm (reservation required)", "cost": "$15", "tags": ["art"], "time_of_day": "Afternoon", "description": "Bernini sculptures and Caravaggio paintings in a stunning villa"},
        {"name": "Spanish Steps", "address": "Piazza di Spagna", "hours": "24/7", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "135 elegant steps connecting Piazza di Spagna to Trinita dei Monti"},
        {"name": "Testaccio Food Tour", "address": "Testaccio neighborhood", "hours": "Morning departures", "cost": "$70-90", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Rome's authentic working-class food scene — carbonara, suppli, and more"},
        {"name": "Gelato Tasting", "address": "Various (Giolitti, Fatamorgana, Grom)", "hours": "10am-midnight", "cost": "$4-6", "tags": ["food"], "time_of_day": "Afternoon", "description": "Artisan gelato at Rome's best shops — try pistachio and stracciatella"},
        {"name": "Pincio Terrace at Sunset", "address": "Viale Gabriele D'Annunzio, Villa Borghese", "hours": "24/7", "cost": "Free", "tags": ["photography"], "time_of_day": "Evening", "description": "Panoramic sunset viewpoint overlooking Piazza del Popolo and St. Peter's"},
    ],
    "Barcelona": [
        {"name": "Sagrada Familia", "address": "Carrer de Mallorca 401", "hours": "9am-8pm", "cost": "$28", "tags": ["architecture", "art"], "time_of_day": "Morning", "description": "Gaudi's unfinished masterpiece — a basilica unlike anything else on earth"},
        {"name": "Park Guell", "address": "Carrer d'Olot, Gracia", "hours": "9:30am-7:30pm", "cost": "$12", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "Mosaic-covered terraces and structures with city views"},
        {"name": "La Boqueria Market", "address": "La Rambla 91", "hours": "8am-8:30pm (closed Sun)", "cost": "$5-15", "tags": ["food", "shopping"], "time_of_day": "Morning", "description": "Vibrant food market with fresh juice, jamon, seafood, and tapas"},
        {"name": "Gothic Quarter", "address": "Barri Gotic, Ciutat Vella", "hours": "24/7", "cost": "Free", "tags": ["architecture", "culture", "photography"], "time_of_day": "Afternoon", "description": "Medieval labyrinth of narrow streets, plazas, and hidden courtyards"},
        {"name": "Barceloneta Beach", "address": "Passeig Maritim de la Barceloneta", "hours": "24/7", "cost": "Free", "tags": ["beaches"], "time_of_day": "Afternoon", "description": "City beach with seafood restaurants and beach bars (chiringuitos)"},
        {"name": "Casa Batllo", "address": "Passeig de Gracia 43", "hours": "9am-9pm", "cost": "$35", "tags": ["architecture", "art"], "time_of_day": "Afternoon", "description": "Gaudi's dragon-scale facade — one of modernisme's greatest works"},
        {"name": "Bunkers del Carmel", "address": "Carrer de Marias Pi i Gibert", "hours": "24/7", "cost": "Free", "tags": ["photography"], "time_of_day": "Evening", "description": "Secret hilltop viewpoint with 360-degree panoramic views of Barcelona"},
        {"name": "Tapas in El Born", "address": "El Born neighborhood", "hours": "7pm-midnight", "cost": "$20-40", "tags": ["food", "nightlife"], "time_of_day": "Evening", "description": "Trendy tapas bars and wine spots in a lively medieval quarter"},
        {"name": "Flamenco Show", "address": "Various tablaos (Tablao Cordobes, Palau Dalmases)", "hours": "Evening shows 7-10pm", "cost": "$30-50", "tags": ["culture", "nightlife"], "time_of_day": "Night", "description": "Intimate flamenco performance in a traditional tablao"},
        {"name": "Picasso Museum", "address": "Carrer Montcada 15-23", "hours": "10am-7pm (closed Mon)", "cost": "$14", "tags": ["art"], "time_of_day": "Afternoon", "description": "Over 4,000 works spanning Picasso's early career through cubism"},
    ],
    "London": [
        {"name": "British Museum", "address": "Great Russell St, Bloomsbury", "hours": "10am-5pm", "cost": "Free", "tags": ["art", "culture"], "time_of_day": "Morning", "description": "World-class collection including the Rosetta Stone and Parthenon Marbles"},
        {"name": "Tower of London", "address": "Tower Hill, EC3N 4AB", "hours": "10am-5:30pm", "cost": "$33", "tags": ["architecture", "culture"], "time_of_day": "Morning", "description": "1,000-year-old fortress with the Crown Jewels and Beefeater tours"},
        {"name": "Borough Market", "address": "8 Southwark St, SE1 1TL", "hours": "10am-5pm (closed Sun-Mon)", "cost": "$5-15", "tags": ["food", "shopping"], "time_of_day": "Midday", "description": "London's finest food market — artisan cheese, fresh bread, street food"},
        {"name": "Tate Modern", "address": "Bankside, SE1 9TG", "hours": "10am-6pm", "cost": "Free", "tags": ["art"], "time_of_day": "Afternoon", "description": "Modern and contemporary art in a converted power station on the Thames"},
        {"name": "West End Theatre", "address": "Theatreland, WC2", "hours": "Evening shows 7:30pm", "cost": "$30-120", "tags": ["culture", "nightlife"], "time_of_day": "Night", "description": "World-class musicals and plays — book Hamilton, Les Mis, or The Mousetrap"},
        {"name": "South Bank Walk", "address": "Westminster Bridge to Tower Bridge", "hours": "24/7", "cost": "Free", "tags": ["photography", "culture"], "time_of_day": "Afternoon", "description": "3km riverside walk past the London Eye, Tate Modern, and Shakespeare's Globe"},
        {"name": "Camden Market", "address": "Camden Lock Place, NW1 8AF", "hours": "10am-6pm", "cost": "Free entry", "tags": ["shopping", "food"], "time_of_day": "Afternoon", "description": "Eclectic market with street food from 30+ cuisines and vintage fashion"},
        {"name": "Buckingham Palace", "address": "Buckingham Palace Rd, SW1A 1AA", "hours": "Changing of Guard at 11am", "cost": "Free to watch (palace tours $33, summer only)", "tags": ["architecture", "culture"], "time_of_day": "Morning", "description": "Watch the iconic Changing of the Guard ceremony"},
        {"name": "Sky Garden", "address": "20 Fenchurch St, EC3M 3BY", "hours": "10am-6pm", "cost": "Free (book ahead)", "tags": ["photography", "architecture"], "time_of_day": "Evening", "description": "Free rooftop garden on the 35th floor with panoramic London views"},
        {"name": "Notting Hill & Portobello Road", "address": "Portobello Rd, W11", "hours": "Sat 9am-7pm (market)", "cost": "Free to browse", "tags": ["shopping", "culture", "photography"], "time_of_day": "Morning", "description": "Colorful houses, antique stalls, and vintage finds on market day"},
    ],
    "Istanbul": [
        {"name": "Hagia Sophia", "address": "Sultan Ahmet, Ayasofya Meydani 1", "hours": "9am-7pm", "cost": "$28", "tags": ["temples", "architecture"], "time_of_day": "Morning", "description": "6th-century marvel — cathedral, mosque, museum, and mosque again"},
        {"name": "Blue Mosque", "address": "Sultan Ahmet Mahallesi, Fatih", "hours": "Outside prayer times", "cost": "Free", "tags": ["temples", "architecture"], "time_of_day": "Morning", "description": "Six-minaret Ottoman mosque with 20,000+ hand-painted Iznik tiles"},
        {"name": "Grand Bazaar", "address": "Beyazit, Fatih", "hours": "9am-7pm (closed Sun)", "cost": "Free entry", "tags": ["shopping", "culture"], "time_of_day": "Afternoon", "description": "One of world's oldest and largest covered markets — 4,000+ shops"},
        {"name": "Bosphorus Cruise", "address": "Eminonu ferry terminal", "hours": "10:35am daily (long tour)", "cost": "$3-10", "tags": ["photography", "culture"], "time_of_day": "Afternoon", "description": "Ferry cruise between Europe and Asia past palaces, mosques, and fortresses"},
        {"name": "Basilica Cistern", "address": "Yerebatan Cd. 1/3, Sultanahmet", "hours": "9am-6:30pm", "cost": "$12", "tags": ["architecture"], "time_of_day": "Afternoon", "description": "6th-century underground water palace with 336 marble columns"},
        {"name": "Topkapi Palace", "address": "Cankurtaran, Fatih", "hours": "9am-6pm (closed Tue)", "cost": "$18", "tags": ["architecture", "culture"], "time_of_day": "Morning", "description": "Ottoman sultans' palace with Harem quarters, jewels, and Bosphorus views"},
        {"name": "Turkish Bath (Hammam)", "address": "Cagaloglu Hamami, Fatih", "hours": "8am-10pm", "cost": "$50-80", "tags": ["wellness", "culture"], "time_of_day": "Afternoon", "description": "300-year-old traditional bath with scrub, soap massage, and relaxation"},
        {"name": "Istiklal Street & Galata Tower", "address": "Beyoglu district", "hours": "24/7 (Tower: 9am-8pm, $8)", "cost": "Free to walk", "tags": ["shopping", "nightlife", "photography"], "time_of_day": "Evening", "description": "Bustling pedestrian avenue and medieval tower with city panoramas"},
        {"name": "Kadikoy Food Tour (Asian Side)", "address": "Kadikoy district (ferry from Eminonu)", "hours": "Morning-afternoon", "cost": "$10-20 for food", "tags": ["food", "culture"], "time_of_day": "Midday", "description": "Local food scene on the Asian side — fish, meze, Turkish breakfast"},
        {"name": "Suleymaniye Mosque", "address": "Prof. Siddik Sami Onar Cd, Fatih", "hours": "Outside prayer times", "cost": "Free", "tags": ["temples", "architecture"], "time_of_day": "Morning", "description": "Sinan's masterpiece — less crowded than Blue Mosque with epic views"},
    ],
    "Bali": [
        {"name": "Tegallalang Rice Terraces", "address": "Tegallalang, Gianyar", "hours": "8am-6pm", "cost": "$2", "tags": ["photography", "hiking"], "time_of_day": "Morning", "description": "Iconic cascading rice paddies carved into the hillside"},
        {"name": "Uluwatu Temple", "address": "Pecatu, South Kuta", "hours": "9am-7pm", "cost": "$5", "tags": ["temples", "photography"], "time_of_day": "Evening", "description": "Clifftop temple with dramatic ocean views and Kecak fire dance at sunset"},
        {"name": "Sacred Monkey Forest", "address": "Jl. Monkey Forest, Ubud", "hours": "9am-6pm", "cost": "$5", "tags": ["wildlife", "culture"], "time_of_day": "Morning", "description": "Ancient temple complex in a lush forest with 1,000+ long-tailed macaques"},
        {"name": "Mount Batur Sunrise Trek", "address": "Kintamani, Bangli", "hours": "2am departure, sunrise at 6am", "cost": "$40-60 (guide required)", "tags": ["hiking", "photography"], "time_of_day": "Morning", "description": "2-hour hike to the summit for sunrise over the caldera lake"},
        {"name": "Tirta Empul Water Temple", "address": "Manukaya, Tampaksiring", "hours": "9am-5pm", "cost": "$3", "tags": ["temples", "wellness", "culture"], "time_of_day": "Morning", "description": "Sacred spring water temple where Balinese perform purification rituals"},
        {"name": "Ubud Art Market", "address": "Jl. Raya Ubud", "hours": "8am-6pm", "cost": "Free entry", "tags": ["shopping", "art"], "time_of_day": "Morning", "description": "Traditional market selling paintings, woodcarvings, silk, and batik"},
        {"name": "Balinese Cooking Class", "address": "Various in Ubud area", "hours": "Morning sessions", "cost": "$25-40", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Market visit + cooking nasi goreng, satay, and Balinese spice paste"},
        {"name": "Seminyak Beach Club", "address": "Jl. Kayu Aya, Seminyak", "hours": "10am-midnight", "cost": "$20-50 min spend", "tags": ["beaches", "nightlife"], "time_of_day": "Afternoon", "description": "Trendy beach clubs like Potato Head and Ku De Ta with pools and DJs"},
        {"name": "Nusa Penida Day Trip", "address": "Boat from Sanur (30 min)", "hours": "Full day trip", "cost": "$40-60 (boat + tour)", "tags": ["beaches", "photography"], "time_of_day": "Morning", "description": "Kelingking Beach cliff, Angel's Billabong, and world-class snorkeling"},
        {"name": "Balinese Dance Performance", "address": "Ubud Royal Palace", "hours": "7:30pm nightly", "cost": "$8-12", "tags": ["culture", "art"], "time_of_day": "Night", "description": "Traditional Legong, Barong, or Kecak dance in a temple courtyard"},
    ],
    "Seoul": [
        {"name": "Gyeongbokgung Palace", "address": "161 Sajik-ro, Jongno-gu", "hours": "9am-6pm (closed Tue)", "cost": "$3 (free in hanbok)", "tags": ["temples", "architecture", "culture"], "time_of_day": "Morning", "description": "Joseon dynasty's main palace — rent a hanbok for free entry and photos"},
        {"name": "Bukchon Hanok Village", "address": "Bukchon-ro, Jongno-gu", "hours": "24/7 (quiet hours after 10pm)", "cost": "Free", "tags": ["architecture", "photography", "culture"], "time_of_day": "Morning", "description": "600-year-old traditional Korean houses on hillside streets"},
        {"name": "Gwangjang Market", "address": "88 Changgyeonggung-ro, Jongno-gu", "hours": "9am-11pm", "cost": "$5-10", "tags": ["food", "culture"], "time_of_day": "Midday", "description": "Seoul's oldest market — try bindaetteok, mayak gimbap, and tteokbokki"},
        {"name": "Namsan Tower (N Seoul Tower)", "address": "105 Namsangongwon-gil, Yongsan-gu", "hours": "10am-11pm", "cost": "$12", "tags": ["photography", "architecture"], "time_of_day": "Evening", "description": "Iconic tower on Namsan Mountain with love locks and city panoramas"},
        {"name": "Hongdae Nightlife", "address": "Hongdae area, Mapo-gu", "hours": "Best after 9pm", "cost": "Varies", "tags": ["nightlife", "culture"], "time_of_day": "Night", "description": "Street performers, indie music clubs, and vibrant bar scene"},
        {"name": "Korean BBQ Experience", "address": "Various (Mapo-gu for best)", "hours": "11am-midnight", "cost": "$15-30/person", "tags": ["food"], "time_of_day": "Evening", "description": "Grill your own meat at the table with soju and banchan side dishes"},
        {"name": "DMZ Tour", "address": "Departs from Seoul (2hr drive)", "hours": "Full day, book ahead", "cost": "$50-80", "tags": ["culture"], "time_of_day": "Morning", "description": "Visit the most heavily fortified border in the world"},
        {"name": "Myeongdong Shopping", "address": "Myeongdong, Jung-gu", "hours": "10am-10pm", "cost": "Free to browse", "tags": ["shopping"], "time_of_day": "Afternoon", "description": "K-beauty flagship stores, street food, and department stores"},
        {"name": "Jjimjilbang (Korean Spa)", "address": "Dragon Hill Spa, Yongsan-gu", "hours": "24/7", "cost": "$12-15", "tags": ["wellness"], "time_of_day": "Evening", "description": "Multi-floor spa with saunas, pools, sleeping rooms, and snack bars"},
        {"name": "Insadong Art Street", "address": "Insadong-gil, Jongno-gu", "hours": "10am-8pm", "cost": "Free to browse", "tags": ["art", "shopping", "culture"], "time_of_day": "Afternoon", "description": "Traditional art galleries, tea houses, and craft shops"},
    ],
    "Lisbon": [
        {"name": "Tram 28 Ride", "address": "Departs Martim Moniz", "hours": "6am-9pm", "cost": "$3", "tags": ["culture", "photography"], "time_of_day": "Morning", "description": "Vintage yellow tram rattling through Alfama's narrow cobblestone streets"},
        {"name": "Pasteis de Belem", "address": "Rua de Belem 84-92", "hours": "8am-11pm", "cost": "$2-5", "tags": ["food"], "time_of_day": "Morning", "description": "The original 1837 pastel de nata factory — warm custard tarts since 1837"},
        {"name": "Castelo de Sao Jorge", "address": "Rua de Santa Cruz do Castelo", "hours": "9am-9pm", "cost": "$12", "tags": ["architecture", "photography"], "time_of_day": "Afternoon", "description": "Moorish castle on the highest hill with panoramic views of the city"},
        {"name": "Alfama Fado Night", "address": "Various in Alfama (Clube de Fado, Mesa de Frades)", "hours": "8pm-midnight", "cost": "$30-60 (dinner + show)", "tags": ["culture", "nightlife"], "time_of_day": "Night", "description": "Soulful Portuguese fado music in intimate taverns"},
        {"name": "Time Out Market", "address": "Av. 24 de Julho 49", "hours": "10am-midnight", "cost": "$8-20/meal", "tags": ["food"], "time_of_day": "Midday", "description": "Food hall with Lisbon's best chefs under one roof"},
        {"name": "Jeronimos Monastery", "address": "Praca do Imperio, Belem", "hours": "10am-5:30pm (closed Mon)", "cost": "$12", "tags": ["architecture", "temples"], "time_of_day": "Morning", "description": "UNESCO masterpiece of Manueline architecture from the Age of Discovery"},
        {"name": "LX Factory", "address": "Rua Rodrigues de Faria 103", "hours": "10am-midnight", "cost": "Free entry", "tags": ["shopping", "food", "art"], "time_of_day": "Afternoon", "description": "Creative hub in a converted industrial complex — shops, food, and art"},
        {"name": "Miradouro da Graca", "address": "Largo da Graca, Graca", "hours": "24/7", "cost": "Free", "tags": ["photography"], "time_of_day": "Evening", "description": "Best sunset viewpoint in Lisbon — bring wine and watch the light change"},
        {"name": "Day Trip to Sintra", "address": "Train from Rossio station (40 min)", "hours": "Full day", "cost": "$3 train + $15-20 palace entry", "tags": ["architecture", "hiking"], "time_of_day": "Morning", "description": "Fairy-tale palaces and castles in misty hilltop forests"},
        {"name": "Ginjinha Tasting", "address": "A Ginjinha, Largo de Sao Domingos 8", "hours": "9am-10pm", "cost": "$2", "tags": ["food", "culture"], "time_of_day": "Afternoon", "description": "Sour cherry liqueur served in chocolate cups at a tiny stand since 1840"},
    ],
    "Cusco": [
        {"name": "Machu Picchu", "address": "Train from Ollantaytambo (1.5h)", "hours": "6am-5pm", "cost": "$50 entry + $60-80 train", "tags": ["hiking", "temples", "photography"], "time_of_day": "Morning", "description": "15th-century Inca citadel high in the Andes — a world wonder"},
        {"name": "Rainbow Mountain", "address": "3h drive from Cusco", "hours": "Full day trip", "cost": "$30-50 (tour)", "tags": ["hiking", "photography"], "time_of_day": "Morning", "description": "Vinicunca's striped mineral layers at 5,200m — breathtaking but strenuous"},
        {"name": "San Pedro Market", "address": "Calle Tupac Amaru, Cusco", "hours": "6am-6pm", "cost": "$2-5", "tags": ["food", "shopping", "culture"], "time_of_day": "Morning", "description": "Bustling local market with fresh juices, empanadas, and alpaca sweaters"},
        {"name": "Sacsayhuaman Fortress", "address": "Above Cusco (15 min walk)", "hours": "7am-6pm", "cost": "$20 (tourist ticket)", "tags": ["temples", "architecture"], "time_of_day": "Afternoon", "description": "Massive Inca stone fortress with walls of boulders weighing 100+ tons"},
        {"name": "Sacred Valley Tour", "address": "Various sites (full day)", "hours": "Full day", "cost": "$30-50 (tour)", "tags": ["culture", "hiking"], "time_of_day": "Morning", "description": "Ollantaytambo, Pisac, Moray terraces, and Maras salt mines"},
        {"name": "Peruvian Cooking Class", "address": "Various in Cusco center", "hours": "Morning sessions", "cost": "$25-40", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Market visit then cook ceviche, lomo saltado, and pisco sour"},
        {"name": "Qorikancha Temple of the Sun", "address": "Plazoleta Santo Domingo", "hours": "8:30am-5:30pm", "cost": "$5", "tags": ["temples", "architecture"], "time_of_day": "Afternoon", "description": "Inca temple foundation beneath a colonial church — walls once covered in gold"},
        {"name": "San Blas Artisan Quarter", "address": "San Blas neighborhood", "hours": "10am-7pm", "cost": "Free to walk", "tags": ["art", "shopping", "photography"], "time_of_day": "Afternoon", "description": "Steep cobblestone streets with artist studios, cafes, and craft shops"},
        {"name": "Plaza de Armas at Night", "address": "Plaza de Armas, Cusco", "hours": "Best at dusk", "cost": "Free", "tags": ["photography", "culture"], "time_of_day": "Evening", "description": "Colonial cathedral and churches illuminated against the Andes skyline"},
        {"name": "Pisco Sour Tasting", "address": "Various bars (Museo del Pisco)", "hours": "5pm-midnight", "cost": "$5-10/drink", "tags": ["food", "nightlife"], "time_of_day": "Evening", "description": "Peru's national cocktail — try classic, maracuya, and coca leaf versions"},
    ],
    "Mexico City": [
        {"name": "Teotihuacan Pyramids", "address": "San Juan Teotihuacan (1h drive)", "hours": "9am-5pm", "cost": "$5", "tags": ["temples", "hiking", "photography"], "time_of_day": "Morning", "description": "Climb the Pyramid of the Sun at the ancient City of the Gods"},
        {"name": "Frida Kahlo Museum (Casa Azul)", "address": "Londres 247, Coyoacan", "hours": "10am-5:30pm (closed Mon)", "cost": "$14", "tags": ["art", "culture"], "time_of_day": "Morning", "description": "Frida's blue house — her art, life, and Diego Rivera memorabilia"},
        {"name": "Palacio de Bellas Artes", "address": "Av. Juarez, Centro Historico", "hours": "10am-6pm (closed Mon)", "cost": "$5", "tags": ["art", "architecture"], "time_of_day": "Afternoon", "description": "Art nouveau palace with Rivera and Orozco murals and ballet performances"},
        {"name": "Tacos al Pastor Street Stands", "address": "Various (El Huequito, Los Cocuyos)", "hours": "Best 7pm-midnight", "cost": "$1-3/taco", "tags": ["food"], "time_of_day": "Evening", "description": "Spit-roasted pork with pineapple — Mexico City's signature street food"},
        {"name": "Chapultepec Castle", "address": "Bosque de Chapultepec", "hours": "9am-5pm (closed Mon)", "cost": "$5", "tags": ["architecture", "photography"], "time_of_day": "Afternoon", "description": "Hilltop castle with panoramic city views and Mexican history exhibits"},
        {"name": "Xochimilco Canals", "address": "Embarcadero Nuevo Nativitas", "hours": "9am-6pm", "cost": "$15-25/boat/hr", "tags": ["culture", "food"], "time_of_day": "Afternoon", "description": "Colorful trajinera boats floating past floating gardens with mariachis"},
        {"name": "Anthropology Museum", "address": "Av. Paseo de la Reforma, Chapultepec", "hours": "9am-7pm (closed Mon)", "cost": "$5", "tags": ["culture", "art"], "time_of_day": "Morning", "description": "World's best collection of pre-Columbian artifacts including the Aztec Sun Stone"},
        {"name": "Roma Norte Food Walk", "address": "Roma Norte neighborhood", "hours": "Best 11am-3pm or 7pm+", "cost": "$10-25", "tags": ["food", "culture"], "time_of_day": "Midday", "description": "Tree-lined streets with world-class restaurants, cafes, and mezcalerias"},
        {"name": "Mezcal Tasting", "address": "Various (Boca del Rio, La Clandestina)", "hours": "6pm-midnight", "cost": "$15-30", "tags": ["food", "nightlife"], "time_of_day": "Evening", "description": "Smoky agave spirits — try espadin, tobala, and mezcal cocktails"},
        {"name": "Coyoacan Market", "address": "Calle Ignacio Allende, Coyoacan", "hours": "9am-7pm", "cost": "$3-8", "tags": ["food", "shopping"], "time_of_day": "Midday", "description": "Colorful neighborhood market with tostadas, quesadillas, and churros"},
    ],
    "Cape Town": [
        {"name": "Table Mountain", "address": "Table Mountain National Park", "hours": "8am-6pm (cable car)", "cost": "$20 round trip cable car", "tags": ["hiking", "photography"], "time_of_day": "Morning", "description": "Flat-topped mountain icon — hike Platteklip Gorge or take the cable car"},
        {"name": "Boulders Beach Penguins", "address": "Kleintuin Rd, Simon's Town", "hours": "8am-5pm", "cost": "$8", "tags": ["wildlife", "photography"], "time_of_day": "Morning", "description": "Colony of 3,000+ African penguins on a sheltered boulder-strewn beach"},
        {"name": "Stellenbosch Wine Tasting", "address": "Stellenbosch (45 min drive)", "hours": "10am-5pm", "cost": "$5-15 per tasting", "tags": ["food"], "time_of_day": "Afternoon", "description": "South Africa's premier wine region — pinotage, chenin blanc, and MCC"},
        {"name": "Bo-Kaap Neighborhood", "address": "Bo-Kaap, Cape Town", "hours": "Best 9am-4pm", "cost": "Free (cooking class $30-50)", "tags": ["culture", "photography", "food"], "time_of_day": "Morning", "description": "Colorful Cape Malay houses on cobblestone streets with spice shops"},
        {"name": "Robben Island", "address": "Ferry from V&A Waterfront", "hours": "9am/11am/1pm departures", "cost": "$25", "tags": ["culture"], "time_of_day": "Morning", "description": "Nelson Mandela's prison cell — guided tour by a former political prisoner"},
        {"name": "Chapman's Peak Drive", "address": "Chapman's Peak, Hout Bay", "hours": "24/7", "cost": "$5 toll", "tags": ["photography"], "time_of_day": "Afternoon", "description": "One of the world's most scenic coastal drives — 114 curves along cliffs"},
        {"name": "Lion's Head Sunset Hike", "address": "Lion's Head trailhead, Signal Hill Rd", "hours": "Allow 2h round trip before sunset", "cost": "Free", "tags": ["hiking", "photography"], "time_of_day": "Evening", "description": "Popular sunset hike with 360-degree views of the city and ocean"},
        {"name": "V&A Waterfront", "address": "V&A Waterfront, Cape Town", "hours": "9am-9pm", "cost": "Free entry", "tags": ["shopping", "food"], "time_of_day": "Afternoon", "description": "Harbourfront mall with restaurants, craft markets, and Table Mountain views"},
        {"name": "Kirstenbosch Botanical Garden", "address": "Rhodes Dr, Newlands", "hours": "8am-6pm", "cost": "$8", "tags": ["hiking", "photography", "wellness"], "time_of_day": "Afternoon", "description": "Stunning gardens on Table Mountain's slopes with a canopy walkway"},
        {"name": "Cape Peninsula Day Trip", "address": "Full day drive (Cape Point, Cape of Good Hope)", "hours": "Full day", "cost": "$15 park entry", "tags": ["photography", "hiking", "wildlife"], "time_of_day": "Morning", "description": "Cape Point, Cape of Good Hope, penguins, and Chapman's Peak in one day"},
    ],
    "Budapest": [
        {"name": "Szechenyi Thermal Baths", "address": "Allatkerti krt. 9-11, City Park", "hours": "6am-10pm", "cost": "$22", "tags": ["wellness"], "time_of_day": "Morning", "description": "Europe's largest medicinal bath complex in a grand neo-baroque palace"},
        {"name": "Hungarian Parliament Building", "address": "Kossuth Lajos ter 1-3", "hours": "8am-6pm (tours every 20 min)", "cost": "$12", "tags": ["architecture", "culture"], "time_of_day": "Morning", "description": "Neo-Gothic masterpiece on the Danube — third-largest parliament in the world"},
        {"name": "Ruin Bars (Szimpla Kert)", "address": "Kazinczy u. 14, Jewish Quarter", "hours": "Noon-4am", "cost": "$3-6/drink", "tags": ["nightlife", "culture"], "time_of_day": "Night", "description": "Eclectic bar in a decaying building — the original ruin bar that started it all"},
        {"name": "Fisherman's Bastion", "address": "Szentharomsag ter, Castle District", "hours": "9am-11pm", "cost": "$4 (upper terrace)", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "Neo-Romanesque terrace with fairy-tale turrets and Parliament panoramas"},
        {"name": "Great Market Hall", "address": "Vamhaz krt. 1-3", "hours": "6am-6pm (closed Sun)", "cost": "Free entry", "tags": ["food", "shopping"], "time_of_day": "Midday", "description": "Three floors of paprika, salami, langos, and Hungarian crafts"},
        {"name": "Danube Night Cruise", "address": "Various piers (Vigado ter popular)", "hours": "8-10pm", "cost": "$15-25", "tags": ["photography"], "time_of_day": "Night", "description": "See Parliament, Chain Bridge, and Castle Hill beautifully illuminated"},
        {"name": "Gellert Hill & Citadella", "address": "Gellert Hill, Buda side", "hours": "24/7", "cost": "Free", "tags": ["hiking", "photography"], "time_of_day": "Evening", "description": "Short steep hike for the best panoramic view of both Buda and Pest"},
        {"name": "Gellert Thermal Baths", "address": "Kelenhegyi ut 4", "hours": "6am-8pm", "cost": "$22", "tags": ["wellness", "architecture"], "time_of_day": "Afternoon", "description": "Art nouveau thermal baths with mosaic tiles, columns, and an outdoor wave pool"},
        {"name": "Shoes on the Danube", "address": "Id. Antall Jozsef rkp, Pest embankment", "hours": "24/7", "cost": "Free", "tags": ["culture"], "time_of_day": "Afternoon", "description": "Moving Holocaust memorial — 60 iron shoes along the river bank"},
        {"name": "Langos at Central Market", "address": "Great Market Hall, upper floor", "hours": "6am-6pm", "cost": "$3-5", "tags": ["food"], "time_of_day": "Midday", "description": "Deep-fried dough topped with sour cream and cheese — Hungary's street food icon"},
    ],
    "Marrakech": [
        {"name": "Jemaa el-Fnaa Square", "address": "Jemaa el-Fnaa, Medina", "hours": "Best after 5pm", "cost": "Free", "tags": ["culture", "food"], "time_of_day": "Evening", "description": "Chaotic square of snake charmers, storytellers, musicians, and food stalls"},
        {"name": "Jardin Majorelle & YSL Museum", "address": "Rue Yves Saint Laurent", "hours": "8am-6pm", "cost": "$14", "tags": ["art", "photography"], "time_of_day": "Morning", "description": "Cobalt blue Art Deco garden restored by Yves Saint Laurent"},
        {"name": "Bahia Palace", "address": "Rue Riad Zitoun el Jdid", "hours": "9am-5pm", "cost": "$8", "tags": ["architecture"], "time_of_day": "Morning", "description": "19th-century palace with stunning zellige tilework, carved cedarwood, and gardens"},
        {"name": "Medina Souk Exploration", "address": "Souks of the Medina", "hours": "9am-8pm", "cost": "Free entry (shopping extra)", "tags": ["shopping", "culture"], "time_of_day": "Afternoon", "description": "Labyrinth of stalls selling leather, spices, lanterns, and ceramics"},
        {"name": "Riad Cooking Class", "address": "Various riads in Medina", "hours": "Morning or afternoon", "cost": "$25-40", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Learn to make tagine, couscous, and pastilla in a traditional riad kitchen"},
        {"name": "Saadian Tombs", "address": "Rue de la Kasbah", "hours": "9am-5pm", "cost": "$8", "tags": ["architecture", "culture"], "time_of_day": "Afternoon", "description": "16th-century royal tombs with intricate carved marble and zellige mosaics"},
        {"name": "Atlas Mountains Day Trip", "address": "1.5h drive from Marrakech", "hours": "Full day", "cost": "$30-50 (tour)", "tags": ["hiking", "culture"], "time_of_day": "Morning", "description": "Berber villages, waterfalls, and mountain scenery in the High Atlas"},
        {"name": "Traditional Hammam", "address": "Various (Heritage Spa, Le Bain Bleu)", "hours": "9am-8pm", "cost": "$20-50", "tags": ["wellness"], "time_of_day": "Afternoon", "description": "Steam, black soap scrub, and ghassoul clay mask in a traditional bathhouse"},
        {"name": "Rooftop Terrace Sunset", "address": "Various cafes (Nomad, Le Jardin)", "hours": "4pm-sunset", "cost": "$5-15", "tags": ["photography", "food"], "time_of_day": "Evening", "description": "Mint tea and views over the Medina rooftops to the Atlas Mountains"},
        {"name": "Koutoubia Mosque", "address": "Avenue Mohammed V", "hours": "Exterior only (non-Muslims)", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "12th-century mosque with a 77m minaret — Marrakech's most iconic landmark"},
    ],
    "Amsterdam": [
        {"name": "Anne Frank House", "address": "Westermarkt 20", "hours": "9am-10pm", "cost": "$16 (book weeks ahead)", "tags": ["culture"], "time_of_day": "Morning", "description": "The secret annex where Anne Frank hid during WWII — deeply moving"},
        {"name": "Rijksmuseum", "address": "Museumstraat 1", "hours": "9am-5pm", "cost": "$22", "tags": ["art", "architecture"], "time_of_day": "Morning", "description": "Dutch masters — Rembrandt's Night Watch and Vermeer's Milkmaid"},
        {"name": "Van Gogh Museum", "address": "Museumplein 6", "hours": "9am-6pm", "cost": "$20", "tags": ["art"], "time_of_day": "Afternoon", "description": "World's largest Van Gogh collection — Sunflowers, Starry Night, Self-Portraits"},
        {"name": "Canal Cruise", "address": "Various departure points (Centraal Station area)", "hours": "Various, sunset best", "cost": "$15-20", "tags": ["photography"], "time_of_day": "Evening", "description": "Glide through UNESCO-listed canals past gabled houses and bridges"},
        {"name": "Vondelpark", "address": "Vondelpark, Oud-Zuid", "hours": "24/7", "cost": "Free", "tags": ["wellness", "culture"], "time_of_day": "Afternoon", "description": "Amsterdam's beloved green heart — cycling, picnics, and open-air theatre"},
        {"name": "Albert Cuyp Market", "address": "Albert Cuypstraat, De Pijp", "hours": "9am-5pm (Mon-Sat)", "cost": "Free entry", "tags": ["food", "shopping"], "time_of_day": "Midday", "description": "Amsterdam's largest outdoor market — stroopwafels, herring, and Dutch cheese"},
        {"name": "Jordaan Neighborhood Walk", "address": "Jordaan district", "hours": "Best 10am-6pm", "cost": "Free", "tags": ["photography", "culture", "shopping"], "time_of_day": "Afternoon", "description": "Charming canal-side streets with indie shops, galleries, and brown cafes"},
        {"name": "Heineken Experience", "address": "Stadhouderskade 78", "hours": "10:30am-7:30pm", "cost": "$23", "tags": ["food", "culture"], "time_of_day": "Afternoon", "description": "Interactive brewery tour in the original Heineken building with tastings"},
        {"name": "NDSM Wharf", "address": "NDSM-plein, Amsterdam-Noord (free ferry)", "hours": "Varies by venue", "cost": "Free to explore", "tags": ["art", "food"], "time_of_day": "Afternoon", "description": "Industrial-chic art district with street art, food trucks, and galleries"},
        {"name": "Nine Streets Shopping", "address": "De 9 Straatjes, Canal Ring", "hours": "10am-6pm", "cost": "Free to browse", "tags": ["shopping"], "time_of_day": "Afternoon", "description": "Nine charming cross-streets with vintage shops, boutiques, and cafes"},
    ],
    "Delhi": [
        {"name": "Red Fort", "address": "Netaji Subhash Marg, Old Delhi", "hours": "9:30am-4:30pm (closed Mon)", "cost": "$7", "tags": ["architecture", "culture"], "time_of_day": "Morning", "description": "Mughal emperor Shah Jahan's massive red sandstone fort complex"},
        {"name": "Humayun's Tomb", "address": "Mathura Rd, Nizamuddin East", "hours": "Sunrise-sunset", "cost": "$7", "tags": ["architecture", "photography"], "time_of_day": "Afternoon", "description": "Precursor to the Taj Mahal — stunning Mughal garden tomb from 1570"},
        {"name": "Chandni Chowk Street Food", "address": "Chandni Chowk, Old Delhi", "hours": "9am-9pm", "cost": "$2-5", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "India's most legendary food street — paranthas, chaat, jalebi, and lassi"},
        {"name": "Jama Masjid", "address": "Jama Masjid Rd, Old Delhi", "hours": "7am-noon, 1:30-6:30pm", "cost": "Free (camera fee $4)", "tags": ["temples", "architecture"], "time_of_day": "Morning", "description": "India's largest mosque — built by Shah Jahan, holds 25,000 worshippers"},
        {"name": "Qutub Minar", "address": "Mehrauli, South Delhi", "hours": "7am-5pm", "cost": "$7", "tags": ["architecture", "photography"], "time_of_day": "Afternoon", "description": "73m victory tower from 1193 — Delhi's earliest surviving Islamic monument"},
        {"name": "Lotus Temple", "address": "Lotus Temple Rd, Bahapur", "hours": "9am-5:30pm (closed Mon)", "cost": "Free", "tags": ["architecture", "wellness"], "time_of_day": "Afternoon", "description": "Stunning lotus-shaped Baha'i house of worship — open to all faiths"},
        {"name": "Cycle Rickshaw Through Old Delhi", "address": "Start at Chawri Bazaar", "hours": "Best 10am-4pm", "cost": "$3-5", "tags": ["culture", "photography"], "time_of_day": "Morning", "description": "Navigate the chaotic, colorful lanes of Mughal-era Old Delhi"},
        {"name": "Hauz Khas Village", "address": "Hauz Khas, South Delhi", "hours": "Best evening", "cost": "Free to walk", "tags": ["nightlife", "art", "food"], "time_of_day": "Evening", "description": "Trendy village with rooftop bars, galleries, and a medieval lake"},
        {"name": "India Gate", "address": "Rajpath, New Delhi", "hours": "24/7", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Evening", "description": "42m war memorial arch beautifully illuminated at night"},
        {"name": "Day Trip to Taj Mahal", "address": "Agra (3-4h by car, 2h by train)", "hours": "Full day", "cost": "$15 entry + transport", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "The world's most beautiful building — white marble at sunrise is unforgettable"},
    ],
    "Medellin": [
        {"name": "Comuna 13 Street Art Tour", "address": "Comuna 13, San Javier", "hours": "9am-5pm", "cost": "$10-20 (guided tour)", "tags": ["art", "culture", "photography"], "time_of_day": "Morning", "description": "Outdoor escalators, vibrant murals, and hip-hop culture in a transformed neighborhood"},
        {"name": "Metrocable Ride", "address": "Various stations (Santo Domingo best)", "hours": "5am-11pm", "cost": "$1", "tags": ["photography"], "time_of_day": "Afternoon", "description": "Cable car over the city to mountaintop barrios — stunning valley views"},
        {"name": "Plaza Botero", "address": "Cra 52, El Centro", "hours": "24/7", "cost": "Free", "tags": ["art", "culture"], "time_of_day": "Morning", "description": "23 oversized bronze sculptures by Colombia's most famous artist"},
        {"name": "Parque Arvi Nature Reserve", "address": "Metrocable from Acevedo station", "hours": "9am-5pm", "cost": "$1 cable + free park", "tags": ["hiking", "wildlife"], "time_of_day": "Morning", "description": "Cloud forest reserve with hiking trails, picnic areas, and bird watching"},
        {"name": "Coffee Farm Day Trip", "address": "Various farms (1-2h drive)", "hours": "Full day", "cost": "$30-50 (tour)", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Visit a working coffee finca, learn the process, and taste fresh-roasted beans"},
        {"name": "El Poblado Nightlife", "address": "Parque Lleras area, El Poblado", "hours": "Best after 10pm", "cost": "$5-15/drink", "tags": ["nightlife"], "time_of_day": "Night", "description": "Rooftop bars, salsa clubs, and restaurants in Medellin's upscale entertainment district"},
        {"name": "Salsa Dance Class", "address": "Various schools (Son Havana, Dancefree)", "hours": "Evening classes", "cost": "$10-15", "tags": ["culture", "nightlife"], "time_of_day": "Evening", "description": "Learn Colombian salsa moves then hit the dance floor for real"},
        {"name": "Medellin Botanical Garden", "address": "Calle 73 #51d-14", "hours": "9am-5pm", "cost": "Free", "tags": ["wellness", "photography"], "time_of_day": "Afternoon", "description": "14-hectare urban oasis with orchid displays and a butterfly house"},
        {"name": "Bandeja Paisa Lunch", "address": "Various (Hatoviejo, Mondongos)", "hours": "11am-3pm", "cost": "$5-10", "tags": ["food"], "time_of_day": "Midday", "description": "Colombia's national dish — beans, rice, meat, plantain, avocado, and egg"},
        {"name": "Guatape Day Trip", "address": "2h bus from Terminal del Norte", "hours": "Full day", "cost": "$5 bus + $4 entry", "tags": ["photography", "hiking"], "time_of_day": "Morning", "description": "Climb 740 steps up the Rock of Guatape for incredible lake and island views"},
    ],
    "Prague": [
        {"name": "Charles Bridge at Sunrise", "address": "Charles Bridge, Mala Strana to Old Town", "hours": "Best 5-7am", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "Gothic stone bridge with 30 baroque statues — magical without crowds"},
        {"name": "Prague Castle Complex", "address": "Hradcany, Prague 1", "hours": "9am-5pm", "cost": "$14", "tags": ["architecture", "culture"], "time_of_day": "Morning", "description": "World's largest ancient castle — St. Vitus Cathedral, Golden Lane, gardens"},
        {"name": "Astronomical Clock", "address": "Old Town Square, Staromestske nam.", "hours": "Hourly show 9am-11pm", "cost": "Free (tower $12)", "tags": ["architecture"], "time_of_day": "Midday", "description": "600-year-old medieval clock with hourly procession of apostle figures"},
        {"name": "Czech Beer Tasting", "address": "Various (U Fleku, Strahov Monastery Brewery)", "hours": "11am-11pm", "cost": "$3-8/beer", "tags": ["food", "nightlife"], "time_of_day": "Evening", "description": "Birthplace of pilsner — taste Czech lagers in medieval beer halls"},
        {"name": "Jewish Quarter (Josefov)", "address": "Josefov, Prague 1", "hours": "9am-6pm", "cost": "$16 (combined ticket)", "tags": ["culture", "architecture"], "time_of_day": "Afternoon", "description": "Six historic synagogues, the Old Jewish Cemetery, and a poignant history"},
        {"name": "Lennon Wall", "address": "Velkoprevroske nam., Mala Strana", "hours": "24/7", "cost": "Free", "tags": ["art", "photography"], "time_of_day": "Afternoon", "description": "Ever-changing graffiti wall of peace messages inspired by John Lennon"},
        {"name": "Letna Park Beer Garden", "address": "Letenske sady, Prague 7", "hours": "11am-11pm", "cost": "$3-5/beer", "tags": ["food", "photography"], "time_of_day": "Evening", "description": "Hilltop beer garden with the best panoramic views of Prague's bridges"},
        {"name": "Vltava River Cruise", "address": "Various piers near Charles Bridge", "hours": "Various, sunset best", "cost": "$15-20", "tags": ["photography"], "time_of_day": "Evening", "description": "See Prague Castle, Charles Bridge, and the National Theatre from the water"},
        {"name": "Petrin Hill & Tower", "address": "Petrin Hill, Mala Strana", "hours": "10am-10pm", "cost": "$6 (tower)", "tags": ["hiking", "photography"], "time_of_day": "Afternoon", "description": "Mini Eiffel Tower on a forested hill with mirror maze and rose garden"},
        {"name": "Trdelnik & Street Food", "address": "Old Town and Mala Strana", "hours": "9am-10pm", "cost": "$4-6", "tags": ["food"], "time_of_day": "Afternoon", "description": "Warm cinnamon-sugar chimney cake — a Prague street food essential"},
    ],
    "Sydney": [
        {"name": "Sydney Opera House", "address": "Bennelong Point", "hours": "Tours 9am-5pm", "cost": "$30 tour / $40-200 performance", "tags": ["architecture", "culture"], "time_of_day": "Afternoon", "description": "UNESCO-listed architectural icon — take a tour or catch a show"},
        {"name": "Bondi to Coogee Coastal Walk", "address": "Start at Bondi Beach", "hours": "24/7 (best morning)", "cost": "Free", "tags": ["hiking", "photography", "beaches"], "time_of_day": "Morning", "description": "6km cliffside walk with ocean pools, sculpture gardens, and stunning views"},
        {"name": "Sydney Harbour Bridge Climb", "address": "3 Cumberland St, The Rocks", "hours": "Various slots dawn to dusk", "cost": "$180-390", "tags": ["hiking", "photography"], "time_of_day": "Afternoon", "description": "Climb to the summit of the bridge for 360-degree harbour views"},
        {"name": "The Rocks Markets", "address": "George St, The Rocks", "hours": "Sat-Sun 10am-5pm", "cost": "Free entry", "tags": ["shopping", "food"], "time_of_day": "Morning", "description": "Weekend markets in Sydney's oldest neighborhood — food, art, and crafts"},
        {"name": "Manly Beach", "address": "Manly (30 min ferry from Circular Quay)", "hours": "24/7", "cost": "Free ($8 ferry)", "tags": ["beaches"], "time_of_day": "Afternoon", "description": "Surf beach with pine-lined promenade — one of the best ferry rides in the world"},
        {"name": "Taronga Zoo", "address": "Bradleys Head Rd, Mosman", "hours": "9:30am-4:30pm", "cost": "$46", "tags": ["wildlife"], "time_of_day": "Morning", "description": "World-class zoo with harbour views — koalas, platypus, and kangaroos"},
        {"name": "Sydney Fish Market", "address": "Bank St, Pyrmont", "hours": "7am-4pm", "cost": "$10-25/meal", "tags": ["food"], "time_of_day": "Midday", "description": "Fresh seafood platters, sashimi, and oysters at the Southern Hemisphere's largest fish market"},
        {"name": "Royal Botanic Garden", "address": "Mrs Macquaries Rd", "hours": "7am-sunset", "cost": "Free", "tags": ["wellness", "photography"], "time_of_day": "Afternoon", "description": "30-hectare garden on the harbour with Opera House views"},
        {"name": "Surry Hills Brunch", "address": "Crown St area, Surry Hills", "hours": "8am-3pm", "cost": "$15-25", "tags": ["food"], "time_of_day": "Morning", "description": "Sydney's best brunch scene — flat whites, avocado toast, and acai bowls"},
        {"name": "Blue Mountains Day Trip", "address": "Katoomba (2h by train)", "hours": "Full day", "cost": "$5 train", "tags": ["hiking", "photography"], "time_of_day": "Morning", "description": "Three Sisters rock formation, bushwalks, and eucalyptus-hazed valleys"},
    ],
    "Rio de Janeiro": [
        {"name": "Christ the Redeemer", "address": "Parque Nacional da Tijuca, Alto da Boa Vista", "hours": "8am-7pm", "cost": "$20 (train + entry)", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "38m Art Deco statue atop Corcovado with arms open over the city"},
        {"name": "Sugarloaf Mountain Cable Car", "address": "Av. Pasteur 520, Urca", "hours": "8am-9pm", "cost": "$25", "tags": ["photography"], "time_of_day": "Evening", "description": "Two-stage cable car to the summit with panoramic bay and city views"},
        {"name": "Ipanema Beach", "address": "Ipanema, Zona Sul", "hours": "24/7", "cost": "Free", "tags": ["beaches", "culture"], "time_of_day": "Afternoon", "description": "Iconic beach with sunset at Arpoador and the Two Brothers mountain backdrop"},
        {"name": "Selaron Steps", "address": "Rua Manuel Carneiro, Santa Teresa/Lapa", "hours": "24/7 (best morning)", "cost": "Free", "tags": ["art", "photography"], "time_of_day": "Morning", "description": "250 mosaic-covered steps decorated with tiles from 60+ countries"},
        {"name": "Tijuca National Forest Hike", "address": "Parque Nacional da Tijuca", "hours": "8am-5pm", "cost": "Free", "tags": ["hiking", "wildlife"], "time_of_day": "Morning", "description": "World's largest urban rainforest with waterfalls and wildlife"},
        {"name": "Lapa Samba Night", "address": "Arcos da Lapa, Centro", "hours": "Best Fri-Sat after 10pm", "cost": "$5-15 cover", "tags": ["nightlife", "culture"], "time_of_day": "Night", "description": "Live samba under the colonial arches — Rio's most vibrant nightlife scene"},
        {"name": "Churrascaria Dinner", "address": "Various (Fogo de Chao, Porcao)", "hours": "Noon-midnight", "cost": "$30-60/person", "tags": ["food"], "time_of_day": "Evening", "description": "All-you-can-eat Brazilian steakhouse with 15+ cuts of grilled meat"},
        {"name": "Arpoador Sunset", "address": "Arpoador Rock, between Ipanema and Copacabana", "hours": "Best 30 min before sunset", "cost": "Free", "tags": ["photography"], "time_of_day": "Evening", "description": "Locals applaud the sunset from this rocky point — a Rio tradition"},
        {"name": "Santa Teresa Neighborhood", "address": "Santa Teresa, Centro", "hours": "Best 10am-6pm", "cost": "Free", "tags": ["art", "culture", "photography"], "time_of_day": "Afternoon", "description": "Hilltop bohemian quarter with art studios, cafes, and city views"},
        {"name": "Acai on the Beach", "address": "Any beach kiosk", "hours": "8am-6pm", "cost": "$3-5", "tags": ["food", "beaches"], "time_of_day": "Afternoon", "description": "Thick frozen acai bowl topped with granola and banana — a Rio staple"},
    ],
    "Buenos Aires": [
        {"name": "San Telmo Sunday Market", "address": "Defensa St, San Telmo", "hours": "Sun 10am-5pm", "cost": "Free entry", "tags": ["shopping", "culture"], "time_of_day": "Morning", "description": "Antiques, tango dancers, and street food stretching 20+ blocks"},
        {"name": "Recoleta Cemetery", "address": "Junin 1760, Recoleta", "hours": "8am-5:45pm", "cost": "Free", "tags": ["architecture", "culture"], "time_of_day": "Morning", "description": "Ornate mausoleums including Eva Peron's tomb — a city of the dead"},
        {"name": "Tango Show & Milonga", "address": "Various (Cafe de los Angelitos, La Ventana)", "hours": "8pm-midnight", "cost": "$40-80 (dinner show)", "tags": ["culture", "nightlife"], "time_of_day": "Night", "description": "Professional tango performance then join a milonga dance hall"},
        {"name": "Parrilla Steak Dinner", "address": "Various (Don Julio, La Cabrera)", "hours": "8pm-midnight", "cost": "$20-50", "tags": ["food"], "time_of_day": "Evening", "description": "Argentina's legendary grass-fed beef grilled to perfection"},
        {"name": "La Boca & Caminito", "address": "Caminito, La Boca", "hours": "10am-6pm", "cost": "Free", "tags": ["art", "photography", "culture"], "time_of_day": "Afternoon", "description": "Colorful tin houses, tango performers, and the spirit of Boca Juniors"},
        {"name": "MALBA Museum", "address": "Av. Pres. Figueroa Alcorta 3415", "hours": "12pm-8pm (closed Tue)", "cost": "$8", "tags": ["art"], "time_of_day": "Afternoon", "description": "Latin American modern art including Frida Kahlo and Diego Rivera"},
        {"name": "Palermo Soho Bars", "address": "Palermo Soho neighborhood", "hours": "Best after 9pm", "cost": "$5-15/drink", "tags": ["nightlife", "food"], "time_of_day": "Night", "description": "Street art-lined streets with speakeasies, craft cocktails, and wine bars"},
        {"name": "Mate & Empanadas in the Park", "address": "Parque Tres de Febrero (Bosques de Palermo)", "hours": "Best afternoon", "cost": "$5-8", "tags": ["food", "wellness"], "time_of_day": "Afternoon", "description": "Join porteños sharing mate tea in Buenos Aires's biggest green space"},
        {"name": "Tigre Delta Day Trip", "address": "Train from Retiro station (1h)", "hours": "Full day", "cost": "$2 train + $10 boat tour", "tags": ["photography"], "time_of_day": "Morning", "description": "Kayak or boat through lush river delta islands with waterside restaurants"},
        {"name": "Cafe Tortoni", "address": "Av. de Mayo 825", "hours": "8am-1am", "cost": "$5-10", "tags": ["food", "culture"], "time_of_day": "Afternoon", "description": "Buenos Aires's oldest cafe since 1858 — coffee, medialunas, and occasional tango"},
    ],
    "Berlin": [
        {"name": "East Side Gallery", "address": "Muhlenstrasse 3-100, Friedrichshain", "hours": "24/7", "cost": "Free", "tags": ["art", "culture"], "time_of_day": "Morning", "description": "1.3km of Berlin Wall murals including the famous Fraternal Kiss"},
        {"name": "Brandenburg Gate", "address": "Pariser Platz, Mitte", "hours": "24/7", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "18th-century neoclassical gate — symbol of German reunification"},
        {"name": "Reichstag Building", "address": "Platz der Republik 1", "hours": "8am-midnight (book ahead)", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Evening", "description": "German parliament with Norman Foster's glass dome and rooftop views"},
        {"name": "Museum Island", "address": "Bodestrasse 1-3, Mitte", "hours": "10am-6pm", "cost": "$22 (day pass)", "tags": ["art", "culture"], "time_of_day": "Afternoon", "description": "Five world-class museums including the Pergamon Altar and Nefertiti bust"},
        {"name": "Holocaust Memorial", "address": "Cora-Berliner-Strasse 1", "hours": "24/7 (info center 10am-7pm)", "cost": "Free", "tags": ["culture"], "time_of_day": "Afternoon", "description": "2,711 concrete blocks of varying heights — a powerful memorial to walk through"},
        {"name": "Markthalle Neun", "address": "Eisenbahnstrasse 42/43, Kreuzberg", "hours": "Thu 5-10pm (Street Food Thursday)", "cost": "$5-12", "tags": ["food"], "time_of_day": "Evening", "description": "Historic market hall's weekly street food event — global cuisines"},
        {"name": "Mauerpark Flea Market", "address": "Bernauer Str 63-64, Prenzlauer Berg", "hours": "Sun 9am-6pm", "cost": "Free entry", "tags": ["shopping", "culture"], "time_of_day": "Morning", "description": "Sunday flea market with karaoke in the amphitheater and vintage finds"},
        {"name": "Tempelhofer Feld", "address": "Tempelhofer Damm, Tempelhof", "hours": "Dawn-dusk", "cost": "Free", "tags": ["wellness", "photography"], "time_of_day": "Afternoon", "description": "Former airport converted into a massive public park — cycle, kite, grill"},
        {"name": "Doner Kebab Tour", "address": "Various (Mustafa's, Ruyam)", "hours": "11am-3am", "cost": "$5-8", "tags": ["food"], "time_of_day": "Midday", "description": "Berlin invented the doner kebab — try the best at legendary stands"},
        {"name": "Berghain Nightclub", "address": "Am Wriezener Bahnhof, Friedrichshain", "hours": "Sat midnight-Mon morning", "cost": "$15-20 cover (if you get in)", "tags": ["nightlife"], "time_of_day": "Night", "description": "World's most famous techno club in a former power plant — notoriously selective door"},
    ],
    "Santorini": [
        {"name": "Oia Sunset", "address": "Oia Castle ruins, Oia", "hours": "Arrive 1h before sunset", "cost": "Free", "tags": ["photography"], "time_of_day": "Evening", "description": "The world's most famous sunset over the caldera — arrive early for a spot"},
        {"name": "Fira to Oia Hike", "address": "Start in Fira, end in Oia", "hours": "Allow 4-5 hours", "cost": "Free", "tags": ["hiking", "photography"], "time_of_day": "Morning", "description": "10km clifftop trail with caldera views, passing through Imerovigli"},
        {"name": "Catamaran Caldera Cruise", "address": "Departs from Vlychada or Ammoudi Bay", "hours": "Various (sunset cruise best)", "cost": "$100-150", "tags": ["photography", "beaches"], "time_of_day": "Afternoon", "description": "Sail the caldera with stops for swimming, hot springs, and sunset dinner"},
        {"name": "Volcanic Wine Tasting", "address": "Santo Wines, Pyrgos", "hours": "10am-8pm", "cost": "$15-25", "tags": ["food"], "time_of_day": "Afternoon", "description": "Taste Assyrtiko and Vinsanto wines grown in volcanic soil with caldera views"},
        {"name": "Akrotiri Archaeological Site", "address": "Akrotiri, South Santorini", "hours": "8am-8pm", "cost": "$14", "tags": ["culture"], "time_of_day": "Morning", "description": "Minoan Bronze Age city buried by volcanic eruption — 'Pompeii of the Aegean'"},
        {"name": "Red Beach", "address": "Near Akrotiri", "hours": "Best 9am-4pm", "cost": "Free", "tags": ["beaches", "photography"], "time_of_day": "Morning", "description": "Dramatic crimson cliffs and volcanic sand — one of Greece's most unique beaches"},
        {"name": "Blue Dome Churches Photo Walk", "address": "Oia and Fira", "hours": "Best morning light", "cost": "Free", "tags": ["photography", "architecture"], "time_of_day": "Morning", "description": "The iconic blue-domed churches against white walls and sea — Instagram heaven"},
        {"name": "Perissa Black Sand Beach", "address": "Perissa, Southeast Santorini", "hours": "Best 10am-6pm", "cost": "Free (sunbed $10)", "tags": ["beaches"], "time_of_day": "Afternoon", "description": "Long black volcanic sand beach backed by Mesa Vouno mountain"},
        {"name": "Caldera-View Dinner", "address": "Various (Ambrosia, Argo, Kastro)", "hours": "7pm-11pm", "cost": "$40-80/person", "tags": ["food", "photography"], "time_of_day": "Evening", "description": "Fine dining perched on the caldera rim with sunset views"},
        {"name": "Hot Springs Swim", "address": "Near Nea Kameni volcano island", "hours": "Part of boat tours", "cost": "Included in boat tour", "tags": ["wellness", "beaches"], "time_of_day": "Afternoon", "description": "Swim in warm sulfurous waters heated by the active volcano"},
    ],
    "Chiang Mai": [
        {"name": "Doi Suthep Temple", "address": "Huay Kaew Rd (15 min from city)", "hours": "6am-6pm", "cost": "$2", "tags": ["temples", "photography"], "time_of_day": "Morning", "description": "Golden hilltop temple with 306 steps and panoramic views of the city"},
        {"name": "Elephant Nature Park", "address": "60km from city (shuttle provided)", "hours": "Full day 8am-5pm", "cost": "$70-80", "tags": ["wildlife", "culture"], "time_of_day": "Morning", "description": "Ethical elephant rescue and rehabilitation — feed, bathe, and observe"},
        {"name": "Sunday Walking Street Market", "address": "Ratchadamnoen Rd, Old City", "hours": "Sun 4pm-midnight", "cost": "Free entry", "tags": ["shopping", "food"], "time_of_day": "Evening", "description": "Huge night market with local crafts, art, street food, and live music"},
        {"name": "Thai Cooking Class at Farm", "address": "Various farms outside city", "hours": "9am-3pm", "cost": "$30-40", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Market visit + cook 5 dishes at an organic farm — take recipes home"},
        {"name": "Old City Temple Walk", "address": "Within the moat, Old City", "hours": "8am-5pm", "cost": "Free-$2 per temple", "tags": ["temples", "culture", "photography"], "time_of_day": "Morning", "description": "Walk between 30+ ancient temples — Wat Chedi Luang, Wat Phra Singh, Wat Chiang Man"},
        {"name": "Muay Thai Class", "address": "Various gyms (Lanna Fighting, Tiger Muay Thai)", "hours": "Morning or afternoon", "cost": "$10-15", "tags": ["culture", "wellness"], "time_of_day": "Morning", "description": "Learn Thailand's national martial art from experienced trainers"},
        {"name": "Nimmanhaemin Road Cafes", "address": "Nimmanhaemin Rd, Suthep", "hours": "8am-10pm", "cost": "$3-8", "tags": ["food", "art"], "time_of_day": "Afternoon", "description": "Trendy street with Instagram-worthy cafes, galleries, and boutiques"},
        {"name": "Doi Inthanon National Park", "address": "90km south of city", "hours": "Full day trip", "cost": "$10 entry + transport", "tags": ["hiking", "photography"], "time_of_day": "Morning", "description": "Thailand's highest peak with twin pagodas, waterfalls, and cloud forest"},
        {"name": "Khao Soi at Khao Soi Khun Yai", "address": "Sri Poom Rd, Old City", "hours": "9am-3pm", "cost": "$2-3", "tags": ["food"], "time_of_day": "Midday", "description": "Chiang Mai's signature dish — coconut curry noodles with crispy topping"},
        {"name": "Night Bazaar", "address": "Chang Klan Rd", "hours": "Nightly 6pm-midnight", "cost": "Free entry", "tags": ["shopping", "food"], "time_of_day": "Evening", "description": "Daily night market with hill tribe crafts, clothing, and street food"},
    ],
    "Hanoi": [
        {"name": "Old Quarter Walking Tour", "address": "36 Streets, Hoan Kiem District", "hours": "Best 7-10am or 5-8pm", "cost": "Free to walk", "tags": ["culture", "photography", "food"], "time_of_day": "Morning", "description": "Chaotic maze of 36 ancient streets each named for its traditional trade"},
        {"name": "Hoan Kiem Lake", "address": "Hoan Kiem District", "hours": "24/7", "cost": "Free", "tags": ["photography", "wellness"], "time_of_day": "Evening", "description": "Sacred lake with Ngoc Son Temple on a tiny island — beautiful at sunset"},
        {"name": "Ho Chi Minh Mausoleum", "address": "Hung Vuong, Ba Dinh District", "hours": "7:30-10:30am (closed Mon-Fri afternoons)", "cost": "Free", "tags": ["culture"], "time_of_day": "Morning", "description": "Preserved body of Vietnam's revolutionary leader in a granite monument"},
        {"name": "Temple of Literature", "address": "58 Quoc Tu Giam, Dong Da", "hours": "8am-5pm", "cost": "$1.50", "tags": ["temples", "architecture", "culture"], "time_of_day": "Morning", "description": "Vietnam's first university from 1070 — tranquil gardens and ancient pavilions"},
        {"name": "Egg Coffee at Cafe Giang", "address": "39 Nguyen Huu Huan, Hoan Kiem", "hours": "7am-10pm", "cost": "$2", "tags": ["food"], "time_of_day": "Afternoon", "description": "Whipped egg yolk coffee — Hanoi's signature drink since 1946"},
        {"name": "Water Puppet Show", "address": "Thang Long Theatre, 57B Dinh Tien Hoang", "hours": "Shows at 3pm, 5pm, 6:30pm, 8pm", "cost": "$5-8", "tags": ["culture", "art"], "time_of_day": "Evening", "description": "Traditional Vietnamese water puppetry with live music — a 1,000-year-old art form"},
        {"name": "Bun Cha at Huong Lien", "address": "24 Le Van Huu, Hai Ba Trung", "hours": "10am-2:30pm", "cost": "$3", "tags": ["food"], "time_of_day": "Midday", "description": "The bun cha restaurant where Obama and Bourdain ate together"},
        {"name": "Train Street", "address": "Tran Phu St area, Hoan Kiem", "hours": "Trains pass ~3:30pm and 7pm", "cost": "Free", "tags": ["photography", "culture"], "time_of_day": "Afternoon", "description": "Narrow street where a train passes inches from houses — sit at a cafe and watch"},
        {"name": "Bia Hoi Corner", "address": "Junction of Ta Hien and Luong Ngoc Quyen", "hours": "Best 5pm-10pm", "cost": "$0.25/glass", "tags": ["nightlife", "food"], "time_of_day": "Evening", "description": "Sit on tiny stools and drink the world's cheapest fresh beer with locals"},
        {"name": "Ha Long Bay Day Trip", "address": "3.5h drive from Hanoi", "hours": "Full day or overnight", "cost": "$50-150 (cruise)", "tags": ["photography", "beaches"], "time_of_day": "Morning", "description": "UNESCO limestone karsts rising from emerald waters — kayak and swim"},
    ],
    "Florence": [
        {"name": "Brunelleschi's Dome (Duomo)", "address": "Piazza del Duomo", "hours": "8:15am-7pm", "cost": "$20 (combined ticket)", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "Climb 463 steps inside the world's largest masonry dome for city panoramas"},
        {"name": "Uffizi Gallery", "address": "Piazzale degli Uffizi 6", "hours": "8:15am-6:30pm (closed Mon)", "cost": "$24", "tags": ["art"], "time_of_day": "Morning", "description": "Botticelli's Birth of Venus, da Vinci, and the greatest Renaissance collection"},
        {"name": "Accademia Gallery (David)", "address": "Via Ricasoli 58-60", "hours": "8:15am-6:50pm (closed Mon)", "cost": "$16", "tags": ["art"], "time_of_day": "Morning", "description": "Michelangelo's David — 5.17m of marble perfection"},
        {"name": "Ponte Vecchio", "address": "Ponte Vecchio, crossing the Arno", "hours": "24/7 (shops 10am-7pm)", "cost": "Free", "tags": ["architecture", "shopping", "photography"], "time_of_day": "Evening", "description": "Medieval stone bridge lined with gold and jewelry shops since 1345"},
        {"name": "Piazzale Michelangelo Sunset", "address": "Piazzale Michelangelo", "hours": "Best 1h before sunset", "cost": "Free", "tags": ["photography"], "time_of_day": "Evening", "description": "The best panoramic viewpoint — all of Florence spread below you"},
        {"name": "Mercato Centrale", "address": "Piazza del Mercato Centrale", "hours": "10am-midnight (upstairs food hall)", "cost": "$8-20", "tags": ["food"], "time_of_day": "Midday", "description": "Two-floor market — fresh produce below, artisan food stalls above"},
        {"name": "Boboli Gardens", "address": "Piazza de Pitti 1", "hours": "8:15am-6:30pm", "cost": "$10", "tags": ["wellness", "architecture"], "time_of_day": "Afternoon", "description": "Renaissance gardens behind Palazzo Pitti with sculptures and grottos"},
        {"name": "Tuscan Cooking Class", "address": "Various (often in countryside)", "hours": "Morning or afternoon", "cost": "$70-100", "tags": ["food", "culture"], "time_of_day": "Morning", "description": "Make fresh pasta, ragù, and tiramisu with a Tuscan nonna"},
        {"name": "Chianti Wine Tour", "address": "Chianti region (30-60 min drive)", "hours": "Half or full day", "cost": "$50-80", "tags": ["food"], "time_of_day": "Afternoon", "description": "Visit vineyards, taste Chianti Classico, and eat in a Tuscan farmhouse"},
        {"name": "Lampredotto Sandwich", "address": "Various stands (Nerbone, L'Antico Trippaio)", "hours": "10am-7pm", "cost": "$5", "tags": ["food"], "time_of_day": "Midday", "description": "Florence's legendary tripe sandwich — adventurous and delicious street food"},
    ],
    "Ho Chi Minh City": [
        {"name": "War Remnants Museum", "address": "28 Vo Van Tan, District 3", "hours": "7:30am-6pm", "cost": "$2", "tags": ["culture"], "time_of_day": "Morning", "description": "Powerful and confronting exhibits about the Vietnam War — essential visit"},
        {"name": "Cu Chi Tunnels", "address": "Ben Duoc, Cu Chi District (1.5h drive)", "hours": "8am-5pm", "cost": "$12", "tags": ["culture", "hiking"], "time_of_day": "Morning", "description": "Crawl through the Viet Cong's incredible 250km underground tunnel network"},
        {"name": "Ben Thanh Market", "address": "Le Loi, District 1", "hours": "6am-6pm (night market until 11pm)", "cost": "Free entry", "tags": ["shopping", "food"], "time_of_day": "Afternoon", "description": "Saigon's most iconic market — lacquerware, ao dai, coffee, and street food"},
        {"name": "Pho Breakfast", "address": "Various (Pho Hoa, Pho Quynh, Pho 2000)", "hours": "6am-10am", "cost": "$2-3", "tags": ["food"], "time_of_day": "Morning", "description": "Start the day like a local — beef pho with herbs, chili, and lime"},
        {"name": "Notre-Dame Cathedral & Post Office", "address": "Paris Square, District 1", "hours": "Exterior 24/7, Post Office 7am-6pm", "cost": "Free", "tags": ["architecture", "photography"], "time_of_day": "Morning", "description": "French colonial cathedral and ornate Gustave Eiffel-designed post office"},
        {"name": "Bui Vien Walking Street", "address": "Bui Vien St, District 1", "hours": "Best after 7pm", "cost": "Free to walk", "tags": ["nightlife", "food"], "time_of_day": "Night", "description": "Saigon's backpacker street — cheap beer, live music, and energy"},
        {"name": "Motorbike Food Tour", "address": "Various operators (pick up District 1)", "hours": "Evening tours 5-9pm", "cost": "$40-60", "tags": ["food", "culture"], "time_of_day": "Evening", "description": "Ride pillion through alleyways tasting banh mi, banh xeo, and com tam"},
        {"name": "Mekong Delta Day Trip", "address": "Ben Tre or My Tho (2h drive)", "hours": "Full day", "cost": "$20-40", "tags": ["culture", "photography"], "time_of_day": "Morning", "description": "Boat through coconut groves, visit fruit orchards, and taste local honey"},
        {"name": "Jade Emperor Pagoda", "address": "73 Mai Thi Luu, District 1", "hours": "7am-6pm", "cost": "Free", "tags": ["temples", "culture"], "time_of_day": "Afternoon", "description": "Atmospheric Taoist temple filled with incense smoke and carved figures"},
        {"name": "Saigon Skydeck", "address": "36 Ho Tung Mau, District 1 (Bitexco Tower)", "hours": "9:30am-9:30pm", "cost": "$8", "tags": ["photography", "architecture"], "time_of_day": "Evening", "description": "49th-floor observation deck in Saigon's lotus-shaped skyscraper"},
    ],
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
    """Copy all 21 existing fields and add detail, visa, practical, and activity fields."""
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

        # Visa info (from COUNTRY_VISA)
        visa = COUNTRY_VISA.get(country, {"status": "unknown", "max_stay": 0, "notes": "Check embassy website"})
        d["visa_status"] = visa["status"]
        d["visa_max_stay"] = visa["max_stay"]
        d["visa_notes"] = visa["notes"]

        # Practical info (from COUNTRY_PRACTICAL)
        prac = COUNTRY_PRACTICAL.get(country, {})
        d["currency"] = prac.get("currency", "USD")
        d["currency_symbol"] = prac.get("currency_symbol", "$")
        d["currency_name"] = prac.get("currency_name", "US Dollar")
        d["plug_type"] = prac.get("plug_type", "A/B")
        d["tipping"] = prac.get("tipping", "10-20% at restaurants")
        d["emergency_number"] = prac.get("emergency", "112")
        d["sim_info"] = prac.get("sim_info", "Available at airport")
        d["tap_water"] = prac.get("tap_water", "Check locally")
        d["dress_code"] = prac.get("dress_code", "Casual")

        # Structured activities (from CITY_STRUCTURED_ACTIVITIES)
        if name in CITY_STRUCTURED_ACTIVITIES:
            activities = []
            for act in CITY_STRUCTURED_ACTIVITIES[name]:
                a = dict(act)
                # Auto-generate Google Maps URL
                from urllib.parse import quote
                search_query = f"{a['name']}, {name}"
                a["maps_url"] = f"https://www.google.com/maps/search/?api=1&query={quote(search_query)}"
                activities.append(a)
            d["structured_activities"] = activities
        else:
            d["structured_activities"] = []

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
        # Detail fields (7)
        lines.append(f'        "neighborhoods": {d["neighborhoods"]},\n')
        lines.append(f'        "top_activities": {d["top_activities"]},\n')
        lines.append(f'        "local_food": {d["local_food"]},\n')
        lines.append(f'        "local_drink": {d["local_drink"]},\n')
        lines.append(f'        "things_to_do": {d["things_to_do"]},\n')
        lines.append(f'        "uber_cost": {d["uber_cost"]},\n')
        lines.append(f'        "airbnb_cost": {d["airbnb_cost"]},\n')
        # Visa fields (3)
        lines.append(f'        "visa_status": {repr(d["visa_status"])},\n')
        lines.append(f'        "visa_max_stay": {d["visa_max_stay"]},\n')
        lines.append(f'        "visa_notes": {repr(d["visa_notes"])},\n')
        # Practical info fields (9)
        lines.append(f'        "currency": {repr(d["currency"])},\n')
        lines.append(f'        "currency_symbol": {repr(d["currency_symbol"])},\n')
        lines.append(f'        "currency_name": {repr(d["currency_name"])},\n')
        lines.append(f'        "plug_type": {repr(d["plug_type"])},\n')
        lines.append(f'        "tipping": {repr(d["tipping"])},\n')
        lines.append(f'        "emergency_number": {repr(d["emergency_number"])},\n')
        lines.append(f'        "sim_info": {repr(d["sim_info"])},\n')
        lines.append(f'        "tap_water": {repr(d["tap_water"])},\n')
        lines.append(f'        "dress_code": {repr(d["dress_code"])},\n')
        # Structured activities
        lines.append(f'        "structured_activities": {repr(d["structured_activities"])},\n')
        lines.append(f'    }},\n')
    lines.append("}\n\n")

    # Write TRANSPORT_ROUTES as a second exported dict
    lines.append("TRANSPORT_ROUTES = {\n")
    for (city_a, city_b), route in TRANSPORT_ROUTES.items():
        lines.append(f'    ("{city_a}", "{city_b}"): {repr(route)},\n')
    lines.append("}\n")

    outpath = os.path.join(os.path.dirname(__file__), "cities.py")
    with open(outpath, "w") as f:
        f.writelines(lines)
    fields_per_city = len(next(iter(enriched.values()))) if enriched else 0
    print(f"Wrote enriched cities.py with {len(enriched)} cities x {fields_per_city} fields + {len(TRANSPORT_ROUTES)} transport routes")


if __name__ == "__main__":
    enriched = enrich()
    write_cities_file(enriched)
    # Verify
    missing = [n for n, d in enriched.items() if not d.get("neighborhoods") or not d.get("top_activities")]
    if missing:
        print(f"WARNING: {len(missing)} cities missing detail data: {missing[:5]}...")
    else:
        print("All cities have complete detail data!")
