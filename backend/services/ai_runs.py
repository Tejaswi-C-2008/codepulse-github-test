from psycopg.types.json import Jsonb

from backend.database import get_connection
from backend.models.ai_runs import AIRunCreate, AIRunResponse


def create_ai_run(data: AIRunCreate):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ai_runs (
                    user_id,
                    week,
                    prompt_version,
                    input_snapshot_hash,
                    output_text,
                    eval_scores
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    data.user_id,
                    data.week,
                    data.prompt_version,
                    data.input_snapshot_hash,
                    data.output_text,
                    Jsonb(data.eval_scores or {}),
                )
            )

            ai_run_id = cur.fetchone()[0]
            conn.commit()

            return ai_run_id

    finally:
        conn.close()


def get_ai_runs_by_user(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    user_id,
                    week,
                    prompt_version,
                    input_snapshot_hash,
                    output_text,
                    eval_scores,
                    created_at
                FROM ai_runs
                WHERE user_id = %s
                ORDER BY week DESC, created_at DESC
                """,
                (user_id,)
            )

            rows = cur.fetchall()

            return [
                AIRunResponse(
                    id=row[0],
                    user_id=row[1],
                    week=row[2],
                    prompt_version=row[3],
                    input_snapshot_hash=row[4],
                    output_text=row[5],
                    eval_scores=row[6],
                    created_at=row[7]
                )
                for row in rows
            ]

    finally:
        conn.close()