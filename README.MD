DeepSeek AI Web Scraper – Eventbrite Comedy Events (Two-Pass System)

Overview
This project is a Python-based two-pass web scraper designed to extract detailed information about stand-up 
comedy events in Ontario, Canada.

How It Works
Pass 1 – Event Links Collector
This scraper navigates through search results pages and collects the URLs of individual event listings. These 
links are saved to a file called event_links.csv.

Pass 2 – Event Details Extractor
This script takes the event_links.csv file, visits each link, and scrapes detailed information (like title, 
venue, summary, producers, date, etc.) using a language model. The results are saved in detailed_event_data.csv.

Implemented in: two_part_scrape.py
Uses: utils/weblinks_event_detail_scrapper_utils.py

File Structure
deepseek-ai-web-crawler/
│
├── main.py                          # CLI-based controller for pass 1
├── two_part_scrape.py              # Script for pass 2
├── config.py                       # Base URL and CSS selector
│
├── utils/
│   ├── link_scraper_utils.py       # Extracts links from result pages
│   ├── weblinks_event_detail_scrapper_utils.py  # Scrapes individual event pages
│   ├── data_utils.py               # Helpers for checking duplicates & completeness
│   └── scraper_utils.py            # (Used for original integrated scraping flow)
│
├── models/
│   └── venue.py                    # Venue Pydantic model for schema validation
│
├── event_links.csv                 # Collected links from pass 1
└── detailed_event_data.csv         # Final detailed event data

