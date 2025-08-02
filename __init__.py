"""
ExcelSearchPro - Fast Excel Database Search Tool
===============================================

A powerful, user-friendly tool for searching through large Excel databases
with both GUI and command-line interfaces.

Features:
- Real-time search as you type
- Support for millions of rows
- Multiple search modes (case sensitive, exact match, regex)
- Unicode filename support
- Export search results
- Memory-efficient processing

Author: ExcelSearchPro Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "ExcelSearchPro Team"
__license__ = "MIT"

# Import main classes for easy access
try:
    from .search_engine import ExcelSearchEngine
    from .excel_search_gui import ExcelSearchGUI
    __all__ = ['ExcelSearchEngine', 'ExcelSearchGUI']
except ImportError:
    # Handle case where package is run directly
    pass
