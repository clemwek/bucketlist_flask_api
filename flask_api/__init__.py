from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route('/auth/register', methods=['POST'])
def register():
    return ''


@app.route('/auth/login', methods=['POST'])
def login():
    return ''


@app.route('/auth/logout', methods=['POST'])
def logout():
    return ''

@app.route('/auth/reset_password', methods=['POST'])
def reset_password():
    return ''


@app.route('/bucketlists', methods=['GET', 'POST'])
def bucketlists():
    return ''


@app.route('/bucketlists/<id>', methods=['GET', 'PUT', 'DELETE'])
def single_bucketlists():
    return ''


@app.route('/bucketlists/<id>/items', methods=['POST'])
def add_items():
    return ''


@app.route('/bucketlists/<id>/items/<items_id>', methods=['PUT', 'DELETE'])
def change_items():
    return ''
