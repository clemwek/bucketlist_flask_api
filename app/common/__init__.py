import os
import jwt
from functools import wraps
from flask import request, jsonify
from app.models.models import User

def token_required(f):
    """This is to if there is a valid token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'token is missing!'}), 401

        try:
            id = jwt.decode(token, os.getenv('SECRET'))['id']
            current_user = User.query.filter_by(id=id).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
