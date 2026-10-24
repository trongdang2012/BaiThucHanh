@echo off
chcp 65001 >nul
echo ========================================================
echo DANG TAT CAC DICH VU (Port 5000, 5001)...
echo ========================================================

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo Tat tien trinh Port 5000 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5001" ^| findstr "LISTENING"') do (
    echo Tat tien trinh Port 5001 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

echo Hoan tat! Tat ca dich vu da duoc tat an toan.
pause
