from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class WebEvent(BaseModel):
    session_id: str
    path: str
    timestamp: Optional[datetime] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    fingerprint: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None