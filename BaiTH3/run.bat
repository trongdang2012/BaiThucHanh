@echo off
chcp 65001 >nul
echo ========================================================
echo KHOI DONG HE THONG DICH VU QUAN LY SAN PHAM (SOA)
echo ========================================================

echo 1. Dang khoi dong Auth Service (Port 5000)...
start "Auth Service - Port 5000" cmd /k "cd /d ""%~dp0auth_service"" && python main.py"

timeout /t 2 >nul

echo 2. Dang khoi dong Product Service (Port 5001)...
start "Product Service - Port 5001" cmd /k "cd /d ""%~dp0product_service"" && python main.py"

timeout /t 2 >nul

echo 3. Dang mo giao dien cac dich vu tren trinh duyet...
start http://localhost:5000/
start http://localhost:5001/

echo ========================================================
echo Cac dich vu da duoc bat thanh cong:
echo - Auth Service Web:    http://localhost:5000/
echo - Product Service Web: http://localhost:5001/
echo - Product API Docs:    http://localhost:5001/docs
echo - Auth API Docs:       http://localhost:5000/docs
echo ========================================================
pause
