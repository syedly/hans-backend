import time
import django
import os
import requests
import dotenv

dotenv.load_dotenv()

purchase_url = os.getenv('API_FETCH_URL_PURCHASE')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hans.settings")
django.setup()

from app.models import Purchase


def fetch_api_data():
    url = purchase_url
    response = requests.get(url)

    if response.status_code != 200:
        print("API failed")
        return

    data = response.json()

    for item in data:
        Purchase.objects.update_or_create(
            external_id=item["id"],
            defaults={

                # --- Purchase Fields ---
                "purchase_date": item["purchase_date"],
                "purchase_month": item["purchase_month"],
                "purchase_year": item["purchase_year"],
                "province": item.get("province", ""),
                "contact": item.get("contact", ""),
                "status": item.get("status", "pending"),
                "last_digits": item.get("last_digits", ""),
                "shipping_address": item.get("shipping_address", ""),

                # --- User Fields ---
                "user_id": item["user_id"],
                "user_username": item["user_username"],
                "user_first_name": item["user_first_name"],
                "user_last_name": item["user_last_name"],
                "user_email": item["user_email"],

                # --- Product Fields ---
                "product_id": item["product_id"],
                "product_name": item["product_name"],
                "product_description": item.get("product_description", ""),
                "product_price": item["product_price"],
                "product_discounted_price": item["product_discounted_price"],
                "product_is_available": item["product_is_available"],
                "product_status": item.get("product_status", ""),
                "product_category": item.get("product_category", ""),
                "product_sku": item.get("product_sku", ""),
                "product_stock": item.get("product_stock", ""),
                "product_image_url": item.get("product_image_url", None),
            }
        )

    print("Fetched one cycle!")


while True:
    fetch_api_data()
    print("Waiting 2 minutes...\n")
    time.sleep(120)

#send mail method
# import time
# import os
# import requests
# import django
# from dotenv import load_dotenv

# load_dotenv()

# purchase_url = os.getenv('API_FETCH_URL_PURCHASE')

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hans.settings")
# django.setup()

# from django.core.mail import send_mail
# from django.conf import settings
# from app.models import Purchase

# # List to collect changes in this cycle
# updated_or_created = []

# def fetch_api_data():
#     global updated_or_created
#     updated_or_created = []  # Reset every cycle

#     try:
#         response = requests.get(purchase_url, timeout=30)
#         response.raise_for_status()
#     except Exception as e:
#         print(f"API failed: {e}")
#         return

#     data = response.json()
#     new_count = 0
#     updated_count = 0

#     for item in data:
#         external_id = item["id"]
#         obj, created = Purchase.objects.update_or_create(
#             external_id=external_id,
#             defaults={
#                 "purchase_date": item["purchase_date"],
#                 "purchase_month": item["purchase_month"],
#                 "purchase_year": item["purchase_year"],
#                 "user_email": item["user__email"],
#                 "user_username": item["user__username"],
#                 "product_name": item["product__name"],
#                 "product_price": item["product__price"],
#                 "product_image_url": item["product__image_url"],
#             }
#         )

#         status = "NEW" if created else "UPDATED"
#         if created:
#             new_count += 1
#         else:
#             updated_count += 1

#         updated_or_created.append({
#             "id": external_id,
#             "status": status,
#             "customer": item["user__username"] or item["user__email"],
#             "product": item["product__name"],
#             "price": item["product__price"],
#             "date": item["purchase_date"],
#         })

#     print(f"Fetched {len(data)} items → {new_count} new, {updated_count} updated")

#     # SEND EMAIL ONLY IF SOMETHING CHANGED
#     if updated_or_created:
#         send_summary_email(new_count, updated_count)

# def send_summary_email(new_count, updated_count):
#     subject = f"New Purchases Alert – {new_count} New, {updated_count} Updated"
    
#     body = f"""
# Hi team,

# Your Order Management System just synced new data!

# Summary:
# • New purchases   : {new_count}
# • Updated purchases: {updated_count}
# • Total synced     : {len(updated_or_created)}
# • Time             : {time.strftime("%Y-%m-%d %H:%M:%S")}

# Details:
# """
#     for entry in updated_or_created:
#         body += f"\n• [{entry['status']}] Order #{entry['id']} | {entry['customer']} bought {entry['product']} (${entry['price']}) on {entry['date']}"

#     body += "\n\nRegards,\nYour Auto Sync Bot 🤖"

#     send_mail(
#         subject=subject,
#         message=body,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=["you@example.com", "team@company.com"],  # CHANGE THESE EMAILS
#         fail_silently=False,
#     )
#     print("Email sent successfully!")

# # MAIN LOOP – Runs forever every 2 minutes
# print("Purchase sync bot started! Running every 2 minutes...")
# while True:
#     fetch_api_data()
#     print("Waiting 2 minutes before next sync...\n")
#     time.sleep(120)  # 120 seconds = 2 minutes
    