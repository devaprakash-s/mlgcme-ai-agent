# db_connect.py

from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

def get_database():
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]

# Test connection
if __name__ == "__main__":
    db = get_database()
    print("Collections available:", db.list_collection_names())
