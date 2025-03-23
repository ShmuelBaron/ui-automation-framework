"""
Base page class that all page objects will inherit from.
Provides common methods for interacting with web elements.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, browser):
        """
        Initialize the base page.
        
        Args:
            browser: WebDriver instance
        """
        self.browser = browser
        self.timeout = 10
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator):
        """
        Find an element using the locator provided.
        
        Args:
            locator: A tuple of (By, path) e.g. (By.ID, 'example')
            
        Returns:
            WebElement: The found element
            
        Raises:
            NoSuchElementException: If element is not found
        """
        try:
            return self.browser.find_element(*locator)
        except NoSuchElementException as e:
            self.logger.error(f"Element not found with locator: {locator}")
            raise e
    
    def find_elements(self, locator):
        """
        Find elements using the locator provided.
        
        Args:
            locator: A tuple of (By, path) e.g. (By.CLASS_NAME, 'example')
            
        Returns:
            List[WebElement]: List of found elements
        """
        return self.browser.find_elements(*locator)
    
    def click(self, locator):
        """
        Click on an element.
        
        Args:
            locator: A tuple of (By, path)
        """
        element = self.find_element(locator)
        element.click()
        self.logger.info(f"Clicked on element with locator: {locator}")
    
    def type_text(self, locator, text):
        """
        Type text into an element.
        
        Args:
            locator: A tuple of (By, path)
            text: Text to type
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Typed '{text}' into element with locator: {locator}")
    
    def get_text(self, locator):
        """
        Get text from an element.
        
        Args:
            locator: A tuple of (By, path)
            
        Returns:
            str: Text of the element
        """
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator):
        """
        Check if an element is present on the page.
        
        Args:
            locator: A tuple of (By, path)
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for an element to be visible.
        
        Args:
            locator: A tuple of (By, path)
            timeout: Time to wait in seconds (default: self.timeout)
            
        Returns:
            WebElement: The visible element
            
        Raises:
            TimeoutException: If element is not visible within timeout
        """
        if timeout is None:
            timeout = self.timeout
            
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException as e:
            self.logger.error(f"Element not visible within {timeout} seconds: {locator}")
            raise e
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for an element to be clickable.
        
        Args:
            locator: A tuple of (By, path)
            timeout: Time to wait in seconds (default: self.timeout)
            
        Returns:
            WebElement: The clickable element
            
        Raises:
            TimeoutException: If element is not clickable within timeout
        """
        if timeout is None:
            timeout = self.timeout
            
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException as e:
            self.logger.error(f"Element not clickable within {timeout} seconds: {locator}")
            raise e
    
    def wait_for_page_load(self, timeout=None):
        """
        Wait for page to load completely.
        
        Args:
            timeout: Time to wait in seconds (default: self.timeout)
            
        Raises:
            TimeoutException: If page does not load within timeout
        """
        if timeout is None:
            timeout = self.timeout
            
        try:
            WebDriverWait(self.browser, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException as e:
            self.logger.error(f"Page did not load within {timeout} seconds")
            raise e
    
    def get_title(self):
        """
        Get the title of the current page.
        
        Returns:
            str: Page title
        """
        return self.browser.title
    
    def get_current_url(self):
        """
        Get the URL of the current page.
        
        Returns:
            str: Current URL
        """
        return self.browser.current_url
    
    def refresh_page(self):
        """Refresh the current page."""
        self.browser.refresh()
        self.wait_for_page_load()
        self.logger.info("Page refreshed")
    
    def navigate_to(self, url):
        """
        Navigate to the specified URL.
        
        Args:
            url: URL to navigate to
        """
        self.browser.get(url)
        self.wait_for_page_load()
        self.logger.info(f"Navigated to URL: {url}")
    
    def switch_to_frame(self, frame_reference):
        """
        Switch to a frame.
        
        Args:
            frame_reference: Frame reference (id, name, index, or WebElement)
        """
        self.browser.switch_to.frame(frame_reference)
        self.logger.info(f"Switched to frame: {frame_reference}")
    
    def switch_to_default_content(self):
        """Switch back to the default content."""
        self.browser.switch_to.default_content()
        self.logger.info("Switched back to default content")
    
    def execute_script(self, script, *args):
        """
        Execute JavaScript in the current window/frame.
        
        Args:
            script: JavaScript to execute
            *args: Arguments to pass to the script
            
        Returns:
            The result of the script execution
        """
        return self.browser.execute_script(script, *args)
