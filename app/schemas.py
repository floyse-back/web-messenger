from pydantic import BaseModel

class UserModel(BaseModel):

    username: str
    hashed_password: str
    email: str|None = None
    is_active: bool = True