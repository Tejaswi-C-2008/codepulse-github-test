from fastapi import APIRouter
from pydantic import BaseModel

from backend.database import get_connection

class RepoCreate(BaseModel):
    user_id: str
    github_repo_id: int
    name: str
    url: str

router = APIRouter(
    prefix="/repos",
    tags=["Repositories"]
)


@router.get("/")
def get_repos():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM repos
                ORDER BY created_at DESC
            """)

            rows = cur.fetchall()

            return [list(row) for row in rows]

    finally:
        conn.close()

@router.post("/")
def create_repo(repo: RepoCreate):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO repos (user_id, github_repo_id, name, url)
                VALUES (%s, %s, %s, %s)
                RETURNING id, user_id, github_repo_id, name, url, created_at
                """,
                (
                    repo.user_id,
                    repo.github_repo_id,
                    repo.name,
                    repo.url,
                ),
            )

            row = cur.fetchone()
            conn.commit()

            return {
                "id": str(row[0]),
                "user_id": str(row[1]),
                "github_repo_id": row[2],
                "name": row[3],
                "url": row[4],
                "created_at": row[5],
            }

    finally:
        conn.close()