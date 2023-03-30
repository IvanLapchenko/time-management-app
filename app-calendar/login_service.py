from .database import User, session
from . import app
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    return session.query(User).where(User.id == user_id).first

