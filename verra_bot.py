import requests
import json
import smtplib
import os
from bs4 import BeautifulSoup

API_URL = "https://www.verra.nl/en/realtime-listings/consumer"
CACHE_FILE = "verra_cache.json"

EMAIL = os.environ["BOT_EMAIL"]
PASSWORD = os.environ["BOT_PASSWORD"]
TO_EMAIL = os.environ["BOT_TO"]
TO_EMAIL_2 = os.environ["BOT_TO_2"]

def fetch_ids():
    try:
        data = requests.get(API_URL, timeout=10).json()
    except Exception as e:
        print("ERROR FETCHING JSON:", e)
        return []

    print("DEBUG JSON SAMPLE:", data[:2])   # print first items

    filtered = [
        item for item in data
        if item.get("city") == "Delft"
        and item.get("isRentals") == True
    ]
    
    return filtered

def notify(msg):
    email_text = f"Subject: Verra Bot Alert\n\n{msg}"
    
    recipients = [TO_EMAIL, TO_EMAIL_2]
    recipients = [r for r in recipients if r]
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, recipients, email_text)

try:
    old_ids = json.load(open(CACHE_FILE))

except:
    old_ids = []

new_ids = fetch_ids()
new_item_ids = [item["_id"] for item in new_ids]
added = [item for item in new_ids if item["_id"] not in old_ids]

if added:
    text = "New Verra Makelaars listing in Delft:\n\n"
    for item in added:
        text+= f"- {item.get('address','Unknown address')} (ID : {item['_id']})\n"
    notify(text)

json.dump(new_item_ids, open(CACHE_FILE, "w"))
