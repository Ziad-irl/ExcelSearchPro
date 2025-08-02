#!/usr/bin/env python3
"""
ExcelSearchPro - Main Launcher
=============================

Entry point for the ExcelSearchPro application.
Provides a simple menu to choose between GUI and CLI interfaces.
"""

import sys
import os
import argparse

# Add current directory to path to allow importing modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_welcome():
    """Display welcome message and menu"""
    print("""
🔍 EXCELSEARCHPRO - Fast Excel Database Search Tool
==================================================

Choose how you want to run ExcelSearchPro:

1️⃣  GUI Interface    - User-friendly graphical interface
2️⃣  CLI Interface    - Command-line interface for power users  
3️⃣  Interactive CLI  - Interactive command-line mode
4️⃣  Help            - Show detailed help and usage
5️⃣  Exit            - Exit the application

""")

def run_gui():
    """Launch the GUI interface"""
    try:
        print("🚀 Starting GUI interface...")
        import excel_search_gui
        excel_search_gui.main()
    except ImportError as e:
        print(f"❌ Error importing GUI module: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        return False
    return True

def run_cli():
    """Launch the CLI interface"""
    try:
        print("🚀 Starting CLI interface...")
        import excel_search_cli
        excel_search_cli.main()
    except ImportError as e:
        print(f"❌ Error importing CLI module: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error starting CLI: {e}")
        return False
    return True

def run_interactive_cli():
    """Launch interactive CLI mode"""
    try:
        print("🚀 Starting interactive CLI...")
        import excel_search_cli
        excel_search_cli.interactive_mode()
    except ImportError as e:
        print(f"❌ Error importing CLI module: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error starting interactive CLI: {e}")
        return False
    return True

def show_help():
    """Show detailed help information"""
    print("""
📚 EXCELSEARCHPRO HELP
=====================

COMMAND LINE OPTIONS:
  python main.py              - Show this menu
  python main.py --gui         - Launch GUI directly
  python main.py --cli         - Launch CLI directly  
  python main.py --interactive - Launch interactive CLI
  python main.py --help        - Show this help

DIRECT LAUNCH:
  python excel_search_gui.py   - GUI interface only
  python excel_search_cli.py   - CLI interface only

QUICK LAUNCHERS:
  run.bat                      - Windows batch launcher
  run.ps1                      - PowerShell launcher

FEATURES:
✅ Fast searching through millions of rows
✅ Real-time search as you type (GUI)
✅ Multiple search modes (case sensitive, exact match, regex)
✅ Unicode filename support
✅ Export search results to Excel/CSV
✅ Memory-efficient processing
✅ Cross-platform compatibility

SUPPORTED FILE FORMATS:
• Excel files (.xlsx, .xls)
• CSV files (.csv)

REQUIREMENTS:
• Python 3.8 or higher
• pandas, openpyxl, xlrd libraries

For more information, visit: https://github.com/yourusername/ExcelSearchPro
""")

def main():
    """Main launcher function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="ExcelSearchPro - Fast Excel Database Search Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--gui", action="store_true", 
                       help="Launch GUI interface directly")
    parser.add_argument("--cli", action="store_true",
                       help="Launch CLI interface directly")
    parser.add_argument("--interactive", action="store_true",
                       help="Launch interactive CLI mode")
    
    args = parser.parse_args()
    
    # Handle direct launch options
    if args.gui:
        return run_gui()
    elif args.cli:
        return run_cli()
    elif args.interactive:
        return run_interactive_cli()
    
    # Show interactive menu if no arguments provided
    try:
        while True:
            show_welcome()
            
            try:
                choice = input("Enter your choice (1-5): ").strip()
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                return True
            except EOFError:
                print("\n\n👋 Goodbye!")
                return True
            
            if choice == "1":
                success = run_gui()
                if not success:
                    input("\nPress Enter to continue...")
                    
            elif choice == "2":
                success = run_cli()
                if not success:
                    input("\nPress Enter to continue...")
                    
            elif choice == "3":
                success = run_interactive_cli()
                if not success:
                    input("\nPress Enter to continue...")
                    
            elif choice == "4":
                show_help()
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                print("\n👋 Thank you for using ExcelSearchPro!")
                return True
                
            else:
                print(f"\n❌ Invalid choice: '{choice}'. Please enter 1-5.")
                input("Press Enter to continue...")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        return True
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
