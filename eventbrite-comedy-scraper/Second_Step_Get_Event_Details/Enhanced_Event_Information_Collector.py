"""
Improved crawler configuration for the second step of the scraper.
This enhances anti-detection measures to match those in the first step.
"""

from crawl4ai import BrowserConfig
import random

def get_enhanced_browser_config(headless: bool = True) -> BrowserConfig:
    """
    Returns an enhanced browser configuration with better anti-detection measures.
    
    Args:
        headless (bool): Whether to run in headless mode
        
    Returns:
        BrowserConfig: Enhanced configuration settings for the browser
    """
    # List of realistic user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    
    # Randomly select a user agent
    user_agent = random.choice(user_agents)
    
    # Create enhanced browser config
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=headless,  # Run in headless mode (no GUI)
        verbose=True,  # Enable verbose logging
        user_agent=user_agent,  # Randomized User-Agent
        window_size={"width": 1920, "height": 1080},  # Window size
        timeout=30000,  # Timeout in milliseconds
        viewport={"width": 1920, "height": 1080},  # Viewport size
        # Additional anti-detection options
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process"
        ],
        # Browser behavior to emulate a real user
        defaultBrowserType="chromium",
        ignoreHTTPSErrors=True,
        slowMo=random.randint(50, 100),  # Random slight delay between actions
    )

def add_anti_detection_scripts(page):
    """
    Add JavaScript-based anti-detection measures to a page.
    
    Args:
        page: The playwright page object
    """
    # Execute JavaScript to modify navigator properties
    scripts = [
        # Remove automation flags
        """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """,
        
        # Modify plugins and mime types
        """
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        })
        """,
        
        # Add fake language preferences
        """
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en', 'fr']
        })
        """,
        
        # Random screen dimensions
        """
        Object.defineProperty(screen, 'width', {
            get: () => 1920
        })
        Object.defineProperty(screen, 'height', {
            get: () => 1080
        })
        """
    ]
    
    # Execute each script
    for script in scripts:
        page.evaluate(script)

async def visit_with_random_behavior(crawler, url, config):
    """
    Visit a page with random human-like behavior to avoid detection.
    
    Args:
        crawler: The AsyncWebCrawler instance
        url: The URL to visit
        config: The crawler configuration
    
    Returns:
        The result from the crawler
    """
    # Get the page from the crawler
    page = await crawler.get_page()
    
    # Add anti-detection scripts
    await page.evaluate("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    # Random wait time before navigation (2-5 seconds)
    await page.wait_for_timeout(random.randint(2000, 5000))
    
    # Visit the URL
    result = await crawler.arun(url=url, config=config)
    
    # Simulate random human-like behavior after page load
    if page:
        # Random scroll
        await page.evaluate("""
            window.scrollTo({
                top: Math.floor(Math.random() * document.body.scrollHeight * 0.7),
                behavior: 'smooth'
            });
        """)
        
        # Random wait after scrolling (1-3 seconds)
        await page.wait_for_timeout(random.randint(1000, 3000))
    
    return result