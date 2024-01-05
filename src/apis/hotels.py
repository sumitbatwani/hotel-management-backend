from fastapi import APIRouter, HTTPException, Query
from typing import List
from db import MongoDB
from models.hotel import Hotel
from bson import ObjectId

router = APIRouter()
mongo = MongoDB(uri="mongodb://localhost:27017/", db_name="hotelsDB")
hotels_collection = mongo.get_database_by_name("hotelsDB")["hotels"]

@router.post("/hotels/", response_model=Hotel)
def create_hotel(hotel: Hotel):
    hotel_data = hotel.dict()
    result = hotels_collection.insert_one(hotel_data)
    hotel_data['_id'] = str(result.inserted_id)
    return hotel_data

@router.get("/hotels/{hotel_id}", response_model=Hotel)
def read_hotel(hotel_id: str):
    result = hotels_collection.find_one({"_id": ObjectId(hotel_id)})
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Hotel not found")

@router.get("/hotels/", response_model=List[Hotel])
def read_hotels(skip: int = 0, limit: int = 10):
    cursor = hotels_collection.find().skip(skip).limit(limit)
    return list(cursor)

@router.patch("/hotels/{hotel_id}", response_model=Hotel)
def update_hotel(hotel_id: str, hotel: Hotel):
    existing_hotel = hotels_collection.find_one({"_id": ObjectId(hotel_id)})

    if existing_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")

    # Update only the fields provided in the request
    update_fields = {k: v for k, v in hotel.dict().items() if v is not None}

    # Perform the update if there are fields to update
    if update_fields:
        hotels_collection.update_one({"_id": ObjectId(hotel_id)}, {"$set": update_fields})

    # Fetch the updated document
    updated_hotel = hotels_collection.find_one({"_id": ObjectId(hotel_id)})

    return updated_hotel

@router.delete("/hotels/{hotel_id}", response_model=dict)
def delete_hotel(hotel_id: str):
    result = hotels_collection.delete_one({"_id": ObjectId(hotel_id)})
    if result.deleted_count == 1:
        return {"message": "Hotel deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
@router.get("/hotels/filter/", response_model=List[Hotel])
def filter_hotels(
    name: str = Query(None, description="Name to filter hotels"),
    location: str = Query(None, description="Location to filter hotels"),
    amenities: List[str] = Query(None, description="List of amenities to filter hotels"),
    min_rating: float = Query(None, description="Minimum rating to filter hotels"),
    max_rating: float = Query(None, description="Maximum rating to filter hotels")
):
    query_params = {}

    if name:
        query_params["name"] = {"$regex": f".*{name}.*", "$options": "i"}

    if location:
        query_params["address"] = {"$regex": f".*{location}.*", "$options": "i"}

    if amenities:
        query_params["amenities"] = {"$all": amenities}

    if min_rating is not None:
        query_params["rating"] = {"$gte": min_rating}

    if max_rating is not None:
        query_params.setdefault("rating", {})["$lte"] = max_rating

    cursor = hotels_collection.find(query_params)
    return list(cursor)
