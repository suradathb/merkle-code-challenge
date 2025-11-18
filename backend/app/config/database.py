# app/config/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
import os

# ตั้งค่า URL ของ MongoDB จาก environment variable หรือ URL ตรงนี้
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")

class MongoDB:
    client: AsyncIOMotorClient = None
    db: Database = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(MONGODB_URL)
    mongodb.db = mongodb.client[DATABASE_NAME]
    print("Connected to MongoDB!")

async def close_mongo_connection():
    mongodb.client.close()
    print("Disconnected from MongoDB!")
