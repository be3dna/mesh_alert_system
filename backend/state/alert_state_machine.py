from models.alert import AlertStatus

ALLOWED_TRANSITIONS = {
    AlertStatus.DRAFT: {
        AlertStatus.SENDING,
        AlertStatus.CANCELLED,
    },
    AlertStatus.SENDING: {
        AlertStatus.DELIVERED,
        AlertStatus.FAILED,
        AlertStatus.CANCELLED,
    },
    AlertStatus.DELIVERED: {
        AlertStatus.EXPIRED,
        AlertStatus.CANCELLED,
    },
    AlertStatus.FAILED: {
        AlertStatus.SENDING,
        AlertStatus.CANCELLED,
    },
    AlertStatus.EXPIRED: set(),
    AlertStatus.CANCELLED: set(),
}


class AlertStateMachine:
    @staticmethod
    def initial_status(*, requires_review: bool) -> AlertStatus:
        if requires_review:
            return AlertStatus.PENDING_REVIEW
        return AlertStatus.CREATED

    @staticmethod
    def can_transition(current: str, target: AlertStatus) -> bool:
        if target == AlertStatus.PUBLISHED:
            return current == AlertStatus.CREATED
        if target == AlertStatus.CANCELED:
            # Statuses are configurable lookup rows, so custom statuses can also be canceled.
            return current != AlertStatus.CANCELED
        return False
