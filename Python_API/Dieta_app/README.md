API per la gestione di una dieta personalizzata: Un'API che tiene traccia dell'apporto calorico, suggerisce pasti e genera liste della spesa basate sugli obiettivi nutrizionali dell'utente.
/dieta_api/

Tracciare l’apporto calorico giornaliero
Suggerire pasti in base agli obiettivi nutrizionali
Generare liste della spesa automatiche
Utilizzeremo FastAPI (un framework moderno, veloce e facile da usare per creare API in Python) e SQLite per la persistenza dei dati.

/dieta_api/
│
├── main.py          # File principale dell'API
├── models.py        # Modelli dati (Pydantic e SQLAlchemy)
├── database.py      # Configurazione del database
├── crud.py          # Operazioni CRUD sul database
├── schemas.py       # Schemi Pydantic per input/output
└── requirements.txt # Dipendenze

Avvio dell’API

uvicorn main:app --reload
L’API sarà disponibile su http://127.0.0.1:8000. Puoi testare gli endpoint con strumenti come Postman o curl.
