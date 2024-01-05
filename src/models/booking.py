from pydantic import BaseModel
from datetime import datetime

class Booking(BaseModel):
    hotel_id: str
    check_in_date: datetime
    check_out_date: datetime
