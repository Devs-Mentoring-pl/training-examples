import pytest
from app import app, db, User


@pytest.fixture
def client():
    """Fixture tworzący klienta testowego z tymczasową bazą danych."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def sample_user(client):
    """Fixture tworzący przykładowego użytkownika w bazie."""
    with app.app_context():
        user = User(username="testuser")
        user.set_password("testpassword123")
        db.session.add(user)
        db.session.commit()
    return {"username": "testuser", "password": "testpassword123"}


@pytest.fixture
def auth_header(client, sample_user):
    """Fixture zwracający nagłówek autoryzacyjny z tokenem."""
    response = client.post(
        "/login",
        json={"username": sample_user["username"], "password": sample_user["password"]},
    )
    data = response.get_json()
    token = data.get("access_token")
    return {"Authorization": f"Bearer {token}"}


def test_register_new_user(client):
    """Rejestracja nowego użytkownika powinna zwrócić 201."""
    response = client.post(
        "/register",
        json={"username": "newuser", "password": "securepass123"},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Konto utworzone pomyślnie"


def test_register_duplicate_user(client, sample_user):
    """Rejestracja istniejącego użytkownika powinna zwrócić 409."""
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "innehaslo"},
    )

    assert response.status_code == 409
    data = response.get_json()
    assert "istnieje" in data["error"]


def test_login_valid_credentials(client, sample_user):
    """Logowanie z poprawnymi danymi powinno zwrócić token."""
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "testpassword123"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_password(client, sample_user):
    """Logowanie z błędnym hasłem powinno zwrócić 401."""
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "zlehaslo"},
    )

    assert response.status_code == 401


def test_get_profile_with_token(client, auth_header):
    """Dostęp do profilu z tokenem powinien zwrócić dane użytkownika."""
    response = client.get("/profile", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "testuser"


def test_get_profile_without_token(client):
    """Dostęp do profilu bez tokenu powinien zwrócić 401."""
    response = client.get("/profile")

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_get_profile_with_invalid_token(client):
    """Dostęp z nieprawidłowym tokenem powinien zwrócić 401."""
    response = client.get(
        "/profile",
        headers={"Authorization": "Bearer jakis.falszywy.token"},
    )

    assert response.status_code == 401
