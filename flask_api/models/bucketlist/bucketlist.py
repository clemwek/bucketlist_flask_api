from flask_api.flask_api import db


class Bucketlist(db.Model):
    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<bucketlist {}.>'.format(self.name)
