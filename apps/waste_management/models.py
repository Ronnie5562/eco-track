from apps import db
from flask_login import current_user
from sqlalchemy.orm import validates


class WasteType(db.Model):
    __tablename__ = 'waste_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'<WasteType {self.name}>'

    def __str__(self):
        return self.name
