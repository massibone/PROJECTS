# Serie A Real-Time Stats
**Estrazione, elaborazione e analisi dei risultati della Serie A tramite API-FOOTBALL.**

## Features
- Estrazione dati in tempo reale da [API-FOOTBALL](https://www.api-football.com/)
- Esportazione in CSV con marcatori, squadre e punteggi
- Calcolo automatico della classifica aggiornata
- Configurazione flessibile via `config.ini`

## Howto
1. Inserisci la tua API key in config.ini
2. Esegui
python main.py --date YYYYMMDD
3. Troverai il CSV in output/risultati_seriea_YYYYMMDD.csv:
| Data | Squadra Casa | Squadra Ospite | Risultato | Marcatori |
| ---        |      --- |   --- | --- |     ---              |
| 2026-04-02 | Juventus | Milan | 2-1 | Gioc1 (J), Gioc2 (M) |


