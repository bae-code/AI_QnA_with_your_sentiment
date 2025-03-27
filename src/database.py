from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from src.config import settings

# Connect to MongoDB
mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB_NAME]

# Connect to Redis
redis_client = redis.from_url(settings.REDIS_URL)


user_collection = mongo_db["users"]
letter_collection = mongo_db["letters"]
token_collection = mongo_db["tokens"]
