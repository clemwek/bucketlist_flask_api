from flask import Blueprint


bucketlist_blueprints = Blueprint('bucketlist', __name__)


@bucketlist_blueprints.route('/bucketlists', methods=['GET', 'POST'])
def bucketlists():
    return ''


@bucketlist_blueprints.route('/bucketlists/<id>', methods=['GET', 'PUT', 'DELETE'])
def single_bucketlists():
    return ''


@bucketlist_blueprints.route('/bucketlists/<id>/items', methods=['POST'])
def add_items():
    return ''


@bucketlist_blueprints.route('/bucketlists/<id>/items/<items_id>', methods=['PUT', 'DELETE'])
def change_items():
    return ''
