import motor.motor_asyncio
from settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.discuss_mongo_url)

database = client.discuss
