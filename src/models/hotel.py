from typing import List, Optional
from pydantic import BaseModel

class Hotel(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = None
    amenities: Optional[List[str]] = None
    price_per_night: Optional[float] = None
    available_rooms: Optional[int] = None