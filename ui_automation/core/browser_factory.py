"""
Browser factory for creating WebDriver instances.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
import os

class BrowserFactory:
    """Factory class for creating WebDriver instances."""
    
    def __init__(self):
        """Initialize the browser factory."""
        self.logger = logging.getLogger(__name__)
    
    def create_browser(self, browser_type="chrome", headless=False):
        """
        Create a WebDriver instance for the specified browser.
        
        Args:
            browser_type: Type of browser ('chrome', 'firefox', 'edge', 'safari')
            headless: Whether to run in headless mode
            
        Returns:
            WebDriver: Browser instance
            
        Raises:
            ValueError: If browser_type is not supported
        """
        browser_type = browser_type.lower()
        self.logger.info(f"Creating {browser_type} browser (headless: {headless})")
        
        if browser_type == "chrome":
            return self._create_chrome(headless)
        elif browser_type == "firefox":
            return self._create_firefox(headless)
        elif browser_type == "edge":
            return self._create_edge(headless)
        elif browser_type == "safari":
            return self._create_safari()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
    
    def _create_chrome(self, headless=False):
        """
        Create a Chrome WebDriver instance.
        
        Args:
            headless: Whether to run in headless mode
            
        Returns:
            WebDriver: Chrome browser instance
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # Add experimental options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        try:
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            self.logger.info("Chrome browser created successfully")
            return driver
        except Exception as e:
            self.logger.error(f"Failed to create Chrome browser: {str(e)}")
            raise
    
    def _create_firefox(self, headless=False):
        """
        Create a Firefox WebDriver instance.
        
        Args:
            headless: Whether to run in headless mode
            
        Returns:
            WebDriver: Firefox browser instance
        """
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        
        try:
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            self.logger.info("Firefox browser created successfully")
            return driver
        except Exception as e:
            self.logger.error(f"Failed to create Firefox browser: {str(e)}")
            raise
    
    def _create_edge(self, headless=False):
        """
        Create an Edge WebDriver instance.
        
        Args:
            headless: Whether to run in headless mode
            
        Returns:
            WebDriver: Edge browser instance
        """
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        try:
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )
            self.logger.info("Edge browser created successfully")
            return driver
        except Exception as e:
            self.logger.error(f"Failed to create Edge browser: {str(e)}")
            raise
    
    def _create_safari(self):
        """
        Create a Safari WebDriver instance.
        
        Returns:
            WebDriver: Safari browser instance
        """
        try:
            driver = webdriver.Safari(service=SafariService())
            self.logger.info("Safari browser created successfully")
            return driver
        except Exception as e:
            self.logger.error(f"Failed to create Safari browser: {str(e)}")
            raise
