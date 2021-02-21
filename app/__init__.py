from flask import Flask
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from .models import User

app = Flask(__name__)
app.config.from_object('config')

from app import views, models


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


# OAuth 2 client setup
client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)