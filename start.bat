@echo off
title Holo3D — Futuristic 3D Gesture-Controlled Interface
color 0B

echo ======================================================================
echo             HOLO3D -- FUTURISTIC 3D AUGMENTED INTERFACE
echo                     Developed by Praveen Raja
echo ======================================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed or not in your system PATH!
    echo Please install Python 3.10+ and check "Add Python to PATH".
    echo.
    pause
    exit /b
)

echo [*] Checking dependencies...
python -c "import cv2, mediapipe, numpy, requests, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Installing missing dependencies from requirements.txt...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b
    )
)

echo [*] Starting Holo3D Interface...
echo.
echo Controls:
echo   - Press 'S' or SPACE in the window to Search ANY Object
echo   - Pinch to Move, Palm to Rotate, 2 Hands to Zoom, Fist to Hide
echo   - Keys 1-5 for 3D Models, R to Reset, Q to Quit
echo.
echo ======================================================================
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Holo3D exited with an error or code %errorlevel%.
    pause
)
