<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Excel Database Search Tool - Copilot Instructions

This project is a Python-based Excel database search tool with both GUI and command-line interfaces.

## Project Structure
- `excel_search_gui.py` - Main GUI application using tkinter
- `excel_search_cli.py` - Command-line interface version
- `search_engine.py` - Core search functionality
- `utils.py` - Helper utilities

## Key Requirements
- Fast searching through large Excel files (millions of rows)
- Real-time search as user types
- Multiple search options (case sensitive, exact match, regex)
- Support for .xlsx, .xls, and .csv files
- Export search results functionality
- Memory-efficient handling of large datasets

## Libraries Used
- pandas: Data manipulation and Excel file handling
- tkinter: GUI framework
- openpyxl: Excel file reading/writing
- xlrd: Legacy Excel file support

## Coding Guidelines
- Use pandas for all data operations for performance
- Implement vectorized operations instead of loops
- Use proper error handling for file operations
- Keep GUI responsive with threading for large operations
- Follow PEP 8 style guidelines
- Add comprehensive docstrings and comments
