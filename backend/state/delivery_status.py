from enum import StrEnum


class DeliveryStatus(StrEnum):
    SENDING = "sending"
    DELIVERED = "delivered"
    RESENDING = "resending"
    CANCELLED = "cancelled"
    FAILED = "failed"
