from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path=env_path)

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL)
db = client["studybuddy"]  # database name
uploads_collection = db["uploads"]  # collection name

#print("MongoDB URL:", os.getenv("MONGODB_URL"))

