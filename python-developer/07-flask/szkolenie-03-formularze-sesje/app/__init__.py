import secrets
from datetime import timedelta
from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.config["SECRET_KEY"] = secrets.token_hex(32)
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    from app.routes.main import login_blueprint, dashboard_blueprint, logout_blueprint

    app.register_blueprint(login_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(logout_blueprint)

    return app
