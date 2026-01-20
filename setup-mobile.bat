@echo off
echo ========================================
echo   AI Debate Platform - Mobile Setup
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run this script as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo [1/3] Adding firewall rules...
echo.

REM 添加前端端口规则
netsh advfirewall firewall add rule name="AI Debate Frontend" dir=in action=allow protocol=TCP localport=5173 >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Frontend port 5173 allowed
) else (
    echo [WARNING] Frontend rule might already exist
)

REM 添加后端端口规则
netsh advfirewall firewall add rule name="AI Debate Backend" dir=in action=allow protocol=TCP localport=8000 >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Backend port 8000 allowed
) else (
    echo [WARNING] Backend rule might already exist
)

echo.
echo [2/3] Getting your IP address...
echo.

REM 获取IP地址并显示访问信息
cd backend
python get_mobile_url.py

echo.
echo [3/3] Configuration complete!
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Start the platform: run.bat
echo 2. Open the URL above on your iPhone
echo 3. Enjoy debating on mobile!
echo.
echo ========================================
pause
