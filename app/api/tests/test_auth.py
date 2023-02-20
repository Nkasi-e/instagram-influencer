import pytest
from app.api.schema import user
from app.cors.config import settings
from jose import jwt


def test_root(client):
    res = client.get("/")
    assert (
        res.json()["Message"]
        == "Welcome to Instagram Influencer search portal"
    )
    assert res.status_code == 200


def test_create_user(client):
    user_in = {
        "email": "test@gmail.com",
        "password": "Password123"
    }
    res = client.post("/account/signup", json=user_in)
    new_user = user.UserResponseSchema(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_user_login(client, test_user):
    res = client.post(
        "/login/",
        json={
            "email": test_user["email"],
            "password": test_user["password"],
        },
    )
    login_response = user.TokenResponseSchema(**res.json())
    payload = jwt.decode(
        login_response.access_token, settings.JWT_SECRET_KEY, algorithms=[
            settings.ALGORITHM]
    )
    id = payload["user_id"]
    assert id == test_user["id"]
    assert login_response.token_type == "Bearer"
    assert login_response.email == test_user["email"]
    assert res.status_code == 200


def test_duplicate_email_error(client, test_user):
    user_in = {
        "email": test_user['email'],
        "password": test_user['password']
    }
    res = client.post("/account/signup", json=user_in)
    assert res.status_code == 409
    assert res.json()['detail'] == f"email already exists"


@pytest.mark.parametrize(
    "email, password, status_code, error_message",
    [
        ("wrongemail@gmail.com", "Password123", 403, "Invalid Credentials"),
        ("test@example.com", "wrongpassword", 403, "Invalid Credentials"),
        ("wrongemail@example.com", "wrongpassword", 403, "Invalid Credentials"),
    ],
)
def test_failed_login(client, email, password, status_code, error_message):
    res = client.post(
        "/login/", json={"email": email, "password": password}
    )
    assert res.status_code == status_code
    assert res.json()['detail'] == error_message


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        (None, "Password123", 422),
        ("test@example.com", None, 422),
    ],
)
def test_failed_login_missing_field(client, email, password, status_code):
    res = client.post(
        "/login/", json={"email": email, "password": password}
    )
    assert res.status_code == status_code
