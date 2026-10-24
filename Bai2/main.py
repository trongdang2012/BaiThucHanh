# 1. Thêm import HTTPBearer và HTTPAuthorizationCredentials ở đầu file
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import datetime

app = FastAPI()
SECRET_KEY = "BiMatCuaKhoaCNTT"
ALGORITHM = "HS256"

# 2. Khai báo scheme bảo mật của FastAPI
security = HTTPBearer()

users_db = [
    {
        "IdUser": 1,
        "UserName": "admin",
        "Password": "YWRtaW4xMjM=", 
        "Token": ""
    }
]

class UserLogin(BaseModel):
    userName: str
    password: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 3. Sửa lại hàm Middleware để dùng cấu trúc của HTTPBearer
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials # Tự động bóc tách token, không cần hàm split
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

@app.post("/")
def login(user: UserLogin):
    for db_user in users_db:
        if db_user["UserName"] == user.userName and db_user["Password"] == user.password:
            access_token = create_access_token(data={"sub": user.userName})
            db_user["Token"] = access_token
            return {"message": "Đăng nhập thành công", "token": access_token}
    raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu")

@app.get("/auth")
def authenticate_token(current_user: dict = Depends(verify_token)):
    return {"message": "Xác thực thành công", "user_info": current_user}

@app.get("/hello", dependencies=[Depends(verify_token)])
def read_root():
    return {"message": "Hello World - API này đã được bảo mật bằng JWT"}