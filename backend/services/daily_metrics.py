from datetime import date
from backend.database import get_connection
from backend.models.daily_metric import DailyMetricCreate


def create_daily_metric(metric: DailyMetricCreate):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO daily_metrics (
                    user_id,
                    date,
                    commits_count,
                    prs_opened,
                    prs_reviewed,
                    focus_score,
                    context_switch_score
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    metric.user_id,
                    metric.date,
                    metric.commits_count,
                    metric.prs_opened,
                    metric.prs_reviewed,
                    metric.focus_score,
                    metric.context_switch_score,
                ),
            )

            metric_id = cursor.fetchone()[0]
            connection.commit()

            return metric_id

    finally:
        connection.close()


def process_daily_metrics(user_id: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # Get all events for this user grouped by day
            cursor.execute(
                """
                SELECT
                    timestamp::date AS event_date,
                    COUNT(*) FILTER (WHERE type = 'commit') AS commits_count,
                    COUNT(*) FILTER (WHERE type = 'pr') AS prs_opened,
                    COUNT(*) FILTER (WHERE type = 'review') AS prs_reviewed,
                    COUNT(DISTINCT repo_id) AS distinct_repos,
                    COUNT(DISTINCT type) AS distinct_event_types,
                    COUNT(*) AS total_events
                FROM events
                WHERE user_id = %s
                GROUP BY timestamp::date
                ORDER BY event_date
                """,
                (user_id,),
            )

            daily_rows = cursor.fetchall()

            if not daily_rows:
                connection.commit()
                return []

            processed = []

            for row in daily_rows:
                (
                    event_date,
                    commits_count,
                    prs_opened,
                    prs_reviewed,
                    distinct_repos,
                    distinct_event_types,
                    total_events,
                ) = row

                commits_count = commits_count or 0
                prs_opened = prs_opened or 0
                prs_reviewed = prs_reviewed or 0
                distinct_repos = distinct_repos or 0
                distinct_event_types = distinct_event_types or 0
                total_events = total_events or 0

                # V1 focus score:
                # More repositories and excessive daily activity
                # slightly reduce the score.
                focus_score = 100 - (
                    max(0, distinct_repos - 1) * 15
                    + max(0, total_events - 5) * 5
                    + max(0, distinct_event_types - 2) * 5
                )

                focus_score = max(0, min(100, focus_score))

                # V1 context-switch score:
                # Higher value means more context switching.
                context_switch_score = (
                    max(0, distinct_repos - 1) * 25
                    + max(0, distinct_event_types - 1) * 10
                )

                context_switch_score = max(
                    0, min(100, context_switch_score)
                )

                # Check whether metrics already exist for this day.
                cursor.execute(
                    """
                    SELECT id
                    FROM daily_metrics
                    WHERE user_id = %s AND date = %s
                    """,
                    (user_id, event_date),
                )

                existing = cursor.fetchone()

                if existing:
                    metric_id = existing[0]

                    cursor.execute(
                        """
                        UPDATE daily_metrics
                        SET
                            commits_count = %s,
                            prs_opened = %s,
                            prs_reviewed = %s,
                            focus_score = %s,
                            context_switch_score = %s
                        WHERE id = %s
                        """,
                        (
                            commits_count,
                            prs_opened,
                            prs_reviewed,
                            focus_score,
                            context_switch_score,
                            metric_id,
                        ),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO daily_metrics (
                            user_id,
                            date,
                            commits_count,
                            prs_opened,
                            prs_reviewed,
                            focus_score,
                            context_switch_score
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            user_id,
                            event_date,
                            commits_count,
                            prs_opened,
                            prs_reviewed,
                            focus_score,
                            context_switch_score,
                        ),
                    )

                    metric_id = cursor.fetchone()[0]

                processed.append(
                    {
                        "date": str(event_date),
                        "metric_id": str(metric_id),
                        "commits_count": commits_count,
                        "prs_opened": prs_opened,
                        "prs_reviewed": prs_reviewed,
                        "focus_score": float(focus_score),
                        "context_switch_score": float(context_switch_score),
                    }
                )

            connection.commit()

            return processed

    finally:
        connection.close()

def process_all_daily_metrics():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM users
                ORDER BY id
                """
            )

            users = cursor.fetchall()

        results = []

        for user in users:
            user_id = str(user[0])
            processed = process_daily_metrics(user_id)

            results.append(
                {
                    "user_id": user_id,
                    "days_processed": len(processed),
                    "metrics": processed,
                }
            )

        return results

    finally:
        connection.close()

def get_daily_metrics(user_id: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    date,
                    commits_count,
                    prs_opened,
                    prs_reviewed,
                    focus_score,
                    context_switch_score
                FROM daily_metrics
                WHERE user_id = %s
                ORDER BY date DESC
                """,
                (user_id,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": str(row[0]),
                    "date": str(row[1]),
                    "commits_count": row[2],
                    "prs_opened": row[3],
                    "prs_reviewed": row[4],
                    "focus_score": float(row[5]) if row[5] is not None else None,
                    "context_switch_score": (
                        float(row[6]) if row[6] is not None else None
                    ),
                }
                for row in rows
            ]

    finally:
        connection.close()