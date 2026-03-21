import os
from datetime import datetime, timezone, timedelta
import jwt
from functools import wraps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///users.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --- Model ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# --- Dekorator autoryzacji ---

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Brak tokenu autoryzacyjnego"}), 401

        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = db.session.get(User, payload["sub"])

            if not current_user:
                return jsonify({"error": "Użytkownik nie istnieje"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token wygasł – zaloguj się ponownie"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Nieprawidłowy token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# --- Endpointy ---

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Brak wymaganych pól"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Użytkownik już istnieje"}), 409

    user = User(username=data["username"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Konto utworzone pomyślnie"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Brak wymaganych pól"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Nieprawidłowy login lub hasło"}), 401

    now = datetime.now(timezone.utc)

    access_token = jwt.encode(
        {
            "sub": user.id,
            "username": user.username,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=30),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    refresh_token = jwt.encode(
        {
            "sub": user.id,
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=7),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 200


@app.route("/refresh", methods=["POST"])
def refresh_token():
    data = request.get_json()
    refresh = data.get("refresh_token") if data else None

    if not refresh:
        return jsonify({"error": "Brak refresh tokenu"}), 400

    try:
        payload = jwt.decode(refresh, app.config["SECRET_KEY"], algorithms=["HS256"])

        if payload.get("type") != "refresh":
            return jsonify({"error": "Nieprawidłowy typ tokenu"}), 401

        user = db.session.get(User, payload["sub"])
        if not user:
            return jsonify({"error": "Użytkownik nie istnieje"}), 401

        new_access_token = jwt.encode(
            {
                "sub": user.id,
                "username": user.username,
                "type": "access",
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return jsonify({"access_token": new_access_token}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token wygasł – zaloguj się ponownie"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Nieprawidłowy token"}), 401


@app.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
    })


@app.route("/users", methods=["GET"])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])


# --- Inicjalizacja bazy ---

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
