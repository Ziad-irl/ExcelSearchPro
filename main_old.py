#!/usr/bin/env python3
"""
Excel Database Search Tool - Main Launcher
Choose between GUI and CLI versions
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['pandas', 'openpyxl', 'xlrd']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def show_banner():
    """Display application banner"""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "🔍 EXCEL DATABASE SEARCH TOOL" + " " * 13 + "║")
    print("║" + " " * 18 + "Fast • Powerful • Easy to Use" + " " * 11 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

def show_menu():
    """Display main menu"""
    print("Choose your interface:")
    print()
    print("1. 🖥️  GUI Version (Recommended)")
    print("   • Beautiful graphical interface")
    print("   • Real-time search as you type")
    print("   • Easy file browsing and column selection")
    print("   • Perfect for beginners")
    print()
    print("2. ⚡ Command Line Version (Power Users)")
    print("   • Ultra-fast performance")
    print("   • Scriptable and automatable")
    print("   • Interactive or batch mode")
    print("   • Perfect for large databases")
    print()
    print("3. 📚 Show Documentation")
    print("4. 🔧 Check System Requirements")
    print("5. ❌ Exit")
    print()

def run_gui():
    """Launch GUI version"""
    try:
        print("🚀 Starting GUI version...")
        print("   (The application window should open shortly)")
        
        # Try to run the GUI
        import excel_search_gui
        excel_search_gui.main()
        
    except ImportError as e:
        print(f"❌ Error importing GUI module: {e}")
        print("   Make sure excel_search_gui.py is in the same directory")
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")

def run_cli():
    """Launch CLI version"""
    try:
        print("🚀 Starting CLI version...")
        print()
        
        # Import and run CLI
        import excel_search_cli
        cli = excel_search_cli.ExcelSearchCLI()
        cli.interactive_mode()
        
    except ImportError as e:
        print(f"❌ Error importing CLI module: {e}")
        print("   Make sure excel_search_cli.py is in the same directory")
    except Exception as e:
        print(f"❌ Error starting CLI: {e}")

def show_documentation():
    """Show basic documentation"""
    print("📚 QUICK START GUIDE")
    print("=" * 50)
    print()
    print("🎯 Purpose:")
    print("   Fast searching through large Excel databases with millions of rows")
    print()
    print("📁 Supported File Formats:")
    print("   • Excel files (.xlsx, .xls)")
    print("   • CSV files (.csv)")
    print()
    print("🔍 Search Features:")
    print("   • Real-time search (GUI)")
    print("   • Case sensitive/insensitive")
    print("   • Exact match or partial match")
    print("   • Regular expressions")
    print("   • Multiple column selection")
    print("   • Export search results")
    print()
    print("⚡ Performance:")
    print("   • Loads entire file into memory for instant searches")
    print("   • Handles millions of rows efficiently")
    print("   • Search times typically under 0.1 seconds")
    print()
    print("🎮 How to Use:")
    print("   GUI Version:")
    print("   1. Click 'Browse Excel File' and select your database")
    print("   2. Click 'Load File' and wait for it to load")
    print("   3. Select which columns to search (first 2 auto-selected)")
    print("   4. Type in search box - results appear instantly!")
    print("   5. Export results if needed")
    print()
    print("   CLI Version:")
    print("   1. Enter file path when prompted")
    print("   2. Use commands like: search john")
    print("   3. Use flags: -c ColumnName, -i (case insensitive), -e (exact)")
    print("   4. Type 'help' for all commands")
    print()

def check_system():
    """Check system requirements"""
    print("🔧 SYSTEM CHECK")
    print("=" * 30)
    print()
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major >= 3 and python_version.minor >= 6:
        print("   ✅ Python version is compatible")
    else:
        print("   ❌ Python 3.6+ required")
    print()
    
    # Check dependencies
    print("📦 Required Packages:")
    packages = [
        ('pandas', 'Data manipulation and Excel file handling'),
        ('openpyxl', 'Excel file reading/writing (.xlsx)'),
        ('xlrd', 'Legacy Excel file support (.xls)'),
        ('tkinter', 'GUI framework (usually built-in)')
    ]
    
    all_good = True
    for package, description in packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} (MISSING)")
            all_good = False
    
    print()
    if all_good:
        print("🎉 All requirements satisfied! You're ready to go.")
    else:
        print("⚠️  Some packages are missing. Install them with:")
        print("   pip install pandas openpyxl xlrd")
    
    # Check available memory (rough estimate)
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        print(f"\n💾 Available RAM: {memory_gb:.1f} GB")
        if memory_gb >= 4:
            print("   ✅ Sufficient memory for large files")
        else:
            print("   ⚠️  Limited memory - consider smaller files")
    except ImportError:
        print("\n💾 Memory info unavailable (psutil not installed)")
        print("   💡 For memory info, install with: pip install psutil")

def main():
    """Main launcher function"""
    show_banner()
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Cannot start application due to missing dependencies.")
        input("Press Enter to exit...")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                print()
                run_gui()
                break
                
            elif choice == '2':
                print()
                run_cli()
                break
                
            elif choice == '3':
                print()
                show_documentation()
                input("\nPress Enter to continue...")
                print()
                
            elif choice == '4':
                print()
                check_system()
                input("\nPress Enter to continue...")
                print()
                
            elif choice == '5':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                print()
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print()

if __name__ == "__main__":
    main()
