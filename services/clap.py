
from models.clap import Clap
from services.database import database

collection = database.claps

collection.create_index(
    [('path', 1), ('unique_token', 1)],
    unique=True
)


async def give_clap(clap: Clap) -> None:
    await collection.insert_one(clap.dict())


async def count_claps(path: str) -> int:
    result = await collection.count_documents({'path': path})
    return result
