from uuid import UUID
from datetime import date
from typing import Optional

from pydantic import BaseModel


class WeeklyHealthCreate(BaseModel):
    user_id: UUID
    week_start: date
    health_score: Optional[float] = None
    burnout_risk_flag: Optional[bool] = False
    ai_summary_text: Optional[str] = None


class WeeklyHealthResponse(BaseModel):
    id: UUID
    user_id: UUID
    week_start: date
    health_score: Optional[float] = None
    burnout_risk_flag: Optional[bool] = False
    ai_summary_text: Optional[str] = None