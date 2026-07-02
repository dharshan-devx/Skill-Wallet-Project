@echo off
echo =======================================================
echo     Credit Card Approval Prediction App - Launcher
echo =======================================================
echo.

REM Check if the virtual environment directory exists
IF NOT EXIST "venv" (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv venv
    
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
    
    echo [INFO] Installing required dependencies...
    pip install -r requirements.txt
) ELSE (
    echo [INFO] Virtual environment found. Activating...
    call venv\Scripts\activate.bat
)

echo.
echo [INFO] Opening browser...
start http://127.0.0.1:5000

echo [INFO] Starting Flask server...
echo [INFO] Press Ctrl+C in this window to stop the server.
echo.
python app.py

pause
