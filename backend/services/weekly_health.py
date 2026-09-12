from backend.database import get_connection
from backend.models.weekly_health import WeeklyHealthCreate, WeeklyHealthResponse


def create_weekly_health(data: WeeklyHealthCreate):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO weekly_health (
                    user_id,
                    week_start,
                    health_score,
                    burnout_risk_flag,
                    ai_summary_text
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id, week_start)
                DO UPDATE SET
                    health_score = EXCLUDED.health_score,
                    burnout_risk_flag = EXCLUDED.burnout_risk_flag,
                    ai_summary_text = EXCLUDED.ai_summary_text
                RETURNING id
                """,
                (
                    data.user_id,
                    data.week_start,
                    data.health_score,
                    data.burnout_risk_flag,
                    data.ai_summary_text,
                )
            )

            weekly_health_id = cur.fetchone()[0]
            conn.commit()

            return weekly_health_id

    finally:
        conn.close()


def get_weekly_health_by_user(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    user_id,
                    week_start,
                    health_score,
                    burnout_risk_flag,
                    ai_summary_text
                FROM weekly_health
                WHERE user_id = %s
                ORDER BY week_start DESC
                """,
                (user_id,)
            )

            rows = cur.fetchall()

            return [
                WeeklyHealthResponse(
                    id=row[0],
                    user_id=row[1],
                    week_start=row[2],
                    health_score=row[3],
                    burnout_risk_flag=row[4],
                    ai_summary_text=row[5],
                )
                for row in rows
            ]

    finally:
        conn.close()