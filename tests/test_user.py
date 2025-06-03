import pytest
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from backend.managers.auth import AuthManager
from tests.factories import UserFactory


def test_create_user_success(session):
    user_data = {
        "name": "Ivan Petkov",
        "email": "ivan@example.com",
        "password": "secondPass123",
        "role": "employee"
    }

    user = AuthManager.create_user(user_data)

    assert user.id is not None
    assert user.email == "ivan@example.com"
    assert user.name == "Ivan Petkov"
    assert user.password != "secondPass123"
    assert check_password_hash(user.password, "secondPass123")


def test_login_user_success(session):
    plain_password = "mySecret123"
    hashed_password = generate_password_hash(plain_password)
    user = UserFactory(password=hashed_password, email="test@login.com")

    user_from_login = AuthManager.login_user({
        "email": user.email,
        "password": plain_password
    })

    assert user_from_login.id == user.id


def test_login_user_wrong_email(session):
    with pytest.raises(BadRequest) as exc:
        AuthManager.login_user({
            "email": "nonexistent@email.com",
            "password": "whatever"
        })
    assert "Invalid email or password" in str(exc.value)


def test_login_user_wrong_password(session):
    user = UserFactory(password="correctpass", email="user@wrongpass.com")

    with pytest.raises(BadRequest) as exc:
        AuthManager.login_user({
            "email": user.email,
            "password": "wrongpass"
        })
    assert "Invalid email or password" in str(exc.value)
