from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from flask_api.models.users.views import user_blueprints
from flask_api.models.bucketlist.views import bucketlist_blueprints


app = Flask(__name__)
app.config.from_object('config')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from flask_api.models.users.user import User
from flask_api.models.bucketlist.bucketlist import Bucketlist
from flask_api.models.items.items import Item

app.register_blueprint(user_blueprints, url_prefix='/auth')
app.register_blueprint(bucketlist_blueprints)
