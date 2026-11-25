"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import academics, auth, courses, questions, quizzes, stats, todos

app = FastAPI(title="ESI Revision Platform", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    auth.router, academics.router, courses.router, questions.router,
    quizzes.router, stats.router, todos.router,
):
    app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Provide a basic liveness response."""
    return {"status": "ok"}
