"""
populate_caffiestaan_menu.py

Seeds the Caffiestaan database with categories, dishes, variants (Half/Full/Sizes),
and auto-downloads high-resolution Unsplash food photography directly into your media storage.
"""

import os
import django
import urllib.request
from decimal import Decimal
from django.core.files.base import ContentFile
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caffiestaan.settings')
django.setup()

from menu.models import MenuCategory, Dish, DishVariant, DishImage

CATEGORIES = {
    "Tandoori Items": {
        "description": "Authentic clay tandoor roasted kebabs, tikkas, rotis, and naans.",
        "display_order": 1,
    },
    "Indian Curries": {
        "description": "Slow-cooked Mughlai and North Indian gravies, paneer, and dals.",
        "display_order": 2,
    },
    "Chinese": {
        "description": "Wok-tossed noodles, Indo-Chinese gravies, and spicy appetizers.",
        "display_order": 3,
    },
    "Continental & Italian": {
        "description": "Artisan pizzas, creamy pastas, and grilled continental mains.",
        "display_order": 4,
    },
    "Sandwiches & Burgers": {
        "description": "Grilled club sandwiches, loaded brioche burgers, and rolls.",
        "display_order": 5,
    },
    "Momos & Starters": {
        "description": "Steamed and fried Himalayan dumplings, crispy fries, nuggets, and popcorn.",
        "display_order": 6,
    },
    "Biryani & Rice": {
        "description": "Dum biryanis, wok-tossed fried rice, and aromatic basmati staples.",
        "display_order": 7,
    },
}

