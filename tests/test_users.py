from unittest.mock import patch

from starlette.testclient import TestClient

from models import UserModel, UserRole
from repository import UserRepository
from start_api import app
from utils import password_hash

client = TestClient(app)


@patch.object(UserRepository, "get_by_login", return_value=None)
def test_login_fail_incorrect_username(mocked):
    response = client.post(
        "/users/login",
        data={"username": "fakeuser23242a", "password": "test"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


@patch.object(
    UserRepository,
    "get_by_login",
    return_value=UserModel(
        id=1,
        login="admin",
        password_hash=password_hash("not_valid"),
        role=UserRole.ADMIN,
    ),
)
def test_login_fail_incorrect_password(mocked):
    response = client.post(
        "/users/login",
        data={"username": "admin", "password": "fakepassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


def login_as_admin():
    return client.post(
        "/users/login",
        data={"username": "admin", "password": "test"},
    )


@patch.object(
    UserRepository,
    "get_by_login",
    return_value=UserModel(
        id=1,
        login="admin",
        password_hash=password_hash("test"),
        role=UserRole.ADMIN,
    ),
)
def test_login_success(mocked):
    response = login_as_admin()
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"


@patch.object(
    UserRepository,
    "get_by_login",
    return_value=UserModel(
        id=1,
        login="admin",
        password_hash=password_hash("test"),
        role=UserRole.ADMIN,
    ),
)
@patch.object(UserRepository, "create_user")
def test_user_create(mocked_login, mocked_method):
    response = login_as_admin()
    print(response.json())
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
