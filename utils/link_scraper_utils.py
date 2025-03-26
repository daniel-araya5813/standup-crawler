# utils/link_scraper_utils.py

from bs4 import BeautifulSoup
from typing import List

def get_event_links_from_page(html_content: str) -> List[str]:
    """
    Extracts all event URLs from the Eventbrite search results page HTML.

    Args:
        html_content (str): Raw HTML content of the Eventbrite search page.

    Returns:
        List[str]: A list of absolute event URLs.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Select all anchor tags pointing to event detail pages
    anchor_tags = soup.select("a.eds-event-card-content__action-link")

    links = []
    for tag in anchor_tags:
        href = tag.get("href")
        if href:
            # Convert relative URLs to absolute
            if href.startswith("http"):
                links.append(href)
            else:
                links.append(f"https://www.eventbrite.ca{href}")

    return links

