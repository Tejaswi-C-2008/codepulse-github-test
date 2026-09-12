from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class EventCreate(BaseModel):
    user_id: UUID
    repo_id: Optional[UUID] = None
    type: str
    timestamp: datetime