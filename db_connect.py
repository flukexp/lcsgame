import os
from dotenv import load_dotenv
from pymongo import MongoClient

def connect_to_mongo():

    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

    if not MONGO_URI:
        raise ValueError("MONGO_URI is not set in .env")

    client = MongoClient(MONGO_URI)
    db = client["LCS"]
    collection = db["user"]

    test_data = {"name": "Test User", "score": 0}
    insert_result = collection.insert_one(test_data)
    print(f"✅ Inserted ID: {insert_result.inserted_id}")

    found_data = collection.find_one({"name": "Test User"})
    print(f"✅ Found Data: {found_data}")

    client.close()
    print("✅ MongoDB connection closed.")
