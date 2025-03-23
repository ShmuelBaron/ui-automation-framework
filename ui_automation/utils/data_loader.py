"""
Data loader utility for UI automation framework.
"""
import csv
import json
import yaml
import os
import logging
from typing import List, Dict, Any, Union

class DataLoader:
    """Class for loading test data from various file formats."""
    
    def __init__(self, data_dir=None):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing data files (default: project_root/data)
        """
        self.logger = logging.getLogger(__name__)
        
        if data_dir is None:
            # Default data directory is project_root/data
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.data_dir = os.path.join(project_root, 'data')
        else:
            self.data_dir = data_dir
    
    def load_csv(self, file_name: str) -> List[Dict[str, str]]:
        """
        Load data from a CSV file.
        
        Args:
            file_name: Name of the CSV file
            
        Returns:
            List[Dict]: List of dictionaries with column names as keys
            
        Raises:
            FileNotFoundError: If file is not found
            Exception: If file cannot be loaded
        """
        file_path = self._get_file_path(file_name, '.csv')
        
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
                self.logger.info(f"Loaded {len(data)} rows from CSV file: {file_path}")
                return data
        except FileNotFoundError:
            self.logger.error(f"CSV file not found: {file_path}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to load CSV file {file_path}: {str(e)}")
            raise
    
    def load_json(self, file_name: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Load data from a JSON file.
        
        Args:
            file_name: Name of the JSON file
            
        Returns:
            Dict or List: JSON data
            
        Raises:
            FileNotFoundError: If file is not found
            Exception: If file cannot be loaded
        """
        file_path = self._get_file_path(file_name, '.json')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.logger.info(f"Loaded JSON data from file: {file_path}")
                return data
        except FileNotFoundError:
            self.logger.error(f"JSON file not found: {file_path}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to load JSON file {file_path}: {str(e)}")
            raise
    
    def load_yaml(self, file_name: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Load data from a YAML file.
        
        Args:
            file_name: Name of the YAML file
            
        Returns:
            Dict or List: YAML data
            
        Raises:
            FileNotFoundError: If file is not found
            Exception: If file cannot be loaded
        """
        # Try both .yaml and .yml extensions
        try:
            file_path = self._get_file_path(file_name, '.yaml')
        except FileNotFoundError:
            try:
                file_path = self._get_file_path(file_name, '.yml')
            except FileNotFoundError:
                self.logger.error(f"YAML file not found: {file_name}")
                raise FileNotFoundError(f"YAML file not found: {file_name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                self.logger.info(f"Loaded YAML data from file: {file_path}")
                return data
        except Exception as e:
            self.logger.error(f"Failed to load YAML file {file_path}: {str(e)}")
            raise
    
    def _get_file_path(self, file_name: str, extension: str = None) -> str:
        """
        Get full path to a file.
        
        Args:
            file_name: Name of the file
            extension: File extension to append if not already present
            
        Returns:
            str: Full path to the file
            
        Raises:
            FileNotFoundError: If file is not found
        """
        # Add extension if not already present
        if extension and not file_name.lower().endswith(extension):
            file_name = f"{file_name}{extension}"
        
        file_path = os.path.join(self.data_dir, file_name)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return file_path
    
    def load_test_data(self, file_name: str) -> List[tuple]:
        """
        Load test data for parameterized tests.
        
        Args:
            file_name: Name of the data file (CSV, JSON, or YAML)
            
        Returns:
            List[tuple]: List of tuples for pytest.mark.parametrize
            
        Raises:
            ValueError: If file format is not supported
            Exception: If file cannot be loaded
        """
        if file_name.lower().endswith('.csv'):
            return self._load_test_data_from_csv(file_name)
        elif file_name.lower().endswith('.json'):
            return self._load_test_data_from_json(file_name)
        elif file_name.lower().endswith(('.yaml', '.yml')):
            return self._load_test_data_from_yaml(file_name)
        else:
            raise ValueError(f"Unsupported file format for test data: {file_name}")
    
    def _load_test_data_from_csv(self, file_name: str) -> List[tuple]:
        """
        Load test data from a CSV file.
        
        Args:
            file_name: Name of the CSV file
            
        Returns:
            List[tuple]: List of tuples for pytest.mark.parametrize
        """
        data = self.load_csv(file_name)
        
        # Convert list of dicts to list of tuples
        result = []
        if data:
            # Get column names from first row
            columns = list(data[0].keys())
            
            # Create tuples with values in column order
            for row in data:
                result.append(tuple(row[col] for col in columns))
        
        return result
    
    def _load_test_data_from_json(self, file_name: str) -> List[tuple]:
        """
        Load test data from a JSON file.
        
        Args:
            file_name: Name of the JSON file
            
        Returns:
            List[tuple]: List of tuples for pytest.mark.parametrize
        """
        data = self.load_json(file_name)
        
        # Expect a list of objects with the same keys
        if not isinstance(data, list):
            raise ValueError(f"JSON test data must be a list of objects: {file_name}")
        
        result = []
        if data:
            # Get keys from first object
            keys = list(data[0].keys())
            
            # Create tuples with values in key order
            for item in data:
                result.append(tuple(item[key] for key in keys))
        
        return result
    
    def _load_test_data_from_yaml(self, file_name: str) -> List[tuple]:
        """
        Load test data from a YAML file.
        
        Args:
            file_name: Name of the YAML file
            
        Returns:
            List[tuple]: List of tuples for pytest.mark.parametrize
        """
        data = self.load_yaml(file_name)
        
        # Expect a list of objects with the same keys
        if not isinstance(data, list):
            raise ValueError(f"YAML test data must be a list of objects: {file_name}")
        
        result = []
        if data:
            # Get keys from first object
            keys = list(data[0].keys())
            
            # Create tuples with values in key order
            for item in data:
                result.append(tuple(item[key] for key in keys))
        
        return result
