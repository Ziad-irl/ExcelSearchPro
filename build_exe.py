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
        print("✅ PyInstaller is available")
        return True
    except ImportError:
        print("❌ PyInstaller not found")
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_icon():
    """Create a simple icon file (optional)"""
    # We'll skip this for now, PyInstaller can use a default icon
    pass

def build_gui_exe():
    """Build GUI executable"""
    print("\n🏗️  Building GUI Executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window for GUI
        "--name", "ExcelSearchPro-GUI", # Output name
        "--add-data", "requirements.txt;.",  # Include requirements
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl", 
        "--hidden-import", "xlrd",
        "--hidden-import", "tkinter",
        "excel_search_gui.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ GUI executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build GUI executable: {e}")
        return False

def build_cli_exe():
    """Build CLI executable"""
    print("\n🏗️  Building CLI Executable...")
    
    cmd = [
        "pyinstaller", 
        "--onefile",                    # Single executable file
        "--console",                    # Keep console window for CLI
        "--name", "ExcelSearchPro-CLI", # Output name
        "--add-data", "requirements.txt;.",  # Include requirements
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "xlrd", 
        "excel_search_cli.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ CLI executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build CLI executable: {e}")
        return False

def build_main_exe():
    """Build main launcher executable"""
    print("\n🏗️  Building Main Launcher Executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--console",                    # Keep console for menu
        "--name", "ExcelSearchPro",     # Output name
        "--add-data", "requirements.txt;.",  # Include requirements  
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "xlrd",
        "--hidden-import", "tkinter",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Main launcher executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build main executable: {e}")
        return False

def create_installer_script():
    """Create a simple installer batch script"""
    installer_content = """@echo off
echo 🔍 ExcelSearchPro Installation
echo ==============================
echo.

echo 📁 Creating installation directory...
set "INSTALL_DIR=%USERPROFILE%\\ExcelSearchPro"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 📦 Copying files...
copy "ExcelSearchPro.exe" "%INSTALL_DIR%\\" >nul
copy "ExcelSearchPro-GUI.exe" "%INSTALL_DIR%\\" >nul  
copy "ExcelSearchPro-CLI.exe" "%INSTALL_DIR%\\" >nul
copy "README.md" "%INSTALL_DIR%\\" >nul

echo 🔗 Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\ExcelSearchPro.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\ExcelSearchPro.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "ExcelSearchPro - Fast Excel Database Search" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul 2>&1
del CreateShortcut.vbs >nul 2>&1

echo.
echo ✅ Installation complete!
echo 📍 Installed to: %INSTALL_DIR%
echo 🖥️  Desktop shortcut created
echo 🚀 Double-click desktop shortcut to run
echo.
pause
"""
    
    with open("install.bat", "w") as f:
        f.write(installer_content)
    
    print("✅ Installer script created: install.bat")

def create_release_package():
    """Create a release package with all executables"""
    print("\n📦 Creating Release Package...")
    
    # Create release directory
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy executables
    dist_dir = Path("dist")
    if dist_dir.exists():
        for exe_file in dist_dir.glob("*.exe"):
            shutil.copy2(exe_file, release_dir)
            print(f"✅ Copied {exe_file.name}")
    
    # Copy documentation
    files_to_copy = ["README.md", "LICENSE", "requirements.txt"]
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, release_dir)
            print(f"✅ Copied {file_name}")
    
    # Copy installer
    if Path("install.bat").exists():
        shutil.copy2("install.bat", release_dir)
        print("✅ Copied install.bat")
    
    print(f"\n🎉 Release package created in: {release_dir.absolute()}")
    return release_dir

def clean_build_files():
    """Clean up build artifacts"""
    print("\n🧹 Cleaning up build files...")
    
    dirs_to_remove = ["build", "__pycache__"]
    for dir_name in dirs_to_remove:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}")
    
    # Remove .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"✅ Removed {spec_file}")

def main():
    """Main build function"""
    print("🏗️  EXCELSEARCHPRO EXECUTABLE BUILDER")
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
        print("\n❌ No executables were created successfully")
        return False
    
    # Create installer and package
    create_installer_script()
    release_dir = create_release_package()
    
    # Show results
    print("\n🎉 BUILD COMPLETE!")
    print("=" * 50)
    print(f"✅ Created {success_count}/3 executables")
    print(f"📁 Release package: {release_dir.absolute()}")
    print("\n📋 Files created:")
    
    if Path("dist").exists():
        for exe_file in Path("dist").glob("*.exe"):
            file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
            print(f"   • {exe_file.name} ({file_size:.1f} MB)")
    
    print(f"\n🚀 Distribution options:")
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
            input("\n❌ Build failed. Press Enter to exit...")
            sys.exit(1)
        else:
            input(f"\n✅ Build successful! Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during build: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
