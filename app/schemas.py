from pydantic import BaseModel

class UserModel(BaseModel):

    username: str
    password: str
    email: str|None = None
    active: bool = True