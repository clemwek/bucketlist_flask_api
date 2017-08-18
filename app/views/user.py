"""
This has all the auth code
"""


from flask import Blueprint, request, jsonify
from app.models.models import User

user_blueprint = Blueprint('auth', __name__)


@user_blueprint.route('/register', methods=['POST'])
def register():
    """ Register a new user """
    username = str(request.data.get('username', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))

    if not email or not username or not password:
        res = jsonify({'message': 'Some data is missing!'})
        res.status_code = 406
        return res

    found_username = User.query.filter_by(username=username).first()
    found_email = User.query.filter_by(email=email).first()
    if found_username:
        res = jsonify({'message': 'Username already used try anotherone.'})
        res.status_code = 409
        return res

    if found_email:
        res = jsonify({'message': 'Email already used try anotherone.'})
        res.status_code = 409
        return res

    new_user = User(username, email)
    new_user.hash_password(password)
    new_user.save()

    res = jsonify({
        'message': 'user created!',
        'username': new_user.username,
        'email': new_user.email
    })
    res.status_code = 201
    return res


@user_blueprint.route('/login', methods=['POST'])
def login():
    """ Login a user """
    username = str(request.data.get('username', ''))
    password = str(request.data.get('password', ''))

    if not username or not password:
        res = jsonify({'message': 'could not veryfy: Some data was not send'})
        res.status_code = 403
        return res

    found_user = User.query.filter_by(username=username).first()
    if not found_user:
        res = jsonify({'message': 'could not veryfy: No user'})
        res.status_code = 401
        return res

    if found_user.check_hashed_password(password, found_user.password_hash):
        res = found_user.gen_token()
        res.status_code = 202
        return res
    else:
        res = jsonify({'message': 'could not veryfy: wrong password'})
        res.status_code = 401
        return res


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    """ Log out a user """
    pass


@user_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    """ Resets a users password """
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
