
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

client   =  AsyncIOMotorClient(MONGO_URI)

db = client["ecommercedb"]

products_collection = db["products"]
orders_collection = db["orders"]


