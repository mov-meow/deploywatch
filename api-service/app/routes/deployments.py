"""Deployment API endpoints."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.deployment import Deployment

router = APIRouter(prefix="/deployments", tags=["deployments"])


class DeploymentCreate(BaseModel):
    service: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=100)
    status: Literal["success", "failed", "rolled_back"]
    deployed_by: str = Field(min_length=1, max_length=100)
    environment: str = Field(default="production", min_length=1, max_length=50)


class DeploymentRead(DeploymentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


@router.get("", response_model=list[DeploymentRead])
async def list_deployments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Deployment).order_by(Deployment.id.desc()))
    return result.scalars().all()


@router.post("", response_model=DeploymentRead, status_code=status.HTTP_201_CREATED)
async def create_deployment(payload: DeploymentCreate, db: AsyncSession = Depends(get_db)):
    deployment = Deployment(**payload.model_dump())
    db.add(deployment)
    await db.commit()
    await db.refresh(deployment)
    return deployment


@router.get("/{deployment_id}", response_model=DeploymentRead)
async def get_deployment(deployment_id: int, db: AsyncSession = Depends(get_db)):
    deployment = await db.get(Deployment, deployment_id)
    if deployment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deployment not found")
    return deployment
