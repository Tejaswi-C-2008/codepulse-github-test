from uuid import UUID

from fastapi import APIRouter

from backend.models.weekly_health import WeeklyHealthCreate
from backend.services.weekly_health import create_weekly_health, get_weekly_health_by_user


router = APIRouter(
    prefix="/weekly-health",
    tags=["Weekly Health"]
)


@router.post("/")
def create_weekly_health_api(data: WeeklyHealthCreate):
    weekly_health_id = create_weekly_health(data)

    return {
        "message": "Weekly health created successfully",
        "weekly_health_id": str(weekly_health_id)
    }


@router.get("/{user_id}")
def get_weekly_health_api(user_id: UUID):
    weekly_health = get_weekly_health_by_user(user_id)

    return {
        "count": len(weekly_health),
        "weekly_health": [
            health.model_dump(mode="json")
            for health in weekly_health
        ]
    }