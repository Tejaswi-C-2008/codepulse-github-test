from datetime import date, timedelta
from hashlib import sha256

from backend.database import get_connection
from backend.models.ai_runs import AIRunCreate
from backend.models.weekly_health import WeeklyHealthCreate
from backend.services.ai_runs import create_ai_run
from backend.services.weekly_health import create_weekly_health


def analyze_user_health(user_id: str, week_start: date):
    week_end = week_start + timedelta(days=6)

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    date,
                    commits_count,
                    prs_opened,
                    prs_reviewed,
                    focus_score,
                    context_switch_score
                FROM daily_metrics
                WHERE user_id = %s
                  AND date BETWEEN %s AND %s
                ORDER BY date
                """,
                (user_id, week_start, week_end),
            )

            rows = cur.fetchall()

    finally:
        conn.close()

    if not rows:
        return {
            "message": "No daily metrics available for this week",
            "user_id": user_id,
            "week": str(week_start),
        }

    total_commits = sum(row[1] or 0 for row in rows)
    total_prs_opened = sum(row[2] or 0 for row in rows)
    total_prs_reviewed = sum(row[3] or 0 for row in rows)

    focus_values = [
        float(row[4])
        for row in rows
        if row[4] is not None
    ]

    context_values = [
        float(row[5])
        for row in rows
        if row[5] is not None
    ]

    average_focus = (
        sum(focus_values) / len(focus_values)
        if focus_values
        else 0
    )

    average_context_switch = (
        sum(context_values) / len(context_values)
        if context_values
        else 0
    )

    if average_focus >= 80 and average_context_switch <= 20:
        health_status = "Healthy"
        health_score = 85
        burnout_risk = "Low"

    elif average_focus >= 60 and average_context_switch <= 40:
        health_status = "Moderate"
        health_score = 65
        burnout_risk = "Medium"

    else:
        health_status = "Needs Attention"
        health_score = 45
        burnout_risk = "High"

    summary = (
        f"Developer health status: {health_status}. "
        f"The developer recorded {total_commits} commits, "
        f"{total_prs_opened} pull requests opened, and "
        f"{total_prs_reviewed} pull requests reviewed during this week. "
        f"Average focus score was {average_focus:.2f}, while "
        f"average context-switch score was "
        f"{average_context_switch:.2f}. "
        f"Estimated burnout risk is {burnout_risk}."
    )

    input_snapshot = (
        f"{user_id}|{week_start}|{total_commits}|"
        f"{total_prs_opened}|{total_prs_reviewed}|"
        f"{average_focus:.2f}|{average_context_switch:.2f}"
    )

    input_snapshot_hash = sha256(
        input_snapshot.encode("utf-8")
    ).hexdigest()

    ai_run = AIRunCreate(
        user_id=user_id,
        week=week_start,
        prompt_version="health-v1",
        input_snapshot_hash=input_snapshot_hash,
        output_text=summary,
        eval_scores={
            "health_score": health_score,
            "average_focus": round(average_focus, 2),
            "average_context_switch": round(
                average_context_switch, 2
            ),
            "burnout_risk": burnout_risk,
        },
    )

    ai_run_id = create_ai_run(ai_run)

    weekly_health = WeeklyHealthCreate(
        user_id=user_id,
        week_start=week_start,
        health_score=health_score,
        burnout_risk_flag=(burnout_risk == "High"),
        ai_summary_text=summary,
    )

    weekly_health_id = create_weekly_health(weekly_health)

    return {
        "message": "Developer health analysis generated successfully",
        "ai_run_id": str(ai_run_id),
        "weekly_health_id": str(weekly_health_id),
        "user_id": user_id,
        "week": str(week_start),
        "health_status": health_status,
        "health_score": health_score,
        "burnout_risk": burnout_risk,
        "total_commits": total_commits,
        "total_prs_opened": total_prs_opened,
        "total_prs_reviewed": total_prs_reviewed,
        "average_focus": round(average_focus, 2),
        "average_context_switch": round(
            average_context_switch, 2
        ),
        "summary": summary,
    }