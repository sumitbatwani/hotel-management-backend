from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    
    def get_database_by_name(self, db_name: str):
        return self.client[db_name]

mongo = MongoDB(uri="mongodb://localhost:27017/", db_name="hotelsDB")
