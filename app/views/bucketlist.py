"""
This has bucketlist code
"""


from flask import Blueprint, request, jsonify
from app.models.models import Bucketlist, Item
from app.common import token_required

bucket_blueprint = Blueprint('bucketlist', __name__)


@bucket_blueprint.route('/bucketlists', methods=['POST'])
@token_required
def bucketlist(current_user):
    """ Register a new user
    ---
    tags:
      - "Bucketlist"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
      - in: "body"
        name: "name"
        description: "name of the bucketlist"
        required: true
        schema:
          type: "object"
          required:
          - "name"
          properties:
            name:
              type: "string"
    responses:
        201:
          description: " Success"
        403:
          description: "Some data is missing!"
    """
    user_id = current_user.id
    name = request.data.get('name').strip(' ')

    # Test for missing data
    if not name:
        res = jsonify({'error': 'Some data is missing!'})
        res.status_code = 403
        return res

    if Bucketlist.query.filter_by(user_id=user_id, name=name).first():
        res = jsonify({'error': 'Name is already used!'})
        res.status_code = 406
        return res

    new_bucketlist = Bucketlist(name, user_id)
    new_bucketlist.save()
    resp = jsonify({
            "id": new_bucketlist.id,
            "name": new_bucketlist.name,
            "items": []
        })
    resp.status_code = 200
    return resp


@bucket_blueprint.route('/bucketlists', methods=['GET'])
@token_required
def get_bucketlist(current_user):
    """ Register a new user
    ---
    tags:
      - "Bucketlist"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
    responses:
        403:
          description: "There are no bucketlists added yet."
        200:
          description: " Success"
    """
    # GET
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
        found_bucketlist = Bucketlist.query.filter_by(user_id=current_user.id).filter(
            Bucketlist.name.like('%'+search+'%')).paginate(page, limit, False)
    else:
        found_bucketlist = Bucketlist.query.filter_by(user_id=current_user.id).paginate(
            page, limit, False)

    if not found_bucketlist.items:
        res = jsonify({'bucketlist': []})
        res.status_code = 200
        return res

    bucketlist_dict = {"bucketlist": []}
    next_page = found_bucketlist.has_next if found_bucketlist.has_next else ''
    previous_page = found_bucketlist.has_prev if found_bucketlist.has_prev else ''
    if next_page:
        next_page = url_endpoint + '?page=' + str(page + 1) + '&limit=' + str(limit)
    else:
        next_page = ''

    if previous_page:
        previous_page = url_endpoint + '?page=' + str(page - 1) + '&limit=' + str(limit)
    else:
        previous_page = ''

    for bucket in found_bucketlist.items:
        found_items = Item.query.filter_by(bucket_id=bucket.id)
        items = []
        for item in found_items:
            item_obj = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "date": item.date,
                "bucket_id": item.bucket_id
            }
            items.append(item_obj)
        dict_obj = {
            "id": bucket.id,
            "name": bucket.name,
            "items": items
        }
        bucketlist_dict["bucketlist"].append(dict_obj)
    bucketlist_dict['next_page'] = next_page
    bucketlist_dict['previous_page'] = previous_page
    response = jsonify(bucketlist_dict)
    response.status_code = 200
    return response


@bucket_blueprint.route('/bucketlists/<int:id>', methods=['DELETE'])
@token_required
def delete_bucketlist(current_user, id):
    """ Delete bucketlist
            ---
            tags:
            - "Bucketlist"
            produces:
                - "application/json"
            parameters:
            - name: "Authorization"
              in: "header"
              description: "Token for user"
              required: true
              type: "string"
            - name: bucketlistID
              in: "path"
              description: "The ID the bucketlist"
              required: true
              type: "string"
            responses:
                200:
                  description: "Bucketlist delete Successfully"
                403:
                  description: "bucketlist do not exist"
           """
    # retrieve a buckelist using it's ID
    found_bucketlist = Bucketlist.get_by_id(current_user.id, id)
    if not found_bucketlist:
        # Raise an HTTPException with a 404 not found status code
        return {
            "error": "bucketlist {} not found".format(found_bucketlist.name)
        }, 403

    if request.method == 'DELETE':
        found_bucketlist.delete()
        return {
            "message": "bucketlist {} deleted successfully".format(found_bucketlist.name),
            "id": found_bucketlist.id
        }, 200


@bucket_blueprint.route('/bucketlists/<int:id>', methods=['GET'])
@token_required
def get_single_bucketlist(current_user, id):
    """ Get bucketlist
            ---
            tags:
            - "Bucketlist"
            produces:
                - "application/json"
            parameters:
            - name: "Authorization"
              in: "header"
              description: "Token for user"
              required: true
              type: "string"
            - name: bucketlistID
              in: "path"
              description: "The ID the bucketlist"
              required: true
              type: "string"
            responses:
                200:
                  description: "Bucketlist found Successfully"
                403:
                  description: "bucketlist do not exist"
           """
    # retrieve a buckelist using it's ID
    found_bucketlist = Bucketlist.get_by_id(current_user.id, id)
    if not found_bucketlist:
        # Raise an HTTPException with a 403 not found status code
        return {
            "message": "bucketlist not found"
        }, 403
    bucket_items = Item.get_all(bucket_id=id)
    bucket_item_list = [item.name for item in bucket_items]

    # GET
    response = jsonify({
        'id': found_bucketlist.id,
        'name': found_bucketlist.name,
        'items': bucket_item_list
    })
    response.status_code = 200
    return response


@bucket_blueprint.route('/bucketlists/<int:id>', methods=['PUT'])
@token_required
def update_bucketlist(current_user, id):
    """ Update bucketlist
            ---
            tags:
            - "Bucketlist"
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
            - name: bucketlistID
              in: "path"
              description: "The ID the bucketlist"
              required: true
              type: "string"
            - name: newname
              in: "formData"
              description: "The new name of the bucketlist"
              required: true
              type: "string"
            responses:
                200:
                  description: "Bucketlist updated Successfully"
                403:
                  description: "Update Doesn't exist"
           """
    # retrieve a buckelist using it's ID
    found_bucketlist = Bucketlist.get_by_id(current_user.id, id)
    if not found_bucketlist:
        # Raise an HTTPException with a 404 not found status code
        return {
            "message": "bucketlist not found"
        }, 403

    # PUT
    name = request.data.get('name').strip(' ')

    if Bucketlist.query.filter_by(user_id=current_user.id, name=name).first():
        res = jsonify({'error': 'Name is already used!'})
        res.status_code = 406
        return res

    found_bucketlist.name = name
    found_bucketlist.save()
    return found_bucketlist.serialize('Bucketlist updated', 200)
