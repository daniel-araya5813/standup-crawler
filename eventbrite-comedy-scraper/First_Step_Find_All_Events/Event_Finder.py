"""
Core tool for finding comedy events on Eventbrite.
Uses a web browser to search and collect event websites.
"""

import csv
import logging
import random
import time
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Import from this directory
from Web_Browser_Configuration import create_chrome_options

# Import from other directories
from Shared_Tools_Both_Steps_Use.File_Manager import ensure_directory_exists
import Main_Settings

class EventbriteFinder:
    """
    A tool that searches Eventbrite for comedy events and collects their website addresses.
    Uses a web browser to automatically search through pages of results.
    """
    
    def __init__(self, headless=True):
        """
        Set up the event finder tool with a web browser.
        
        Args:
            headless (bool): Whether to show the browser window (False) or hide it (True)
        """
        # Get standard chrome options (with experimental options)
        chrome_options = create_chrome_options(headless)
        
        # Try to use undetected_chromedriver if available, otherwise fallback to standard
        try:
            import undetected_chromedriver as uc
            
            # For undetected_chromedriver, we need to create a clean Options object
            # without the experimental options that cause problems
            uc_options = uc.ChromeOptions()
            
            # Copy over the regular arguments from our standard options
            for argument in chrome_options.arguments:
                uc_options.add_argument(argument)
            
            # Now use these cleaned options with undetected_chromedriver
            self.driver = uc.Chrome(options=uc_options)
            
            # Add JavaScript-based anti-detection
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            logging.info("Using undetected_chromedriver for better anti-detection")
            
        except ImportError:
            # Fallback to standard WebDriver (with all experimental options intact)
            from selenium.webdriver.chrome import service
            from webdriver_manager.chrome import ChromeDriverManager
            
            service_obj = service.Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service_obj, options=chrome_options)
            
            # Add additional JavaScript-based anti-detection for standard ChromeDriver
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            
            logging.info("Using standard ChromeDriver")

    def search_multiple_pages(self, base_url, start=1, end=3, run_date="run", delay=5, retry=1):
        """
        Search multiple pages of Eventbrite results to find comedy events.
        
        Args:
            base_url (str): The Eventbrite search URL
            start (int): The page number to start from
            end (int): The page number to end at
            run_date (str): Timestamp for this search
            delay (int): How many seconds to wait between page loads
            retry (int): How many times to retry if a page fails to load
            
        Returns:
            list: A list of unique event website addresses
        """
        logging.info(f"📄 Starting search from page {start} to {end}")
        all_urls = []
        
        # Ensure screenshots directory exists
        screenshots_dir = f"{Main_Settings.OUTPUT_DIRS['screenshots']}"
        ensure_directory_exists(screenshots_dir)
        
        for i in range(start, end + 1):
            url = f"{base_url}?page={i}"
            logging.info(f"🔍 Searching: {url}")
            
            for attempt in range(retry):
                try:
                    # Navigate to the page
                    self.driver.get(url)
                    
                    # Wait for page to load with random delay to appear more human-like
                    time.sleep(random.uniform(delay, delay + 3))
                    
                    # Take screenshot for reference
                    self.driver.save_screenshot(f"{screenshots_dir}/{run_date}_page_{i}_screenshot.png")
                    
                    # Try to find event links with multiple strategies
                    links = self._extract_links_from_page()
                    
                    # Extract URLs
                    page_urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]
                    
                    logging.info(f"✅ Found {len(page_urls)} links on page {i}")
                    all_urls.extend(page_urls)
                    
                    # Wait before moving to next page to be polite to the server
                    time.sleep(2)
                    
                    # Break retry loop if successful
                    break
                
                except Exception as e:
                    logging.error(f"❌ Failed to extract page {i} on attempt {attempt + 1}: {e}")
                    self.driver.save_screenshot(f"{screenshots_dir}/{run_date}_error_page_{i}_attempt_{attempt + 1}.png")
                    
                    # If this was the last retry, continue to next page
                    if attempt == retry - 1:
                        logging.warning(f"⚠️ All {retry} attempts failed for page {i}, moving to next page")
        
        # Return de-duplicated list of URLs
        return list(set(all_urls))

    def _extract_links_from_page(self):
        """
        Extract event links from the current page using different strategies.
        
        Returns:
            list: WebElement objects representing links
        """
        try:
            # Strategy 1: Wait for specific event card links (preferred method)
            wait = WebDriverWait(self.driver, 20)
            links = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.eds-event-card-content__action-link")
            ))
            return links
        except TimeoutException:
            logging.warning("⚠️ Primary link selector failed, trying alternative method")
            
            # Strategy 2: Broader link search as fallback
            return self.driver.find_elements(By.XPATH, "//a[contains(@href, 'eventbrite.ca/e/')]")

    def save_to_csv(self, urls, filename="event_links.csv", run_date="run"):
        """
        Save the found event websites to a CSV file.
        
        Args:
            urls (list): List of event website addresses
            filename (str): Name of the output file
            run_date (str): Timestamp for this run
        """
        # Ensure the output directory exists
        ensure_directory_exists(Main_Settings.OUTPUT_DIRS["links"])
        
        output_path = f"{Main_Settings.OUTPUT_DIRS['links']}/{run_date}_{filename}"
        logging.info(f"💾 Saving {len(urls)} links to {output_path}")
        
        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["event_link"])
            writer.writeheader()
            for url in urls:
                writer.writerow({"event_link": url})

    def close(self):
        """Close the browser when finished."""
        self.driver.quit()