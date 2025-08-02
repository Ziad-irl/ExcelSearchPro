#!/usr/bin/env python3
"""
ExcelSearchPro Installation Script
Handles installation and setup for ExcelSearchPro
"""

import sys
import subprocess
import os
import platform


def check_python_version():
    """Check if Python version is supported"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Update pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def create_shortcuts():
    """Create desktop shortcuts and start menu entries"""
    system = platform.system()
    
    if system == "Windows":
        create_windows_shortcuts()
    elif system == "Darwin":  # macOS
        create_macos_shortcuts()
    elif system == "Linux":
        create_linux_shortcuts()


def create_windows_shortcuts():
    """Create Windows shortcuts"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        # Get desktop and start menu paths
        desktop = winshell.desktop()
        start_menu = winshell.start_menu()
        
        # Create desktop shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(os.path.join(desktop, "ExcelSearchPro.lnk"))
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{os.path.join(os.getcwd(), "main.py")}"'
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("✅ Desktop shortcut created")
        
    except ImportError:
        print("⚠️  Could not create shortcuts (optional feature)")
    except Exception as e:
        print(f"⚠️  Could not create shortcuts: {e}")


def create_macos_shortcuts():
    """Create macOS shortcuts (Automator apps)"""
    # This would require creating .app bundles
    print("ℹ️  Manual shortcut creation on macOS:")
    print("   1. Open Automator")
    print("   2. Create new Application")
    print(f"   3. Add 'Run Shell Script' action with: python3 '{os.path.join(os.getcwd(), 'main.py')}'")
    print("   4. Save as 'ExcelSearchPro.app'")


def create_linux_shortcuts():
    """Create Linux desktop entries"""
    try:
        desktop_file_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=ExcelSearchPro
Comment=Fast Excel Database Search Tool
Exec=python3 "{os.path.join(os.getcwd(), 'main.py')}"
Icon=accessories-calculator
Terminal=false
Categories=Office;Utility;
StartupNotify=true
"""
        
        # Try to create desktop entry
        desktop_dir = os.path.expanduser("~/.local/share/applications")
        os.makedirs(desktop_dir, exist_ok=True)
        
        with open(os.path.join(desktop_dir, "excelsearchpro.desktop"), "w") as f:
            f.write(desktop_file_content)
        
        print("✅ Desktop entry created")
        
    except Exception as e:
        print(f"⚠️  Could not create desktop entry: {e}")


def run_verification():
    """Run the verification script"""
    print("\n🔍 Running verification tests...")
    
    try:
        result = subprocess.run([sys.executable, "verify_setup.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Verification passed!")
            return True
        else:
            print("❌ Verification failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running verification: {e}")
        return False


def main():
    """Main installation function"""
    print("🔍 EXCELSEARCHPRO INSTALLATION")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Run verification
    if not run_verification():
        print("\n⚠️  Installation completed but verification failed")
        print("   You can still try running the application manually")
    
    # Create shortcuts (optional)
    print("\n🔗 Creating shortcuts...")
    create_shortcuts()
    
    print("\n🎉 INSTALLATION COMPLETE!")
    print("=" * 50)
    print("🚀 You can now run ExcelSearchPro using:")
    print("   • Double-click the desktop shortcut (if created)")
    print("   • Run: python main.py")
    print("   • Run: python excel_search_gui.py (GUI only)")
    print("   • Run: python excel_search_cli.py --interactive (CLI only)")
    print("   • Use the batch files: run.bat or run.ps1")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\n❌ Installation failed. Press Enter to exit...")
            sys.exit(1)
        else:
            input("\n✅ Installation successful! Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
