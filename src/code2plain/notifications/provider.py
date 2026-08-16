from __future__ import annotations

import uuid

from abc import (
    ABC,
    abstractmethod,
)

from code2plain.notifications.models import (
    NotificationMessage,
    NotificationResult,
)


class NotificationProvider(ABC):
    """
    Provider-neutral notification interface.
    """

    @abstractmethod
    def send(
        self,
        message: NotificationMessage,
    ) -> NotificationResult:
        raise NotImplementedError


class InMemoryNotificationProvider(
    NotificationProvider
):
    """
    Test/development provider.

    Does not contact any external service.
    """

    def __init__(
        self,
    ) -> None:
        self.sent: list[
            NotificationMessage
        ] = []


    def send(
        self,
        message: NotificationMessage,
    ) -> NotificationResult:

        self.sent.append(
            message
        )

        return NotificationResult(
            success=True,
            provider="memory",
            device_id=message.device_id,
            message_id=(
                "msg_"
                + uuid.uuid4().hex
            ),
        )
