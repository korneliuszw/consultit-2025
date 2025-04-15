from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AccessPointResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    parent_access_point_id: Optional[str]


class DowntimeResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(alias="downtime_id")
    start_date: datetime
    end_date: datetime
    access_point: AccessPointResponseSchema


class DowntimeCreateSchema(BaseModel):
    access_point_id: str
    start_date: datetime
    end_date: datetime


class DowntimeUpdateSchema(BaseModel):
    end_date: datetime
    start_date: datetime
    access_point_id: str
