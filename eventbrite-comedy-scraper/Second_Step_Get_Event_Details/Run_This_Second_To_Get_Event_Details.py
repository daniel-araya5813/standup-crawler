#!/usr/bin/env python3
"""
This is the main script for Step 2: Collecting detailed information about comedy events.
Run this script after Step 1 to get full details about the events found.
Enhanced with better anti-detection measures.
"""

import csv
import asyncio
import logging
import argparse
import sys
import os
import random
from datetime import datetime

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from crawl4ai
from crawl4ai import AsyncWebCrawler

# Import from this directory
from Event_Information_Collector import scrape_event_details_from_url
from Smart_Text_Analyzer_Configuration import get_event_detail_llm_strategy
from Enhanced_Event_Information_Collector import get_enhanced_browser_config, visit_with_random_behavior, add_anti_detection_scripts

# Import from other directories
from Shared_Tools_Both_Steps_Use.File_Manager import ensure_directory_exists, find_newest_file

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
    parser.add_argument("--batch-size", type=int, default=8,
                      help="Number of links to process per browser session")
    parser.add_argument("--headless", action="store_true", default=True,
                      help="Run browser in headless mode")
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

def update_csv_with_batch(events, csv_file):
    """
    Append a batch of events to an existing CSV file or create a new one.
    
    Args:
        events (list): List of event dictionaries to append
        csv_file (str): Path to the CSV file
    """
    if not events:
        return
        
    file_exists = os.path.isfile(csv_file)
    
    try:
        mode = "a" if file_exists else "w"
        with open(csv_file, mode=mode, newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=REQUIRED_KEYS)
            if not file_exists:
                writer.writeheader()
            for event in events:
                writer.writerow(event)
        
        logging.info(f"💾 Saved batch of {len(events)} events to '{csv_file}'")
    except Exception as e:
        logging.error(f"❌ Error writing batch to output file: {e}")

async def process_batch(links_batch, crawler, llm_strategy, session_id, delay_base):
    """
    Process a batch of links with a single browser instance.
    
    Args:
        links_batch (list): List of links to process
        crawler (AsyncWebCrawler): Crawler instance
        llm_strategy: LLM extraction strategy
        session_id (str): Session identifier
        delay_base (int): Base delay between requests
        
    Returns:
        list: List of successfully extracted events
    """
    results = []
    
    # Get the page for adding anti-detection scripts
    page = await crawler.get_page()
    await page.goto("about:blank")  # Navigate to blank page first
    
    # Add anti-detection scripts
    await add_anti_detection_scripts(page)
    
    for idx, link in enumerate(links_batch, start=1):
        logging.info(f"🔍 Processing {idx}/{len(links_batch)}: {link}")
        
        try:
            # Create a new configuration for each request with random parameters
            from crawl4ai import CrawlerRunConfig, CacheMode
            
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=llm_strategy,
                session_id=f"{session_id}_{random.randint(1000, 9999)}",  # Randomize session ID
            )
            
            # Visit the page with random human-like behavior
            result = await visit_with_random_behavior(crawler, link, config)
            
            # Extract event details
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
            
            # Random delay between requests
            random_delay = delay_base + random.uniform(1, 4)
            logging.info(f"⏱️ Waiting {random_delay:.2f} seconds before next request")
            await asyncio.sleep(random_delay)
            
            # Occasionally perform random actions to appear more human-like
            if random.random() < 0.3:  # 30% chance
                await page.evaluate("""
                    window.scrollTo({
                        top: Math.floor(Math.random() * document.body.scrollHeight * 0.8),
                        behavior: 'smooth'
                    });
                """)
                await asyncio.sleep(random.uniform(0.5, 2))
            
        except Exception as e:
            logging.error(f"❌ Error processing {link}: {e}")
    
    return results

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
    
    # Initialize LLM strategy
    llm_strategy = get_event_detail_llm_strategy()
    
    # Setup session ID with timestamp and random component
    session_id = f"event_detail_scrape_{run_date}_{random.randint(1000, 9999)}"
    
    # Process links in batches to restart browser regularly
    batch_size = args.batch_size
    all_results = []
    
    # Split links into batches
    batches = [links_to_process[i:i+batch_size] for i in range(0, len(links_to_process), batch_size)]
    
    for batch_num, batch in enumerate(batches, start=1):
        logging.info(f"🔄 Processing batch {batch_num}/{len(batches)} ({len(batch)} links)")
        
        # Create a fresh browser instance for each batch
        browser_config = get_enhanced_browser_config(headless=args.headless)
        
        try:
            # Create a new browser instance with enhanced config
            async with AsyncWebCrawler(config=browser_config) as crawler:
                # Process current batch
                batch_results = await process_batch(
                    links_batch=batch,
                    crawler=crawler,
                    llm_strategy=llm_strategy,
                    session_id=f"{session_id}_batch_{batch_num}",
                    delay_base=args.delay
                )
                
                # Add results from this batch
                all_results.extend(batch_results)
                
                # Update CSV after each batch to save progress
                update_csv_with_batch(batch_results, output_file)
                
            # Add a longer delay between batches
            between_batch_delay = random.uniform(10, 20)
            logging.info(f"⏱️ Waiting {between_batch_delay:.2f} seconds before next batch")
            await asyncio.sleep(between_batch_delay)
            
        except Exception as e:
            logging.error(f"❌ Error during batch {batch_num}: {e}")
    
    # Show LLM usage statistics
    if hasattr(llm_strategy, 'show_usage'):
        llm_strategy.show_usage()
    
    logging.info(f"🎉 Event detail collection completed. Processed {len(links_to_process)} links, " 
               f"successfully extracted {len(all_results)} events.")
               
    print("\n================================================")
    print(f"✅ COLLECTED INFORMATION ABOUT {len(all_results)} EVENTS!")
    print(f"✅ SAVED TO: {output_file}")
    print("================================================")
    
    return 0

if __name__ == "__main__":
    asyncio.run(main())