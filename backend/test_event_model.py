from backend.models.event import EventCreate

from uuid import uuid4
from datetime import datetime, timezone


event = EventCreate(
    user_id=uuid4(),
    repo_id=uuid4(),
    type="commit",
    timestamp=datetime.now(timezone.utc)
)

print(event)

print(event.model_dump())