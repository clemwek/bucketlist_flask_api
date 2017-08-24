"""
This has all the items code
"""


from flask import Blueprint, request, jsonify
from app.models.models import Item
from app.common import token_required
from app.common import validate_date

item_blueprint = Blueprint('items', __name__)


@item_blueprint.route('/bucketlists/<id>/items', methods=['POST'])
@token_required
def add_items(current_user, id):

    """Add item to bucketlist
                ---
                tags:
                - "Items"
                consumes:
                    - "application/json"
                produces:
                    - "application/json"
                parameters:
                - name: "Authorization"
                  in: "header"
                  description: "Token of a logged in user"
                  required: true
                  type: "string"
                - name: bucketlist_id
                  in: "path"
                  description: "The ID the bucketlist"
                  required: true
                  type: "string"
                - name: name
                  in: "data"
                  description: "The name for the new item"
                  required: true
                  type: "string"
                - name: date
                  in: "date"
                  description: "The deadline for the new item"
                  required: true
                  type: "string"
                - name: description
                  in: "data"
                  description: "The description of the new item"
                  required: true
                  type: "string"
                responses:
                    200:
                      description: "Item added Successfully"
                    403:
                      description: "Some data is missing!"
               """

    item_name = request.data.get('name')
    item_description = request.data.get('description')
    item_date = request.data.get('date')
    item_bucket_id = id

    if not item_name or not item_description or not item_date:
        res = jsonify({'message': 'Some data is missing!'})
        res.status_code = 403
        return res

    if not validate_date(item_date):
        res = jsonify({'message': 'date is not valid'})
        res.status_code = 403
        return res

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


@item_blueprint.route('/bucketlists/<id>/items', methods=['GET'])
@token_required
def get_items(current_user, id):

    """Add item to bucketlist
                ---
                tags:
                - "Items"
                produces:
                    - "application/json"
                parameters:
                - name: "Authorization"
                  in: "header"
                  description: "Token of a logged in user"
                  required: true
                  type: "string"
                - name: bucketlist_id
                  in: "path"
                  description: "The ID the bucketlist"
                  required: true
                  type: "string"
                responses:
                    200:
                      description: "Item found"
                    403:
                      description: "Items not found in the list"
               """
    search = request.args.get('q')
    limit = request.args.get('limit')

    if search:
        # TODO: search for like and pagination
        items = Item.query.filter_by(name=search, bucket_id=id).all()
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
        response = jsonify({'message': 'Items not found in the list'})
        response.status_code = 403
        return response

    if limit:
        try:
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
        except ValueError:
            res = jsonify({'message': 'Please pass a numeral.'})
            res.status_code = 406
            return res

    # TODO: Add pagination
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

@item_blueprint.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
@token_required
def edit_items(current_user, id, item_id):
    """ Edit Item
    ---
    tags:
      - "Items"
    parameters:
      - in: "body"
        name: "data"
        description: ""
        required: true
        schema:
          type: "object"
          required:
          - "name"
          - "date"
          - "description"
          properties:
            name:
              type: "string"
            date:
              type: "string"
            description:
              type: "string"
    responses:
        200:
          description: "successful operation"
        400:
          description: "Forbidden" 
    """
    found_item = Item.query.filter_by(id=item_id, bucket_id=id).first()
    if not found_item:
        res = jsonify({'message': 'Item not found'})
        res.status_code = 404
        return res

    # PUT
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

@item_blueprint.route('/bucketlists/<id>/items/<item_id>', methods=['GET'])
@token_required
def get_single_items(current_user, id, item_id):
    """Returns single Item when GET, Edits when PUT and Deletes when DELETE"""
    found_item = Item.query.filter_by(id=item_id, bucket_id=id).first()
    if not found_item:
        res = jsonify({'message': 'Item not found'})
        res.status_code = 404
        return res

    # GET
    response = jsonify({
        'id': found_item.id,
        'name': found_item.name,
        'description': found_item.description,
        'date': found_item.date
    })
    response.status_code = 200
    return response

@item_blueprint.route('/bucketlists/<id>/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def delete_items(current_user, id, item_id):
    """ Delete item 
    ---
    tags:
      - "Items"
    responses:
        200:
          description: "successful operation"
        400:
          description: "Forbidden"
    """
    found_item = Item.query.filter_by(id=item_id, bucket_id=id).first()
    if not found_item:
        res = jsonify({'message': 'Item not found'})
        res.status_code = 404
        return res

    # DELETE
    found_item.delete()
    return jsonify({
        'message': 'Item was deleted successful'
    })
