from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import get_connection
from backend.routes.users import router as users_router
from backend.routes.repos import router as repos_router
from backend.routes.events import router as events_router
from backend.routes.daily_metrics import router as daily_metrics_router
from backend.routes.weekly_health import router as weekly_health_router
from backend.routes.ai_runs import router as ai_runs_router
from backend.routes.github import router as github_router
from backend.routes.auth import router as auth_router


app = FastAPI(title="CodePulse API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(repos_router)
app.include_router(events_router)
app.include_router(ai_runs_router)
app.include_router(daily_metrics_router)
app.include_router(weekly_health_router)
app.include_router(github_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "CodePulse API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-health")
def db_health():
    conn = get_connection()
    conn.close()
    return {"database": "connected"}