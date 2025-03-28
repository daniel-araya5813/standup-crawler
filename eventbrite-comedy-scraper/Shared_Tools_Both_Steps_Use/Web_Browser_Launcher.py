"""
Web browser setup tool used by both steps of the application.
"""

from crawl4ai import BrowserConfig

def get_browser_config(headless: bool = True) -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.
    
    Args:
        headless (bool): Whether to run in headless mode
        
    Returns:
        BrowserConfig: The configuration settings for the browser
    """
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=headless,  # Run in headless mode (no GUI)
        verbose=True,  # Enable verbose logging
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # Spoofed User-Agent
        window_size={"width": 1920, "height": 1080},  # Window size
        timeout=30000,  # Timeout in milliseconds
        viewport={"width": 1920, "height": 1080},  # Viewport size
    )