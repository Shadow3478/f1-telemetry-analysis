@echo off
echo =========================================
echo      Clearing FastF1 Cache
echo =========================================
echo.

cd PlanE-backend
IF EXIST .venv\Scripts\activate (
    call .venv\Scripts\activate
    echo Virtual environment activated.
) ELSE (
    echo Using system Python.
)

python clear_cache.py

echo.
echo =========================================
echo Done! Press any key to exit.
pause >nul
