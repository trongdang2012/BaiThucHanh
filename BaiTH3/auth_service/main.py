from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import jwt
import datetime
import uvicorn
import base64

app = FastAPI(title="Auth Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "BiMatCuaKhoaCNTT"
ALGORITHM = "HS256"

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
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token da het han"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token khong hop le"
        )

def check_credentials(input_pwd: str, stored_pwd: str) -> bool:
    if input_pwd == stored_pwd:
        return True
    try:
        decoded = base64.b64decode(stored_pwd).decode("utf-8")
        if input_pwd == decoded:
            return True
    except Exception:
        pass
    return False

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SOA Authentication Service</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
            body { background: #f8fafc; color: #1e293b; padding: 32px 20px; line-height: 1.5; }
            .container { max-width: 820px; margin: 0 auto; }
            .header { display: flex; justify-content: space-between; align-items: center; background: white; padding: 20px 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 24px; }
            .title { font-size: 20px; font-weight: 700; color: #0f172a; }
            .subtitle { font-size: 13px; color: #64748b; }
            .nav-link { font-size: 13px; font-weight: 600; text-decoration: none; padding: 7px 14px; border-radius: 8px; background: #eef2ff; color: #4f46e5; border: 1px solid #c7d2fe; transition: all 0.2s; }
            .nav-link:hover { background: #e0e7ff; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
            @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
            .card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 22px; }
            .card-title { font-size: 16px; font-weight: 700; margin-bottom: 14px; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; }
            .form-group { margin-bottom: 14px; }
            .form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 5px; color: #475569; }
            .form-group input, .form-group textarea { width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; font-family: inherit; }
            .btn { width: 100%; background: #4f46e5; color: white; padding: 9px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; transition: background 0.2s; }
            .btn:hover { background: #4338ca; }
            .btn-secondary { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; margin-top: 8px; }
            .btn-secondary:hover { background: #e2e8f0; }
            .output { margin-top: 14px; background: #0f172a; color: #38bdf8; padding: 12px; border-radius: 8px; font-size: 12px; word-break: break-all; min-height: 48px; max-height: 160px; overflow-y: auto; white-space: pre-wrap; }
            .account-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-size: 13px; color: #64748b; margin-bottom: 16px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header class="header">
                <div>
                    <h1 class="title">SOA Authentication Service</h1>
                    <p class="subtitle">Dịch vụ Xác thực Tập trung • Cổng 5000</p>
                </div>
                <div style="display: flex; gap: 10px;">
                    <a href="http://localhost:5001" class="nav-link">Mở Product Service (5001)</a>
                    <a href="/docs" target="_blank" class="nav-link">API Docs (Swagger)</a>
                </div>
            </header>

            <div class="account-box">
                <strong>Tài khoản mặc định:</strong> Tên đăng nhập: <code>admin</code> | Mật khẩu: <code>admin123</code>
            </div>

            <div class="grid">
                <div class="card">
                    <h2 class="card-title">1. Đăng nhập & Tạo Token (POST /login)</h2>
                    <div class="form-group">
                        <label>Tên đăng nhập</label>
                        <input type="text" id="login-user" value="admin">
                    </div>
                    <div class="form-group">
                        <label>Mật khẩu</label>
                        <input type="password" id="login-pwd" value="admin123">
                    </div>
                    <button class="btn" onclick="executeLogin()">Thực hiện Đăng nhập</button>
                    <div class="output" id="login-result">Kết quả phản hồi sẽ hiển thị ở đây...</div>
                    <button class="btn btn-secondary" onclick="copyToken()">Sao chép Token</button>
                </div>

                <div class="card">
                    <h2 class="card-title">2. Xác thực Token (GET /auth)</h2>
                    <div class="form-group">
                        <label>Chuỗi Bearer Token</label>
                        <textarea id="auth-token-input" rows="4" placeholder="Dán JWT Token vào đây..."></textarea>
                    </div>
                    <button class="btn" onclick="executeAuth()">Kiểm tra Xác thực Token</button>
                    <div class="output" id="auth-result">Kết quả giải mã sẽ hiển thị ở đây...</div>
                </div>
            </div>
        </div>

        <script>
            let lastToken = "";
            async function executeLogin() {
                const u = document.getElementById("login-user").value;
                const p = document.getElementById("login-pwd").value;
                const out = document.getElementById("login-result");
                out.textContent = "Đang gửi yêu cầu xác thực...";
                try {
                    const res = await fetch("/login", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ userName: u, password: p })
                    });
                    const data = await res.json();
                    out.textContent = JSON.stringify(data, null, 2);
                    if (data.token) {
                        lastToken = data.token;
                        document.getElementById("auth-token-input").value = data.token;
                    }
                } catch (e) {
                    out.textContent = "Lỗi kết nối: " + e.message;
                }
            }

            async function executeAuth() {
                const token = document.getElementById("auth-token-input").value.trim();
                const out = document.getElementById("auth-result");
                if (!token) {
                    out.textContent = "Vui lòng nhập chuỗi token!";
                    return;
                }
                out.textContent = "Đang kiểm tra token...";
                try {
                    const res = await fetch("/auth", {
                        headers: { "Authorization": "Bearer " + token }
                    });
                    const data = await res.json();
                    out.textContent = JSON.stringify(data, null, 2);
                } catch (e) {
                    out.textContent = "Lỗi: " + e.message;
                }
            }

            function copyToken() {
                if (!lastToken) {
                    alert("Chưa có token. Vui lòng đăng nhập trước!");
                    return;
                }
                navigator.clipboard.writeText(lastToken);
                alert("Đã sao chép token vào bộ nhớ tạm!");
            }
        </script>
    </body>
    </html>
    """

@app.post("/login")
@app.post("/")
def login(user: UserLogin):
    for db_user in users_db:
        if db_user["UserName"] == user.userName and check_credentials(user.password, db_user["Password"]):
            access_token = create_access_token(data={"sub": user.userName, "user_id": db_user["IdUser"]})
            db_user["Token"] = access_token
            return {
                "message": "Dang nhap thanh cong",
                "token": access_token
            }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sai ten dang nhap hoac mat khau"
    )

@app.get("/auth")
def authenticate_token(current_user: dict = Depends(verify_token)):
    return {
        "message": "Xac thuc thanh cong",
        "user_info": current_user
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "auth_service", "port": 5000}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
