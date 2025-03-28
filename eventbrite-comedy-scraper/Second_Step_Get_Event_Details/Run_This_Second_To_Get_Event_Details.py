#!/usr/bin/env python3
"""
This is the main script for Step 2: Collecting detailed information about comedy events.
Run this script after Step 1 to get full details about the events found.
"""

import csv
import asyncio
import logging
import argparse
import sys
import os
from datetime import datetime

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from crawl4ai
from crawl4ai import AsyncWebCrawler

# Import from this directory
from Event_Information_Collector import scrape_event_details_from_url
from Smart_Text_Analyzer_Configuration import get_event_detail_llm_strategy

# Import from other directories
from Shared_Tools_Both_Steps_Use.File_Manager import ensure_directory_exists, find_newest_file
from Shared_Tools_Both_Steps_Use.Web_Browser_Launcher import get_browser_config

# Import main settings
from Main_Settings import REQUIRED_KEYS

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Collect detailed information about comedy events")
    parser.add_argument("--input", type=str, help="Path to input CSV file with event links")
    parser.add_argument("--output", type=str, help="Path to output CSV file for event details")
    parser.add_argument("--start-index", type=int, default=0, 
                      help="Starting index in the links list (for resuming)")
    parser.add_argument("--max-links", type=int, default=0, 
                      help="Maximum number of links to process (0 for all)")
    parser.add_argument("--delay", type=int, default=2, 
                      help="Delay between requests in seconds")
    return parser.parse_args()

def setup_logging():
    """Set up logging configuration."""
    # Ensure logs directory exists
    ensure_directory_exists("Logs")
    
    # Generate a timestamp for this run
    run_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(f"Logs/detail_collector_{run_date}.log"),
            logging.StreamHandler()
        ]
    )
    
    return run_date

def read_event_links(csv_file):
    """
    Read event website addresses from a CSV file.
    
    Args:
        csv_file (str): Path to the CSV file containing event links
        
    Returns:
        list: List of event links
    """
    links = []
    logging.info(f"📂 Reading event links from: {csv_file}")
    
    try:
        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "event_link" in row:
                    links.append(row["event_link"])
    except FileNotFoundError:
        logging.error(f"❌ Input file not found: {csv_file}")
        return []
    except Exception as e:
        logging.error(f"❌ Error reading input file: {e}")
        return []
    
    logging.info(f"📊 Found {len(links)} event links")
    return links

def write_event_data(events, csv_file):
    """
    Write event data to a CSV file.
    
    Args:
        events (list): List of event dictionaries
        csv_file (str): Path to the output CSV file
    """
    if not events:
        logging.warning("⚠️ No event data to write.")
        return
    
    try:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=REQUIRED_KEYS)
            writer.writeheader()
            for event in events:
                writer.writerow(event)
        
        logging.info(f"💾 Successfully saved {len(events)} events to '{csv_file}'")
    except Exception as e:
        logging.error(f"❌ Error writing output file: {e}")

async def main():
    """Main function to run the event detail collector."""
    print("🔍 STEP 2: COLLECTING DETAILED EVENT INFORMATION 🔍")
    print("================================================")
    
    args = parse_args()
    run_date = setup_logging()
    
    logging.info("🚀 Starting Event Detail Collection (Step 2)")
    
    # Determine input file
    input_file = args.input
    if not input_file:
        # Find most recent event links file if not specified
        input_file = find_newest_file("Collected_Data/Discovered_Event_Websites", "event_links")
        if not input_file:
            logging.error("❌ No input file specified and no event_links file found")
            print("❌ ERROR: No event links file found. Please run Step 1 first.")
            return 1
    
    # Read event links
    links = read_event_links(input_file)
    if not links:
        print("❌ ERROR: No event links found in the input file.")
        return 1
    
    # Determine which links to process
    start_idx = max(0, min(args.start_index, len(links) - 1))
    end_idx = len(links)
    if args.max_links > 0:
        end_idx = min(start_idx + args.max_links, len(links))
    
    links_to_process = links[start_idx:end_idx]
    logging.info(f"🔍 Processing {len(links_to_process)} links (from index {start_idx} to {end_idx-1})")
    
    # Determine output file
    output_file = args.output
    if not output_file:
        # Ensure output directory exists
        ensure_directory_exists("Collected_Data/Complete_Event_Descriptions")
        output_file = f"Collected_Data/Complete_Event_Descriptions/detailed_events_{run_date}.csv"
    
    # Initialize crawler and LLM strategy
    llm_strategy = get_event_detail_llm_strategy()
    session_id = f"event_detail_scrape_{run_date}"
    results = []
    
    # Configure browser for crawling
    browser_config = get_browser_config()
    
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for idx, link in enumerate(links_to_process, start=1):
                print(f"Processing event {idx}/{len(links_to_process)}: {link}")
                logging.info(f"🔍 Processing {idx}/{len(links_to_process)}: {link}")
                
                event = await scrape_event_details_from_url(
                    crawler=crawler,
                    url=link,
                    session_id=session_id,
                    llm_strategy=llm_strategy,
                    required_keys=REQUIRED_KEYS
                )
                
                if event:
                    results.append(event)
                    logging.info(f"✅ Successfully extracted details for event: {event.get('title', 'Unknown')}")
                else:
                    logging.warning(f"⚠️ Failed to extract details from: {link}")
                
                # Be polite to the server
                await asyncio.sleep(args.delay)
    except Exception as e:
        logging.error(f"❌ Error during crawling: {e}")
        # Still try to save partial results
        if results:
            write_event_data(results, output_file)
        return 1
    
    # Write results to CSV
    write_event_data(results, output_file)
    
    # Show LLM usage statistics
    if hasattr(llm_strategy, 'show_usage'):
        llm_strategy.show_usage()
    
    logging.info(f"🎉 Event detail collection completed. Processed {len(links_to_process)} links, " 
               f"successfully extracted {len(results)} events.")
               
    print("\n================================================")
    print(f"✅ COLLECTED INFORMATION ABOUT {len(results)} EVENTS!")
    print(f"✅ SAVED TO: {output_file}")
    print("================================================")
    
    return 0

if __name__ == "__main__":
    asyncio.run(main())