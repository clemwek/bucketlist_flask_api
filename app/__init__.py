from flask_api import FlaskAPI
from flask import request, jsonify, json, abort
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


    from app.models.models import User, Bucketlist, Item


    @app.route('/auth/register', methods=['POST'])
    def register():
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if username is None or password is None or email is None:
            res = jsonify({'message': 'some arguments are missing.'})
            res.status_code = 400
            return res
        if User.query.filter_by(username=username).first() is not None:
            res = jsonify({'message': 'Username already used.'})
            res.status_code = 400
            return res
        new_user = User(username, email)
        new_user.hash_password(password)
        new_user.save()
        response = jsonify({
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        })
        response.status_code = 201
        return response

    @app.route('/auth/login', methods=['POST'])
    def login():
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            res = jsonify({'message': 'some arguments are missing.'})
            res.status_code = 400
            return res
        if User.query.filter_by(username = username).first() is None:
            res = jsonify({'message': 'Username does not exist.'})
            res.status_code = 400
            return res
        found_user = User.query.filter_by(username=username).first()
        if found_user and found_user.verify_password(password):
            response = jsonify({
                "id": found_user.id,
                "username": found_user.username,
                "email": found_user.email
            })
            response.status_code = 202
            return response
        return abort(404)


    @app.route('/auth/logout', methods=['POST'])
    def logout():
        pass

    @app.route('/auth/reset-password', methods=['POST'])
    def reset_password():
        username = request.data.get('username')
        new_password = request.data.get('password')
        found_user = User.query.filter_by(username=username).first()
        found_user.hash_password(new_password)
        found_user.save()
        response = jsonify({
            "id": found_user.id,
            "username": found_user.username,
            "email": found_user.email
        })
        response.status_code = 200
        return response

    @app.route('/bucketlists', methods=['GET', 'POST'])
    def bucketlist():
        if request.method == 'POST':
            name = request.data.get('name')
            user_id = 5 #To Do
            new_bucketlist = Bucketlist(name, user_id)
            new_bucketlist.save()
            response = jsonify({
                'id': new_bucketlist.id,
                'name': new_bucketlist.name
            })
            response.status_code = 201
            return response
        user_id = 5
        bucketlist = Bucketlist.query.filter_by(user_id=user_id).all()
        bucketlist_dict = {"bucketlist": []}
        for bucket in bucketlist:
            dict_obj = {
                "id": bucket.id,
                "name": bucket.name
            }
            bucketlist_dict["bucketlist"].append(dict_obj)
        print(bucketlist_dict)
        response = jsonify(bucketlist_dict)
        response.status_code = 200
        return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id):
     # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
            "message": "bucketlist {} deleted successfully".format(bucketlist.id) 
         }, 200

        elif request.method == 'PUT':
            # PUT
            name = request.data.get('name')
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name
            })
            response.status_code = 200
            return response
        elif request.method == 'GET':
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name
            })
            response.status_code = 200
            return response

    return app
