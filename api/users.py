import sqlite3
import uuid
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import create_access_token, Token, AdminRequired, AnyUser
from api.schemas.user import NewUserSchema
from database import SessionDep
from models import UserRole, UserModel
from repository import UserRepository
from utils import password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login_user(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    db_user = UserRepository.get_by_login(session, data.username)
    if db_user is None or not bcrypt.checkpw(
        data.password.encode("utf-8"), db_user.password_hash
    ):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    session_id = uuid.uuid4()
    db_user.current_session_id = session_id
    session.commit()
    if db_user.role == UserRole.ADMIN:
        scopes = [
            UserRole.ADMIN.value,
            UserRole.CONSULTANT.value,
            UserRole.SERVICEMAN.value,
        ]
    else:
        scopes = [db_user.role.value]
    access_token = create_access_token(
        data={"uid": db_user.id, "scopes": scopes, "sid": str(session_id)},
        expires_delta=None,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/{role}", status_code=201, responses={409: {"description": "User already exists"}}
)
async def create_user(
    _: AdminRequired, role: UserRole, new_user: NewUserSchema, session: SessionDep
):
    model = UserModel(
        login=new_user.login,
        password_hash=password_hash(new_user.password),
        role=role.value,
        current_session_id=None,
    )
    try:
        UserRepository.create_user(session, model)
    except sqlite3.IntegrityError:
        raise HTTPException(409, "User already exists")

    return {"status": "ok", "user": model}


@router.get("/me")
async def get_current_user(user: AnyUser):
    return user
