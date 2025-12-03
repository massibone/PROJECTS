# Weather Tracker

Script Python per tracciare le condizioni meteo di una città usando l'API di OpenWeatherMap.

## Funzionalità
- Recupera previsioni meteo (temperatura, umidità, condizioni).
- Salva i dati in un CSV giornaliero (`meteo_<città>_YYYYMMDD.csv`).
- Invia un alert se è prevista pioggia nelle prossime 24 ore.

## Uso
1. Ottieni una API key da [OpenWeatherMap](https://openweathermap.org/api).
2. Inserisci la tua API key nello script (`API_KEY`).
3. Esegui:
   ```bash
   python weather_tracker.py

