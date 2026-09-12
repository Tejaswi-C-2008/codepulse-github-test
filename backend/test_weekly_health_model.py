from uuid import UUID
from datetime import date

from backend.models.weekly_health import WeeklyHealthCreate


test_data = WeeklyHealthCreate(
    user_id=UUID("00000000-0000-0000-0000-000000000001"),
    week_start=date(2026, 9, 7),
    health_score=82.50,
    burnout_risk_flag=False,
    ai_summary_text="Developer activity looks healthy this week."
)

print("Weekly Health model verified successfully")
print(test_data)