"""
Tools for reading and extracting information from Eventbrite web pages.
"""

from bs4 import BeautifulSoup
from typing import List, Dict

def extract_event_links_from_html(html_content: str) -> List[str]:
    """
    Find all event links in the HTML of an Eventbrite search results page.
    
    Args:
        html_content (str): The HTML content of the page
        
    Returns:
        List[str]: List of event website addresses
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find all links to event detail pages
    anchor_tags = soup.select("a.eds-event-card-content__action-link")
    
    links = []
    for tag in anchor_tags:
        href = tag.get("href")
        if href:
            # Make sure the link is a complete website address
            if href.startswith("http"):
                links.append(href)
            else:
                # If it's a partial link, add the website domain
                links.append(f"https://www.eventbrite.ca{href}")
    
    return links

def extract_pagination_info(html_content: str) -> Dict:
    """
    Find information about page numbers in search results.
    
    Args:
        html_content (str): The HTML content of the page
        
    Returns:
        dict: Information about current page and total pages
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # This is a placeholder implementation - actual selectors would need to be determined
    # by examining the Eventbrite HTML structure
    pagination_info = {
        "current_page": 1,
        "total_pages": 1
    }
    
    # Try to find pagination elements
    pagination_elements = soup.select(".pagination-element")
    if pagination_elements:
        # Extract pagination information based on site-specific structure
        # This would need to be adapted based on actual Eventbrite HTML
        pass
    
    return pagination_info

def check_for_no_results(html_content: str) -> bool:
    """
    Check if the page shows "No Results Found".
    
    Args:
        html_content (str): The HTML content of the page
        
    Returns:
        bool: True if no results were found
    """
    # Check for common "no results" indicators
    no_results_texts = [
        "No Results Found",
        "No events found",
        "We couldn't find any events",
        "Sorry, no events matched your search"
    ]
    
    # Look for any of these texts in the page
    for text in no_results_texts:
        if text in html_content:
            return True
            
    return False