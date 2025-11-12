mongo = PyMongo()

class Sensore:
    @staticmethod
    def get_all():
        return list(mongo.db.sensori.find())

    @staticmethod
    def get_by_id(sensore_id):
        return mongo.db.sensori.find_one({"_id": ObjectId(sensore_id)})

    @staticmethod
    def add(dati):
        dati["timestamp"] = datetime.utcnow()
        return mongo.db.sensori.insert_one(dati)

    @staticmethod
    def update(sensore_id, dati):
        return mongo.db.sensori.update_one({"_id": ObjectId(sensore_id)}, {"$set": dati})

    @staticmethod
    def delete(sensore_id):
        return mongo.db.sensori.delete_one({"_id": ObjectId(sensore_id)})

class Attuatore:
    @staticmethod
    def get_all():
        return list(mongo.db.attuatori.find())

    @staticmethod
    def get_by_id(attuatore_id):
        return mongo.db.attuatori.find_one({"_id": ObjectId(attuatore_id)})

    @staticmethod
    def add(dati):
        dati["timestamp"] = datetime.utcnow()
        return mongo.db.attuatori.insert_one(dati)

    @staticmethod
    def update(attuatore_id, dati):
        return mongo.db.attuatori.update_one({"_id": ObjectId(attuatore_id)}, {"$set": dati})

    @staticmethod
    def delete(attuatore_id):
        return mongo.db.attuatori.delete_one({"_id": ObjectId(attuatore_id)})
