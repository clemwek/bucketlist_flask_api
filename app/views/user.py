"""
This has all the auth code
"""

from flask import Blueprint, request, jsonify

from app.common import email_is_valid
from app.models.models import User

user_blueprint = Blueprint('auth', __name__)


@user_blueprint.route('/register', methods=['POST'])
def register():
    """ Register a new user 
    ---
    tags:
      - "auth"
    parameters:
      - in: "body"
        name: "data"
        description: "Username and password submitted"
        required: true
        schema:
          type: "object"
          required:
          - "username"
          - "password"
          properties:
            username:
              type: "string"
            password:
              type: "string"
    responses:
        406:
          description: "Some data is missing!"
        201:
          description: " Success"
        409:
          description: " Username already used try anotherone."
    """
    username = str(request.data.get('username', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))

    if not email or not username or not password:
        res = jsonify({'message': 'Some data is missing!'})
        res.status_code = 406
        return res

    if not email_is_valid(email):
        res = jsonify({'message': 'Please provide a valid email.'})
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
    """ Login in old users 
    ---
    tags:
      - "auth"
    parameters:
      - in: "body"
        name: "data"
        description: "Username and password submitted"
        required: true
        schema:
          type: "object"
          required:
          - "username"
          - "password"
          properties:
            username:
              type: "string"
            password:
              type: "string"
    responses:
        401:
          description: " Invalid credentials"
        200:
          description: " Success"
    """
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
    """ Enable users to reset passwords
    ---
    tags:
      - "auth"
    parameters:
      - in: "body"
        name: "data"
        description: "Username and password submitted"
        required: true
        schema:
          type: "object"
          required:
          - "username"
          - "old_password"
          - "new_password"
          properties:
            username:
              type: "string"
            old_password:
              type: "string"
            new_password:
              type: "string"
    responses:
        400:
          description: " Invalid credentials"
        200:
          description: " Success"
    """
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
