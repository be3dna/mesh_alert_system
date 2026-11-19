from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .common import Schema, TimeRange, UUIDRead


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    severity_id: UUID
    alert_type_id: UUID
    created_at: datetime
    starts_at: datetime
    ends_at: datetime
    created_by: UUID
    current_status_id: UUID
    is_test: bool


class AlertCreate(TimeRange):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    severity_id: UUID
    alert_type_id: UUID
    territory_ids: list[UUID] = Field(min_length=1)
    is_test: bool = False


class AlertUpdate(Schema):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    severity_id: UUID | None = None
    alert_type_id: UUID | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    territory_ids: list[UUID] | None = None
    is_test: bool | None = None
    change_reason: str = Field(min_length=1)


class AlertRead(UUIDRead):
    title: str
    description: str
    severity_id: UUID
    alert_type_id: UUID
    created_at: datetime
    starts_at: datetime
    ends_at: datetime | None
    created_by: UUID
    current_status_id: UUID
    is_test: bool


class AlertSnapshot(BaseModel):
    title: str
    description: str
    severity_id: UUID
    alert_type_id: UUID
    starts_at: datetime
    ends_at: datetime | None
    is_test: bool
    territory_ids: list[UUID]


class AlertFilters(BaseModel):
    severity_id: UUID | None = None
    status_id: UUID | None = None
    alert_type_id: UUID | None = None
    territory_id: UUID | None = None

    period_from: datetime | None = None
    period_to: datetime | None = None

    is_test: bool | None = None

    @model_validator(mode="after")
    def validate_period(self) -> Self:
        if (
            self.period_from is not None
            and self.period_to is not None
            and self.period_from > self.period_to
        ):
            raise ValueError(
                "Начало периода не может быть позже окончания"
            )

        return self

class AlertDetail(AlertRead):
    territory_ids: list[UUID] = Field(default_factory=list)


class AlertCancel(Schema):
    reason: str = Field(min_length=1)


class LookupCreate(Schema):
    name: str = Field(min_length=1, max_length=50)


class LookupRead(LookupCreate, UUIDRead):
    pass


class SeverityCreate(Schema):
    title: str = Field(min_length=1, max_length=50)


class SeverityRead(SeverityCreate, UUIDRead):
    pass


class StatusCreate(LookupCreate):
    description: str


class StatusRead(StatusCreate, UUIDRead):
    pass
