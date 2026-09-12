from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class DailyMetricCreate(BaseModel):
    user_id: UUID
    date: date
    commits_count: int = 0
    prs_opened: int = 0
    prs_reviewed: int = 0
    focus_score: Optional[float] = None
    context_switch_score: Optional[float] = None