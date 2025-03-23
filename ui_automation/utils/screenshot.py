"""
Screenshot utility for UI automation framework.
"""
import os
import time
from datetime import datetime
import logging

class Screenshot:
    """Class for capturing and managing screenshots."""
    
    def __init__(self, browser, screenshot_dir=None):
        """
        Initialize the screenshot utility.
        
        Args:
            browser: WebDriver instance
            screenshot_dir: Directory for screenshots (default: project_root/screenshots)
        """
        self.browser = browser
        self.logger = logging.getLogger(__name__)
        
        if screenshot_dir is None:
            # Default screenshot directory is project_root/screenshots
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.screenshot_dir = os.path.join(project_root, 'screenshots')
        else:
            self.screenshot_dir = screenshot_dir
        
        # Create screenshot directory if it doesn't exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def capture(self, name=None):
        """
        Capture a screenshot.
        
        Args:
            name: Screenshot name (default: timestamp)
            
        Returns:
            str: Path to the screenshot file
        """
        if name is None:
            # Generate name with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            name = f"screenshot_{timestamp}"
        
        # Ensure name has .png extension
        if not name.lower().endswith('.png'):
            name = f"{name}.png"
        
        # Create full path
        screenshot_path = os.path.join(self.screenshot_dir, name)
        
        try:
            # Capture screenshot
            self.browser.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot captured: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {str(e)}")
            return None
    
    def capture_element(self, element, name=None):
        """
        Capture a screenshot of a specific element.
        
        Args:
            element: WebElement to capture
            name: Screenshot name (default: timestamp)
            
        Returns:
            str: Path to the screenshot file
        """
        # Scroll element into view
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        
        # Wait for element to be in view
        time.sleep(0.5)
        
        # Capture screenshot
        return self.capture(name)
    
    def capture_on_failure(self, test_name):
        """
        Capture a screenshot on test failure.
        
        Args:
            test_name: Name of the test that failed
            
        Returns:
            str: Path to the screenshot file
        """
        # Generate name with test name and timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name = f"FAIL_{test_name}_{timestamp}.png"
        
        return self.capture(name)
