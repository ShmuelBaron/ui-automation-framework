"""
Element helper for UI automation framework.
"""
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import logging

class ElementHelper:
    """Helper class for interacting with web elements."""
    
    def __init__(self, browser):
        """
        Initialize the element helper.
        
        Args:
            browser: WebDriver instance
        """
        self.browser = browser
        self.logger = logging.getLogger(__name__)
    
    def select_dropdown_by_text(self, element, text):
        """
        Select dropdown option by visible text.
        
        Args:
            element: Select WebElement
            text: Option text to select
        """
        select = Select(element)
        select.select_by_visible_text(text)
        self.logger.info(f"Selected dropdown option with text: {text}")
    
    def select_dropdown_by_value(self, element, value):
        """
        Select dropdown option by value.
        
        Args:
            element: Select WebElement
            value: Option value to select
        """
        select = Select(element)
        select.select_by_value(value)
        self.logger.info(f"Selected dropdown option with value: {value}")
    
    def select_dropdown_by_index(self, element, index):
        """
        Select dropdown option by index.
        
        Args:
            element: Select WebElement
            index: Option index to select
        """
        select = Select(element)
        select.select_by_index(index)
        self.logger.info(f"Selected dropdown option with index: {index}")
    
    def get_dropdown_selected_text(self, element):
        """
        Get selected option text from dropdown.
        
        Args:
            element: Select WebElement
            
        Returns:
            str: Selected option text
        """
        select = Select(element)
        return select.first_selected_option.text
    
    def get_dropdown_options(self, element):
        """
        Get all options from dropdown.
        
        Args:
            element: Select WebElement
            
        Returns:
            List[str]: List of option texts
        """
        select = Select(element)
        return [option.text for option in select.options]
    
    def hover_over_element(self, element):
        """
        Hover over an element.
        
        Args:
            element: WebElement to hover over
        """
        actions = ActionChains(self.browser)
        actions.move_to_element(element).perform()
        self.logger.info("Hovered over element")
    
    def drag_and_drop(self, source_element, target_element):
        """
        Drag and drop an element.
        
        Args:
            source_element: Source WebElement
            target_element: Target WebElement
        """
        actions = ActionChains(self.browser)
        actions.drag_and_drop(source_element, target_element).perform()
        self.logger.info("Performed drag and drop")
    
    def right_click(self, element):
        """
        Right-click on an element.
        
        Args:
            element: WebElement to right-click on
        """
        actions = ActionChains(self.browser)
        actions.context_click(element).perform()
        self.logger.info("Performed right-click")
    
    def double_click(self, element):
        """
        Double-click on an element.
        
        Args:
            element: WebElement to double-click on
        """
        actions = ActionChains(self.browser)
        actions.double_click(element).perform()
        self.logger.info("Performed double-click")
    
    def press_key(self, element, key):
        """
        Press a key on an element.
        
        Args:
            element: WebElement
            key: Key to press (use Keys class)
        """
        element.send_keys(key)
        self.logger.info(f"Pressed key: {key}")
    
    def press_enter(self, element):
        """
        Press Enter key on an element.
        
        Args:
            element: WebElement
        """
        self.press_key(element, Keys.ENTER)
    
    def press_tab(self, element):
        """
        Press Tab key on an element.
        
        Args:
            element: WebElement
        """
        self.press_key(element, Keys.TAB)
    
    def press_escape(self, element):
        """
        Press Escape key on an element.
        
        Args:
            element: WebElement
        """
        self.press_key(element, Keys.ESCAPE)
    
    def scroll_to_element(self, element):
        """
        Scroll to an element.
        
        Args:
            element: WebElement to scroll to
        """
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info("Scrolled to element")
    
    def scroll_to_top(self):
        """Scroll to the top of the page."""
        self.browser.execute_script("window.scrollTo(0, 0);")
        self.logger.info("Scrolled to top of page")
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.info("Scrolled to bottom of page")
    
    def is_checkbox_checked(self, element):
        """
        Check if a checkbox is checked.
        
        Args:
            element: Checkbox WebElement
            
        Returns:
            bool: True if checked, False otherwise
        """
        return element.is_selected()
    
    def check_checkbox(self, element):
        """
        Check a checkbox if not already checked.
        
        Args:
            element: Checkbox WebElement
        """
        if not self.is_checkbox_checked(element):
            element.click()
            self.logger.info("Checked checkbox")
    
    def uncheck_checkbox(self, element):
        """
        Uncheck a checkbox if already checked.
        
        Args:
            element: Checkbox WebElement
        """
        if self.is_checkbox_checked(element):
            element.click()
            self.logger.info("Unchecked checkbox")
    
    def get_attribute(self, element, attribute):
        """
        Get attribute value from an element.
        
        Args:
            element: WebElement
            attribute: Attribute name
            
        Returns:
            str: Attribute value
        """
        return element.get_attribute(attribute)
    
    def get_css_value(self, element, property_name):
        """
        Get CSS property value from an element.
        
        Args:
            element: WebElement
            property_name: CSS property name
            
        Returns:
            str: CSS property value
        """
        return element.value_of_css_property(property_name)
    
    def is_element_enabled(self, element):
        """
        Check if an element is enabled.
        
        Args:
            element: WebElement
            
        Returns:
            bool: True if enabled, False otherwise
        """
        return element.is_enabled()
    
    def is_element_displayed(self, element):
        """
        Check if an element is displayed.
        
        Args:
            element: WebElement
            
        Returns:
            bool: True if displayed, False otherwise
        """
        return element.is_displayed()
