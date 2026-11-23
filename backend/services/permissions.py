from enum import StrEnum


class Permission(StrEnum):
    ALERT_CREATE = "alerts.create"
    ALERT_PROPOSE = "alerts.propose"
    ALERT_UPDATE = "alerts.update"
    ALERT_REVIEW = "alerts.review"
    ALERT_PUBLISH = "alerts.publish"
    ALERT_CANCEL = "alerts.cancel"
    
    ALERT_UPDATE_ANY = "alerts.update_any"
    ALERT_CANCEL_ANY = "alerts.cancel_any"
    OPERATOR_MANAGE_ROLE = "operator.manage_role"

    USERS_MANAGE_ROLES = "users.manage_roles"
    DEVICES_MANAGE = "devices.manage"
    SETTINGS_MANAGE = "settings.manage"


ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {
    "user": frozenset(
        {
            Permission.ALERT_PROPOSE,
        }
    ),
    "operator": frozenset(
        {
            Permission.ALERT_PROPOSE,
            Permission.ALERT_CREATE,
            Permission.ALERT_UPDATE,
            Permission.ALERT_REVIEW,
            Permission.ALERT_PUBLISH,
            Permission.ALERT_CANCEL,
        }
    ),
    "supervisor": frozenset(
        {
            Permission.ALERT_PROPOSE,
            Permission.ALERT_CREATE,
            Permission.ALERT_UPDATE,
            Permission.ALERT_REVIEW,
            Permission.ALERT_PUBLISH,
            Permission.ALERT_CANCEL,
            Permission.OPERATOR_MANAGE_ROLE,
            Permission.ALERT_CANCEL_ANY,
            Permission.ALERT_UPDATE_ANY
        }
    ),
    "admin": frozenset(
        {
            Permission.USERS_MANAGE_ROLES,
            Permission.DEVICES_MANAGE,
            Permission.SETTINGS_MANAGE,
        }
    ),
}
