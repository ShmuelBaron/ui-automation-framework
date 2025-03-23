# UI Automation Framework

A comprehensive, modular framework for automating UI testing across web applications.

## Overview

This UI Automation Framework provides a robust solution for creating and maintaining automated UI tests. Built with Python and supporting multiple browsers, it offers a page object model architecture, powerful reporting capabilities, and flexible configuration options.

## Features

- **Cross-Browser Support**: Run tests on Chrome, Firefox, Edge, and Safari
- **Page Object Model**: Maintain clean separation between test logic and page interactions
- **Flexible Element Handling**: Robust element location and interaction capabilities
- **Comprehensive Reporting**: Detailed HTML reports with screenshots and logs
- **Data-Driven Testing**: Support for multiple data sources including CSV, JSON, and Excel
- **Configuration Management**: Environment-specific settings with easy overrides
- **Screenshot Capture**: Automatic screenshot capture on test failures
- **Logging**: Detailed logging for troubleshooting and audit trails

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ui-automation-framework.git
cd ui-automation-framework

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
ui_automation/
├── core/                  # Core framework components
│   ├── base_page.py       # Base page object class
│   ├── browser_factory.py # Browser initialization
│   ├── config_loader.py   # Configuration management
│   └── element_helper.py  # Element interaction utilities
├── pages/                 # Page object classes
├── utils/                 # Utility functions
│   ├── logger.py          # Logging functionality
│   ├── screenshot.py      # Screenshot capture
│   └── data_loader.py     # Test data loading
├── reporting/             # Reporting components
│   └── html_reporter.py   # HTML report generation
├── tests/                 # Test cases
├── data/                  # Test data files
├── config/                # Configuration files
└── reports/               # Generated test reports
```

## Usage

### Basic Test Example

```python
from ui_automation.core.browser_factory import BrowserFactory
from ui_automation.pages.login_page import LoginPage
import pytest

class TestLogin:
    def setup_method(self):
        self.browser = BrowserFactory().get_browser("chrome")
        self.login_page = LoginPage(self.browser)
    
    def teardown_method(self):
        self.browser.quit()
    
    def test_valid_login(self):
        self.login_page.navigate()
        self.login_page.login("valid_user", "valid_password")
        assert self.login_page.is_logged_in()
```

### Creating a Page Object

```python
from ui_automation.core.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")
    
    def navigate(self):
        self.browser.get("https://example.com/login")
    
    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def is_logged_in(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run with HTML report
pytest --html=reports/report.html
```

## Configuration

The framework uses a configuration system that supports multiple environments. Configuration files are located in the `config` directory.

Example configuration file (`config/default.json`):

```json
{
  "browser": "chrome",
  "headless": false,
  "implicit_wait": 10,
  "base_url": "https://example.com",
  "screenshot_dir": "reports/screenshots",
  "log_level": "INFO"
}
```

## Advanced Features

### Data-Driven Testing

```python
from ui_automation.utils.data_loader import DataLoader

class TestLogin:
    def test_multiple_logins(self):
        test_data = DataLoader.load_json("login_data.json")
        for data in test_data:
            self.login_page.navigate()
            self.login_page.login(data["username"], data["password"])
            assert self.login_page.is_logged_in() == data["expected_result"]
```

### Custom Reporting

```python
from ui_automation.reporting.html_reporter import HtmlReporter

def test_with_custom_reporting():
    reporter = HtmlReporter("Custom Test Report")
    reporter.start_test("Login Test")
    
    # Test steps
    login_page.navigate()
    reporter.add_step("Navigated to login page", "PASS", screenshot="login_page.png")
    
    login_page.login("user", "pass")
    reporter.add_step("Entered credentials and clicked login", "PASS")
    
    reporter.end_test()
    reporter.generate_report("custom_report.html")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
