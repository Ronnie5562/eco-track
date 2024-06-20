import enum
from flask_login import UserMixin
from sqlalchemy import Enum
from apps import db, login_manager
from apps.authentication.util import hash_pass


class RoleEnum(enum.Enum):
    user = "user"
    wc_service = "wc_service"
    admin = "admin"


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    # Authentication Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    # Profile Fields
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(32), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)

    # Role Field with Choices
    role = db.Column(Enum(RoleEnum), nullable=False, default=RoleEnum.user)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass(value)
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def __str__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
