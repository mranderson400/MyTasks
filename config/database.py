from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing from environment variables")

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["task_management"]  # Change this to your DB name
users_collection = db["users"]
tasks_collection = db["tasks"]  

