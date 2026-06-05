@echo off
echo =========================================
echo      Starting Plan E - F1 Telemetry
echo =========================================

echo.
echo Starting Backend (FastAPI)...
start "PlanE Backend" cmd /k "cd PlanE-backend && IF EXIST .venv\Scripts\activate (call .venv\Scripts\activate && echo Virtual environment activated.) ELSE (echo WARNING: No .venv found! If you haven't yet, you may need to set one up and install requirements.) && python -m uvicorn main:app --reload --port 8000"

echo.
echo Starting Frontend (Vanilla JS)...
start "PlanE Frontend" cmd /k "cd PlanE-frontend && python dev_server.py"

echo.
echo Both servers have been started in separate windows!
echo Wait a moment for the servers to initialize.
echo You can close this window now.
pause
