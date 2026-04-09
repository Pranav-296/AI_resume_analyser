from pymongo import MongoClient

MONGO_URI = "your_mongodb_url_here"

client = MongoClient(MONGO_URI)
db = client["resume_db"]
collection = db["results"]