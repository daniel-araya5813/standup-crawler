from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import argparse
import csv
import logging
import random
import time

class EventbriteScraper:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        
        # Enhanced anti-detection measures
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        
        # Experimental: Undetected Chrome
        try:
            import undetected_chromedriver as uc
            self.driver = uc.Chrome(options=chrome_options)
        except ImportError:
            # Fallback to standard WebDriver
            from selenium.webdriver.chrome import service
            from webdriver_manager.chrome import ChromeDriverManager
            service_obj = service.Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service_obj, options=chrome_options)

    def scrape_multiple_pages(self, base_url, start=1, end=3, run_date="run", delay=5, retry=1):
        logging.info(f"📄 Starting link scrape from page {start} to {end}")
        all_urls = []
        
        for i in range(start, end + 1):
            url = f"{base_url}?page={i}"
            logging.info(f"🔍 Visiting: {url}")
            
            for attempt in range(retry):
                try:
                    # Navigate to the page
                    self.driver.get(url)
                    
                    # Wait for page to load
                    time.sleep(random.uniform(delay, delay + 3))  # Random wait time delays
                    
                    # Take screenshot for debugging
                    self.driver.save_screenshot(f"screenshots/{run_date}_page_{i}_screenshot.png")
                    
                    # Try to find event links with multiple strategies
                    try:
                        # Strategy 1: Wait for specific event card links
                        wait = WebDriverWait(self.driver, 20)
                        links = wait.until(EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "a.eds-event-card-content__action-link")
                        ))
                    except TimeoutException:
                        # Strategy 2: Broader link search
                        links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'eventbrite.ca/e/')]")
                    
                    # Extract URLs
                    page_urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]
                    
                    logging.info(f"✅ Found {len(page_urls)} links on page {i}")
                    all_urls.extend(page_urls)
                    
                    time.sleep(2)  # Be polite between page scrapes
                    break  # Exit retry loop if successful
                
                except Exception as e:
                    logging.error(f"❌ Failed to extract page {i} on attempt {attempt + 1}: {e}")
                    # Optional: Additional logging or screenshot
                    self.driver.save_screenshot(f"screenshots/{run_date}_error_page_{i}_attempt_{attempt + 1}_screenshot.png")
        
        return list(set(all_urls))  # De-duplicate

    def save_to_csv(self, urls, filename="event_links.csv", run_date="run"):
        logging.info(f"💾 Saving {len(urls)} links to data/{run_date}_{filename}")
        with open(f"data/{run_date}_{filename}", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["event_link"])
            writer.writeheader()
            for url in urls:
                writer.writerow({"event_link": url})

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape event links with Selenium")
    parser.add_argument("--start", type=int, default=1, help="Start page number")
    parser.add_argument("--end", type=int, default=3, help="End page number")
    parser.add_argument("--base-url", type=str, default="https://www.eventbrite.ca/d/canada--ontario/stand-up-comedy/", help="Base URL to scrape")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--retry", type=int, default=1, help="Number of retries per page")
    parser.add_argument("--browser", type=str, choices=["chrome", "firefox"], default="chrome", help="Browser to use")
    parser.add_argument("--delay", type=int, default=5, help="Delay in seconds between requests")
    args = parser.parse_args()

    run_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Moved here
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(f"logs/scraper_{run_date}.log"),
            logging.StreamHandler()
        ]
    )
    
    try:
        scraper = EventbriteScraper(headless=args.headless if args.headless else False)
        links = scraper.scrape_multiple_pages(
            base_url=args.base_url,
            start=args.start,
            end=args.end,
            run_date=run_date,
            delay=args.delay,
            retry=args.retry
        )
        scraper.save_to_csv(links, filename="event_links.csv", run_date=run_date)
        scraper.close()
        logging.info("🎉 Done scraping event links.")
    except Exception as e:
        logging.error(f"Critical Error: {e}")