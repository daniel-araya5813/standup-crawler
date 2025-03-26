import csv
import asyncio
import logging
from datetime import datetime

from utils.weblinks_event_detail_scrapper_utils import 
extract_event_details_from_link

# CONFIG
INPUT_CSV = "event_links.csv"  # This should be created by your pass 1 script
OUTPUT_CSV = f"event_details_{datetime.now().strftime('%Y-%m-%d')}.csv"
REQUIRED_KEYS = [
    "title", "venue", "summary", "address", "email",
    "city", "province", "producers", "event_link", "date"
]

# Set up logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

def read_event_links(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def save_event_details(data, output_file):
    if not data:
        logging.warning("No event data to save.")
        return

    with open(output_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_KEYS)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    logging.info(f"Saved {len(data)} events to '{output_file}'")


async def main():
    links = read_event_links(INPUT_CSV)
    logging.info(f"🔗 Loaded {len(links)} event links")

    extracted = []
    for i, url in enumerate(links, 1):
        logging.info(f"[{i}/{len(links)}] Extracting from: {url}")
        data = await extract_event_details_from_link(url, REQUIRED_KEYS)
        if data:
            extracted.append(data)
        await asyncio.sleep(2)  # Be polite

    save_event_details(extracted, OUTPUT_CSV)


if __name__ == "__main__":
    asyncio.run(main())
