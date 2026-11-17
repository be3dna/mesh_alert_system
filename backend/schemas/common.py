from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

class UUIDRead(Schema):
    id: UUID

class TimeRange(Schema):
    starts_at: datetime
    ends_at: datetime | None = None

    @model_validator(mode="after")
    def validate_interval(self):
        if self.ends_at is not None and self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        return self

class Page(Schema):
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
