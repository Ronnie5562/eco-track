from apps import db


class RecyclingTracker(db.Model):
    __tablename__ = 'recycling_trackers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    service_id = db.Column(
        db.Integer, db.ForeignKey('Users.id'), nullable=False)
    waste_type_id = db.Column(db.Integer, db.ForeignKey('waste_types.id'), nullable=False)
    date_collected = db.Column(db.DateTime, nullable=False)
    # Weight of the recycled material in kilograms
    weight = db.Column(db.Float, nullable=False)

    user = db.relationship('Users', foreign_keys=[user_id])
    service = db.relationship('Users', foreign_keys=[service_id])
    waste_type = db.relationship('WasteType')
