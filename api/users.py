import sqlite3
import uuid
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.db import conn
from api.models.NewUserApiModel import NewUserApiModel
from api.token import create_access_token, Token, get_current_user
from dao.users import UserDAO, UserRole, UserModel

router = APIRouter(
    prefix="/users"
)

@router.post('/login')
async def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_user = UserDAO.get_by_login(conn, data.username)
    if db_user is None or not bcrypt.checkpw(data.password.encode('utf-8'), db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    session_id = uuid.uuid4()
    UserDAO.open_session(conn, db_user.id, session_id)
    # TODO: Magic value
    access_token = create_access_token(data={
        "uid": db_user.id,
        "scopes": [db_user.role.value],
        "sid": str(session_id)
    }, expires_delta=None)
    return Token(access_token=access_token, token_type="bearer")
@router.post('/{role}')
async def create_user(role: UserRole, new_user: NewUserApiModel):
    password_hash = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
    print(role)
    model = UserModel(
        id=None,
        login=new_user.login,
        password_hash=password_hash,
        role=role.value,
        current_session_id=None
    )
    try:
        UserDAO.create_user(conn, model)
    except sqlite3.IntegrityError:
        return {
            "status": "error",
            "message": "User already exists"
        }

    return {
        "status": "ok",
        "user": model
    }


@router.get('/me')
async def get_current_user(token: Annotated[UserModel, Depends(get_current_user)]):
    return {
        token
    }