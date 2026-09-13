from fastapi import APIRouter
from pydantic import BaseModel, Field
from psycopg.types.json import Json
from backend.database import get_connection


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


class UserCreate(BaseModel):
    github_id: int
    name: str
    email: str | None = None
    settings: dict = Field(default_factory=dict)


@router.get("/")
def get_users():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    github_id,
                    name,
                    email,
                    settings,
                    created_at,
                    updated_at
                FROM users
                ORDER BY created_at DESC
                """
            )

            rows = cur.fetchall()

            return [
                {
                    "id": str(row[0]),
                    "github_id": row[1],
                    "name": row[2],
                    "email": row[3],
                    "settings": row[4],
                    "created_at": row[5],
                    "updated_at": row[6],
                }
                for row in rows
            ]

    finally:
        conn.close()


@router.post("/")
def create_user(user: UserCreate):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (
                    github_id,
                    name,
                    email,
                    settings
                )
                VALUES (%s, %s, %s, %s)
                RETURNING
                    id,
                    github_id,
                    name,
                    email,
                    settings,
                    created_at,
                    updated_at
                """,
                (
                    user.github_id,
                    user.name,
                    user.email,
                    Json(user.settings),
                ),
            )

            row = cur.fetchone()
            conn.commit()

            return {
                "id": str(row[0]),
                "github_id": row[1],
                "name": row[2],
                "email": row[3],
                "settings": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
