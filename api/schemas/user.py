from pydantic import BaseModel


class NewUserSchema(BaseModel):
    login: str
    password: str
