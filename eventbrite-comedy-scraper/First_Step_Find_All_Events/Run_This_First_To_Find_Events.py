#!/usr/bin/env python3
"""
This is the main script for Step 1: Finding all comedy events on Eventbrite.
Run this script first to collect the websites of all comedy events.
"""

import argparse
import logging
from datetime import datetime
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from this directory
from Event_Finder import EventbriteFinder

# Import from other directories
from Shared_Tools_Both_Steps_Use.File_Manager import ensure_directory_exists
import Main_Settings

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Find comedy events on Eventbrite")
    parser.add_argument("--start", type=int, default=1, help="Start page number")
    parser.add_argument("--end", type=int, default=3, help="End page number")
    parser.add_argument("--base-url", type=str, 
                      default=Main_Settings.BASE_URL, 
                      help="Base URL to search")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--retry", type=int, default=Main_Settings.DEFAULT_RETRIES, 
                      help="Number of retries per page")
    parser.add_argument("--browser", type=str, choices=["chrome", "firefox"], 
                      default="chrome", help="Browser to use")
    parser.add_argument("--delay", type=int, default=Main_Settings.DEFAULT_DELAY, 
                      help="Delay in seconds between requests")
    return parser.parse_args()

def setup_logging(run_date):
    """Set up logging configuration."""
    # Ensure logs directory exists
    ensure_directory_exists(Main_Settings.OUTPUT_DIRS["logs"])
    
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(f"{Main_Settings.OUTPUT_DIRS['logs']}/event_finder_{run_date}.log"),
            logging.StreamHandler()
        ]
    )

def main():
    """Main function to run the event finder."""
    print("🔍 STEP 1: FINDING COMEDY EVENTS ON EVENTBRITE 🔍")
    print("================================================")
    
    args = parse_args()
    
    # Generate a timestamp for this run
    run_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    setup_logging(run_date)
    
    logging.info("🚀 Starting Event Finder (Step 1)")
    logging.info(f"📄 Will search pages {args.start} to {args.end}")
    
    try:
        # Create and run the event finder
        finder = EventbriteFinder(headless=args.headless)
        
        links = finder.search_multiple_pages(
            base_url=args.base_url,
            start=args.start,
            end=args.end,
            run_date=run_date,
            delay=args.delay,
            retry=args.retry
        )
        
        # Save the collected links
        output_file = f"event_links_{run_date}.csv"
        finder.save_to_csv(links, filename=output_file, run_date=run_date)
        
        # Close the browser
        finder.close()
        
        logging.info(f"🎉 Successfully found {len(links)} event websites")
        logging.info(f"📁 Results saved to {Main_Settings.OUTPUT_DIRS['links']}/{run_date}_{output_file}")
        
        print("\n================================================")
        print(f"✅ FOUND {len(links)} COMEDY EVENTS!")
        print(f"✅ SAVED TO: {Main_Settings.OUTPUT_DIRS['links']}/{run_date}_{output_file}")
        print("================================================")
        print("🚀 Now you can run STEP 2 to collect detailed information about these events.")
        print("🚀 Run: python Second_Step_Get_Event_Details/Run_This_Second_To_Get_Event_Details.py")
        
    except Exception as e:
        logging.error(f"❌ Critical Error: {e}")
        print(f"\n❌ ERROR: {e}")
        print("❌ Check the log file for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())