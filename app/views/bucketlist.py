import os
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, make_response, abort
from app.models.models import User, Bucketlist

bucket_blueprint = Blueprint('bucketlist', __name__)

def token_required(f):
    """This is to if there is a valid token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'auth-token' in request.data:
            token = request.data['auth-token']

        if not token:
            return jsonify({'message': 'token is missing!'}), 401

        try:
            id = jwt.decode(token, os.getenv('SECRET'))['id']
            current_user = User.query.filter_by(id=id).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@bucket_blueprint.route('/bucketlists', methods=['GET', 'POST'])
@token_required
def bucketlist(current_user):
    """ Adds bucketlist when post a shows when get """
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
        response = jsonify({'message': 'Bucket not found in the list'})
        response.status_code = 404
        return response

    if limit:
        try:
            bucketlist = Bucketlist.query.filter_by(user_id=current_user.id).limit(int(limit))
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
        except ValueError:
            res = jsonify({'message': 'Please pass a numeral.'})
            res.status_code = 406
            return res

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

@bucket_blueprint.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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
