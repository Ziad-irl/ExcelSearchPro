"""
Utility functions for Excel Search Tool
Helper functions for file handling, data processing, and formatting
"""

import os
import re
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """
    Validate if file path exists and is a supported format
    
    Args:
        file_path: Path to file
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not file_path:
        return False, "File path is empty"
    
    if not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"
    
    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"
    
    # Check file extension
    _, ext = os.path.splitext(file_path.lower())
    supported_formats = ['.xlsx', '.xls', '.csv']
    
    if ext not in supported_formats:
        return False, f"Unsupported file format: {ext}. Supported: {', '.join(supported_formats)}"
    
    # Check file size (warn if very large)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > 500:  # 500 MB
        return True, f"Warning: Large file ({file_size_mb:.1f} MB) may take time to load"
    
    return True, "File is valid"

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename

def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Detect and suggest better column types for searching
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary mapping column names to suggested types
    """
    suggestions = {}
    
    for column in df.columns:
        col_data = df[column].dropna()
        
        if len(col_data) == 0:
            suggestions[column] = "empty"
            continue
        
        # Convert to string for analysis
        str_data = col_data.astype(str)
        
        # Check for patterns
        if str_data.str.match(r'^\d+$').all():
            suggestions[column] = "integer"
        elif str_data.str.match(r'^\d*\.\d+$').all():
            suggestions[column] = "decimal"
        elif str_data.str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$').any():
            suggestions[column] = "email"
        elif str_data.str.match(r'^\d{3}-\d{3}-\d{4}$').any():
            suggestions[column] = "phone"
        elif str_data.str.match(r'^\d{4}-\d{2}-\d{2}').any():
            suggestions[column] = "date"
        else:
            suggestions[column] = "text"
    
    return suggestions

def create_search_patterns() -> Dict[str, str]:
    """
    Create common search patterns for regex searches
    
    Returns:
        Dictionary of pattern names to regex patterns
    """
    return {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone_us": r"\d{3}-\d{3}-\d{4}",
        "phone_intl": r"\+\d{1,3}[-.\s]?\d{1,14}",
        "date_iso": r"\d{4}-\d{2}-\d{2}",
        "date_us": r"\d{1,2}/\d{1,2}/\d{4}",
        "ssn": r"\d{3}-\d{2}-\d{4}",
        "zip_code": r"\d{5}(-\d{4})?",
        "url": r"https?://[^\s]+",
        "ip_address": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        "credit_card": r"\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}"
    }

def optimize_dataframe_for_search(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize DataFrame for faster searching
    
    Args:
        df: Original DataFrame
        
    Returns:
        Optimized DataFrame
    """
    optimized_df = df.copy()
    
    # Convert object columns to string for consistent searching
    for column in optimized_df.columns:
        if optimized_df[column].dtype == 'object':
            optimized_df[column] = optimized_df[column].astype(str)
    
    # Fill NaN values with empty strings for text columns
    text_columns = optimized_df.select_dtypes(include=['object', 'string']).columns
    optimized_df[text_columns] = optimized_df[text_columns].fillna('')
    
    return optimized_df

def generate_search_suggestions(df: pd.DataFrame, column: str, limit: int = 10) -> List[str]:
    """
    Generate search suggestions based on column data
    
    Args:
        df: DataFrame
        column: Column name
        limit: Maximum number of suggestions
        
    Returns:
        List of suggested search terms
    """
    if column not in df.columns:
        return []
    
    # Get most common values
    value_counts = df[column].value_counts()
    
    # Filter out very common or very rare values
    total_rows = len(df)
    filtered_values = value_counts[
        (value_counts > total_rows * 0.001) &  # More than 0.1% of data
        (value_counts < total_rows * 0.5)      # Less than 50% of data
    ]
    
    # Convert to strings and limit length
    suggestions = []
    for value in filtered_values.head(limit).index:
        str_value = str(value)
        if len(str_value) <= 50 and str_value.strip():  # Reasonable length and not empty
            suggestions.append(str_value)
    
    return suggestions

def create_backup_filename(original_path: str) -> str:
    """
    Create a backup filename with timestamp
    
    Args:
        original_path: Original file path
        
    Returns:
        Backup filename
    """
    directory = os.path.dirname(original_path)
    filename = os.path.basename(original_path)
    name, ext = os.path.splitext(filename)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{name}_backup_{timestamp}{ext}"
    
    return os.path.join(directory, backup_filename)

def estimate_memory_usage(file_path: str) -> Dict[str, Any]:
    """
    Estimate memory usage for loading a file
    
    Args:
        file_path: Path to file
        
    Returns:
        Dictionary with memory estimates
    """
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    # Rough estimates based on file type and size
    if file_path.lower().endswith('.csv'):
        # CSV files are usually more memory efficient
        estimated_ram_mb = file_size_mb * 2
    else:
        # Excel files might use more memory
        estimated_ram_mb = file_size_mb * 3
    
    return {
        'file_size_mb': file_size_mb,
        'estimated_ram_mb': estimated_ram_mb,
        'is_large_file': file_size_mb > 100,
        'warning_message': f"File may use approximately {estimated_ram_mb:.1f} MB of RAM" if estimated_ram_mb > 500 else None
    }

def validate_regex_pattern(pattern: str) -> Tuple[bool, str]:
    """
    Validate regex pattern
    
    Args:
        pattern: Regex pattern to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        re.compile(pattern)
        return True, "Valid regex pattern"
    except re.error as e:
        return False, f"Invalid regex pattern: {e}"

def get_search_statistics(results: pd.DataFrame, search_time: float, total_rows: int) -> Dict[str, Any]:
    """
    Generate comprehensive search statistics
    
    Args:
        results: Search results DataFrame
        search_time: Time taken for search
        total_rows: Total rows in original dataset
        
    Returns:
        Dictionary with search statistics
    """
    result_count = len(results)
    match_percentage = (result_count / total_rows * 100) if total_rows > 0 else 0
    
    return {
        'result_count': result_count,
        'total_rows': total_rows,
        'match_percentage': match_percentage,
        'search_time': search_time,
        'results_per_second': result_count / search_time if search_time > 0 else 0,
        'efficiency_rating': 'Excellent' if search_time < 0.1 else 'Good' if search_time < 1 else 'Slow'
    }
