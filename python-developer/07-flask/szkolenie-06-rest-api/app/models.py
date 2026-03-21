from datetime import datetime, timezone

from . import db, ma
from marshmallow import fields


class Trainings(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(length=5000), nullable=True)

    def __init__(self, name, date, duration, note):
        self.name = name
        self.date = date
        self.duration = duration
        self.note = note

    def update(self, modified_training):
        """Aktualizuje trening danymi z innego obiektu Trainings."""
        self.name = modified_training.name
        self.date = modified_training.date
        self.duration = modified_training.duration
        self.note = modified_training.note

    @staticmethod
    def create_from_json(json_body):
        """Tworzy obiekt Trainings z danych JSON."""
        if 'date' not in json_body:
            date = datetime.now(timezone.utc)
        else:
            date = datetime.strptime(json_body['date'], '%d/%m/%y')

        return Trainings(
            name=json_body['name'],
            date=date,
            duration=json_body['duration'],
            note=json_body.get('note'),
        )


class TrainingSchema(ma.Schema):
    """Schemat Marshmallow do serializacji treningów."""
    _id = fields.Integer()
    name = fields.Str()
    date = fields.DateTime(format='%d-%m-%y')
    duration = fields.Integer()
    note = fields.Str()
