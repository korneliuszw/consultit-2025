from models import UserModel, UserRole
from repository import UserRepository
from utils import password_hash


def create_admin(session, login, password):
    if len(login) < 2 or len(password) < 2:
        raise Exception("Login and password must be at least 2 characters")
    UserRepository.create_user(
        session,
        UserModel(
            login=login,
            password_hash=password_hash(password),
            role=UserRole.ADMIN,
        ),
    )
    session.commit()
