from flask_api.flask_api import db
from flask_api.models.Bucketlist.Bucketlist import Bucketlist


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    buckets = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return '<User: {} with username {} and email {}>'.format(self.name, self.username, self.email)
