from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .config import Config
from .db import init_db
from .auth import auth_bp, login_manager
from .routes import main_bp

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    if not app.config.get('SECRET_KEY'):
        raise RuntimeError('SECRET_KEY must be set in the environment')

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    csrf.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    init_db()

    return app
