from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from typing import List
import requests
from app.models.data_exchang import DataExchange
from app.config.database import mongodb

router = APIRouter(
    prefix='/crypto/api',
    tags=['Exchange Management'],
    responses={404:{
        'message': 'Exchange Management'
    }}
)

app = FastAPI()


data_storage= []

# ฟังก์ชันสำหรับรับข้อมูล
@router.post("/data/", response_model=DataExchange)
def receive_data(data: DataExchange):
    data_storage.append(data)
    return data

# ฟังก์ชันสำหรับดึงข้อมูลทั้งหมด
@router.get("/data/", response_model=List[DataExchange])
def get_data():
    return data_storage

# ฟังก์ชันสำหรับส่งข้อมูลไปยังระบบภายนอก
@router.post("/send-data/")
def send_data_to_external_system(data: DataExchange):
    external_url = "https://example.com/api/external"  # URL ของระบบภายนอก
    response = requests.post(external_url, json=data.dict())
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to send data")
    
    return {"message": "Data sent successfully", "response": response.json()}

# ฟังก์ชันสำหรับดึงข้อมูลจากระบบภายนอก
@router.get("/fetch-data/")
def fetch_data_from_external_system():
    external_url = "https://example.com/api/external"  # URL ของระบบภายนอก
    response = requests.get(external_url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    
    return response.json()

@router.get("/items")
async def get_items():
    items = await mongodb.db["items_collection"].find().to_list(length=100)
    
    # แปลง ObjectId ในแต่ละ item ให้เป็น string
    for item in items:
        item["_id"] = str(item["_id"])

    return jsonable_encoder(items)

