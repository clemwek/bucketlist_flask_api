from flask_api.flask_api import db
from flask_api.models.bucketlist.bucketlist import Bucketlist


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.String())
    bucket_id = db.Column(db.Integer(), db.ForeignKey('bucket.id'))


    def __init__(self, bucket_id, name, desciption, date):
        self.bucket_id = bucket_id
        self.name = name
        self.desciption = desciption
        self.date = date

    def __repr__(self):
        return '<Item {}, to be completed on {}.>'.format(self.name, self.date)
