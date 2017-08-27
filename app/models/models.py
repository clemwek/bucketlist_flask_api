import os
import datetime
import jwt
from flask import jsonify
from passlib.hash import pbkdf2_sha512

from app import db


class User(db.Model):
    """This class represents the users table."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String(250))
    buckets = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        """initialize with username, email, password."""
        self.username = username
        self.email = email
        self.password_hash = ''

    def hash_password(self, password):
        self.password_hash = pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def gen_token(self):
        token = jwt.encode({
            'id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, os.getenv('SECRET'))
        return token.decode('UTF-8')

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self, message, status_code):
        return jsonify({
            'token': self.gen_token(),
            'message': message,
            'username': self.username,
            'email': self.email
        }), status_code

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
        """Saves to the database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """gets all bucketlist for a user"""
        return Bucketlist.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_id(user_id, bucket_id):
        """Gets buckelist for an id"""
        return Bucketlist.query.filter_by(user_id=user_id, id=bucket_id).first()

    def delete(self):
        """Deletes a buckelist from the database"""
        db.session.delete(self)
        db.session.commit()

    def serialize(self, message, status_code):
        """This returns a json with status_code and message"""
        return jsonify({
            'message': message,
            'id': self.id,
            'name': self.name
        }), status_code

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
        """Saves to the database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(bucket_id):
        """gets all items from the database"""
        return Item.query.filter_by(bucket_id=bucket_id).all()

    @staticmethod
    def get_by_id(bucket_id, id):
        """Gets an item by id"""
        return Item.query.filter_by(bucket_id=bucket_id, id=id).first()

    def serialize(self, message, status_code):
        """This returns a json with status_code and message"""
        return jsonify({
            'message': message,
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'descrition': self.description
        }), status_code

    def delete(self):
        """Delets from the database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Items: {}>".format(self.name)
