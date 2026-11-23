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

class InvalidAlertStatusError(Exception):
    def __init__(self, comment):
        super().__init__(f"Invalid Alert status: {comment}")

class AlreadyReviewedError(Exception):
    def __init__(self, uuid):
        super().__init__(f"Proposal {uuid} already reviewed.")

class TimeMachineError(Exception):
    def __init__(self, comment):
        super().__init__(f"Proposal alert cant be approved in future: {comment}")


class DeliveryNotFoundError(AppError):
    def __init__(self, delivery):
        super().__init__(f"Delivery {delivery} not found")


class NodeNotFoundError(AppError):
    def __init__(self, node_id):
        self.node_id = node_id
        super().__init__(f"Node {node_id} not found")


class ReferenceArticleNotFoundError(AppError):
    def __init__(self, article_id):
        self.article_id = article_id
        super().__init__(f"Reference article {article_id} not found")


class ReferenceCategoryNotFoundError(AppError):
    def __init__(self, category_id):
        self.category_id = category_id
        super().__init__(f"Reference category {category_id} not found")


class RoleNotFoundError(AppError):
    def __init__(self, role_id):
        self.role_id = role_id
        super().__init__(f"Role {role_id} not found")
