from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_alert_service
from schemas.alert import AlertResponse
from services.alert_service import (
    AlertService,
    AlertNotFoundError,
    AlertNotPublishedError
)


router = APIRouter(
    prefix="/api/alerts",
    tags=["alerts"]
)


@router.get(
    "/{alert_id}",
    response_model=AlertResponse
)
async def get_alert(
    alert_id: UUID,
    service: Annotated[
        AlertService,
        Depends(get_alert_service)
    ]
):

    try:
        return await service.get_public_alert(
            alert_id
        )

    except AlertNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    except AlertNotPublishedError:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )