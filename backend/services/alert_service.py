from uuid import UUID

from models.alert import Alert
from repositories.interfaces.alert_repository import AlertRepository

class AlertNotFoundError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class AlertNotPublishedError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class AlertService:

    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def get_public_alert(
        self,
        alert_id: UUID
    ) -> Alert:

        alert = await self.repository.get_by_id(
            alert_id
        )

        if alert is None:
            raise AlertNotFoundError()

        if alert.status != "published":
            raise AlertNotPublishedError()

        return alert