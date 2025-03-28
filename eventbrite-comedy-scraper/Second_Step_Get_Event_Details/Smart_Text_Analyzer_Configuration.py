"""
Configuration for the smart text analyzer (AI/LLM) used to extract event information.
"""

import os
import logging
from dotenv import load_dotenv
from typing import Dict

from crawl4ai import LLMExtractionStrategy

# Load environment variables from .env file
load_dotenv()

def get_event_detail_llm_strategy() -> LLMExtractionStrategy:
    """
    Configure the smart text analyzer (AI/LLM) for extracting event details.
    
    Returns:
        LLMExtractionStrategy: Configured AI text analyzer
    """
    # Check if API key is available
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logging.warning("⚠️ GROQ_API_KEY not found in environment variables")
        logging.warning("Please create a .env file based on .env.example with your API key")
    
    # Define the event information structure - this matches the required fields in Main_Settings.py
    event_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the comedy event"},
            "venue": {"type": "string", "description": "The name of the venue where the event is held"},
            "summary": {"type": "string", "description": "A brief summary or description of the event"},
            "address": {"type": "string", "description": "The physical address of the venue"},
            "email": {"type": "string", "description": "Contact email for the event or venue"},
            "city": {"type": "string", "description": "The city where the event is taking place"},
            "province": {"type": "string", "description": "The province where the event is taking place"},
            "producers": {"type": "string", "description": "The names of individuals or organizations producing the event"},
            "event_link": {"type": "string", "description": "URL link to the event page"},
            "date": {"type": "string", "description": "The date and time when the event takes place"}
        },
        "required": [
            "title", "venue", "summary", "address", "email", 
            "city", "province", "producers", "event_link", "date"
        ]
    }
    
    # Define instructions for the AI on how to extract information
    extraction_instructions = """
    Extract detailed information about this comedy event. For each field:
    
    - title: Extract the complete title of the event
    - venue: Extract the name of the venue where the event is held
    - summary: Extract a concise description of the event (1-3 sentences)
    - address: Extract the full physical address of the venue
    - email: Extract any contact email address for the event or venue
    - city: Extract only the city name
    - province: Extract only the province name
    - producers: Extract names of individuals or organizations producing/hosting the event
    - date: Extract the date and time of the event
    
    If a field is not explicitly found on the page, make your best inference based on
    available information. For email, if not found, return "Not provided".
    """
    
    # Configure and return the AI text analyzer
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",  # AI model to use
        api_token=api_key,  # API key for authentication
        schema=event_schema,  # Information structure to extract
        extraction_type="schema",  # Use structured extraction
        instruction=extraction_instructions,  # Instructions for the AI
        input_format="markdown",  # Format of the input content
        verbose=True,  # Show detailed information during extraction
    )

def get_usage_stats(llm_strategy: LLMExtractionStrategy) -> Dict:
    """
    Get usage statistics from the AI text analyzer.
    
    Args:
        llm_strategy (LLMExtractionStrategy): The AI text analyzer
        
    Returns:
        Dict: Usage statistics
    """
    # This is a placeholder - actual implementation depends on the AI provider's API
    return {
        "total_tokens": getattr(llm_strategy, "total_tokens", 0),
        "total_cost": getattr(llm_strategy, "total_cost", 0),
        "total_requests": getattr(llm_strategy, "total_requests", 0),
    }