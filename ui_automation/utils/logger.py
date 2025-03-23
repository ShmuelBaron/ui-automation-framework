"""
Logger utility for UI automation framework.
"""
import logging
import os
from datetime import datetime

class Logger:
    """Class for setting up and managing logging."""
    
    @staticmethod
    def setup_logging(log_level=logging.INFO, log_to_file=True, log_dir=None):
        """
        Set up logging configuration.
        
        Args:
            log_level: Logging level (default: INFO)
            log_to_file: Whether to log to file (default: True)
            log_dir: Directory for log files (default: project_root/logs)
        """
        # Create root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add console handler to root logger
        root_logger.addHandler(console_handler)
        
        # Add file handler if requested
        if log_to_file:
            if log_dir is None:
                # Default log directory is project_root/logs
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                log_dir = os.path.join(project_root, 'logs')
            
            # Create log directory if it doesn't exist
            os.makedirs(log_dir, exist_ok=True)
            
            # Create log file with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = os.path.join(log_dir, f'test_run_{timestamp}.log')
            
            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            
            # Add file handler to root logger
            root_logger.addHandler(file_handler)
            
            logging.info(f"Logging to file: {log_file}")
        
        logging.info("Logging setup complete")
        return root_logger
    
    @staticmethod
    def get_logger(name):
        """
        Get a logger with the specified name.
        
        Args:
            name: Logger name
            
        Returns:
            Logger: Logger instance
        """
        return logging.getLogger(name)
