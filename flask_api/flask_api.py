from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from flask_api.models.users.views import user_blueprints
from flask_api.models.bucketlist.views import bucketlist_blueprints


app = Flask(__name__)
app.config['SQLALCHEM_DATABASE_URI'] = 'postgressql://postgres:newpassword@localhost/flask_api_db'
db = SQLAlchemy(app)

app.register_blueprint(user_blueprints, url_prefix='/auth')
app.register_blueprint(bucketlist_blueprints)
