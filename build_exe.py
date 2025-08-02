#!/usr/bin/env python3
"""
ExcelSearchPro Executable Builder
Creates standalone .exe files for distribution
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("[OK] PyInstaller is available")
        return True
    except ImportError:
        print("[ERROR] PyInstaller not found")
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[OK] PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install PyInstaller")
            return False

def build_gui_exe():
    """Build the GUI executable"""
    print("\n[BUILD] Building GUI Executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=ExcelSearchPro-GUI",
        "--icon=icon.ico",
        "--add-data=icon.ico;.",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
        "excel_search_gui.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("[OK] GUI executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to build GUI executable: {e}")
        return False

def build_cli_exe():
    """Build the CLI executable"""
    print("\n[BUILD] Building CLI Executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=ExcelSearchPro-CLI",
        "--icon=icon.ico",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
        "excel_search_cli.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("[OK] CLI executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to build CLI executable: {e}")
        return False

def build_main_exe():
    """Build the main launcher executable"""
    print("\n[BUILD] Building Main Launcher Executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=ExcelSearchPro",
        "--icon=icon.ico",
        "--add-data=icon.ico;.",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
        "main.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("[OK] Main launcher executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to build main executable: {e}")
        return False

def create_installer_script():
    """Create Windows installer batch script"""
    installer_content = '''@echo off
title ExcelSearchPro Installer
echo ================================================
echo          EXCELSEARCHPRO INSTALLER
echo ================================================

echo [INFO] Creating installation directory...
set "INSTALL_DIR=%USERPROFILE%\\ExcelSearchPro"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [INFO] Copying files...
copy "ExcelSearchPro.exe" "%INSTALL_DIR%\\" >nul
copy "ExcelSearchPro-GUI.exe" "%INSTALL_DIR%\\" >nul
copy "ExcelSearchPro-CLI.exe" "%INSTALL_DIR%\\" >nul
copy "README.md" "%INSTALL_DIR%\\" >nul
copy "LICENSE" "%INSTALL_DIR%\\" >nul

echo [INFO] Creating desktop shortcut...
set "DESKTOP=%USERPROFILE%\\Desktop"
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\\ExcelSearchPro.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\ExcelSearchPro.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "ExcelSearchPro - Fast Excel Database Search" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul
del CreateShortcut.vbs

echo.
echo [OK] Installation complete!
echo.
echo [INFO] Desktop shortcut created
echo [INFO] Double-click desktop shortcut to run
echo.
pause
'''
    
    with open("install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("[OK] Installer script created: install.bat")

def create_release_package():
    """Create release directory with all files"""
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # Copy executables
    dist_dir = Path("dist")
    if dist_dir.exists():
        for exe_file in dist_dir.glob("*.exe"):
            shutil.copy2(exe_file, release_dir)
            print(f"[OK] Copied {exe_file.name}")
    
    # Copy documentation
    files_to_copy = ["README.md", "LICENSE", "install.bat"]
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, release_dir)
            print(f"[OK] Copied {file_name}")
    
    return release_dir

def clean_build_files():
    """Clean up build artifacts"""
    print("\n[CLEANUP] Removing build artifacts...")
    
    # Remove build directories
    for dir_name in ["build", "__pycache__"]:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"[OK] Removed {dir_name}")
    
    # Remove .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"[OK] Removed {spec_file}")

def main():
    """Main build function"""
    print("EXCELSEARCHPRO EXECUTABLE BUILDER")
    print("=" * 50)
    
    # Check PyInstaller
    if not check_pyinstaller():
        return False
    
    # Build executables
    success_count = 0
    
    if build_main_exe():
        success_count += 1
    
    if build_gui_exe():
        success_count += 1
        
    if build_cli_exe():
        success_count += 1
    
    if success_count == 0:
        print("\n[ERROR] No executables were created successfully")
        return False
    
    # Create installer and package
    create_installer_script()
    release_dir = create_release_package()
    
    # Show results
    print("\n[SUCCESS] BUILD COMPLETE!")
    print("=" * 50)
    print(f"[OK] Created {success_count}/3 executables")
    print(f"[INFO] Release package: {release_dir.absolute()}")
    print("\n[INFO] Files created:")
    
    if Path("dist").exists():
        for exe_file in Path("dist").glob("*.exe"):
            file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
            print(f"   - {exe_file.name} ({file_size:.1f} MB)")
    
    print(f"\n[INFO] Distribution options:")
    print(f"   1. Share the entire 'release' folder")
    print(f"   2. Users run 'install.bat' for easy installation")
    print(f"   3. Or just share individual .exe files")
    
    # Clean up
    clean_build_files()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n[ERROR] Build failed.")
            sys.exit(1)
        else:
            print(f"\n[SUCCESS] Build successful!")
    except KeyboardInterrupt:
        print("\n\n[WARNING] Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error during build: {e}")
        sys.exit(1)
