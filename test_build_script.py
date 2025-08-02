#!/usr/bin/env python3
"""
Test script to verify build_exe.py improvements work correctly
"""

import sys
import os
from pathlib import Path

def test_build_script():
    """Test the build script without actually building executables"""
    print("TESTING BUILD SCRIPT IMPROVEMENTS")
    print("=" * 50)
    
    # Import our build functions
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from build_exe import check_dependencies, check_pyinstaller
        
        print("[TEST] Testing dependency checker...")
        if check_dependencies():
            print("[OK] Dependency checker works")
        else:
            print("[ERROR] Dependency checker failed")
            
        print("\n[TEST] Testing PyInstaller checker...")
        if check_pyinstaller():
            print("[OK] PyInstaller checker works")
        else:
            print("[ERROR] PyInstaller checker failed")
            
        print("\n[TEST] Testing required files check...")
        required_files = ['main.py', 'excel_search_gui.py', 'excel_search_cli.py']
        all_exist = True
        for file_name in required_files:
            if Path(file_name).exists():
                print(f"[OK] Found {file_name}")
            else:
                print(f"[ERROR] Missing {file_name}")
                all_exist = False
        
        if all_exist:
            print("[OK] All required files present")
        else:
            print("[ERROR] Some required files missing")
            
        print("\n[TEST] Testing OS detection...")
        print(f"[INFO] OS name: {os.name}")
        print(f"[INFO] Platform: {sys.platform}")
        
        if os.name == 'nt':
            print("[INFO] Windows detected - will use ';' for --add-data")
        else:
            print("[INFO] Unix-like system detected - will use ':' for --add-data")
            
        print("\n[SUCCESS] Build script tests completed!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == "__main__":
    test_build_script()
