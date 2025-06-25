import requests
from bs4 import BeautifulSoup
import time
import telebot
from flask import Flask
from threading import Thread

# CONFIGURATION
URL = "https://www.mobile.bg/obiavi/avtomobili-dzhipove/opel/astra/dizelov/ot-2018/do-2021?price1=7350&currency=EUR&km=150000"
TELEGRAM_TOKEN = "8140801114:AAG57jEzy0T4-GzRk3jtV2xFgpbyEq7Wu2g"
chat_id = -4939922320

bot = telebot.TeleBot(TELEGRAM_TOKEN)
seen_ads = set()

def check_new_listings():
    global seen_ads
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.select("div.listing a.lnk")
    new_ads = []
    for link in listings:
        href = link.get("href")
        title = link.get_text(strip=True)
        if href and href.startswith("/obiava"):
            full_url = "https://www.mobile.bg" + href
            if full_url not in seen_ads:
                seen_ads.add(full_url)
                new_ads.append((title, full_url))
    for title, url in new_ads:
        msg = f"🚗 <b>New Opel Astra Listing</b>\n<a href=\"{url}\">{title}</a>"
        bot.send_message(CHAT_ID, msg, parse_mode="HTML")

def start_scraper():
    print("🚀 Opel Astra monitor started...")
    while True:
        try:
            check_new_listings()
            print("✅ Checked for new listings.")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(60)

# Flask server for uptime robot
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=start_scraper).start()
Thread(target=run_web).start()
