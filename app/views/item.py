import os
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, make_response, abort
from app.models.models import User, Bucketlist, Item

item_blueprint = Blueprint('items', __name__)

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

@item_blueprint.route('/bucketlists/<id>/items', methods=['GET', 'POST'])
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
    search = request.args.get('q')
    limit = request.args.get('limit')

    if search:
        items = Item.query.filter_by(bucket_id=id, name=search).all()
        if items:
            items_dict = {"items": []}
            for item in items:
                dict_obj = {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "date": item.date
                }
                items_dict["items"].append(dict_obj)
            response = jsonify(items_dict)
            response.status_code = 200
            return response
        response =jsonify({'message': 'Items not found in the list'})
        response.status_code = 404
        return response

    if limit:
        items = Item.query.filter_by(bucket_id=id).limit(int(limit))
        items_dict = {"items": []}
        for item in items:
            dict_obj = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "date": item.date
            }
            items_dict["items"].append(dict_obj)
        response = jsonify(items_dict)
        response.status_code = 200
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

@item_blueprint.route('/bucketlists/<id>/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def items_manipulations(current_user, id, item_id):

    found_item = Item.query.filter_by(id=item_id, bucket_id=id).first()
    if not found_item:
        res = jsonify({'message': 'Item not found'})
        res.status_code = 404
        return res

    if request.method == 'PUT':
        found_item.name = request.data.get('item_name')
        found_item.description = request.data.get('description')
        found_item.date = request.data.get('date')

        found_item.save()
        response = jsonify({
            'id': found_item.id,
            'item_name': found_item.name,
            'item_description': found_item.description,
            'item_date': found_item.date
        })
        response.status_code = 200
        return response
    elif request.method == 'GET':
        # GET
        response = jsonify({
            'id': found_item.id,
            'name': found_item.name,
            'description': found_item.description,
            'date': found_item.date
        })
        response.status_code = 200
        return response

    elif request.method == 'DELETE':
        found_item.delete()
        return jsonify({
            'message': 'Item was deleted successful'
        })
