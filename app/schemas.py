from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

class UserModel(BaseModel):

    username: str
    password: str
    email: str|None = None
    active: bool = True