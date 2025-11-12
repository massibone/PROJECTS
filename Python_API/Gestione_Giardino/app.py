from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import mongo, Sensore, Attuatore

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/giardino_intelligente"
mongo.init_app(app)
api = Api(app)

class SensoreResource(Resource):
    def get(self, sensore_id=None):
        if sensore_id:
            sensore = Sensore.get_by_id(sensore_id)
            if sensore:
                sensore["_id"] = str(sensore["_id"])
                return jsonify(sensore)
            return {"message": "Sensore non trovato"}, 404
        else:
            sensori = Sensore.get_all()
            for sensore in sensori:
                sensore["_id"] = str(sensore["_id"])
            return jsonify(sensori)

    def post(self):
        dati = request.get_json()
        result = Sensore.add(dati)
        return {"message": "Sensore aggiunto", "id": str(result.inserted_id)}, 201

    def put(self, sensore_id):
        dati = request.get_json()
        Sensore.update(sensore_id, dati)
        return {"message": "Sensore aggiornato"}

    def delete(self, sensore_id):
        Sensore.delete(sensore_id)
        return {"message": "Sensore eliminato"}

class AttuatoreResource(Resource):
    def get(self, attuatore_id=None):
        if attuatore_id:
            attuatore = Attuatore.get_by_id(attuatore_id)
            if attuatore:
                attuatore["_id"] = str(attuatore["_id"])
                return jsonify(attuatore)
            return {"message": "Attuatore non trovato"}, 404
        else:
            attuatori = Attuatore.get_all()
            for attuatore in attuatori:
                attuatore["_id"] = str(attuatore["_id"])
            return jsonify(attuatori)

    def post(self):
        dati = request.get_json()
        result = Attuatore.add(dati)
        return {"message": "Attuatore aggiunto", "id": str(result.inserted_id)}, 201

    def put(self, attuatore_id):
        dati = request.get_json()
        Attuatore.update(attuatore_id, dati)
        return {"message": "Attuatore aggiornato"}

    def delete(self, attuatore_id):
        Attuatore.delete(attuatore_id)
        return {"message": "Attuatore eliminato"}

api.add_resource(SensoreResource, "/sensori", "/sensori/<string:sensore_id>")
api.add_resource(AttuatoreResource, "/attuatori", "/attuatori/<string:attuatore_id>")

if __name__ == "__main__":
    app.run(debug=True)
