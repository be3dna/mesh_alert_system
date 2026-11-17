from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from services.alert_service import AlertService
from repositories.interfaces.alert_repository import (
    AlertRepository
)
from repositories.sqlalchemy.alert_repository import (
    SqlAlchemyAlertRepository
)


def get_alert_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_session)
    ]
) -> AlertRepository:

    return SqlAlchemyAlertRepository(session)


def get_alert_service(
    repository: Annotated[
        AlertRepository,
        Depends(get_alert_repository)
    ]
) -> AlertService:

    return AlertService(repository)