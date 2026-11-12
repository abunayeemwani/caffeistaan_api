import os
import django
import urllib.request
from django.core.files.base import ContentFile
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caffiestaan.settings')
django.setup()

from menu.models import MenuCategory, Dish, DishImage

CATEGORIES = {
    "Coffee": "Specialty espresso, filter coffee, and cold brew roasts.",
    "Grills & BBQ": "Clay tandoor and open charcoal grilled delicacies.",
    "Seafood": "Fresh water and coastal fish specialties.",
    "Fast Food": "Handcrafted brioche burgers, grilled sourdoughs, and fries.",
    "Desserts": "Freshly baked brownies, cupcakes, and confectionery.",
    "Biryani & Rice": "Authentic dum biryanis and aromatic pulao.",
    "Sides & Drinks": "Traditional teas, fresh sodas, and accompaniments."
}

DISHES_DATA = [
    # Coffee
    {
        "category": "Coffee",
        "name": "Americano Coffee",
        "short_desc": "Double-shot espresso diluted with hot filtered water, rich crema.",
        "price": 140.00,
        "prep": 5,
        "diet": "VEGAN",
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80"
    },
    {
        "category": "Coffee",
        "name": "Cappuccino",
        "short_desc": "Balanced shot of rich espresso topped with textured microfoam and cocoa dust.",
        "price": 180.00,
        "prep": 7,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800&q=80"
    },
    {
        "category": "Coffee",
        "name": "Latte Coffee",
        "short_desc": "Smooth espresso gently lifted with steamed whole milk and artisan latte art.",
        "price": 190.00,
        "prep": 7,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=800&q=80"
    },
    {
        "category": "Coffee",
        "name": "Cold Coffee",
        "short_desc": "Chilled espresso blended with whole cream milk and vanilla bean reduction.",
        "price": 210.00,
        "prep": 6,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=800&q=80"
    },
    # Seafood
    {
        "category": "Seafood",
        "name": "Fish Fried",
        "short_desc": "Crispy golden trout fillet coated in spiced gram flour with mint chutney.",
        "price": 340.00,
        "prep": 18,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80"
    },
    {
        "category": "Seafood",
        "name": "Fish Tandoori",
        "short_desc": "Marinated fish fillets roasted in clay tandoor with Kashmiri deggi mirch.",
        "price": 380.00,
        "prep": 22,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80"
    },
    {
        "category": "Seafood",
        "name": "Fish Kanti",
        "short_desc": "Kashmiri style pan-tossed boneless fish chunks with sliced onions and tomatoes.",
        "price": 390.00,
        "prep": 20,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&q=80"
    },
    # Grills & BBQ
    {
        "category": "Grills & BBQ",
        "name": "Kabab Kanti",
        "short_desc": "Tender spiced seekh kababs stir-fried on high flame with charred chilies and onion.",
        "price": 360.00,
        "prep": 18,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=800&q=80"
    },
    {
        "category": "Grills & BBQ",
        "name": "Tandoori Chicken",
        "short_desc": "Half spring chicken steeped in hung curd, ginger garlic, and chargrilled over coal.",
        "price": 380.00,
        "prep": 25,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=800&q=80"
    },
    {
        "category": "Grills & BBQ",
        "name": "Chicken Barbeque",
        "short_desc": "Skewered chicken breast basted in smoky artisanal honey-chili glaze.",
        "price": 420.00,
        "prep": 22,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80"
    },
    {
        "category": "Grills & BBQ",
        "name": "Paneer Tikka",
        "short_desc": "Charred cottage cheese cubes marinated in tandoori yogurt with bell peppers.",
        "price": 280.00,
        "prep": 15,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800&q=80"
    },
    # Fast Food
    {
        "category": "Fast Food",
        "name": "Truffle Grilled Cheese Sandwich",
        "short_desc": "Toasted country sourdough with melted cheddar, gouda, and truffle butter.",
        "price": 240.00,
        "prep": 12,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800&q=80"
    },
    {
        "category": "Fast Food",
        "name": "Crispy Chicken Burger",
        "short_desc": "Buttermilk fried chicken breast, brioche bun, house spicy slaw, and gherkins.",
        "price": 260.00,
        "prep": 15,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80"
    },
    {
        "category": "Fast Food",
        "name": "Peri Peri French Fries",
        "short_desc": "Golden skin-on potato fries dusted with house peri-peri seasoning.",
        "price": 140.00,
        "prep": 10,
        "diet": "VEGAN",
        "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=800&q=80"
    },
    # Desserts
    {
        "category": "Desserts",
        "name": "Hot Chocolate Fudge",
        "short_desc": "Warm dark chocolate fudge poured over vanilla gelato and toasted walnuts.",
        "price": 220.00,
        "prep": 8,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&q=80"
    },
    {
        "category": "Desserts",
        "name": "Red Velvet Cupcake",
        "short_desc": "Moist cocoa crumb cupcake crowned with cream cheese frosting and raspberry dust.",
        "price": 120.00,
        "prep": 5,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1587668178277-295251f900ce?w=800&q=80"
    },
    {
        "category": "Desserts",
        "name": "Fudgy Walnut Brownie",
        "short_desc": "70% dark Belgian chocolate brownie with roasted walnuts and salted caramel.",
        "price": 160.00,
        "prep": 5,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800&q=80"
    },
    # Biryani & Rice
    {
        "category": "Biryani & Rice",
        "name": "Chicken Biryani",
        "short_desc": "Fragrant long-grain aged basmati dum-cooked with tender chicken and saffron.",
        "price": 320.00,
        "prep": 25,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80"
    },
    {
        "category": "Biryani & Rice",
        "name": "Muradabadi Biryani",
        "short_desc": "Subtle, whole-spice infused Muradabadi yakhni pulao served with red chili chutney.",
        "price": 340.00,
        "prep": 25,
        "diet": "NON_VEG",
        "image_url": "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=800&q=80"
    },
    # Sides & Drinks
    {
        "category": "Sides & Drinks",
        "name": "Masala Chai",
        "short_desc": "Assam tea slow-brewed with fresh green cardamom, ginger, and buffalo milk.",
        "price": 80.00,
        "prep": 6,
        "diet": "VEG",
        "image_url": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=800&q=80"
    }
]

