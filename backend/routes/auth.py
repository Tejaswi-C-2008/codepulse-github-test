from fastapi import APIRouter
from pydantic import BaseModel
from psycopg.types.json import Json

from backend.database import get_connection


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class LoginRequest(BaseModel):
    github_id: int


@router.post("/login")
def login(request: LoginRequest):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, github_id, name, email, settings
                FROM users
                WHERE github_id = %s
                """,
                (request.github_id,),
            )

            row = cur.fetchone()

            if row:
                return {
                    "message": "Login successful",
                    "user": {
                        "id": str(row[0]),
                        "github_id": row[1],
                        "name": row[2],
                        "email": row[3],
                        "settings": row[4],
                    },
                }

            return {
                "message": "User not found",
                "user": None,
            }

    finally:
        conn.close()