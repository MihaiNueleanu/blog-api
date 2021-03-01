from services.clap import count_claps, give_clap
from models.clap import Clap
from starlette.requests import Request
from services.discussion import find_comment_by_path,  post_comment
from models.comment import Comment
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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
