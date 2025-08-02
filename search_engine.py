"""
Core search engine for Excel database searching
Provides fast, efficient searching capabilities for large datasets
"""

import pandas as pd
import re
import time
import os
from typing import List, Optional, Tuple, Dict, Any

class ExcelSearchEngine:
    """High-performance search engine for Excel databases"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.original_df: Optional[pd.DataFrame] = None
        self.file_path: str = ""
        self.load_time: float = 0
        self.file_info: Dict[str, Any] = {}
    
    def load_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Load Excel file into memory for fast searching
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            start_time = time.time()
            
            # Handle Unicode filenames
            if not os.path.exists(file_path):
                return False, f"File not found: {os.path.basename(file_path)}"
            
            # Determine file type and load accordingly
            if file_path.lower().endswith('.csv'):
                # Try different encodings for CSV files
                encodings = ['utf-8', 'utf-8-sig', 'cp1256', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        self.df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    return False, "Could not read CSV file with any supported encoding"
                    
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                # Use openpyxl for .xlsx, xlrd for .xls
                engine = 'openpyxl' if file_path.lower().endswith('.xlsx') else 'xlrd'
                self.df = pd.read_excel(file_path, engine=engine)
            else:
                return False, f"Unsupported file format: {os.path.splitext(file_path)[1]}"
            
            self.original_df = self.df.copy()
            self.file_path = file_path
            self.load_time = time.time() - start_time
            
            # Gather file information
            rows, cols = self.df.shape
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            
            self.file_info = {
                'rows': rows,
                'columns': cols,
                'file_size_mb': file_size,
                'load_time': self.load_time,
                'column_names': list(self.df.columns)
            }
            
            return True, f"Successfully loaded {rows:,} rows and {cols} columns in {self.load_time:.2f} seconds"
            
        except Exception as e:
            return False, f"Error loading file: {str(e)}"
    
    def search(self, 
               search_term: str,
               search_columns: List[str],
               case_sensitive: bool = False,
               exact_match: bool = False,
               use_regex: bool = False,
               max_results: Optional[int] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Perform search operation on loaded data
        
        Args:
            search_term: Text to search for
            search_columns: List of column names to search in
            case_sensitive: Whether search should be case sensitive
            exact_match: Whether to match exact strings only
            use_regex: Whether to treat search_term as regex
            max_results: Maximum number of results to return
            
        Returns:
            Tuple of (results_dataframe, search_stats)
        """
        if self.df is None:
            return pd.DataFrame(), {'error': 'No data loaded'}
        
        start_time = time.time()
        
        try:
            # Validate search columns
            invalid_columns = [col for col in search_columns if col not in self.df.columns]
            if invalid_columns:
                return pd.DataFrame(), {'error': f'Invalid columns: {invalid_columns}'}
            
            if not search_term.strip():
                return self.df.copy(), {'search_time': 0, 'total_results': len(self.df)}
            
            # Prepare search term
            processed_term = search_term if case_sensitive else search_term.lower()
            
            # Create boolean mask for filtering
            mask = pd.Series([False] * len(self.df))
            
            # Search in each specified column
            for column in search_columns:
                if column not in self.df.columns:
                    continue
                
                # Convert column to string and handle NaN values
                col_data = self.df[column].astype(str).fillna("")
                
                if not case_sensitive:
                    col_data = col_data.str.lower()
                
                # Apply search logic
                if use_regex:
                    try:
                        col_mask = col_data.str.contains(processed_term, regex=True, na=False)
                    except re.error as e:
                        return pd.DataFrame(), {'error': f'Invalid regex pattern: {e}'}
                elif exact_match:
                    col_mask = col_data == processed_term
                else:
                    # Partial match (default)
                    col_mask = col_data.str.contains(processed_term, regex=False, na=False)
                
                # Combine with existing mask using OR logic
                mask = mask | col_mask
            
            # Apply filter
            results = self.df[mask].copy()
            
            # Limit results if specified
            if max_results and len(results) > max_results:
                results = results.head(max_results)
            
            search_time = time.time() - start_time
            
            # Prepare search statistics
            stats = {
                'search_time': search_time,
                'total_results': len(self.df[mask]),
                'returned_results': len(results),
                'search_term': search_term,
                'search_columns': search_columns,
                'case_sensitive': case_sensitive,
                'exact_match': exact_match,
                'use_regex': use_regex
            }
            
            return results, stats
            
        except Exception as e:
            return pd.DataFrame(), {'error': f'Search failed: {str(e)}'}
    
    def get_column_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all columns in the dataset
        
        Returns:
            List of dictionaries with column information
        """
        if self.df is None:
            return []
        
        column_info = []
        for col in self.df.columns:
            info = {
                'name': col,
                'dtype': str(self.df[col].dtype),
                'non_null_count': self.df[col].count(),
                'null_count': self.df[col].isnull().sum(),
                'unique_values': self.df[col].nunique()
            }
            
            # Add sample values (first 3 non-null values)
            sample_values = self.df[col].dropna().head(3).tolist()
            info['sample_values'] = [str(val) for val in sample_values]
            
            column_info.append(info)
        
        return column_info
    
    def export_results(self, results: pd.DataFrame, output_path: str) -> Tuple[bool, str]:
        """
        Export search results to file
        
        Args:
            results: DataFrame to export
            output_path: Path for output file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if results.empty:
                return False, "No results to export"
            
            file_ext = os.path.splitext(output_path)[1].lower()
            
            if file_ext == '.csv':
                results.to_csv(output_path, index=False)
            elif file_ext in ['.xlsx', '.xls']:
                results.to_excel(output_path, index=False, engine='openpyxl')
            else:
                return False, f"Unsupported export format: {file_ext}"
            
            return True, f"Successfully exported {len(results)} rows to {output_path}"
            
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get information about the loaded file"""
        return self.file_info.copy() if self.file_info else {}
    
    def reset(self):
        """Reset the search engine state"""
        self.df = None
        self.original_df = None
        self.file_path = ""
        self.load_time = 0
        self.file_info = {}
