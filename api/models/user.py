from pydantic import BaseModel


class NewUserRequest(BaseModel):
    login: str
    password: str
