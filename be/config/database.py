from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()  # Load biến môi trường từ .env

def get_database():
    uri = os.getenv("MONGODB_URI")
    try:
        client = MongoClient(uri)
        client.admin.command("ping")  # Kiểm tra kết nối
        print("✅ Successfully connected to MongoDB!")
        return client["smart_home"]
    except ConnectionFailure as e:
        print("❌ MongoDB connection failed:", e)
        return None
