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

REM Auto-train model if pkl files are missing
IF NOT EXIST "model.pkl" (
    echo [INFO] model.pkl not found. Training model now...
    python train_model.py
    IF ERRORLEVEL 1 (
        echo [ERROR] Model training failed. Please check train_model.py and try again.
        pause
        exit /b 1
    )
    echo [INFO] Model trained successfully!
    echo.
) ELSE (
    echo [INFO] model.pkl found. Skipping training.
)

echo.
echo [INFO] Opening browser...
start http://127.0.0.1:5000

echo [INFO] Starting Flask server...
echo [INFO] Press Ctrl+C in this window to stop the server.
echo.
python app.py

pause
