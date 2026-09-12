from fastapi import APIRouter
from backend.models.event import EventCreate
from backend.services.events import create_event

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/")
def test_events():
    return {"message": "Events route is working"}


@router.post("/")
def add_event(event: EventCreate):
    event_id = create_event(event)

    return {
        "message": "Event created successfully",
        "event_id": event_id
    }