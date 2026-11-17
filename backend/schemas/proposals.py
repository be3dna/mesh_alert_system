from datetime import datetime
from uuid import UUID

from pydantic import Field

from .common import Schema, UUIDRead


# The current DB table lacks proposal content and proposer identity.
# This request is an API contract, not yet persistable without a migration.
class ProposalCreate(Schema):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    proposed_severity_id: UUID
    alert_type_id: UUID
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius_m: float = Field(gt=0)
    starts_at: datetime | None = None
    ends_at: datetime | None = None

class ProposalReview(Schema):
    decision_id: UUID
    review_comment: str | None = None

class ProposalRead(UUIDRead):
    reviewed_by: UUID | None
    reviewed_at: datetime | None
    alert_id: UUID | None
    decision_id: UUID
    review_comment: str

class ReviewDecisionRead(UUIDRead):
    name: str
    description: str | None
