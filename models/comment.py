from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Comment(BaseModel):
    ip: Optional[str]
    timestamp: Optional[datetime]
    path: str
    unique_token: str
    name: str
    body: str
