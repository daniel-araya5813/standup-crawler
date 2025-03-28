"""
Main settings for the Eventbrite comedy events finder and information collector.
"""

# Base URL for search results
BASE_URL = "https://www.eventbrite.ca/d/canada--ontario/stand-up-comedy/"

# CSS selector for event cards on search results pages
CSS_SELECTOR = "div[data-testid='event-card']"

# Required fields for event data
REQUIRED_KEYS = [
    "title",      # Title of the event
    "venue",      # Name of the venue where the event is held
    "summary",    # Brief description of the event
    "address",    # Physical address of the venue
    "email",      # Contact email for the event or venue
    "city",       # City where the event is taking place
    "province",   # Province where the event is taking place
    "producers",  # Names of individuals or organizations producing the event
    "event_link", # URL link to the event page
    "date"        # Date and time when the event takes place
]

# Maximum number of pages to search in one run (to prevent overloading the server)
MAX_PAGES = 10

# Default delay between requests (in seconds)
DEFAULT_DELAY = 5

# Default number of retries for failed requests
DEFAULT_RETRIES = 1

# Output directories
OUTPUT_DIRS = {
    "links": "Collected_Data/Discovered_Event_Websites",
    "details": "Collected_Data/Complete_Event_Descriptions",
    "logs": "Logs",
    "screenshots": "Logs/Screenshots"
}

# File paths
DEFAULT_LINKS_FILE = "event_links.csv"
DEFAULT_DETAILS_FILE = "detailed_events.csv"

# Example configuration for venue scraping (commented out, kept for reference)
"""
VENUE_CONFIG = {
    "BASE_URL": "https://www.theknot.com/marketplace/wedding-reception-venues-atlanta-ga",
    "CSS_SELECTOR": "[class^='info-container']",
    "REQUIRED_KEYS": [
        "name",
        "price",
        "location",
        "capacity",
        "rating",
        "reviews",
        "description",
    ]
}
"""