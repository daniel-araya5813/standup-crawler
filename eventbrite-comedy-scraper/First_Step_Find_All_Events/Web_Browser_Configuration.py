"""
Setup and configuration for the web browser used to find events.
"""

from selenium.webdriver.chrome.options import Options

def create_chrome_options(headless=True):
    """
    Create Chrome browser settings with anti-detection measures.
    
    Args:
        headless (bool): Whether to run in headless mode (no visible window)
        
    Returns:
        Options: Configured Chrome options
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
    
    # Anti-detection measures to make the browser harder to detect as automated
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Set a realistic user agent so the website thinks we're a normal browser
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
    
    # Disable automation-specific flags
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    return chrome_options

def create_firefox_options(headless=True):
    """
    Create Firefox browser settings with anti-detection measures.
    
    Args:
        headless (bool): Whether to run in headless mode (no visible window)
        
    Returns:
        FirefoxOptions: Configured Firefox options
    """
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    
    firefox_options = FirefoxOptions()
    
    if headless:
        firefox_options.add_argument("--headless")
    
    # Set a realistic user agent
    firefox_options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    )
    
    # Disable webdriver mode
    firefox_options.set_preference("dom.webdriver.enabled", False)
    
    return firefox_options