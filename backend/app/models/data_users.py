from pydantic import BaseModel,Field
from bson import ObjectId


# โมเดลผู้ใช้
class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

class ItemModel(BaseModel):
    id: str =  Field(alias = "_id",default = None) # เปลี่ยน ObjectId เป็น str
    name:str
    description:str = None
    price:float
    quantity:int

    class Config:
        arbitrary_types_allowed = True  # อนุญาตให้ใช้ชนิดข้อมูลพิเศษจาก MongoDB
        json_encoders = {ObjectId: str}  # แปลง ObjectId เป็น string