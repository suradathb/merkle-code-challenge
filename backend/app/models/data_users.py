from pydantic import BaseModel

# โมเดลผู้ใช้
class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str