"""
This create an instance of FlaskAPI and initialize some values
"""


from flask_api import FlaskAPI
from flasgger import Swagger
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# local import
from instance.config import app_config


# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)
    swagger = Swagger(app)

    # Import user/ auth blueprint
    from app.views.user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/auth')

    # Import bucketlist blueprint
    from app.views.bucketlist import bucket_blueprint
    app.register_blueprint(bucket_blueprint)

    # Import items blueprint
    from app.views.item import item_blueprint
    app.register_blueprint(item_blueprint)

    return app
