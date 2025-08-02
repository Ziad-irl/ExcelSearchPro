@echo off
REM ExcelSearchPro Package Builder Script for Windows

echo 🏗️  Building ExcelSearchPro Package...
echo ======================================

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Build source distribution
echo 📦 Building source distribution...
python setup.py sdist

REM Build wheel distribution
echo 🎯 Building wheel distribution...
python setup.py bdist_wheel

REM Check the package
echo 🔍 Checking package integrity...
python -m twine check dist/*

echo.
echo ✅ Package build complete!
echo 📁 Files created in dist/ directory:
dir dist\

echo.
echo 🚀 To upload to PyPI:
echo    python -m twine upload dist/*

pause
