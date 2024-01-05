import datetime
from fastapi import APIRouter, HTTPException, Query
from typing import List
from db import MongoDB
from models.user import User
from bson import ObjectId
from models.booking import Booking

router = APIRouter()
mongo = MongoDB(uri="mongodb://localhost:27017/", db_name="hotelsDB")
users_collection = mongo.get_database_by_name("hotelsDB")["users"]

@router.post("/", response_model=User)
def create_user(user: User):
    user_data = user.dict()
    result = users_collection.insert_one(user_data)
    user_data['_id'] = str(result.inserted_id)
    return user_data

@router.get("/{user_id}", response_model=User)
def read_user(user_id: str):
    result = users_collection.find_one({"_id": ObjectId(user_id)})
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10):
    cursor = users_collection.find().skip(skip).limit(limit)
    return list(cursor)

@router.post("/{user_id}/bookings/{hotel_id}")
def book_hotel(user_id: str, hotel_id: str):
    check_in_date = datetime.now()
    check_out_date = check_in_date + datetime.timedelta(days=7)  # Add a default booking duration (7 days in this example)

    booking = Booking(hotel_id=hotel_id, check_in_date=check_in_date, check_out_date=check_out_date)
    
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$addToSet": {"bookings": booking.dict()}}
    )
    
    if result.modified_count == 1:
        return {"message": "Hotel booked successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found or Hotel not found")
