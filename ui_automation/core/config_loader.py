"""
Configuration loader for UI automation framework.
"""
import yaml
import json
import os
import logging
from typing import Dict, Any, Optional

class ConfigLoader:
    """Class for loading configuration from YAML or JSON files."""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize the config loader.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.logger = logging.getLogger(__name__)
        self.config_dir = config_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        self.config_cache = {}
    
    def load_config(self, config_name: str, environment: str = 'default') -> Dict[str, Any]:
        """
        Load configuration from a file.
        
        Args:
            config_name: Name of the configuration file (without extension)
            environment: Environment to load (default, dev, prod, etc.)
            
        Returns:
            Dict: Configuration data
            
        Raises:
            FileNotFoundError: If configuration file is not found
            ValueError: If configuration file format is not supported
        """
        cache_key = f"{config_name}_{environment}"
        if cache_key in self.config_cache:
            return self.config_cache[cache_key]
        
        # Try to load environment-specific config
        config_data = self._try_load_config(f"{config_name}_{environment}")
        
        # If not found, try to load default config
        if config_data is None and environment != 'default':
            config_data = self._try_load_config(config_name)
        
        if config_data is None:
            raise FileNotFoundError(f"Configuration file not found for {config_name} ({environment})")
        
        self.config_cache[cache_key] = config_data
        return config_data
    
    def _try_load_config(self, config_name: str) -> Optional[Dict[str, Any]]:
        """
        Try to load configuration from YAML or JSON file.
        
        Args:
            config_name: Name of the configuration file (without extension)
            
        Returns:
            Dict or None: Configuration data if file exists, None otherwise
        """
        # Try YAML format
        yaml_path = os.path.join(self.config_dir, f"{config_name}.yaml")
        if os.path.exists(yaml_path):
            return self._load_yaml(yaml_path)
        
        # Try YML format
        yml_path = os.path.join(self.config_dir, f"{config_name}.yml")
        if os.path.exists(yml_path):
            return self._load_yaml(yml_path)
        
        # Try JSON format
        json_path = os.path.join(self.config_dir, f"{config_name}.json")
        if os.path.exists(json_path):
            return self._load_json(json_path)
        
        return None
    
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load YAML file.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            Dict: YAML data
            
        Raises:
            Exception: If YAML file cannot be loaded
        """
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                self.logger.info(f"Loaded YAML configuration from {file_path}")
                return data
        except Exception as e:
            self.logger.error(f"Failed to load YAML configuration from {file_path}: {str(e)}")
            raise
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """
        Load JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Dict: JSON data
            
        Raises:
            Exception: If JSON file cannot be loaded
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.logger.info(f"Loaded JSON configuration from {file_path}")
                return data
        except Exception as e:
            self.logger.error(f"Failed to load JSON configuration from {file_path}: {str(e)}")
            raise
    
    def get_browser_config(self, environment: str = 'default') -> Dict[str, Any]:
        """
        Get browser configuration.
        
        Args:
            environment: Environment to load (default, dev, prod, etc.)
            
        Returns:
            Dict: Browser configuration
        """
        return self.load_config('browser', environment)
    
    def get_test_config(self, environment: str = 'default') -> Dict[str, Any]:
        """
        Get test configuration.
        
        Args:
            environment: Environment to load (default, dev, prod, etc.)
            
        Returns:
            Dict: Test configuration
        """
        return self.load_config('test', environment)
    
    def get_environment_url(self, environment: str = 'default') -> str:
        """
        Get base URL for the specified environment.
        
        Args:
            environment: Environment to load (default, dev, prod, etc.)
            
        Returns:
            str: Base URL
        """
        config = self.load_config('environment', environment)
        return config.get('base_url', '')
