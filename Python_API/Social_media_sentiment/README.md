API per l'analisi del sentiment sui social media: Un'API che analizza il sentiment dei post sui social media riguardanti un determinato argomento o marca.

'''
Social Media Sentiment Analysis API
API REST per l'analisi del sentiment di post sui social media

Questa API permette di analizzare il sentiment (positivo, negativo, neutro) di testi
provenienti da social media riguardo a specifici topic, marche o argomenti.

🎯 Funzionalità:
  • Analisi sentiment con polarity score (-1 a +1)
  • Supporto testo italiano e inglese
  • Classificazione: positivo, negativo, neutro
  • Analisi batch di multipli post
  • Statistiche aggregate per topic
  • Rate limiting per protezione API
  • Cache risultati per performance
  • Export risultati in JSON/CSV

📦 Installazione dipendenze:
    pip install flask textblob flask-limiter
    python -m textblob.download_corpora

🚀 Avvio server:
    python sentiment_api.py

🌐 Endpoints disponibili:
    POST   /api/v1/analyze          - Analizza singolo testo
    POST   /api/v1/analyze/batch    - Analizza multipli post
    GET    /api/v1/stats/<topic>    - Statistiche per topic
    GET    /api/v1/health           - Health check
    GET    /                        - Documentazione interattiva

📝 Esempio richiesta:
    curl -X POST http://localhost:5000/api/v1/analyze \
         -H "Content-Type: application/json" \
         -d '{"text": "Adoro Netflix!", "topic": "Netflix"}'

🔑 Note:
    - Polarity: -1 (molto negativo) a +1 (molto positivo)
    - Subjectivity: 0 (oggettivo) a 1 (soggettivo)
    - Per produzione: implementare autenticazione e database

Autore: Social Media Analytics Team
License: MIT
'''
