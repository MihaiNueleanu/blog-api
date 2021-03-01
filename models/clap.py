from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Clap(BaseModel):
    ip: Optional[str]
    timestamp: Optional[datetime]
    path: str
    unique_token: str
