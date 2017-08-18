"""
This has bucketlist code
"""


from flask import Blueprint, request, jsonify, make_response, abort
from app.models.models import User, Bucketlist
from app.common import token_required

bucket_blueprint = Blueprint('bucketlist', __name__)


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
        found_bucketlist = Bucketlist.query.filter_by(user_id=current_user.id, name=search).all()
        if found_bucketlist:
            bucketlist_dict = {"bucketlist": []}
            for bucket in found_bucketlist:
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
            found_bucketlist = Bucketlist.query.filter_by(user_id=current_user.id).limit(int(limit))
            bucketlist_dict = {"bucketlist": []}
            for bucket in found_bucketlist:
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
    found_bucketlist = Bucketlist.query.filter_by(user_id=user_id).all()
    bucketlist_dict = {"bucketlist": []}
    for bucket in found_bucketlist:
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
    """returns individual post when GET, Edits when PUT and deletes when DELETE"""
    # retrieve a buckelist using it's ID
    found_bucketlist = Bucketlist.query.filter_by(id=id).first()
    if not found_bucketlist:
        # Raise an HTTPException with a 404 not found status code
        abort(404)

    if request.method == 'DELETE':
        found_bucketlist.delete()
        return {
            "message": "bucketlist {} deleted successfully".format(found_bucketlist.id)
        }, 200

    elif request.method == 'PUT':
        # PUT
        name = request.data.get('name')
        found_bucketlist.name = name
        found_bucketlist.save()
        response = jsonify({
            'id': found_bucketlist.id,
            'name': found_bucketlist.name
        })
        response.status_code = 200
        return response
    elif request.method == 'GET':
        # GET
        response = jsonify({
            'id': found_bucketlist.id,
            'name': found_bucketlist.name
        })
        response.status_code = 200
        return response
