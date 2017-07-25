from flask_api import FlaskAPI
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

    return app










# app = Flask(__name__)
# app.config.from_object('config')
# db = SQLAlchemy(app)


# @app.route('/auth/register', methods=['POST'])
# def register():
#     return ''


# @app.route('/auth/login', methods=['POST'])
# def login():
#     return ''


# @app.route('/auth/logout', methods=['POST'])
# def logout():
#     return ''

# @app.route('/auth/reset_password', methods=['POST'])
# def reset_password():
#     return ''


# @app.route('/bucketlists', methods=['GET', 'POST'])
# def bucketlists():
#     return ''


# @app.route('/bucketlists/<id>', methods=['GET', 'PUT', 'DELETE'])
# def single_bucketlists():
#     return ''


# @app.route('/bucketlists/<id>/items', methods=['POST'])
# def add_items():
#     return ''


# @app.route('/bucketlists/<id>/items/<items_id>', methods=['PUT', 'DELETE'])
# def change_items():
#     return ''
