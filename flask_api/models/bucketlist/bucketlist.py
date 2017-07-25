from flask_api.flask_api import db
from flask_api.models.items.items import Item
from flask_api.models.users.user import User



class Bucketlist(db.Model):
    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='bucket', lazy='dynamic', cascade=('all', 'delete-orphan'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<bucketlist {}.>'.format(self.name)
