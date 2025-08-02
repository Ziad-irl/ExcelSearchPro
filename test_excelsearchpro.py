"""
Test suite for ExcelSearchPro
"""

import unittest
import os
import tempfile
import pandas as pd
from search_engine import ExcelSearchEngine


class TestExcelSearchEngine(unittest.TestCase):
    """Test cases for ExcelSearchEngine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = ExcelSearchEngine()
        
        # Create test data
        self.test_data = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown', 'Diana Prince', 'Eve Wilson'],
            'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'Score': [95, 87, 92, 88, 94]
        })
        
        # Create temporary Excel file
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        self.temp_file.close()
        self.test_data.to_excel(self.temp_file.name, index=False)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_file(self):
        """Test file loading functionality"""
        success, message = self.engine.load_file(self.temp_file.name)
        self.assertTrue(success)
        self.assertIsNotNone(self.engine.df)
        self.assertEqual(len(self.engine.df), 5)
    
    def test_search_simple(self):
        """Test simple search functionality"""
        self.engine.load_file(self.temp_file.name)
        
        results, stats = self.engine.search(
            search_term="Alice",
            search_columns=["Name"],
            case_sensitive=False,
            exact_match=False,
            use_regex=False
        )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]['Name'], 'Alice Smith')
        self.assertGreater(stats['total_results'], 0)
    
    def test_search_case_sensitive(self):
        """Test case sensitive search"""
        self.engine.load_file(self.temp_file.name)
        
        # Should find result
        results, _ = self.engine.search(
            search_term="Alice",
            search_columns=["Name"],
            case_sensitive=True,
            exact_match=False,
            use_regex=False
        )
        self.assertEqual(len(results), 1)
        
        # Should not find result
        results, _ = self.engine.search(
            search_term="alice",
            search_columns=["Name"],
            case_sensitive=True,
            exact_match=False,
            use_regex=False
        )
        self.assertEqual(len(results), 0)
    
    def test_search_exact_match(self):
        """Test exact match search"""
        self.engine.load_file(self.temp_file.name)
        
        # Should find exact match
        results, _ = self.engine.search(
            search_term="Alice Smith",
            search_columns=["Name"],
            case_sensitive=False,
            exact_match=True,
            use_regex=False
        )
        self.assertEqual(len(results), 1)
        
        # Should not find partial match in exact mode
        results, _ = self.engine.search(
            search_term="Alice",
            search_columns=["Name"],
            case_sensitive=False,
            exact_match=True,
            use_regex=False
        )
        self.assertEqual(len(results), 0)
    
    def test_multiple_columns(self):
        """Test searching in multiple columns"""
        self.engine.load_file(self.temp_file.name)
        
        results, _ = self.engine.search(
            search_term="New",
            search_columns=["Name", "City"],
            case_sensitive=False,
            exact_match=False,
            use_regex=False
        )
        
        # Should find "New York" in City column
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]['City'], 'New York')
    
    def test_get_file_info(self):
        """Test file info functionality"""
        self.engine.load_file(self.temp_file.name)
        
        info = self.engine.get_file_info()
        self.assertEqual(info['rows'], 5)
        self.assertEqual(info['columns'], 4)
        self.assertIn('file_size_mb', info)
        self.assertIn('load_time', info)
    
    def test_get_column_info(self):
        """Test column info functionality"""
        self.engine.load_file(self.temp_file.name)
        
        column_info = self.engine.get_column_info()
        self.assertEqual(len(column_info), 4)
        
        # Check first column info
        first_col = column_info[0]
        self.assertEqual(first_col['name'], 'ID')
        self.assertEqual(first_col['non_null_count'], 5)
        self.assertIn('dtype', first_col)


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent file"""
        engine = ExcelSearchEngine()
        success, message = engine.load_file("nonexistent_file.xlsx")
        
        self.assertFalse(success)
        self.assertIn("not found", message.lower())
    
    def test_search_without_loading_file(self):
        """Test searching without loading a file first"""
        engine = ExcelSearchEngine()
        
        results, stats = engine.search(
            search_term="test",
            search_columns=["Name"],
            case_sensitive=False,
            exact_match=False,
            use_regex=False
        )
        
        self.assertTrue(results.empty)
        self.assertIn('error', stats)


if __name__ == '__main__':
    unittest.main()
