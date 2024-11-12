from fastapi import FastAPI
from app.routers import labexchang,user_management,exchange
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือระบุโดเมนที่อนุญาต
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def config_router():
    app.include_router(labexchang.router)
    app.include_router(user_management.router)
    app.include_router(exchange.router)
config_router()