"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text

from app.config import settings
from app.db.database import Base, engine
from app.routes.deployments import router as deployments_router

# Import models before creating tables so SQLAlchemy registers their metadata.
from app.models import Deployment  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create schema once the PostgreSQL service is available."""
    async with engine.begin() as connection:
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
app.include_router(deployments_router)
Instrumentator().instrument(app).expose(app)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
