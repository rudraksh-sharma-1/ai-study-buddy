import cloudinary
from dotenv import load_dotenv
import os

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path=env_path)


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)
#print("Cloudinary config loaded:")
#print("CLOUD_NAME:", os.getenv("CLOUDINARY_CLOUD_NAME"))
#print("API_KEY:", os.getenv("CLOUDINARY_API_KEY"))
