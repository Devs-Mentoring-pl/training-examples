from flask import Blueprint, request, jsonify
from . import db
from .models import Trainings, TrainingSchema

# Schematy Marshmallow
training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)


def add_to_db(record):
    """Dodaje rekord do bazy i zatwierdza transakcję."""
    db.session.add(record)
    db.session.commit()


# --- Blueprinty ---

add_training_blueprint = Blueprint('add_training', __name__)
get_trainings_blueprint = Blueprint('get_trainings', __name__)
get_training_by_id_blueprint = Blueprint('get_training_by_id', __name__)
update_training_blueprint = Blueprint('update_training', __name__)
delete_training_blueprint = Blueprint('delete_training', __name__)


# --- 1. POST /training – Dodanie nowego treningu ---

@add_training_blueprint.route('/training', methods=['POST'])
def add_training():
    body = request.json

    if not body or 'name' not in body or 'duration' not in body:
        return jsonify({"error": "Wymagane pola: name, duration"}), 400

    new_training = Trainings.create_from_json(json_body=body)
    add_to_db(new_training)

    return training_schema.jsonify(new_training), 201


# --- 2. GET /trainings – Pobranie wszystkich treningów ---

@get_trainings_blueprint.route('/trainings', methods=['GET'])
def get_trainings():
    all_trainings = Trainings.query.all()
    return trainings_schema.jsonify(all_trainings)


# --- 3. GET /training/<id> – Pobranie treningu po ID ---

@get_training_by_id_blueprint.route('/training/<int:training_id>', methods=['GET'])
def get_training_by_id(training_id):
    training = db.session.get(Trainings, training_id)

    if training is None:
        return jsonify({"error": "Trening nie znaleziony"}), 404

    return training_schema.jsonify(training)


# --- 4. PUT /training/<id> – Aktualizacja treningu ---

@update_training_blueprint.route('/training/<int:training_id>', methods=['PUT'])
def update_training(training_id):
    training = db.session.get(Trainings, training_id)

    if training is None:
        return jsonify({"error": "Trening nie znaleziony"}), 404

    body = request.json

    if not body or 'name' not in body or 'duration' not in body:
        return jsonify({"error": "Wymagane pola: name, duration"}), 400

    modified_training = Trainings.create_from_json(json_body=body)
    training.update(modified_training)
    db.session.commit()

    return training_schema.jsonify(training)


# --- 5. DELETE /training/<id> – Usunięcie treningu ---

@delete_training_blueprint.route('/training/<int:training_id>', methods=['DELETE'])
def delete_training(training_id):
    training = db.session.get(Trainings, training_id)

    if training is None:
        return jsonify({"error": "Trening nie znaleziony"}), 404

    db.session.delete(training)
    db.session.commit()

    return '', 204
