from pydantic import BaseModel


class LoginApiModel(BaseModel):
    login: str
    password: str