from flask_api import FlaskAPI
from flask import request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config


# initialize sql-alchemy
db = SQLAlchemy()

from app.models.models import User, Bucketlist, Item

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    @app.route('/auth/register', methods=['POST'])
    def register():
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        new_user = User(username, email, password)
        new_user.save()
        response = jsonify({
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'password': new_user.password
        })
        response.status_code = 201
        return response

    @app.route('/auth/login', methods=['POST'])
    def login():
        username = request.data.get('username')
        password = request.data.get('password')
        found_user = User.query.filter_by(username=username).first()
        print(found_user)
        if found_user and found_user.password == password:
            response = jsonify({found_user})
            response.status_code = 201
            return response
        return abort(404)


    # @app.route('/bucketlists', methods=['GET', 'POST'])
    # def bucketlist():
    #     if request.method == 'POST':
    #         name = str(request.data.get('name', ''))
    #         user_id = 'test' #To Do
    #         new_bucketlist = Bucketlist(name, user_id)
    #         new_bucketlist.save()
    #         response = jsonify({
    #             'id': new_bucketlist.id,
    #             'name': new_bucketlist.name
    #         })
    #         response.status_code = 201
    #         return response
    #     bucketlist = Bucketlist.query.filter_by(user_id=user_id).all()
    #     response = jsonify({ bucketlist })
    #     response.status_code = 200
    #     return response


    # @app.route('/bucketlists', methods=['GET', 'POST'])
    # def bucketlis():
    #     if request.method == 'POST':
    #         name = str(request.data.get('name', ''))
    #         user_id = 'test' #To Do
    #         new_bucketlist = Bucketlist(name, user_id)
    #         new_bucketlist.save()
    #         response = jsonify({
    #             'id': new_bucketlist.id,
    #             'name': new_bucketlist.name
    #         })
    #         response.status_code = 201
    #         return response
    #     bucketlist = Bucketlist.query.filter_by(user_id=user_id).all()
    #     response = jsonify({ bucketlist })
    #     response.status_code = 200
    #     return response


    # @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    # def bucketlist_manipulation(id, **kwargs):
    #  # retrieve a buckelist using it's ID
    #     bucketlist = Bucketlist.query.filter_by(id=id).first()
    #     if not bucketlist:
    #         # Raise an HTTPException with a 404 not found status code
    #         abort(404)

    #     if request.method == 'DELETE':
    #         bucketlist.delete()
    #         return {
    #         "message": "bucketlist {} deleted successfully".format(bucketlist.id) 
    #      }, 200

    #     elif request.method == 'PUT':
    #         name = str(request.data.get('name', ''))
    #         bucketlist.name = name
    #         bucketlist.save()
    #         response = jsonify({
    #             'id': bucketlist.id,
    #             'name': bucketlist.name,
    #             'date_created': bucketlist.date_created,
    #             'date_modified': bucketlist.date_modified
    #         })
    #         response.status_code = 200
    #         return response
    #     else:
    #         # GET
    #         response = jsonify({
    #             'id': bucketlist.id,
    #             'name': bucketlist.name,
    #             'date_created': bucketlist.date_created,
    #             'date_modified': bucketlist.date_modified
    #         })
    #         response.status_code = 200
    #         return response

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
