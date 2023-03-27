from datetime import datetime, timedelta
from typing import List
from models.event import WebEvent
from services.database import database
from user_agents import parse

collection = database.analytics


async def create_event(event: WebEvent) -> None:
    await collection.insert_one(event.dict())


async def get_sessions_per_day(number_of_days=7):
    start_date = datetime.now() - timedelta(days=number_of_days)
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


async def get_hits_per_page(number_of_days=7):
    start_date = datetime.now() - timedelta(days=number_of_days)
    end_date = datetime.now()
    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start_date, "$lt": end_date}
            }
        },
        {
            "$group": {
                "_id": {"path": "$path"},
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]
    results = await collection.aggregate(pipeline).to_list(None)

    return results


async def get_unique_sessions_per_page(number_of_days=7):
    start_date = datetime.now() - timedelta(days=number_of_days)
    end_date = datetime.now()
    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start_date, "$lt": end_date}
            }
        },
        {
            "$group": {
                "_id": {"path": "$path", "session_id": "$session_id"},
                "count": {"$sum": 1}
            }
        },
        {
            "$group": {
                "_id": {"path": "$_id.path"},
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]
    results = await collection.aggregate(pipeline).to_list(None)

    return results


def enrich_event(event, request):
    real_ip = request.headers.get("X-Real-IP")
    event.timestamp = datetime.now()
    event.user_agent = request.headers.get("User-Agent")
    event.language = request.headers.get("Accept-Language")
    event.country = request.headers.get("CF-IPCountry")

    event.ip = real_ip if real_ip else request.client.host
    if request.headers.get("cf-connecting-ip"):
        event.ip = request.headers.get("cf-connecting-ip")

    if event.user_agent:
        user_agent = parse(event.user_agent)
        event.browser = user_agent.browser._asdict()
        event.os = user_agent.os._asdict()
        event.device = user_agent.device._asdict()
