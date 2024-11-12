from pydantic import BaseModel

# โมเดลสำหรับข้อมูลที่แลกเปลี่ยน
class DataExchange(BaseModel):
    user_id:int
    data:str