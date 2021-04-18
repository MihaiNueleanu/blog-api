
import asyncio
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from models.clap import Clap
from models.comment import Comment
from services.clap import count_claps, give_clap
from services.discussion import find_comment_by_path, post_comment
from services.email import send_email
from services.medium import sync_blog_to_medium
from settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/discussions")
async def get_comments(path: Optional[str]):
    if not path:
        return {}

    result = await find_comment_by_path(path)
    return result


@app.put("/api/discussions")
async def create_comment(comment: Comment, request: Request):
    comment.ip = request.client.host
    comment.timestamp = datetime.now()
    await post_comment(comment)

    send_email(receiver=settings.MY_EMAIL,
               subject="dotmethod | new message on the blog",
               text=f"From: {comment.name}\nMessage: {comment.body}")

    return comment


@app.get("/api/clap")
async def get_claps(path: str):
    claps = await count_claps(path)
    return {
        "claps": claps
    }


@app.put("/api/clap")
async def clap(clap: Clap, request: Request):
    try:
        clap.ip = request.client.host
        clap.timestamp = datetime.now()
        await give_clap(clap)
        return clap
    except Exception:
        raise HTTPException(status_code=400, detail="Already voted")


@app.get("/api/sync_medium")
async def sync_medium(x_secret_token: Optional[str] = Header(None)):
    if not x_secret_token or x_secret_token != settings.secret_token:
        raise HTTPException(status_code=403, detail="Not allowed")

    loop = asyncio.get_event_loop()
    loop.create_task(sync_blog_to_medium())

    return {"message": "Success"}
