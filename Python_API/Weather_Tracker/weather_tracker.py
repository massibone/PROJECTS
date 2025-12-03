import requests
import csv
import datetime
import os

# Configurazione
API_KEY = "INSERISCI_LA_TUA_API_KEY"  # Ottieni la tua API key da https://openweathermap.org/api
CITY = "Firenze"                      # Puoi cambiare con "Roma", "Milano", ecc.
UNITS = "metric"                      # metric = °C, imperial = °F
LANG = "it"                           # lingua italiana

# URL per le previsioni a 5 giorni/3 ore
url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANG}"

# Richiesta all'API
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Errore API: {response.status_code}, {response.text}")

data = response.json()

# Nome file CSV giornaliero
today = datetime.datetime.now().strftime("%Y%m%d")
filename = f"meteo_{CITY.lower()}_{today}.csv"

# Scrittura CSV
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["datetime", "temperature_C", "humidity_%", "conditions"])

    rain_alert = False

    for forecast in data["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        humidity = forecast["main"]["humidity"]
        conditions = forecast["weather"][0]["description"]

        writer.writerow([dt_txt, temp, humidity, conditions])

        # Controllo pioggia nelle prossime 24 ore
        if "pioggia" in conditions.lower() or "rain" in conditions.lower():
            rain_alert = True

# Alert pioggia
if rain_alert:
    print(f"⚠️ Attenzione: è prevista pioggia nelle prossime 24 ore a {CITY}!")
else:
    print(f"✅ Nessuna pioggia prevista nelle prossime 24 ore a {CITY}.")

print(f"Dati salvati in: {filename}")


