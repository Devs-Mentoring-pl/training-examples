import os
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .constants import DB_NAME, DB_PATH

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="../templates")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = secrets.token_hex(32)

    db.init_app(app)

    from .main import main_bp
    app.register_blueprint(main_bp)

    create_db(app)

    return app


def create_db(app):
    """Tworzy bazę danych, jeśli jeszcze nie istnieje."""
    with app.app_context():
        if not os.path.exists(DB_PATH):
            db.create_all()
            print("Baza danych utworzona!")
