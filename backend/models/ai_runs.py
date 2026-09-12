from uuid import UUID
from datetime import date, datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class AIRunCreate(BaseModel):
    user_id: UUID
    week: date
    prompt_version: str
    input_snapshot_hash: Optional[str] = None
    output_text: Optional[str] = None
    eval_scores: Optional[Dict[str, Any]] = None


class AIRunResponse(BaseModel):
    id: UUID
    user_id: UUID
    week: date
    prompt_version: str
    input_snapshot_hash: Optional[str] = None
    output_text: Optional[str] = None
    eval_scores: Optional[Dict[str, Any]] = None
    created_at: datetime