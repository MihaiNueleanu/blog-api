from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class EmailMessage(BaseModel):
    subject: str
    body: str
    from_email: str
