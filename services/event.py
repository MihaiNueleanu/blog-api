from typing import List
from models.event import WebEvent
from services.database import database

collection = database.analytics


async def create_event(event: WebEvent) -> None:
    await collection.insert_one(event.dict())
