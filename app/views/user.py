import os
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, make_response
from app.models.models import User

user_blueprint = Blueprint('auth', __name__)

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


@user_blueprint.route('/register', methods=['POST'])
def register():
    """ Register a new user """
    username = str(request.data.get('username', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    found_username = User.query.filter_by(username=username).first()
    found_email = User.query.filter_by(email=email).first()
    if not email or not username or not password:
        res = jsonify({'message': 'Some data is missing!'})
        res.status_code = 406
        return res
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
        return make_response('could not veryfy: No data was send', 401,
                            {'WWW-Authenticate':'Basic realm="login required!"'})

    found_user = User.query.filter_by(username=username).first()
    if not found_user:
        return make_response('could not veryfy: No user', 401,
                            {'WWW-Authenticate':'Basic realm="login required!"'})

    if found_user.check_hashed_password(password, found_user.password_hash):
        res = found_user.gen_token()
        res.status_code = 202
        return res
    return make_response('could not veryfy: wrong password', 401,
                        {'WWW-Authenticate':'Basic realm="login required!"'})


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
