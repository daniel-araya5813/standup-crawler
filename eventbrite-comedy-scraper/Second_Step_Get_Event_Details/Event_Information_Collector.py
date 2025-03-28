"""
Tools for extracting detailed information from individual event pages.
"""

import json
import logging
from typing import Dict, List, Optional

from crawl4ai import (
    AsyncWebCrawler,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

async def scrape_event_details_from_url(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
    llm_strategy: LLMExtractionStrategy,
    required_keys: List[str],
) -> Optional[Dict]:
    """
    Extract detailed information from a single event page.
    
    Args:
        crawler (AsyncWebCrawler): The crawler instance
        url (str): Website address of the event page
        session_id (str): Unique session identifier
        llm_strategy (LLMExtractionStrategy): Smart text analyzer configuration
        required_keys (List[str]): List of required information fields
        
    Returns:
        Optional[Dict]: Extracted event data or None if extraction failed
    """
    try:
        # Visit the event page and extract information using the smart text analyzer
        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,  # Don't use cached results
                extraction_strategy=llm_strategy,
                session_id=session_id,
            ),
        )
        
        # Check if the visit was successful
        if not (result.success and result.extracted_content):
            logging.error(f"❌ Failed to extract content from {url}: {result.error_message}")
            return None
        
        # Convert the extracted text to a dictionary
        try:
            data = json.loads(result.extracted_content)
            
            # Sometimes the AI returns a list instead of a single object
            if isinstance(data, list):
                if not data:  # Empty list
                    logging.warning(f"⚠️ AI returned empty list for {url}")
                    return None
                data = data[0]  # Take the first item
                
        except json.JSONDecodeError:
            logging.error(f"❌ Failed to parse JSON from {url}")
            return None
        
        # Check if all required information was found
        if not _is_complete_event(data, required_keys):
            logging.warning(f"⚠️ Incomplete event data from {url}")
            _log_missing_fields(data, required_keys)
            return None
        
        # Make sure the event_link field is set
        data["event_link"] = url
        
        return data
        
    except Exception as e:
        logging.error(f"❌ Exception while processing {url}: {str(e)}")
        return None

def _is_complete_event(event: Dict, required_keys: List[str]) -> bool:
    """
    Check if an event dictionary has all required information.
    
    Args:
        event (Dict): Event data dictionary
        required_keys (List[str]): List of required information fields
        
    Returns:
        bool: True if all required fields are present with non-empty values
    """
    return all(key in event and event[key] for key in required_keys)

def _log_missing_fields(event: Dict, required_keys: List[str]) -> None:
    """
    Log which required fields are missing from the event data.
    
    Args:
        event (Dict): Event data dictionary
        required_keys (List[str]): List of required fields
    """
    missing = []
    for key in required_keys:
        if key not in event:
            missing.append(f"{key} (missing)")
        elif not event[key]:
            missing.append(f"{key} (empty)")
    
    if missing:
        logging.warning(f"Missing or empty fields: {', '.join(missing)}")
