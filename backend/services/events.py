from backend.database import get_connection
from backend.models.event import EventCreate


def create_event(event: EventCreate):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO events (user_id, repo_id, type, timestamp)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    event.user_id,
                    event.repo_id,
                    event.type,
                    event.timestamp,
                ),
            )

            event_id = cursor.fetchone()[0]
            connection.commit()

            return event_id

    finally:
        connection.close()