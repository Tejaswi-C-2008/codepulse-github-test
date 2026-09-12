from uuid import UUID

from fastapi import APIRouter

from backend.services.github import sync_github_repository


router = APIRouter(prefix="/github", tags=["GitHub"])


@router.post("/sync")
def sync_repository(
    user_id: UUID,
    repo_id: UUID,
    owner: str,
    repo: str,
):
    return sync_github_repository(
        str(user_id),
        str(repo_id),
        owner,
        repo,
    )