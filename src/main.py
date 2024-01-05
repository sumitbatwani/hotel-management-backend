from http.client import HTTPException
from typing import List
from fastapi import FastAPI
from db import MongoDB
from fastapi.middleware.cors import CORSMiddleware
from apis.hotels import router as hotel_router

app = FastAPI()

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MongoDB connection
mongo = MongoDB(uri="mongodb://localhost:27017/", db_name="hotelsDB")
db = mongo.get_database_by_name("hotelsDB")
hotels_collection = db["hotels"]

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/ping")
async def ping_db():
    try:
        # Attempt to run a simple MongoDB command to check the connection
        mongo.db.command("ping")
        return {"ping": "pong", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Include your API routers
app.include_router(hotel_router, prefix="/hotels", tags=["hotels"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)