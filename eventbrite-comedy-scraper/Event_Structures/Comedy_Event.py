"""
Definition of the comedy event data structure.
"""

from pydantic import BaseModel, Field
from typing import Optional

class ComedyEvent(BaseModel):
    """
    Represents the data structure of a comedy event.
    """
    title: str = Field(..., description="The title of the comedy event")
    venue: str = Field(..., description="The name of the venue where the event is held")
    summary: str = Field(..., description="A brief summary or description of the event")
    address: str = Field(..., description="The physical address of the venue")
    email: str = Field(default="Not provided", description="Contact email for the event or venue")
    city: str = Field(..., description="The city where the event is taking place")
    province: str = Field(..., description="The province where the event is taking place")
    producers: str = Field(..., description="The names of individuals or organizations producing the event")
    event_link: str = Field(..., description="URL link to the event page")
    date: str = Field(..., description="The date and time when the event takes place")
    
    # Optional fields
    price: Optional[str] = Field(None, description="Ticket price information")
    capacity: Optional[int] = Field(None, description="Venue capacity")
    duration: Optional[str] = Field(None, description="Duration of the event")
    performers: Optional[str] = Field(None, description="Names of performers")
    age_restriction: Optional[str] = Field(None, description="Age restrictions for the event")
    
    class Config:
        """Configuration for the ComedyEvent model."""
        schema_extra = {
            "example": {
                "title": "Comedy Night at The Laugh Factory",
                "venue": "The Laugh Factory",
                "summary": "A night of stand-up comedy featuring top local comedians.",
                "address": "123 Main St, Toronto, ON M5V 1A1",
                "email": "info@laughfactory.com",
                "city": "Toronto",
                "province": "Ontario",
                "producers": "Laugh Productions Inc.",
                "event_link": "https://www.eventbrite.ca/e/comedy-night-at-the-laugh-factory-tickets-123456789",
                "date": "2023-12-15 8:00 PM",
                "price": "$25-35",
                "capacity": 150,
                "duration": "2 hours",
                "performers": "John Doe, Jane Smith, Bob Johnson",
                "age_restriction": "19+"
            }
        }