MENU_DATA = [
    # ----------------------------------------------------
    # 1. TANDOORI ITEMS
    # ----------------------------------------------------
    {
        "category": "Tandoori Items",
        "name": "Tandoori Chicken",
        "short_desc": "Spring chicken marinated in hung curd, Kashmiri chilies, and clay-oven roasted.",
        "base_price": 350.00,
        "prep_time": 25,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 350.00, "is_default": False},  # Total 700
        ]
    },
    {
        "category": "Tandoori Items",
        "name": "Chicken Tikka",
        "short_desc": "Boneless chicken cubes spiced with mustard oil, tandoori masala, and char-grilled.",
        "base_price": 300.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 350.00, "is_default": False},  # Total 650
        ]
    },
    {
        "category": "Tandoori Items",
        "name": "Plain Naan",
        "short_desc": "Classic soft refined flour bread baked in a hot tandoor.",
        "base_price": 40.00,
        "prep_time": 8,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800&q=80",
        "variants": []
    },
    {
        "category": "Tandoori Items",
        "name": "Butter Naan",
        "short_desc": "Flaky layered tandoori naan brushed generously with farm butter.",
        "base_price": 50.00,
        "prep_time": 8,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?w=800&q=80",
        "variants": []
    },
    {
        "category": "Tandoori Items",
        "name": "Garlic Naan",
        "short_desc": "Artisan tandoori naan infused with minced garlic and coriander butter.",
        "base_price": 50.00,
        "prep_time": 8,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800&q=80",
        "variants": []
    },
    {
        "category": "Tandoori Items",
        "name": "Tandoori Roti",
        "short_desc": "Traditional whole wheat flour flatbread crisp-baked in clay oven.",
        "base_price": 30.00,
        "prep_time": 6,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1505253758473-96b3d5eb926f?w=800&q=80",
        "variants": []
    },

    # ----------------------------------------------------
    # 2. INDIAN CURRIES
    # ----------------------------------------------------
    {
        "category": "Indian Curries",
        "name": "Dal Fry",
        "short_desc": "Yellow lentils tempered with ghee, cumin seeds, garlic, and fresh green chilies.",
        "base_price": 150.00,
        "prep_time": 15,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&q=80",
        "variants": []
    },
    {
        "category": "Indian Curries",
        "name": "Rajma Masala",
        "short_desc": "Slow-cooked Kashmiri red kidney beans in a robust onion-tomato gravy.",
        "base_price": 160.00,
        "prep_time": 15,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&q=80",
        "variants": []
    },
    {
        "category": "Indian Curries",
        "name": "Mattar Mushroom",
        "short_desc": "Tender button mushrooms and sweet green peas simmered in a spiced curry.",
        "base_price": 180.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80",
        "variants": []
    },
    {
        "category": "Indian Curries",
        "name": "Paneer Butter Masala",
        "short_desc": "Soft paneer cubes in a mildly sweet, velvety tomato butter and cashew gravy.",
        "base_price": 250.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80",
        "variants": []
    },
    {
        "category": "Indian Curries",
        "name": "Kadai Paneer",
        "short_desc": "Cottage cheese and crunchy bell peppers tossed in fresh freshly roasted kadai spices.",
        "base_price": 250.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800&q=80",
        "variants": []
    },
    {
        "category": "Indian Curries",
        "name": "Paneer Lababdar",
        "short_desc": "Royal Mughlai curry with grated and cubed paneer in a luscious onion-tomato cream.",
        "base_price": 250.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&q=80",
        "variants": []
    },
    {
        "category": "Indian Curries",
        "name": "Butter Chicken",
        "short_desc": "Tender chicken simmered in a rich tomato, butter, and cream satin sauce.",
        "base_price": 350.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 350.00, "is_default": False},  # Total 700
        ]
    },
    {
        "category": "Indian Curries",
        "name": "Boneless Butter Chicken",
        "short_desc": "Succulent boneless chicken tikka cooked in classic velvet makhani gravy.",
        "base_price": 380.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 370.00, "is_default": False},  # Total 750
        ]
    },
    {
        "category": "Indian Curries",
        "name": "Chicken Kanti",
        "short_desc": "Kashmiri-style pan-seared boneless chicken tossed with charred onions and tomatoes.",
        "base_price": 320.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 330.00, "is_default": False},  # Total 650
        ]
    },
    {
        "category": "Indian Curries",
        "name": "Kadai Chicken",
        "short_desc": "Chicken chunks braised in a wok with ground coriander, red chillies, and bell peppers.",
        "base_price": 350.00,
        "prep_time": 22,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 300.00, "is_default": False},  # Total 650
        ]
    },
    {
        "category": "Indian Curries",
        "name": "Chicken Lababdar",
        "short_desc": "Boneless chicken simmered in an aromatic spiced cashew, onion, and tomato emulsion.",
        "base_price": 350.00,
        "prep_time": 22,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 300.00, "is_default": False},  # Total 650
        ]
    },
    {
        "category": "Indian Curries",
        "name": "Mughlai Chicken",
        "short_desc": "Royal delicacy prepared with egg ribbons, saffron, and cream-enriched mild gravy.",
        "base_price": 350.00,
        "prep_time": 25,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 350.00, "is_default": False},  # Total 700
        ]
    },

    # ----------------------------------------------------
    # 3. CHINESE
    # ----------------------------------------------------
    {
        "category": "Chinese",
        "name": "Chicken Hakka Noodles",
        "short_desc": "Thin noodles stir-fried with shredded chicken, crunchy vegetables, and soy glaze.",
        "base_price": 180.00,
        "prep_time": 14,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&q=80",
        "variants": []
    },
    {
        "category": "Chinese",
        "name": "Chicken Chowmein",
        "short_desc": "Street-style wok-fried noodles tossed with chicken shreds and dark chili sauce.",
        "base_price": 150.00,
        "prep_time": 14,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=800&q=80",
        "variants": []
    },
    {
        "category": "Chinese",
        "name": "Veg Chowmein",
        "short_desc": "Classic stir-fried noodles loaded with julienned cabbage, carrots, and scallions.",
        "base_price": 140.00,
        "prep_time": 12,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&q=80",
        "variants": []
    },
    {
        "category": "Chinese",
        "name": "Veg Hakka Noodles",
        "short_desc": "Non-greasy wok tossed noodles with shredded seasonal veggies and white pepper.",
        "base_price": 150.00,
        "prep_time": 12,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&q=80",
        "variants": []
    },
    {
        "category": "Chinese",
        "name": "Chilli Chicken",
        "short_desc": "Crispy chicken cubes tossed with capsicum, onions, dark soy, and green chilies.",
        "base_price": 250.00,
        "prep_time": 15,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800&q=80",
        "variants": [
            {"name": "Dry", "price_adj": 0.00, "is_default": True},          # 250
            {"name": "Semi Gravy", "price_adj": 50.00, "is_default": False},  # 300
        ]
    },
    {
        "category": "Chinese",
        "name": "Lemon Chicken",
        "short_desc": "Golden fried chicken morsels glazed in a tangy lemon and honey reduction.",
        "base_price": 250.00,
        "prep_time": 16,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1527477378370-d7d8e6a21855?w=800&q=80",
        "variants": []
    },
    {
        "category": "Chinese",
        "name": "Chicken 65",
        "short_desc": "Spicy, crispy South-Indian style boneless chicken tossed with curry leaves.",
        "base_price": 350.00,
        "prep_time": 16,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=800&q=80",
        "variants": []
    },
    {
        "category": "Chinese",
        "name": "Honey Chilli Potatoes",
        "short_desc": "Crisp fried potato fingers glazed with sweet honey and spicy chili-garlic paste.",
        "base_price": 180.00,
        "prep_time": 14,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1585109649139-366815a0d713?w=800&q=80",
        "variants": []
    },
    {
        "category": "Chinese",
        "name": "Chilli Paneer",
        "short_desc": "Fried paneer cubes wok-tossed with diced bell peppers, onions, and spicy soy.",
        "base_price": 250.00,
        "prep_time": 15,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800&q=80",
        "variants": []
    },

    # ----------------------------------------------------
    # 4. CONTINENTAL & PIZZAS
    # ----------------------------------------------------
    {
        "category": "Continental & Italian",
        "name": "Grilled Chicken",
        "short_desc": "Herb-marinated chicken breast served with sautéed vegetables and pepper jus.",
        "base_price": 350.00,
        "prep_time": 22,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},
            {"name": "Full", "price_adj": 350.00, "is_default": False},  # Total 700
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Grilled Fish",
        "short_desc": "Pan-seared river fish fillet basted with lemon garlic herb butter.",
        "base_price": 700.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800&q=80",
        "variants": []
    },
    {
        "category": "Continental & Italian",
        "name": "Pasta Alfredo",
        "short_desc": "Penne pasta bathed in rich parmesan cheese and velvety garlic cream sauce.",
        "base_price": 180.00,
        "prep_time": 15,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=800&q=80",
        "variants": []
    },
    {
        "category": "Continental & Italian",
        "name": "Pasta Arrabbiata",
        "short_desc": "Penne pasta simmered in spicy San Marzano tomato sauce, garlic, and dried chili.",
        "base_price": 200.00,
        "prep_time": 15,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800&q=80",
        "variants": []
    },
    {
        "category": "Continental & Italian",
        "name": "Chicken Blast Pizza",
        "short_desc": "Loaded with spicy shredded chicken, chicken sausages, jalapeños, and mozzarella.",
        "base_price": 220.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},     # 220
            {"name": "Medium", "price_adj": 80.00, "is_default": False},  # 300
            {"name": "Large", "price_adj": 330.00, "is_default": False},  # 550
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Chicken Tikka Pizza",
        "short_desc": "Clay-oven baked chicken tikka chunks, sliced onions, and melted mozzarella.",
        "base_price": 250.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},      # 250
            {"name": "Medium", "price_adj": 100.00, "is_default": False},  # 350
            {"name": "Large", "price_adj": 330.00, "is_default": False},   # 580
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Roasted Chicken Pizza",
        "short_desc": "Oven-roasted herb chicken, bell peppers, cracked black pepper, and cheese.",
        "base_price": 190.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},     # 190
            {"name": "Medium", "price_adj": 90.00, "is_default": False},  # 280
            {"name": "Large", "price_adj": 300.00, "is_default": False},  # 490
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Butter Chicken Pizza",
        "short_desc": "Makhani sauce base crowned with tender butter chicken and diced onions.",
        "base_price": 250.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1544982503-9f984c14501a?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},      # 250
            {"name": "Medium", "price_adj": 130.00, "is_default": False},  # 380
            {"name": "Large", "price_adj": 330.00, "is_default": False},   # 580
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Peri Peri Chicken Pizza",
        "short_desc": "Fiery peri-peri spiced chicken shreds, red paprika, corn, and mozzarella.",
        "base_price": 240.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},      # 240
            {"name": "Medium", "price_adj": 130.00, "is_default": False},  # 370
            {"name": "Large", "price_adj": 340.00, "is_default": False},   # 580
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Kids Special Pizza",
        "short_desc": "Mild cheese pizza topped with sweet corn kernels and sweet tomato reduction.",
        "base_price": 220.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},     # 220
            {"name": "Medium", "price_adj": 80.00, "is_default": False},  # 300
            {"name": "Large", "price_adj": 330.00, "is_default": False},  # 550
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Cafestan Special Pizza",
        "short_desc": "Chef's gourmet creation with secret herb marinara and supreme multi-toppings.",
        "base_price": 450.00,
        "prep_time": 22,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&q=80",
        "variants": [
            {"name": "Medium", "price_adj": 0.00, "is_default": True},    # 450
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Margherita Pizza",
        "short_desc": "Classic Neapolitan crust, San Marzano tomato sauce, fresh basil, and mozzarella.",
        "base_price": 180.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},     # 180
            {"name": "Medium", "price_adj": 70.00, "is_default": False},  # 250
            {"name": "Large", "price_adj": 270.00, "is_default": False},  # 450
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Plain Cheese Pizza",
        "short_desc": "Simple double mozzarella crust baked golden brown with Italian herbs.",
        "base_price": 190.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},      # 190
            {"name": "Medium", "price_adj": 110.00, "is_default": False},  # 300
            {"name": "Large", "price_adj": 300.00, "is_default": False},   # 490
        ]
    },
    {
        "category": "Continental & Italian",
        "name": "Cheese & Corn Pizza",
        "short_desc": "Crisp sweet corn kernels paired with stretchy mozzarella and gouda.",
        "base_price": 220.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},      # 220
            {"name": "Medium", "price_adj": 120.00, "is_default": False},  # 340
            {"name": "Large", "price_adj": 240.00, "is_default": False},   # 460
        ]
    },

    # ----------------------------------------------------
    # 5. SANDWICHES, BURGERS & ROLLS
    # ----------------------------------------------------
    {
        "category": "Sandwiches & Burgers",
        "name": "Veg Grilled Sandwich",
        "short_desc": "Toasted bread with spiced vegetable stuffing, mint chutney, and butter.",
        "base_price": 100.00,
        "prep_time": 12,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Veg Plain Sandwich",
        "short_desc": "Soft untoasted sandwich with cucumber, tomatoes, and seasoned mint spread.",
        "base_price": 80.00,
        "prep_time": 10,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Chicken Grilled Sandwich",
        "short_desc": "Shredded spiced chicken with melted cheese pressed in sourdough bread.",
        "base_price": 130.00,
        "prep_time": 14,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Chicken Plain Sandwich",
        "short_desc": "Fresh bread slices layered with pulled chicken, mayonnaise, and black pepper.",
        "base_price": 110.00,
        "prep_time": 10,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Cafestan Club Sandwich",
        "short_desc": "Triple-decker layered sandwich stuffed with fried egg, grilled chicken, and cheese.",
        "base_price": 160.00,
        "prep_time": 15,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1567234669003-dce7a7a88821?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Chicken Burst Burger",
        "short_desc": "Crispy chicken patty stuffed with molten cheese on toasted brioche.",
        "base_price": 130.00,
        "prep_time": 15,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Veg Burger",
        "short_desc": "Crispy potato and vegetable patty with lettuce, tomatoes, and house mayo.",
        "base_price": 100.00,
        "prep_time": 12,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Mexican Burger",
        "short_desc": "Spiced patty with salsa, jalapeños, melted cheddar, and chipotle mayo.",
        "base_price": 150.00,
        "prep_time": 15,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Chicken Zinger Burger",
        "short_desc": "Extra-crunchy fried chicken fillet, ice-cold lettuce, and spicy mayo.",
        "base_price": 180.00,
        "prep_time": 15,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Cheese Burger",
        "short_desc": "Classic juicy patty smothered with double layers of cheddar cheese.",
        "base_price": 120.00,
        "prep_time": 12,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Chicken Kathi Roll",
        "short_desc": "Flaky paratha rolled with spiced chicken boti, sautéed onions, and mint chutney.",
        "base_price": 130.00,
        "prep_time": 12,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Chicken Twist Roll",
        "short_desc": "Crispy chicken strips wrapped with creamy slaw in a soft griddle roll.",
        "base_price": 120.00,
        "prep_time": 12,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=800&q=80",
        "variants": []
    },
    {
        "category": "Sandwiches & Burgers",
        "name": "Chicken Tikka Roll",
        "short_desc": "Charcoal grilled tikka pieces wrapped with pickled onions in a warm paratha.",
        "base_price": 150.00,
        "prep_time": 14,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=800&q=80",
        "variants": []
    },

    # ----------------------------------------------------
    # 6. MOMOS & STARTERS
    # ----------------------------------------------------
    {
        "category": "Momos & Starters",
        "name": "Veg Momos",
        "short_desc": "Himalayan dumplings stuffed with finely minced vegetables and scallions.",
        "base_price": 90.00,
        "prep_time": 15,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1625398407797-40916a29bc01?w=800&q=80",
        "variants": []
    },
    {
        "category": "Momos & Starters",
        "name": "Chicken Momos",
        "short_desc": "Juicy minced chicken dumplings served with authentic spicy red chili chutney.",
        "base_price": 110.00,
        "prep_time": 15,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1625398407797-40916a29bc01?w=800&q=80",
        "variants": [
            {"name": "Steamed", "price_adj": 0.00, "is_default": True},    # 110
            {"name": "Fried", "price_adj": 10.00, "is_default": False},     # 120
        ]
    },
    {
        "category": "Momos & Starters",
        "name": "French Fries",
        "short_desc": "Golden fried potato batons seasoned with sea salt.",
        "base_price": 150.00,
        "prep_time": 10,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=800&q=80",
        "variants": []
    },
    {
        "category": "Momos & Starters",
        "name": "Chicken Nuggets",
        "short_desc": "Breaded minced chicken bites fried until crispy golden, served with dip.",
        "base_price": 200.00,
        "prep_time": 12,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710?w=800&q=80",
        "variants": []
    },
    {
        "category": "Momos & Starters",
        "name": "Chicken Popcorn",
        "short_desc": "Bite-sized seasoned chicken tenders fried crunchy.",
        "base_price": 130.00,
        "prep_time": 12,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710?w=800&q=80",
        "variants": [
            {"name": "Small", "price_adj": 0.00, "is_default": True},     # 130
            {"name": "Medium", "price_adj": 70.00, "is_default": False},  # 200
            {"name": "Large", "price_adj": 120.00, "is_default": False},  # 250
        ]
    },
    {
        "category": "Momos & Starters",
        "name": "Chicken Strips",
        "short_desc": "Succulent chicken breast strips breaded in spiced panko crumbs.",
        "base_price": 150.00,
        "prep_time": 14,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710?w=800&q=80",
        "variants": [
            {"name": "3 Pieces (Small)", "price_adj": 0.00, "is_default": True},    # 150
            {"name": "6 Pieces (Medium)", "price_adj": 150.00, "is_default": False}, # 300
            {"name": "12 Pieces (Large)", "price_adj": 350.00, "is_default": False}, # 500
        ]
    },

    # ----------------------------------------------------
    # 7. BIRYANI & RICE
    # ----------------------------------------------------
    {
        "category": "Biryani & Rice",
        "name": "Chicken Biryani",
        "short_desc": "Fragrant aged basmati rice dum-cooked with spiced chicken and saffron ghee.",
        "base_price": 120.00,
        "prep_time": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},     # 120
            {"name": "Full", "price_adj": 80.00, "is_default": False},   # 200
        ]
    },
    {
        "category": "Biryani & Rice",
        "name": "Veg Biryani",
        "short_desc": "Aromatic long-grain basmati layered with garden veggies, whole spices, and mint.",
        "base_price": 100.00,
        "prep_time": 18,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},     # 100
            {"name": "Full", "price_adj": 80.00, "is_default": False},   # 180
        ]
    },
    {
        "category": "Biryani & Rice",
        "name": "Chicken Fried Rice",
        "short_desc": "Wok-tossed basmati rice with egg, chicken shreds, scallions, and soy.",
        "base_price": 150.00,
        "prep_time": 14,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},      # 150
            {"name": "Full", "price_adj": 140.00, "is_default": False},   # 290
        ]
    },
    {
        "category": "Biryani & Rice",
        "name": "Veg Fried Rice",
        "short_desc": "Classic Indo-Chinese wok fried rice loaded with finely diced vegetables.",
        "base_price": 120.00,
        "prep_time": 12,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800&q=80",
        "variants": [
            {"name": "Half", "price_adj": 0.00, "is_default": True},      # 120
            {"name": "Full", "price_adj": 120.00, "is_default": False},   # 240
        ]
    },
    {
        "category": "Biryani & Rice",
        "name": "Plain Steamed Rice",
        "short_desc": "Fluffy, premium long-grain boiled basmati rice.",
        "base_price": 100.00,
        "prep_time": 8,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=800&q=80",
        "variants": []
    },
]

