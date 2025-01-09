from core.database import Optional
from pydantic import BaseModel

class UserDTO(BaseModel):

    id: str
    pw: str
    nickname: str

class LoginUser(BaseModel):
    id: str
    pw: str
