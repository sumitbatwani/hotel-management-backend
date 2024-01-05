from typing import List, Optional
from pydantic import BaseModel
from .booking import Booking

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    bookings: List[Booking] = []