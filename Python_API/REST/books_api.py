'''
API REST per la gestione di una libreria digitale

Questa applicazione Flask fornisce un'API RESTful completa per gestire un catalogo di libri.
Utilizza SQLAlchemy con database SQLite per la persistenza dei dati.

Funzionalità:
- GET /books - Recupera tutti i libri
- GET /books/<id> - Recupera un libro specifico per ID
- POST /books - Aggiunge un nuovo libro
- PUT /books/<id> - Aggiorna un libro esistente
- DELETE /books/<id> - Elimina un libro

Modello dati:
- title: titolo del libro (stringa, obbligatorio)
- author: autore del libro (stringa, obbligatorio)
- publication_date: data di pubblicazione (formato YYYY-MM-DD, obbligatorio)
- isbn: codice ISBN univoco (stringa 13 caratteri, obbligatorio)

Esempio richiesta POST:
{
    "title": "Il Nome della Rosa",
    "author": "Umberto Eco",
    "publication_date": "1980-10-28",
    "isbn": "9788845292613"
}
'''

