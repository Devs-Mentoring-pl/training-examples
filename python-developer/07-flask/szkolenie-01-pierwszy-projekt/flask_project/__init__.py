from flask import Flask


def create_app():
    """Application Factory – tworzy i konfiguruje instancję aplikacji Flask."""
    app = Flask(__name__)

    from .main import index_blueprint

    app.register_blueprint(index_blueprint)

    return app
