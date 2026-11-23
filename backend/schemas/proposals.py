from datetime import datetime
from uuid import UUID

from .common import Schema, UUIDRead


# The current DB table lacks proposal content and proposer identity.
# This request is an API contract, not yet persistable without a migration.
class ProposalCreate(Schema):
    review_comment: str | None = None
    alert_id: UUID
    decision_id: UUID | None = None
    reviewed_at: datetime | None = None

class ProposalReview(Schema):
    decision_id: UUID
    review_comment: str | None = None
    reviewed_at: datetime | None = None

class ProposalRead(UUIDRead):
    reviewed_by: UUID | None
    reviewed_at: datetime | None
    alert_id: UUID | None
    decision_id: UUID
    review_comment: str

class ReviewDecisionRead(UUIDRead):
    name: str
    description: str | None
