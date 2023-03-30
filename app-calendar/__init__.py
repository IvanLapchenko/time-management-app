import secrets
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
CORS(app)
JWTManager(app)
app.config["JWT_SECRET_KEY"] = secrets.token_hex(16)

from .login_service import *
from . import routes

