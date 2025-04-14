from pydantic import BaseModel


class NewUserApiModel(BaseModel):
     login: str
     password: str
