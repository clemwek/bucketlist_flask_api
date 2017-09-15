"""
This has all the items code
"""


from flask import Blueprint, request, jsonify
from app.models.models import Bucketlist, Item
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
    if not Bucketlist.get_by_id(current_user.id, id):
        res = jsonify({'items': []})
        res.status_code = 200
        return res

    item_name = request.data.get('name')
    item_description = request.data.get('description')
    item_date = request.data.get('date')
    item_bucket_id = id

    if not item_name or not item_description or not item_date:
        res = jsonify({'error': 'Some data is missing!'})
        res.status_code = 403
        return res

    if not validate_date(item_date):
        res = jsonify({'error': 'date is not valid'})
        res.status_code = 403
        return res

    new_item = Item(item_name, item_description, item_date, item_bucket_id)
    new_item.save()
    return new_item.serialize('Item created.', 201)


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

    if not Bucketlist.get_by_id(current_user.id, id):
        res = jsonify({'error': 'Bucketlist not found'})
        res.status_code = 403
        return res

    url_endpoint = '/bucketlists'
    search = request.args.get('q')
    page = int(request.args.get('page', default=1))

    try:
        limit = int(request.args.get('limit', default=10))
    except ValueError:
        res = jsonify({'error': 'Please pass a numeral.'})
        res.status_code = 406
        return res

    if search:
        found_items = Item.query.filter_by(bucket_id=id).filter(
            Item.name.like('%'+search+'%')).paginate(page, limit, False)
    else:
        found_items = Item.query.filter_by(bucket_id=id).paginate(page, limit, False)

    if not found_items.items:
        res = jsonify({'error': 'There are no items added yet.'})
        res.status_code = 403
        return res

    items_dict = {"items": []}
    next_page = found_items.has_next if found_items.has_next else ''
    previous_page = found_items.has_prev if found_items.has_prev else ''

    if next_page:
        next_page = url_endpoint + '?page=' + str(page + 1) + '&limit=' + str(limit)
    else:
        next_page = ''

    if previous_page:
        previous_page = url_endpoint + '?page=' + str(page - 1) + '&limit=' + str(limit)
    else:
        previous_page = ''

    for item in found_items.items:
        dict_obj = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "date": item.date
        }
        items_dict["items"].append(dict_obj)
    items_dict['next_page'] = next_page
    items_dict['previous_page'] = previous_page
    response = jsonify(items_dict)
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

    if not Bucketlist.get_by_id(current_user.id, id):
        res = jsonify({'error': 'Bucketlist not found'})
        res.status_code = 403
        return res

    found_item = Item.get_by_id(id, item_id)
    if not found_item:
        res = jsonify({'error': 'Item not found'})
        res.status_code = 403
        return res

    # PUT
    found_item.name = request.data.get('name')
    found_item.description = request.data.get('description')
    found_item.date = request.data.get('date')

    found_item.save()
    return found_item.serialize('Item updated', 200)


@item_blueprint.route('/bucketlists/<id>/items/<item_id>', methods=['GET'])
@token_required
def get_single_items(current_user, id, item_id):
    """Returns single Item when GET, Edits when PUT and Deletes when DELETE"""

    if not Bucketlist.get_by_id(current_user.id, id):
        res = jsonify({'error': 'Bucketlist not found'})
        res.status_code = 403
        return res

    found_item = Item.get_by_id(id, item_id)
    if not found_item:
        res = jsonify({'error': 'Item not found'})
        res.status_code = 404
        return res

    return found_item.serialize('success', 200)


@item_blueprint.route('/bucketlists/<id>/items/<item_id>', methods=['PUT', 'DELETE'])
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
    if not Bucketlist.get_by_id(current_user.id, id):
        res = jsonify({'error': 'Bucketlist not found'})
        res.status_code = 403
        return res

    found_item = Item.query.filter_by(id=item_id, bucket_id=id).first()
    if not found_item:
        res = jsonify({'error': 'Item not found'})
        res.status_code = 404
        return res

    # DELETE
    found_item.delete()
    return jsonify({
        'message': 'Item was deleted successful'
    })
