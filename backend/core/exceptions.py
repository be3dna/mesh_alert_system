class AppError(Exception):
    """Base application exception."""
    pass


class UserNotFoundError(AppError):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

class AlertNotFoundError(AppError):
    def __init__(self, alert_id):
        self.alert_id = alert_id
        super().__init__(f"Alert {alert_id} not found")


class PermissionDeniedError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidTerritoryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class StatusNotFoundError(Exception):
    def __init__(self, status):
        self.status= status
        super().__init__(f"Status {status} not found")