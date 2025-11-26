import time
import django
import os
import requests
import dotenv

dotenv.load_dotenv()

purchase_url = os.getenv('API_FETCH_URL_PURCHASE')
product_url = os.getenv('API_FETCH_URL_PRODUCT')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hans.settings")
django.setup()

from app.models import Purchase, Product


# ================================
# Fetch & Save Product Data
# ================================
def fetch_product_data():
    response = requests.get(product_url)

    if response.status_code != 200:
        print("Product API failed")
        return

    products = response.json()

    for item in products:
        external_id = item.get("id")

        # Skip if product already exists
        if Product.objects.filter(external_id=external_id).exists():
            print(f"Skipping existing product: {external_id}")
            continue

        Product.objects.create(
            external_id=external_id,
            name=item.get("name", ""),
            description=item.get("description", ""),

            price=item.get("price"),
            discounted_price=item.get("discounted_price"),

            is_available=item.get("is_available", True),
            status=item.get("status", ""),

            category=item.get("category", ""),
            sku=item.get("sku", ""),

            stock=item.get("stock"),
            image=item.get("image"),
        )

        print(f"Added new product: {external_id}")


# ================================
# Fetch & Save Purchase Data
# ================================
def fetch_purchase_data():
    response = requests.get(purchase_url)

    if response.status_code != 200:
        print("Purchase API failed")
        return

    purchases = response.json()

    for item in purchases:
        external_id = item.get("id")

        # Skip if purchase already exists
        if Purchase.objects.filter(external_id=external_id).exists():
            print(f"Skipping existing purchase: {external_id}")
            continue

        user = item.get("user", {})
        product = item.get("product", {})

        Purchase.objects.create(
            external_id=external_id,

            purchase_date=item.get("purchase_date"),
            purchase_month=item.get("purchase_month"),
            purchase_year=item.get("purchase_year"),

            province=item.get("province", ""),
            contact=item.get("contact", ""),
            status=item.get("status", "pending"),
            last_digits=item.get("last_digits", ""),
            shipping_address=item.get("shipping_address", ""),

            user_id=user.get("id"),
            user_username=user.get("username", ""),
            user_first_name=user.get("first_name", ""),
            user_last_name=user.get("last_name", ""),
            user_email=user.get("email", ""),

            product_id=product.get("id"),
            product_name=product.get("name", ""),
            product_description=product.get("description", ""),
            product_price=product.get("price"),
            product_discounted_price=product.get("discounted_price"),
            product_is_available=product.get("is_available", True),
            product_status=product.get("status", ""),
            product_category=product.get("category", ""),
            product_sku=product.get("sku", ""),
            product_stock=product.get("stock", ""),
            product_image_url=product.get("image_url", None),
        )

        print(f"Added new purchase: {external_id}")


# ================================
# Main Loop
# ================================
while True:
    print("\n=== Fetching Products ===")
    fetch_product_data()

    print("\n=== Fetching Purchases ===")
    fetch_purchase_data()

    print("Waiting 2 minutes...\n")
    time.sleep(120)
