#!/usr/bin/env python3
"""
Excel Database Search Tool - Command Line Interface
Ultra-fast searching for power users and automation
"""

import argparse
import os
import sys
from datetime import datetime
from search_engine import ExcelSearchEngine

class ExcelSearchCLI:
    """Command-line interface for Excel database searching"""
    
    def __init__(self):
        self.search_engine = ExcelSearchEngine()
        self.last_results = None
    
    def print_header(self):
        """Print application header"""
        print("🔍 EXCEL DATABASE SEARCH TOOL - CLI")
        print("=" * 60)
        print("Ultra-fast searching for large Excel databases")
        print()
    
    def load_file_interactive(self):
        """Interactive file loading"""
        while True:
            print("📁 Enter the path to your Excel file:")
            print("   (or 'quit' to exit)")
            
            file_path = input("File path: ").strip().strip('"')
            
            if file_path.lower() in ['quit', 'exit', 'q']:
                return False
            
            if not file_path:
                print("❌ Please enter a file path\n")
                continue
            
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}\n")
                continue
            
            print(f"\n📥 Loading file: {os.path.basename(file_path)}")
            success, message = self.search_engine.load_file(file_path)
            
            if success:
                print(f"✅ {message}")
                self.print_file_summary()
                return True
            else:
                print(f"❌ {message}\n")
    
    def print_file_summary(self):
        """Print loaded file summary"""
        file_info = self.search_engine.get_file_info()
        
        print(f"\n📊 FILE SUMMARY:")
        print(f"   📏 Size: {file_info['file_size_mb']:.2f} MB")
        print(f"   📐 Dimensions: {file_info['rows']:,} rows × {file_info['columns']} columns")
        print(f"   ⏱️  Load time: {file_info['load_time']:.2f} seconds")
        print(f"   🗂️  Columns: {', '.join(file_info['column_names'][:5])}")
        if len(file_info['column_names']) > 5:
            print(f"            ... and {len(file_info['column_names']) - 5} more")
        print()
    
    def interactive_mode(self):
        """Run in interactive mode"""
        self.print_header()
        
        # Load file
        if not self.load_file_interactive():
            print("👋 Goodbye!")
            return
        
        print("🎯 INTERACTIVE SEARCH MODE")
        print("-" * 30)
        print("Commands:")
        print("  search <term>                    - Search in first 2 columns")
        print("  search <term> -c <col1> <col2>   - Search in specific columns")
        print("  search <term> -e                 - Exact match")
        print("  search <term> -i                 - Case insensitive")
        print("  search <term> -r                 - Regex search")
        print("  columns                          - Show all columns")
        print("  info                             - Show file information")
        print("  export <filename>                - Export last results")
        print("  help                             - Show this help")
        print("  quit                             - Exit")
        print()
        
        while True:
            try:
                command = input("🔍 Enter command: ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                
                elif command.lower() == 'help':
                    self.show_help()
                
                elif command.lower() == 'columns':
                    self.show_columns()
                
                elif command.lower() == 'info':
                    self.show_file_info()
                
                elif command.startswith('export '):
                    filename = command[7:].strip()
                    self.export_last_results(filename)
                
                elif command.startswith('search '):
                    self.process_search_command(command[7:])
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                
                print()  # Add spacing between commands
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def process_search_command(self, args_str):
        """Process search command with arguments"""
        if not args_str.strip():
            print("❌ Please provide a search term")
            return
        
        # Parse arguments
        args = args_str.split()
        search_term = args[0]
        
        # Default parameters
        columns = None
        case_sensitive = True  # Default to case sensitive
        exact_match = False
        use_regex = False
        
        # Parse flags
        i = 1
        while i < len(args):
            if args[i] == '-c' and i + 1 < len(args):
                # Column specification
                i += 1
                columns = []
                while i < len(args) and not args[i].startswith('-'):
                    columns.append(args[i])
                    i += 1
            elif args[i] == '-e':
                exact_match = True
                i += 1
            elif args[i] == '-i':
                case_sensitive = False
                i += 1
            elif args[i] == '-r':
                use_regex = True
                i += 1
            else:
                i += 1
        
        # Default to first 2 columns if none specified
        if columns is None:
            all_columns = self.search_engine.get_file_info()['column_names']
            columns = all_columns[:2]  # First 2 columns as requested
        
        # Validate columns
        valid_columns = self.search_engine.get_file_info()['column_names']
        invalid_columns = [col for col in columns if col not in valid_columns]
        if invalid_columns:
            print(f"❌ Invalid columns: {invalid_columns}")
            print(f"📋 Available columns: {', '.join(valid_columns)}")
            return
        
        # Perform search
        print(f"🔍 Searching for: '{search_term}'")
        print(f"📂 In columns: {', '.join(columns)}")
        
        results, stats = self.search_engine.search(
            search_term=search_term,
            search_columns=columns,
            case_sensitive=case_sensitive,
            exact_match=exact_match,
            use_regex=use_regex
        )
        
        if 'error' in stats:
            print(f"❌ {stats['error']}")
            return
        
        # Display results
        self.display_search_results(results, stats)
        self.last_results = results
    
    def display_search_results(self, results, stats):
        """Display search results"""
        print(f"✅ Found {stats['total_results']:,} results in {stats['search_time']:.3f} seconds")
        
        if stats['total_results'] == 0:
            print("🔍 No matches found")
            return
        
        # Show first few results
        display_limit = 10
        print(f"\n📋 Results (showing first {min(len(results), display_limit)}):")
        print("-" * 80)
        
        # Get column widths for formatting
        columns = results.columns.tolist()
        col_widths = {}
        for col in columns:
            max_width = max(
                len(str(col)),
                results[col].astype(str).str.len().max() if len(results) > 0 else 0
            )
            col_widths[col] = min(max_width, 20)  # Limit column width
        
        # Print header
        header = " | ".join(f"{col:<{col_widths[col]}}" for col in columns)
        print(header)
        print("-" * len(header))
        
        # Print rows
        for i, (_, row) in enumerate(results.head(display_limit).iterrows()):
            row_str = " | ".join(
                f"{str(row[col]):<{col_widths[col]}}"[:col_widths[col]]
                for col in columns
            )
            print(row_str)
        
        if len(results) > display_limit:
            print(f"... and {len(results) - display_limit:,} more results")
    
    def show_columns(self):
        """Show all available columns"""
        columns = self.search_engine.get_file_info()['column_names']
        print("📋 Available columns:")
        for i, col in enumerate(columns, 1):
            print(f"  {i:2d}. {col}")
    
    def show_file_info(self):
        """Show detailed file information"""
        file_info = self.search_engine.get_file_info()
        column_info = self.search_engine.get_column_info()
        
        print("📊 DETAILED FILE INFORMATION")
        print("=" * 50)
        print(f"📁 File: {os.path.basename(self.search_engine.file_path)}")
        print(f"📍 Path: {self.search_engine.file_path}")
        print(f"📏 Size: {file_info['file_size_mb']:.2f} MB")
        print(f"⏱️  Load Time: {file_info['load_time']:.2f} seconds")
        print(f"📐 Dimensions: {file_info['rows']:,} rows × {file_info['columns']} columns")
        print(f"🕒 Loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📋 COLUMN DETAILS")
        print("-" * 30)
        for i, col_info in enumerate(column_info[:10], 1):  # Show first 10 columns
            print(f"{i:2d}. {col_info['name']}")
            print(f"    Type: {col_info['dtype']}")
            print(f"    Non-null: {col_info['non_null_count']:,}")
            print(f"    Unique: {col_info['unique_values']:,}")
            if col_info['sample_values']:
                samples = ', '.join(col_info['sample_values'][:2])
                print(f"    Sample: {samples}")
            print()
        
        if len(column_info) > 10:
            print(f"... and {len(column_info) - 10} more columns")
    
    def export_last_results(self, filename):
        """Export last search results"""
        if self.last_results is None or self.last_results.empty:
            print("❌ No results to export")
            return
        
        if not filename:
            print("❌ Please provide a filename")
            return
        
        # Add extension if not provided
        if not os.path.splitext(filename)[1]:
            filename += '.xlsx'
        
        success, message = self.search_engine.export_results(self.last_results, filename)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    def show_help(self):
        """Show help information"""
        print("🎯 COMMAND HELP")
        print("-" * 20)
        print("Search Commands:")
        print("  search <term>                    - Search in first 2 columns")
        print("  search john                      - Find 'john' in first 2 columns")
        print("  search john -i                   - Case insensitive search")
        print("  search 'John Doe' -e             - Exact match")
        print("  search user@email.com -c Email   - Search in Email column")
        print("  search '^\\d+$' -r               - Regex search")
        print()
        print("Other Commands:")
        print("  columns                          - List all columns")
        print("  info                             - Show file details")
        print("  export results.xlsx              - Export last results")
        print("  help                             - Show this help")
        print("  quit                             - Exit program")
    
    def run_command_line_search(self, args):
        """Run single search from command line arguments"""
        if not args.file:
            print("❌ Please provide a file path")
            return False
        
        # Load file
        print(f"📥 Loading file: {args.file}")
        success, message = self.search_engine.load_file(args.file)
        
        if not success:
            print(f"❌ {message}")
            return False
        
        print(f"✅ {message}")
        
        # Determine search columns
        columns = args.columns if args.columns else self.search_engine.get_file_info()['column_names'][:2]
        
        # Perform search
        results, stats = self.search_engine.search(
            search_term=args.search,
            search_columns=columns,
            case_sensitive=not args.ignore_case,
            exact_match=args.exact,
            use_regex=args.regex,
            max_results=args.max_results
        )
        
        if 'error' in stats:
            print(f"❌ {stats['error']}")
            return False
        
        # Display results
        self.display_search_results(results, stats)
        
        # Export if requested
        if args.output:
            success, message = self.search_engine.export_results(results, args.output)
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")
        
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Excel Database Search Tool - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python excel_search_cli.py --interactive
  python excel_search_cli.py data.xlsx -s "john" -i
  python excel_search_cli.py data.xlsx -s "user@email.com" -c Email -o results.xlsx
        """
    )
    
    parser.add_argument("file", nargs='?', help="Path to Excel file")
    parser.add_argument("-s", "--search", help="Search term")
    parser.add_argument("-c", "--columns", nargs='+', help="Columns to search in")
    parser.add_argument("-e", "--exact", action="store_true", help="Exact match")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Case insensitive")
    parser.add_argument("-r", "--regex", action="store_true", help="Use regex")
    parser.add_argument("-o", "--output", help="Output file for results")
    parser.add_argument("-m", "--max-results", type=int, help="Maximum results to show")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    cli = ExcelSearchCLI()
    
    # Interactive mode or no search term provided
    if args.interactive or not args.search:
        cli.interactive_mode()
    else:
        # Command line search
        if not args.file:
            print("❌ File path required for command line search")
            parser.print_help()
            sys.exit(1)
        
        cli.print_header()
        success = cli.run_command_line_search(args)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
