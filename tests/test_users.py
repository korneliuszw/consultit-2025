from unittest.mock import patch

import bcrypt
from starlette.testclient import TestClient

from dao.users import UserDAO, UserRole, UserModel
from start_api import app

client = TestClient(app)


@patch.object(UserDAO, "get_by_login", return_value=None)
def test_login_fail_incorrect_username(mocked):
    response = client.post(
        "/users/login",
        data={"username": "fakeuser23242a", "password": "test"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


@patch.object(
    UserDAO,
    "get_by_login",
    return_value=UserModel(
        1, "admin", bcrypt.hashpw(b"notvalid", bcrypt.gensalt()), "ADMIN", None
    ),
)
def test_login_fail_incorrect_password(mocked):
    response = client.post(
        "/users/login",
        data={"username": "admin", "password": "fakepassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


@patch.object(
    UserDAO,
    "get_by_login",
    return_value=UserModel(
        1, "admin", bcrypt.hashpw(b"test", bcrypt.gensalt()), "ADMIN", None
    ),
)
def login_as_admin(mocked):
    return client.post(
        "/users/login",
        data={"username": "admin", "password": "test"},
    )


def test_login_success(mocked):
    response = login_as_admin()
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"


@patch.object(UserDAO, "create_user")
def test_user_create(mocked_method):
    response = login_as_admin()
    response = client.post(
        "/users/CONSULTANT",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"},
        json={"login": "testuser", "password": "test"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["user"]["login"] == "testuser"
    assert response.json()["user"]["role"] == UserRole.CONSULTANT.value
    mocked_method.assert_called_once()
