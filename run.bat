@echo off
chcp 65001 >nul
title Excel Database Search Tool
color 0A

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.6+ from https://python.org
    echo.
    pause
    exit /b 1
)

:: Run the main launcher
echo.
echo 🚀 Starting Excel Database Search Tool...
echo    Supports Unicode filenames like: نتيجة الثانوية العامة 2025.xlsx
echo.
python main.py

:: Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Press any key to exit...
    pause >nul
)
