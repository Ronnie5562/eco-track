import enum
from apps import db
from sqlalchemy import Enum


class ScheduleStatus(enum.Enum):
    scheduled = "scheduled"
    completed = "completed"


class CollectionSchedule(db.Model):
    __tablename__ = 'collection_schedules'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    route_id = db.Column(
        db.Integer,
        db.ForeignKey('collection_routes.id'),
        nullable=False
    )
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        Enum(ScheduleStatus),
        nullable=False,
        default=ScheduleStatus.scheduled
    )

    user = db.relationship('Users', backref='schedules')
    route = db.relationship('CollectionRoute', backref='schedules')

    def __repr__(self):
        return f'<CollectionSchedule id={self.id}, date={self.date}, status={self.status}>'
