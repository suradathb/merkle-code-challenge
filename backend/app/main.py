from fastapi import FastAPI
from app.routers import labexchang,user_management,exchange,labuser
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import connect_to_mongo,close_mongo_connection


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือระบุโดเมนที่อนุญาต
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# เรียกใช้ฟังก์ชันเมื่อแอปเริ่มต้น
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

# เรียกใช้ฟังก์ชันเมื่อแอปปิดตัวลง
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

def config_router():
    app.include_router(labexchang.router)
    app.include_router(user_management.router)
    app.include_router(exchange.router)
    app.include_router(labuser.router)
config_router()