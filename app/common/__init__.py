"""
This has globaly needed functions
"""


import os
import re
import datetime
from functools import wraps
import jwt
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


def validate_date(date):
    """This validates is the passed date"""
    try:
        datetime.datetime.strptime(date, '%m/%d/%Y')
        return True
    except ValueError:
        return False


def email_is_valid(email):
    """This validates an email"""
    email_address_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
    return True if email_address_matcher.match(email) else False
