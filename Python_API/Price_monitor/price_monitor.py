import os
import requests
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# Configurazione email (per notifiche)
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'
TO_EMAIL = 'recipient_email@example.com'

# Configurazione prodotto
PRODUCT_NAME = 'iPhone 15'
AMAZON_API_URL = 'https://api.amazon.com/products'  # Sostituisci con l'URL corretto
EBAY_API_URL = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
OUTPUT_FILE = f"prezzi_{PRODUCT_NAME.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"

def get_price_amazon(product_name):
    # Implementare l'integrazione con Amazon API
    response = requests.get(f'{AMAZON_API_URL}?query={product_name}')
    if response.status_code == 200:
        # Elaborare la risposta per ottenere il prezzo
        price = response.json()['price']
        return price
    return None

def get_price_ebay(product_name):
    # Implementare l'integrazione con eBay API
    response = requests.get(f'{EBAY_API_URL}?q={product_name}')
    if response.status_code == 200:
        price = response.json()['itemSummaries'][0]['price']['value']
        return float(price)
    return None

def notify_price_drop(old_price, new_price):
    if new_price < old_price * 0.90:  # Se il nuovo prezzo è sceso del 10%
        message = f"Il prezzo è sceso da {old_price} a {new_price}!"
        send_email_notification(message)

def send_email_notification(message):
    msg = MIMEText(message)
    msg['Subject'] = 'Notifica di Variazione Prezzo'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def record_price(price):
    if os.path.exists(OUTPUT_FILE):
        df = pd.read_csv(OUTPUT_FILE)
    else:
        df = pd.DataFrame(columns=['Date', 'Price'])
    
    today = datetime.now().date()
    df = df.append({'Date': today, 'Price': price}, ignore_index=True)
    df.to_csv(OUTPUT_FILE, index=False)

def main():
    price_amazon = get_price_amazon(PRODUCT_NAME)
    price_ebay = get_price_ebay(PRODUCT_NAME)

    if price_amazon is not None:
        record_price(price_amazon)
        print(f"Prezzo Amazon: {price_amazon}")
    if price_ebay is not None:
        record_price(price_ebay)
        print(f"Prezzo eBay: {price_ebay}")

    # Controlla se c'è un prezzo precedente per notifiche
    if os.path.exists(OUTPUT_FILE):
        last_price = pd.read_csv(OUTPUT_FILE).iloc[-1]['Price']
        notify_price_drop(last_price, price_amazon if price_amazon else price_ebay)

if __name__ == "__main__":
    main()
