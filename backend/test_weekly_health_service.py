from backend.database import get_connection
from backend.models.weekly_health import WeeklyHealthCreate
from backend.services.weekly_health import create_weekly_health


# Get the existing test user's UUID
conn = get_connection()

try:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM users WHERE github_id = %s",
            (100001,)
        )
        user = cur.fetchone()
finally:
    conn.close()


if user is None:
    raise Exception("Test user with github_id 100001 not found")

user_id = user[0]


# Create weekly health data
data = WeeklyHealthCreate(
    user_id=user_id,
    week_start="2026-09-07",
    health_score=82.50,
    burnout_risk_flag=False,
    ai_summary_text="Developer activity looks healthy this week."
)


# Insert using the service
weekly_health_id = create_weekly_health(data)

print("Weekly Health database insertion successful")
print("Weekly Health ID:", weekly_health_id)