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

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'publication_date': book.publication_date.isoformat(),
            'isbn': book.isbn
        } for book in books
    ])


@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date(),
        isbn=data['isbn']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publication_date': book.publication_date.isoformat(),
        'isbn': book.isbn
    })


@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.json
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    if 'publication_date' in data:
        book.publication_date = datetime.strptime(data['publication_date'], '%Y-%m-%d').date()
    book.isbn = data.get('isbn', book.isbn)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
