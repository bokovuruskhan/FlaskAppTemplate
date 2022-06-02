from werkzeug.security import generate_password_hash, check_password_hash

from config import MyApp
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin

database = MyApp.database


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), unique=True, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def find_by_username(username):
        return database.session.query(User).filter(User.username == username).first()


class Parent(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    children = database.relationship("Children",
                                     backref=database.backref("parent", lazy=True))

    def __str__(self):
        return self.name


class Children(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    parent_id = database.Column(database.Integer, database.ForeignKey('parent.id'), nullable=True)

    def __str__(self):
        return self.name


def save(obj):
    try:
        database.session.add(obj)
        database.session.commit()
    except SQLAlchemyError:
        database.session.rollback()


def get_all(obj_class):
    return database.session.query(obj_class).all()


def find_by_id(obj_class, obj_id):
    return database.session.query(obj_class).filter(obj_class.id == obj_id).first()
