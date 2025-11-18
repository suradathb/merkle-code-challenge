from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from app.config.database import mongodb
from datetime import datetime, timedelta
from app.models.data_users import User,UserInDB
import jwt
import os
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  # ใช้ค่า default ถ้าไม่มีใน .env
ALGORITHM = "HS256"

router = APIRouter(
    prefix='/crypto/api',
    tags=['User Management'],
    responses={404:{
        'message': 'User Management'
    }}
)

app = FastAPI()
# ตั่งค่าการเข้ารหัสรหัสผ่าน
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ฟังก์ชันสำหรับเข้ารหัสรหัสผ่าน
def hash_password(password: str):
    return pwd_context.hash(password)

# ฟังก์ชันสำหรับตรวจสอบรหัสผ่าน
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ตัวแปรเก็บข้อมูลผู้ใช้
fake_users_db = {
    "user1": {
        "username": "user1",
        "email": "user1@example.com",
        "full_name": "User One",
        "hashed_password": pwd_context.hash("P@ssw0rd1"),
        "disabled": False,
    },
    "user2": {
        "username": "user2",
        "email": "user2@example.com",
        "full_name": "User Two",
        "hashed_password": pwd_context.hash("P@ssw0rd2"),
        "disabled": True,
    },
}

# ฟังก์ชันสำหรับสร้าง token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ฟังก์ชันสำหรับสร้างผู้ใช้ใหม่
@router.post("/users/", response_model=User)
def create_user(user: User, password: str):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(password)
    fake_users_db[user.username] = UserInDB(**user.dict(), hashed_password=hashed_password)
    return user

# ฟังก์ชันสำหรับดึงข้อมูลผู้ใช้
@router.get("/users/{username}", response_model=User)
def read_user(username: str):
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ฟังก์ชันสำหรับเข้าสู่ระบบ
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

# ฟังก์ชันสำหรับตรวจสอบสิทธิ์การเข้าถึง
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return User(**user)  # คืนค่าข้อมูลผู้ใช้ที่ถูกต้อง

# ฟังก์ชันสำหรับดึงข้อมูลผู้ใช้ที่เข้าสู่ระบบ
@router.get("/users/me", response_model=User)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users")
async def get_users():
    users = await mongodb.db["user_collection"].find().to_list(length=100)
    
    # แปลง ObjectId ในแต่ละ item ให้เป็น string
    for user in users:
        user["_id"] = str(user["_id"])

    return jsonable_encoder(users)

