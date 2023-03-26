from datetime import datetime, timedelta
from typing import List
from models.event import WebEvent
from services.database import database

collection = database.analytics


async def create_event(event: WebEvent) -> None:
    await collection.insert_one(event.dict())


async def get_sessions_per_day(number_of_days: int):
    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()
    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start_date, "$lt": end_date}
            }
        },
        {
            "$group": {
                "_id": {"year": {"$year": "$timestamp"}, "month": {"$month": "$timestamp"}, "day": {"$dayOfMonth": "$timestamp"}, "session_id": "$session_id"}
            }
        },
        {
            "$group": {
                "_id": {"year": "$_id.year", "month": "$_id.month", "day": "$_id.day"},
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "_id.year": 1, "_id.month": 1, "_id.day": 1
            }
        }
    ]
    results = await collection.aggregate(pipeline).to_list(None)

    return results
