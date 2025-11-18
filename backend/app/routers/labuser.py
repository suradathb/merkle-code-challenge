# app/routes/items.py
from fastapi import FastAPI,HTTPException,APIRouter
from app.config.database import mongodb
from app.models.data_users import ItemModel
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix='/crypto/api',
    tags=['Lab User CRUD'],
    responses={404:{
        'message': 'Lab User CRUD'
    }}
)


app = APIRouter()

def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in data.items()}
    else:
        return data

# Create - เพิ่มข้อมูลใหม่ใน MongoDB
@router.post("/items", response_model=ItemModel)
async def create_item(item: ItemModel):
    item_dict = item.dict(by_alias=True)
    
    # ลบฟิลด์ `_id` หรือ `id` ก่อน insert เพื่อให้ MongoDB สร้าง ObjectId ใหม่
    item_dict.pop("_id", None)
    item_dict.pop("id", None)
    
    # เพิ่มข้อมูลลงใน MongoDB
    new_item = await mongodb.db["items_collection"].insert_one(item_dict)
    created_item = await mongodb.db["items_collection"].find_one({"_id": new_item.inserted_id})
    
    # แปลง ObjectId เป็น string ก่อนส่งกลับ
    if created_item:
        created_item["_id"] = str(created_item["_id"])  # แปลง _id เป็น string
    return jsonable_encoder(created_item)

# Read - อ่านข้อมูลทั้งหมดจาก MongoDB
@router.get("/items", response_model=list[ItemModel])
async def get_items():
    items = await mongodb.db["items_collection"].find().to_list(length=100)
    return jsonable_encoder(items)

# Read - อ่านข้อมูล item ตาม id
@router.get("/items/{item_id}")
async def get_item(item_id: str):
    item = await mongodb.db["items_collection"].find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return convert_objectid_to_str(item)

# Update - อัปเดตข้อมูล item ตาม id
@router.put("/items/{item_id}", response_model=ItemModel)
async def update_item(item_id: str, item: ItemModel):
    item_dict = item.dict(by_alias=True)
    
    # ลบ _id ออกจาก item_dict เพื่อป้องกันไม่ให้อัปเดตฟิลด์นี้
    item_dict.pop("_id", None)
    item_dict.pop("id", None)
    
    # ทำการอัปเดตข้อมูลโดยใช้คำสั่ง $set
    result = await mongodb.db["items_collection"].update_one(
        {"_id": ObjectId(item_id)}, {"$set": item_dict}
    )
    
    # ตรวจสอบว่าอัปเดตสำเร็จหรือไม่
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # ค้นหาและส่งคืนข้อมูลที่อัปเดต
    updated_item = await mongodb.db["items_collection"].find_one({"_id": ObjectId(item_id)})
    
    # แปลง ObjectId เป็น string เพื่อส่งกลับได้อย่างถูกต้อง
    if updated_item:
        updated_item["_id"] = str(updated_item["_id"])
    
    return jsonable_encoder(updated_item)

# Delete - ลบข้อมูล item ตาม id
@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await mongodb.db["items_collection"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
