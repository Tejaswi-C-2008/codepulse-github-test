from typing import Optional
from pydantic import BaseModel

class GitHubRepository(BaseModel):
    id: int
    name: str
    full_name: str
    html_url: str
    private: bool
    description: Optional[str] = None