def run_seed():
    print("Seeding Caffiestaan Menu and downloading media images...")

    # 1. Populate Categories
    for cat_name, desc in CATEGORIES.items():
        cat_obj, created = MenuCategory.objects.get_or_create(
            name=cat_name,
            defaults={"description": desc, "is_active": True}
        )
        if created:
            print(f"Created Category: {cat_name}")

    # Browser header to prevent Unsplash CDN 403 request blocks
    headers = {'User-Agent': 'Mozilla/5.0'}

    # 2. Populate Dishes and Attach Images
    for item in DISHES_DATA:
        category = MenuCategory.objects.get(name=item["category"])
        dish, created = Dish.objects.get_or_create(
            name=item["name"],
            defaults={
                "category": category,
                "short_description": item["short_desc"],
                "base_price": item["price"],
                "preparation_time": item["prep"],
                "dietary_type": item["diet"],
                "is_available": True,
                "is_featured": True
            }
        )
        if created:
            print(f"Created Dish: {dish.name}")

        # Download and link DishImage if not already attached
        if not dish.images.exists():
            image_url = item.get("image_url")
            if image_url:
                try:
                    req = urllib.request.Request(image_url, headers=headers)
                    with urllib.request.urlopen(req) as resp:
                        image_data = resp.read()

                    filename = f"{slugify(dish.name)}.jpg"
                    dish_image = DishImage(
                        dish=dish,
                        alt_text=f"{dish.name} photo",
                        is_primary=True
                    )
                    dish_image.image.save(filename, ContentFile(image_data), save=True)
                    print(f"  --> Attached image for {dish.name}")
                except Exception as e:
                    print(f"  [!] Failed to download image for {dish.name}: {e}")

    print("\nMenu seeding & image sync completed!")

if __name__ == "__main__":
    run_seed()