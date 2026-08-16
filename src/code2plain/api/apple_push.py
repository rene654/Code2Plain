from __future__ import annotations

from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException,
)
from pydantic import (
    BaseModel,
    Field,
)

from code2plain.devices import (
    ApplePushRegistrationService,
    ApplePushRegistry,
    DeviceRegistry,
)


router = APIRouter(
    prefix="/api/v1/devices/apple",
    tags=[
        "apple-push"
    ],
)


class ApplePushRegistrationRequest(
    BaseModel
):
    pairing_token: str = Field(
        min_length=1
    )

    apns_token: str = Field(
        min_length=1
    )

    bundle_id: str = Field(
        min_length=1
    )

    environment: str = "sandbox"


class ApplePushRegistrationResponse(
    BaseModel
):
    device_id: str
    status: str


def build_registration_service(
) -> ApplePushRegistrationService:

    database = Path(
        "code2plain_devices.db"
    )

    return ApplePushRegistrationService(
        DeviceRegistry(
            database
        ),
        ApplePushRegistry(
            database
        ),
    )


@router.post(
    "/register",
    response_model=(
        ApplePushRegistrationResponse
    ),
)
def register_apple_push(
    request:
        ApplePushRegistrationRequest,
):

    service = (
        build_registration_service()
    )

    try:

        result = service.register(
            pairing_token=(
                request.pairing_token
            ),
            apns_token=(
                request.apns_token
            ),
            bundle_id=(
                request.bundle_id
            ),
            environment=(
                request.environment
            ),
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(
                error
            ),
        ) from error

    return ApplePushRegistrationResponse(
        device_id=(
            result.device_id
        ),
        status=(
            result.status
        ),
    )
