from enum import StrEnum


class AlertStatus(StrEnum):
    CREATED = "created"
    PENDING_REVIEW = "pending_review"
    PUBLISHED = "published"
    CANCELED = "canceled"
