from typing import List
from models.comment import Comment
from services.database import database

collection = database.discussions


async def post_comment(comment: Comment) -> None:
    await collection.insert_one(comment.dict())


async def find_comment_by_path(path: str) -> List[Comment]:
    cursor = collection.find({'path': path}, {'_id': 0})
    result = await cursor.to_list(length=100)
    return result
