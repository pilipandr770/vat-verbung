@echo off
REM Promotion Hub - Start Script for Windows
REM Run this to start the automation system

echo.
echo ╔════════════════════════════════════════╗
echo ║   PROMOTION HUB - Starting...           ║
echo ╚════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please copy .env.example to .env and fill in your credentials
    pause
    exit /b 1
)

REM Run system check first
echo Running pre-flight checks...
python system_check.py
if errorlevel 1 (
    echo.
    echo Pre-flight checks failed. Please fix errors above.
    pause
    exit /b 1
)

REM Run main application
echo.
echo Starting Promotion Hub...
echo.
python main.py

REM If we get here, app exited
echo.
echo Application exited. Check logs/promotion_hub.log for details.
pause
