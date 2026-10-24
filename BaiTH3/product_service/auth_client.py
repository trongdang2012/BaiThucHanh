import requests
import jwt
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

AUTH_SERVICE_URL = "http://localhost:5000/auth"
SECRET_KEY = "BiMatCuaKhoaCNTT"
ALGORITHM = "HS256"

security = HTTPBearer(auto_error=False)

def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yeu cau token xac thuc (Bearer token)"
        )
    token = credentials.credentials

    try:
        res = requests.get(
            AUTH_SERVICE_URL,
            headers={"Authorization": f"Bearer {token}"},
            timeout=3.0
        )
        if res.status_code == 200:
            return res.json().get("user_info", {})
        elif res.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token khong hop le hoac da het han tu Auth Service"
            )
    except requests.RequestException:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token da het han")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token khong hop le")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Xac thuc that bai")
