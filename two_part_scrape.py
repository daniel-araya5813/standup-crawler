import csv
import asyncio
import logging
from datetime import datetime

from utils.weblinks_event_detail_scrapper_utils import scrape_event_details_from_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

INPUT_CSV = "event_links.csv"   # This should be created by your pass 1 script
OUTPUT_CSV = "detailed_event_data.csv"
REQUIRED_KEYS = [
    "title",
    "venue",
    "summary",
    "address",
    "email",
    "city",
    "province",
    "producers",
    "event_link",
    "date"
]


def read_event_links(csv_file):
    links = []
    with open(csv_file, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if "event_link" in row:
                links.append(row["event_link"])
    return links


def write_event_data(venues, csv_file):
    if not venues:
        logging.warning("No venue data to write.")
        return

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_KEYS)
        writer.writeheader()
        for venue in venues:
            writer.writerow(venue)


async def main():
    logging.info("🚀 Starting pass 2: Scraping individual event pages")

    links = read_event_links(INPUT_CSV)
    logging.info(f"🔗 Found {len(links)} event links to process")

    results = []
    for idx, link in enumerate(links, start=1):
        logging.info(f"🔍 Processing {idx}/{len(links)}: {link}")
        venue = await scrape_event_details_from_url(link, REQUIRED_KEYS)
        if venue:
            results.append(venue)
        await asyncio.sleep(2)

    write_event_data(results, OUTPUT_CSV)
    logging.info(f"✅ Saved {len(results)} complete events to '{OUTPUT_CSV}'")


if __name__ == "__main__":
    asyncio.run(main())

