from backend.database import get_connection
from backend.models.ai_runs import AIRunCreate
from backend.services.ai_runs import create_ai_run


# Get the existing test user
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


# Create AI run data
data = AIRunCreate(
    user_id=user_id,
    week="2026-09-07",
    prompt_version="v1",
    input_snapshot_hash="test-hash-001",
    output_text="Developer health analysis generated successfully.",
    eval_scores={
        "quality": 0.90,
        "relevance": 0.95
    }
)


# Insert using the service
ai_run_id = create_ai_run(data)

print("AI Runs database insertion successful")
print("AI Run ID:", ai_run_id)