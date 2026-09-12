from uuid import UUID

from fastapi import APIRouter

from backend.models.ai_runs import AIRunCreate
from backend.services.ai_runs import create_ai_run, get_ai_runs_by_user
from backend.services.health_analysis import analyze_user_health


router = APIRouter(
    prefix="/ai-runs",
    tags=["AI Runs"]
)


@router.post("/")
def create_ai_run_api(data: AIRunCreate):
    ai_run_id = create_ai_run(data)

    return {
        "message": "AI run created successfully",
        "ai_run_id": str(ai_run_id)
    }


@router.get("/{user_id}")
def get_ai_runs_api(user_id: UUID):
    ai_runs = get_ai_runs_by_user(user_id)

    return {
        "count": len(ai_runs),
        "ai_runs": [
            ai_run.model_dump(mode="json")
            for ai_run in ai_runs
        ]
    }

@router.post("/health/{user_id}/{week_start}")
def generate_health_analysis(user_id: UUID, week_start: str):
    from datetime import date

    week_date = date.fromisoformat(week_start)

    result = analyze_user_health(
        str(user_id),
        week_date
    )

    return result

@router.get("/health/{user_id}/{week_start}")
def get_health_analysis(user_id: UUID, week_start: str):
    from datetime import date

    week_date = date.fromisoformat(week_start)

    ai_runs = get_ai_runs_by_user(user_id)

    matching_runs = [
        run for run in ai_runs
        if run.week == week_date
        and run.prompt_version == "health-v1"
    ]

    if not matching_runs:
        return {
            "message": "No health analysis found for this week",
            "user_id": str(user_id),
            "week": week_start
        }

    latest_run = matching_runs[0]

    return {
        "message": "Health analysis retrieved successfully",
        "ai_run": latest_run.model_dump(mode="json")
    }