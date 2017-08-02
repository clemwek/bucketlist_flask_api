from functools import wraps
from flask_api import FlaskAPI
from flask import request, jsonify, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import jwt


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

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'auth-token' in request.headers:
                token = request.headers['auth-token']

            if not token:
                return jsonify({'message': 'token is missing!'}), 401

            try:
                id = jwt.decode(token, os.getenv('SECRET'))['id']
                current_user = User.query.filter_by(id=id).first()
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated


    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json()

        new_user = User(username=data['username'], email=data['email'])
        new_user.hash_password(data['password'])
        new_user.save()

        return jsonify({'message': 'user created!'})


    @app.route('/auth/login', methods=['POST'])
    def login():
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('could not veryfy', 401,{'WWW-Authenticate':'Basic realm="login required!"'})

        found_user = User.query.filter_by(username=auth.username).first()
        if not found_user:
            return make_response('could not veryfy', 401,{'WWW-Authenticate':'Basic realm="login required!"'})

        if found_user.check_hashed_password(auth.password, found_user.password_hash):
            return found_user.gen_token()
        return make_response('could not veryfy', 401,{'WWW-Authenticate':'Basic realm="login required!"'})


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
    @token_required
    def bucketlist(current_user):
        if request.method == 'POST':
            name = request.data.get('name')
            user_id = current_user.id
            new_bucketlist = Bucketlist(name, user_id)
            new_bucketlist.save()
            response = jsonify({
                'id': new_bucketlist.id,
                'name': new_bucketlist.name
            })
            response.status_code = 201
            return response
        search = request.args.get('q')
        limit = request.args.get('limit')
        if search:
            bucketlist = Bucketlist.query.filter_by(user_id=current_user.id, name=search).all()
            if bucketlist:
                bucketlist_dict = {"bucketlist": []}
                for bucket in bucketlist:
                    dict_obj = {
                        "id": bucket.id,
                        "name": bucket.name
                    }
                    bucketlist_dict["bucketlist"].append(dict_obj)
                response = jsonify(bucketlist_dict)
                response.status_code = 200
                return response
            response =jsonify({'message': 'Bucket not found in the list'})
            response.status_code = 404
            return response
        if limit = request.args.get('limit'):
            pass


        user_id = current_user.id
        bucketlist = Bucketlist.query.filter_by(user_id=user_id).all()
        bucketlist_dict = {"bucketlist": []}
        for bucket in bucketlist:
            dict_obj = {
                "id": bucket.id,
                "name": bucket.name
            }
            bucketlist_dict["bucketlist"].append(dict_obj)
        response = jsonify(bucketlist_dict)
        response.status_code = 200
        return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    @token_required
    def bucketlist_manipulation(current_user, id):
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
    
    @app.route('/bucketlists/<id>/items', methods=['GET', 'POST'])
    @token_required
    def add_items(current_user, id):
        if request.method == 'POST':
            item_name = request.data.get('name')
            item_description = request.data.get('description')
            item_date = request.data.get('date')
            item_bucket_id = id

            new_item = Item(item_name, item_description, item_date, item_bucket_id)
            new_item.save()
            response = jsonify({
                'id': new_item.id,
                'item_name': new_item.name,
                'item_description': new_item.description,
                'item_date': new_item.date
            })
            response.status_code = 201
            return response
        items = Item.query.filter_by(bucket_id=id).all()
        item_dict = {"items": []}
        for item in items:
            dict_obj = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "date": item.date
            }
            item_dict["items"].append(dict_obj)
        response = jsonify(item_dict)
        response.status_code = 200
        return response

    @app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT', 'DELETE'])
    @token_required
    def items_manipulations(current_user, id, item_id):

        found_item = Item.query.filter_by(id=item_id, bucket_id=id).first()
        if not found_item:
            return jsonify({'message': 'Item not found'})

        if request.method == 'PUT':
            found_item.name = request.data.get('name')
            found_item.description = request.data.get('name')
            found_item.date = request.data.get('name')

            found_item.save()
            response = jsonify({
                'id': found_item.id,
                'item_name': found_item.name,
                'item_description': found_item.description,
                'item_date': found_item.date
            })
            response.status_code = 200
            return response
        elif request.method == 'DELETE':
            found_item.delete()
            return jsonify({
                'message': 'Item was deleted successful'
            })

    return app
