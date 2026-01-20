@echo off
SETLOCAL EnableExtensions

echo =========================================
echo      AI Debate Platform Launcher
echo =========================================

set "PROJECT_ROOT=%~dp0"

:: 1. 启动后端服务 (Backend)
echo.
echo [1/3] Launching Backend Server...
:: 使用 python -m uvicorn 方式启动，避免 path 问题，并启用 reload
start "AI_Debate_Backend" cmd /k "cd /d "%PROJECT_ROOT%backend" && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: 2. 启动前端界面 (Frontend)
echo.
echo [2/3] Launching Frontend Server...
start "AI_Debate_Frontend" cmd /k "cd /d "%PROJECT_ROOT%frontend" && npm run dev"

:: 3. 打开浏览器
echo.
echo [3/3] Opening Browser...
echo Waiting 5 seconds for services to warm up...
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo =========================================
echo Done! Services are running.
echo Please leave the terminal windows open.
echo =========================================
pause
