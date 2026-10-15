"""Database model for deployments being monitored."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Index, String, text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Deployment(Base):
    __tablename__ = "deployments"
    __table_args__ = (
        Index("idx_deployments_service", "service"),
        Index("idx_deployments_created", text("created_at DESC")),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    service: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    deployed_by: Mapped[str] = mapped_column(String(100), nullable=False)
    environment: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=text("'production'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("NOW()")
    )
