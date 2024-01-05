from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List

app = FastAPI()

# MongoDB Connection
DATABASE_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "hotelsDB"
COLLECTION_NAME = "hotels"

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Model for Hotel
class Hotel(BaseModel):
    name: str
    address: str
    rating: float
    amenities: List[str]
    price_per_night: float
    available_rooms: int

# Sample Data
sample_data = [
  {
    "name": "Scenic Chalet",
    "address": "567 Mountain Road, Hilltop",
    "rating": 4.5,
    "amenities": ["Panoramic Views", "Fireplace", "Private Balcony"],
    "price_per_night": 220.0,
    "available_rooms": 12
  },
  {
    "name": "Luxury Penthouse Suites",
    "address": "789 Skyline Avenue, Uptown",
    "rating": 4.9,
    "amenities": ["Exclusive Penthouse Access", "Sky Lounge", "Butler Service"],
    "price_per_night": 400.0,
    "available_rooms": 8
  },
  {
    "name": "Riverside Retreat",
    "address": "321 Riverbank Lane, Waterside",
    "rating": 4.3,
    "amenities": ["River View", "Kayaking Excursions", "Riverside Dining"],
    "price_per_night": 170.0,
    "available_rooms": 20
  },
  {
    "name": "Historical Manor House",
    "address": "987 Heritage Road, Old Estates",
    "rating": 4.7,
    "amenities": ["Antique Decor", "Formal Gardens", "Tea Room"],
    "price_per_night": 250.0,
    "available_rooms": 15
  },
  {
    "name": "Urban Loft Apartments",
    "address": "543 Loft Lane, Downtown",
    "rating": 4.6,
    "amenities": ["Modern Loft Design", "City Views", "Rooftop Terrace"],
    "price_per_night": 180.0,
    "available_rooms": 18
  },
  {
    "name": "Mountain View Lodge",
    "address": "876 Alpine Way, Summit Peaks",
    "rating": 4.4,
    "amenities": ["Mountain Views", "Ski Access", "Cozy Fireplace"],
    "price_per_night": 190.0,
    "available_rooms": 16
  },
  {
    "name": "Family Beach Resort",
    "address": "234 Seaside Boulevard, Coastal Haven",
    "rating": 4.2,
    "amenities": ["Kids Club", "Beachfront Suites", "Family-Friendly Activities"],
    "price_per_night": 150.0,
    "available_rooms": 25
  },
  {
    "name": "Zen Garden Retreat",
    "address": "432 Tranquil Lane, Serenity Valley",
    "rating": 4.8,
    "amenities": ["Japanese Zen Garden", "Meditation Room", "Holistic Spa"],
    "price_per_night": 280.0,
    "available_rooms": 10
  },
  {
    "name": "Golf Resort Paradise",
    "address": "765 Fairway Drive, Golfville",
    "rating": 4.6,
    "amenities": ["Championship Golf Course", "Clubhouse", "Golf Suites"],
    "price_per_night": 220.0,
    "available_rooms": 14
  },
  {
    "name": "Classic European Hotel",
    "address": "109 Vintage Avenue, Old World City",
    "rating": 4.5,
    "amenities": ["Elegant Decor", "Fine Dining", "Classic Architecture"],
    "price_per_night": 200.0,
    "available_rooms": 22
  }
]


# Insert Sample Data into MongoDB
def insert():
    for data in sample_data:
        result = collection.insert_one(data)
        inserted_id = str(result.inserted_id)
        print(f"Sample data inserted with ID: {inserted_id}")

# CRUD Operations...

# Run the FastAPI app
if __name__ == "__main__":
    insert()