def run():
    print("=" * 65)
    print(" Populating Caffiestaan Database with Menu and Photos")
    print("=" * 65)

    # 1. Categories
    category_objs = {}
    for cat_name, info in CATEGORIES.items():
        cat, created = MenuCategory.objects.get_or_create(
            name=cat_name,
            defaults={
                "description": info["description"],
                "display_order": info["display_order"],
                "is_active": True,
            }
        )
        category_objs[cat_name] = cat
        status = "Created" if created else "Found"
        print(f"[{status}] Category: {cat_name}")

    headers = {'User-Agent': 'Mozilla/5.0'}

    # 2. Dishes & Variants
    for item in MENU_DATA:
        category = category_objs[item["category"]]
        dish, created = Dish.objects.get_or_create(
            name=item["name"],
            defaults={
                "category": category,
                "short_description": item["short_desc"],
                "base_price": Decimal(str(item["base_price"])),
                "preparation_time": item["prep_time"],
                "dietary_type": item["diet"],
                "is_available": True,
                "is_featured": True,
            }
        )
        if created:
            print(f"  + Added Dish: {dish.name} (Base ₹{dish.base_price})")
        else:
            print(f"  ~ Updating Dish: {dish.name}")

        # Add size variants if specified
        for var in item.get("variants", []):
            DishVariant.objects.get_or_create(
                dish=dish,
                name=var["name"],
                defaults={
                    "price_adjustment": Decimal(str(var["price_adj"])),
                    "is_default": var["is_default"]
                }
            )

        # Download & attach photo if not already downloaded
        if not dish.images.exists():
            image_url = item.get("image_url")
            if image_url:
                try:
                    req = urllib.request.Request(image_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=12) as response:
                        img_data = response.read()

                    filename = f"{slugify(dish.name)}.jpg"
                    dish_img = DishImage(
                        dish=dish,
                        alt_text=f"{dish.name} photo",
                        is_primary=True
                    )
                    dish_img.image.save(filename, ContentFile(img_data), save=True)
                    print(f"    --> Downloaded and attached image: {filename}")
                except Exception as exc:
                    print(f"    [!] Failed to download image for {dish.name}: {exc}")

    print("\n" + "=" * 65)
    print(" Seeding successfully completed!")
    print("=" * 65)

if __name__ == "__main__":
    run()