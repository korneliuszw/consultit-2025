from models import UserRole, UserModel


def test_login_fail_incorrect_username(client):
    response = client.post(
        "/users/login",
        data={"username": "fakeuser23242a", "password": "test"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


def test_login_fail_incorrect_password(client):
    response = client.post(
        "/users/login",
        data={"username": "admin", "password": "fakepassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}


def login_as_admin(client):
    return client.post(
        "/users/login",
        data={"username": "admin", "password": "admintest"},
    )


def test_login_success(client):
    response = login_as_admin(client)
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"


def test_user_create(db, client):
    response = login_as_admin(client)
    response = client.post(
        "/users/CONSULTANT",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"},
        json={"login": "testuser", "password": "test"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "ok"
    assert response.json()["user"]["login"] == "testuser"
    assert response.json()["user"]["role"] == UserRole.CONSULTANT.value
    assert db.query(UserModel).filter_by(login="testuser").one().login == "testuser"
