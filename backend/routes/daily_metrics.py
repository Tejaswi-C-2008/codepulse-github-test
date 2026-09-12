from fastapi import APIRouter
from backend.models.daily_metric import DailyMetricCreate
from backend.services.daily_metrics import (
    create_daily_metric,
    process_daily_metrics,
    process_all_daily_metrics,
    get_daily_metrics,
)

router = APIRouter(prefix="/daily-metrics", tags=["Daily Metrics"])


@router.post("/")
def add_daily_metric(metric: DailyMetricCreate):
    metric_id = create_daily_metric(metric)

    return {
        "message": "Daily metric created successfully",
        "metric_id": metric_id
    }


@router.post("/process/{user_id}")
def process_metrics(user_id: str):
    processed = process_daily_metrics(user_id)

    return {
        "message": "Daily metrics processed successfully",
        "user_id": user_id,
        "days_processed": len(processed),
        "metrics": processed,
    }

@router.post("/process-all")
def process_all_metrics():
    results = process_all_daily_metrics()

    return {
        "message": "Daily metrics processed for all users",
        "users_processed": len(results),
        "results": results,
    }

@router.get("/{user_id}")
def get_metrics(user_id: str):
    metrics = get_daily_metrics(user_id)

    return {
        "user_id": user_id,
        "days": len(metrics),
        "metrics": metrics,
    }