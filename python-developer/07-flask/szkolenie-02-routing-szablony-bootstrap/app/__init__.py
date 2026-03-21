from flask import Flask


def create_app():
    app = Flask(__name__)

    from .main import welcome_blueprint, goodbye_blueprint
    app.register_blueprint(welcome_blueprint)
    app.register_blueprint(goodbye_blueprint)

    return app
