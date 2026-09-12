from backend.services.events import create_event
from backend.models.event import EventCreate
from datetime import datetime
from backend.database import get_connection


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
    event = EventCreate(
        user_id=user[0],
        repo_id=None,
        type="commit",
        timestamp=datetime.now()
    )

    event_id = create_event(event)

    print("Event created successfully!")
    print("Event ID:", event_id)