from backend.models.daily_metric import DailyMetricCreate
from uuid import uuid4
from datetime import date


metric = DailyMetricCreate(
    user_id=uuid4(),
    date=date.today(),
    commits_count=5,
    prs_opened=2,
    prs_reviewed=3,
    focus_score=82.50,
    context_switch_score=15.25
)

print(metric)
print(metric.model_dump())