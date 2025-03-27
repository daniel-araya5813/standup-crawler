from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import csv
import logging
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

    def scrape_multiple_pages(self, base_url, start=1, end=3):
        logging.info(f"📄 Starting link scrape from page {start} to {end}")
        all_urls = []
        
        for i in range(start, end + 1):
            url = f"{base_url}?page={i}"
            logging.info(f"🔍 Visiting: {url}")
            
            try:
                # Navigate to the page
                self.driver.get(url)
                
                # Wait for page to load
                time.sleep(5)  # Increased wait time
                
                # Take screenshot for debugging
                self.driver.save_screenshot(f"page_{i}_screenshot.png")
                
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
                
            except Exception as e:
                logging.error(f"❌ Failed to extract page {i}: {e}")
                # Optional: Additional logging or screenshot
                self.driver.save_screenshot(f"error_page_{i}_screenshot.png")
        
        return list(set(all_urls))  # De-duplicate

    def save_to_csv(self, urls, filename="event_links.csv"):
        logging.info(f"💾 Saving {len(urls)} links to {filename}")
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["event_link"])
            writer.writeheader()
            for url in urls:
                writer.writerow({"event_link": url})

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("scraper.log"),
            logging.StreamHandler()
        ]
    )
    
    try:
        scraper = EventbriteScraper(headless=False)  # Set to False for debugging
        base_url = "https://www.eventbrite.ca/d/canada--ontario/stand-up-comedy/"
        links = scraper.scrape_multiple_pages(base_url, start=1, end=3)
        scraper.save_to_csv(links)
        scraper.close()
        logging.info("🎉 Done scraping event links.")
    except Exception as e:
        logging.error(f"Critical Error: {e}")