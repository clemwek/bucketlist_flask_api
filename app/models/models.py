import os
import datetime
import bcrypt
import jwt
from passlib.apps import custom_app_context as pwd_context

from app import db


class User(db.Model):
    """This class represents the users table."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    buckets = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        """initialize with username, email, password."""
        self.username = username
        self.email = email

    def hash_password(password):
        self.password_hash = bcrypt.hashpw(password,  bcrypt.gensalt())

    def verify_password(password, password_hash):
        return  bcrypt.checkpw(password, password_hash)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}, with email: {}.>".format(self.username, self.email)


class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='bucket', lazy='dynamic',
                            cascade=('all', 'delete-orphan'))

    def __init__(self, name, user_id):
        """initialize with name."""
        self.name = name
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

class Item(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.String())
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, name, description, date, bucket_id):
        """initialize with name."""
        self.name = name
        self.description = description
        self.date = date
        self.bucket_id = bucket_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Items: {}>".format(self.name)
