from app import db


# class Base(db.Model):
#     def __init__(self, name):
#         """initialize with name."""
#         self.name = name

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     @staticmethod
#     def get_all():
#         return Bucketlist.query.all()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def __repr__(self):
#         pass

class User(db.Model):
    """This class represents the users table."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    buckets = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, name, username, email, password):
        """initialize with name, username, email, password."""
        self.name = name
        self.username = username
        self.email = email
        self.password = password

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
        return "<User: {}, with email: {}.>".format(self.name, self.email)


class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='bucket', lazy='dynamic', cascade=('all', 'delete-orphan'))


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
    bucket_id = db.Column(db.Integer(), db.ForeignKey('bucket.id'))
    name = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.String())
    bucket_id = db.Column(db.Integer(), db.ForeignKey('bucket.id'))

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





# from flask_api import db


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     username = db.Column(db.String(), unique=True)
#     email = db.Column(db.String(), unique=True)
#     password = db.Column(db.String())
#     buckets = db.relationship('Bucketlist', backref='user', lazy='dynamic')

#     def __init__(self, name, username, email, password):
#         self.name = name
#         self.username = username
#         self.email = email
#         self.password = password

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()


#     def __repr__(self):
#         return '<User: {} with username {} and email {}>'.format(self.name, self.username, self.email)


# class Bucketlist(db.Model):
#     __tablename__ = 'bucketlist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
#     items = db.relationship('Item', backref='bucket', lazy='dynamic', cascade=('all', 'delete-orphan'))

#     def __init__(self, name):
#         self.name = name

#     def __repr__(self):
#         return '<bucketlist {}.>'.format(self.name)


# class Item(db.Model):
#     __tablename__ = 'items'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     description = db.Column(db.String())
#     date = db.Column(db.String())
#     bucket_id = db.Column(db.Integer(), db.ForeignKey('bucket.id'))


#     def __init__(self, bucket_id, name, desciption, date):
#         self.bucket_id = bucket_id
#         self.name = name
#         self.desciption = desciption
#         self.date = date

#     def __repr__(self):
#         return '<Item {}, to be completed on {}.>'.format(self.name, self.date)
