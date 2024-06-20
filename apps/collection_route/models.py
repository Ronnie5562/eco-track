from apps import db


class CollectionRoute(db.Model):
    __tablename__ = 'collection_routes'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    name = db.Column(db.String(128), nullable=False)
    area = db.Column(db.String(128), nullable=False)
    schedule = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    service = db.relationship('Users', backref='collection_routes')
