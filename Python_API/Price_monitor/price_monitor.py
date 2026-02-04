import os
import requests
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# Configurazione email
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'
TO_EMAIL = 'recipient_email@example.com'

# Configurazione prodotto
PRODUCT_NAME = 'iPhone 15'
AMAZON_API_URL = 'https://api.amazon.com/products'   # placeholder
EBAY_API_URL = 'https://api.ebay.com/buy/browse/v1/item_summary/search'

OUTPUT_FILE = f"prezzi_{PRODUCT_NAME.lower().replace(' ', '_')}.csv"


def get_price_amazon(product_name):
    response = requests.get(f"{AMAZON_API_URL}?query={product_name}")
    if response.status_code == 200:
        return response.json().get('price')
    return None


def get_price_ebay(product_name):
    response = requests.get(f"{EBAY_API_URL}?q={product_name}")
    if response.status_code == 200:
        return float(response.json()['itemSummaries'][0]['price']['value'])
    return None


def send_email_notification(message):
    msg = MIMEText(message)
    msg['Subject'] = 'Notifica variazione prezzo'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def notify_price_drop(old_price, new_price):
    if old_price and new_price and new_price < old_price * 0.9:
        send_email_notification(
            f"Prezzo sceso da {old_price} a {new_price}"
        )


def record_price(price, source):
    row = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'source': source,
        'price': price
    }

    df = pd.read_csv(OUTPUT_FILE) if os.path.exists(OUTPUT_FILE) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(OUTPUT_FILE, index=False)


def main():
    last_price = None
    if os.path.exists(OUTPUT_FILE):
        last_price = pd.read_csv(OUTPUT_FILE).iloc[-1]['price']

    price_amazon = get_price_amazon(PRODUCT_NAME)
    price_ebay = get_price_ebay(PRODUCT_NAME)

    if price_amazon:
        record_price(price_amazon, 'Amazon')
        notify_price_drop(last_price, price_amazon)
        print(f"Prezzo Amazon: {price_amazon}")

    if price_ebay:
        record_price(price_ebay, 'eBay')
        notify_price_drop(last_price, price_ebay)
        print(f"Prezzo eBay: {price_ebay}")


if __name__ == "__main__":
    main()
