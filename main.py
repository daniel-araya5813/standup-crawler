import asyncio
import argparse
import logging
from datetime import datetime
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import save_venues_to_csv
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

# Load environment variables
load_dotenv()

# Set up logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)


async def crawl_venues(start_page: int, end_page: int):
    logging.info(f"🕸️ Starting crawl from page {start_page} to {end_page}")

    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "venue_crawl_session"

    page_number = start_page
    all_venues = []
    seen_names = set()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        while page_number <= end_page:
            logging.info(f"🌐 Fetching page {page_number}...")
            venues, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                logging.warning("❌ No results found. Exiting crawl.")
                break

            if not venues:
                logging.warning(f"⚠️ No venues extracted from page {page_number}.")
                break

            logging.info(f"✅ {len(venues)} venues scraped from page {page_number}")
            all_venues.extend(venues)
            page_number += 1
            await asyncio.sleep(2)  # Be polite

    if all_venues:
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"eventbrite_p{start_page}_to_{page_number-1}_{date_str}.csv"
        save_venues_to_csv(all_venues, filename)
        logging.info(f"📁 Saved {len(all_venues)} venues to '{filename}'")
    else:
        logging.warning("🫥 No venues were found during the crawl.")

    llm_strategy.show_usage()


def parse_args():
    parser = argparse.ArgumentParser(description="Eventbrite Stand-Up Scraper")
    parser.add_argument("--start", type=int, default=1, help="Start page number")
    parser.add_argument("--end", type=int, default=2, help="End page number")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(crawl_venues(args.start, args.end))

