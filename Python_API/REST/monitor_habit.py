'''
API per il monitoraggio delle abitudini: Un'API che permette agli utenti di tracciare le proprie abitudini quotidiane, settimanali o mensili.
API Endpoints

GET /habits: restituisce l'elenco delle abitudini dell'utente
POST /habits: crea una nuova abitudine
GET /habits/{id}: restituisce i dettagli di un'abitudine specifica
PUT /habits/{id}: aggiorna un'abitudine esistente
DELETE /habits/{id}: elimina un'abitudine
GET /habits/{id}/logs: restituisce i log delle attività relative a un'abitudine specifica
POST /habits/{id}/logs: registra una nuova attività per un'abitudine specifica
'''


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
db = SQLAlchemy(app)

class Habits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    frequency = db.Column(db.String(50), nullable=False)  # quotidiana, settimanale, mensile

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(200), nullable=True)

@app.route("/habits", methods=["GET"])
def get_habits():
    habits = Habits.query.all()
    return jsonify([{"id": h.id, "name": h.name, "description": h.description, "frequency": h.frequency} for h in habits])

@app.route("/habits", methods=["POST"])
def create_habit():
    data = request.get_json()
    habit = Habits(name=data["name"], description=data["description"], frequency=data["frequency"])
    db.session.add(habit)
    db.session.commit()
    return jsonify({"id": habit.id, "name": habit.name, "description": habit.description, "frequency": habit.frequency})

@app.route("/habits/<int:habit_id>", methods=["GET"])
def get_habit(habit_id):
    habit = Habits.query.get(habit_id)
    if habit is None:
        return jsonify({"error": "Abitudine non trovata"}), 404
    return jsonify({"id": habit.id, "name": habit.name, "description": habit.description, "frequency": habit.frequency})

@app.route("/habits/<int:habit_id>/logs", methods=["GET"])
def get_logs(habit_id):
    logs = Logs.query.filter_by(habit_id=habit_id).all()
    return jsonify([{"id": l.id, "date": l.date, "notes": l.notes} for l in logs])

@app.route("/habits/<int:habit_id>/logs", methods=["POST"])
def create_log(habit_id):
    data = request.get_json()
    log = Logs(habit_id=habit_id, date=data["date"], notes=data["notes"])
    db.session.add(log)
    db.session.commit()
    return jsonify({"id": log.id, "date": log.date, "notes": log.notes})

if __name__ == "__main__":
    app.run(debug=True)
