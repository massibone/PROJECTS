import requests
import pandas as pd
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurazione
CRYPTO_IDS = ["bitcoin", "ethereum", "solana"]  # Aggiungi altre cripto se vuoi
THRESHOLDS = {"bitcoin": 30000, "ethereum": 2000, "solana": 50}  # Soglie per alert
EMAIL_ENABLED = False  # Imposta a True per abilitare le email
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "tua@email.com"
SMTP_PASSWORD = "tua_password"
EMAIL_TO = "destinatario@email.com"

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cripto_monitor.log'),
        logging.StreamHandler()
    ]
)

def fetch_crypto_prices():
    """Recupera i prezzi delle criptovalute da CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(CRYPTO_IDS),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Errore nel recupero dei dati: {e}")
        return None

def save_to_csv(data, filename):
    """Salva i dati in un file CSV."""
    if not data:
        return False
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.reset_index().rename(columns={'index': 'crypto'})
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.to_csv(filename, index=False)
    logging.info(f"Dati salvati in {filename}")
    return True

def check_thresholds(data):
    """Controlla se i prezzi sono sotto soglia e invia alert."""
    alerts = []
    for crypto, price_data in data.items():
        current_price = price_data['usd']
        threshold = THRESHOLDS.get(crypto)
        if threshold and current_price < threshold:
            alerts.append(f"{crypto}: {current_price} USD (sotto soglia di {threshold} USD)")
    return alerts

def send_email_alert(alerts):
    """Invia un'email di alert."""
    if not EMAIL_ENABLED or not alerts:
        return
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = "Alert Prezzo Criptovalute"
    body = "Attenzione, i seguenti prezzi sono sotto soglia:\n\n" + "\n".join(alerts)
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        logging.info("Email di alert inviata")
    except Exception as e:
        logging.error(f"Errore nell'invio email: {e}")

def main():
    data = fetch_crypto_prices()
    if not data:
        return
    filename = f"cripto_prezzi_{datetime.now().strftime('%Y%m%d')}.csv"
    if save_to_csv(data, filename):
        alerts = check_thresholds(data)
        if alerts:
            logging.warning("Prezzi sotto soglia: " + ", ".join(alerts))
            send_email_alert(alerts)

if __name__ == "__main__":
    main()
