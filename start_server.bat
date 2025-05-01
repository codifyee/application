@echo off
echo Starting Task Management System...
echo Server will be available at http://127.0.0.1:8002

REM Activate virtual environment if it exists
IF EXIST ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) ELSE (
    echo No virtual environment found at .venv
    echo Make sure dependencies are installed globally
)

REM Run the server
python -m uvicorn taskmanager.asgi:application --host 127.0.0.1 --port 8002 --reload

pause 