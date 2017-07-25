from flask import Blueprint


user_blueprints = Blueprint('users', __name__)


@user_blueprints.route('/register', methods=['POST'])
def register():
    return ''


@user_blueprints.route('/login', methods=['POST'])
def login():
    return ''


@user_blueprints.route('/logout', methods=['POST'])
def logout():
    return ''

@user_blueprints.route('/reset_password', methods=['POST'])
def reset_password():
    return ''
