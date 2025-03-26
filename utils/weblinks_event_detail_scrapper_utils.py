# utils/event_detail_scraper_utils.py

import os
import json
from typing import List, Dict

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

from models.venue import Venue
from utils.data_utils import is_complete_venue


def get_event_detail_llm_strategy() -> LLMExtractionStrategy:
    """
    Defines how to extract event details from a single event page.
    """
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",
        api_token=os.getenv("GROQ_API_KEY"),
        schema=Venue.model_json_schema(),
        extraction_type="schema",
        instruction="""
            Extract a single event object with the following fields: 'title', 
'venue', 'summary', '
            address', 'email', 'city', 'province', 'producers', 'event_link', and 
'date'.
""",
        input_format="markdown",
        verbose=True,
    )


def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for crawling event pages.
    """
    return BrowserConfig(
        browser_type="chromium",
        headless=False,
        verbose=True,
    )


async def scrape_event_details_from_url(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
    llm_strategy: LLMExtractionStrategy,
    required_keys: List[str],
) -> Dict:
    """
    Extracts event details from a single event page.

    Args:
        crawler (AsyncWebCrawler): The crawler instance.
        url (str): The URL of the event page.
        session_id (str): Unique session ID.
        llm_strategy (LLMExtractionStrategy): Strategy for LLM extraction.
        required_keys (List[str]): Fields that must be present.

    Returns:
        Dict: Extracted event data, or None if invalid.
    """
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=llm_strategy,
            session_id=session_id,
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"❌ Failed to extract from {url}")
        return None

    try:
        data = json.loads(result.extracted_content)
        if isinstance(data, list):
            data = data[0]  # Sometimes the LLM returns a list
    except json.JSONDecodeError:
        print(f"⚠️ Failed to parse extracted content from {url}")
        return None

    if not is_complete_venue(data, required_keys):
        print(f"⚠️ Incomplete venue data from {url}")
        return None

    data["event_link"] = url  # Add the source URL
    return data

    if __name__ == "__main__":
        # Dummy HTML or URL for testing individual event page scraping
        # Call your function here with sample input
        pass   
  
