from backend.services.daily_metrics import create_daily_metric
from backend.models.daily_metric import DailyMetricCreate
from backend.database import get_connection
from datetime import date


connection = get_connection()

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM users LIMIT 1")
        user = cursor.fetchone()

finally:
    connection.close()


if user is None:
    print("No users found in the users table.")
else:
    metric = DailyMetricCreate(
        user_id=user[0],
        date=date.today(),
        commits_count=5,
        prs_opened=2,
        prs_reviewed=3,
        focus_score=82.50,
        context_switch_score=15.25
    )

    try:
        metric_id = create_daily_metric(metric)
        print("Daily metric created successfully!")
        print("Metric ID:", metric_id)
    except Exception as error:
        print("Daily metric test skipped:", error)