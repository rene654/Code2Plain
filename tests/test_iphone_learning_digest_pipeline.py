import httpx

from code2plain.devices import (
    DeviceRegistry,
    NtfyEndpointRegistry,
)
from code2plain.entitlements import (
    EntitlementService,
    SubscriptionPlan,
)
from code2plain.learning import (
    AdaptiveSessionDigestBuilder,
    SessionLearningTracker,
)
from code2plain.notifications import (
    NotificationDispatcher,
    NtfyNotificationProvider,
)


def test_learning_digest_reaches_mobile_provider(
    tmp_path,
):

    database = (
        tmp_path
        / "devices.db"
    )


    learner_id = (
        "learner_1"
    )

    account_id = (
        "account_1"
    )


    # --------------------------------------------------------
    # Pair physical device
    # --------------------------------------------------------

    devices = DeviceRegistry(
        database
    )

    pairing = (
        devices
        .create_pairing_request(
            learner_id
        )
    )

    device = (
        devices
        .redeem_pairing_token(
            pairing.token
        )
    )


    # --------------------------------------------------------
    # Attach free proof endpoint
    # --------------------------------------------------------

    ntfy = NtfyEndpointRegistry(
        database
    )

    ntfy.register(
        device_id=(
            device.device_id
        ),
        topic=(
            "code2plain-e2e-test"
        ),
    )


    # --------------------------------------------------------
    # Create learning session
    # --------------------------------------------------------

    tracker = SessionLearningTracker(
        learner_id=learner_id,
        session_id="session_1",
    )


    tracker.observe_explanation(
        {
            "sections": [
                {
                    "concept":
                        "IMPORT"
                },
                {
                    "concept":
                        "HANDLE ERROR"
                },
            ]
        }
    )


    digest = (
        AdaptiveSessionDigestBuilder(
            "es"
        )
        .build(
            tracker.session,
            tracker.profile,
        )
    )


    assert (
        digest.focus_concept
        == "HANDLE ERROR"
    )


    # --------------------------------------------------------
    # Entitlement
    # --------------------------------------------------------

    entitlements = (
        EntitlementService()
    )

    entitlements.set_plan(
        account_id,
        SubscriptionPlan.PRO,
    )


    # --------------------------------------------------------
    # Physical provider mock
    # --------------------------------------------------------

    captured = {}


    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        captured[
            "request"
        ] = request

        return httpx.Response(
            200,
            json={
                "id":
                    "physical-e2e-message"
            },
        )


    provider = (
        NtfyNotificationProvider(
            ntfy,
            client=httpx.Client(
                transport=(
                    httpx.MockTransport(
                        handler
                    )
                )
            ),
        )
    )


    # --------------------------------------------------------
    # Dispatcher
    # --------------------------------------------------------

    dispatcher = NotificationDispatcher(
        devices,
        provider,
        entitlements,
    )


    results = (
        dispatcher.dispatch_digest(
            learner_id,
            digest,
            account_id=account_id,
        )
    )


    assert len(
        results
    ) == 1

    assert results[
        0
    ].success

    assert (
        results[
            0
        ].provider
        == "ntfy"
    )


    assert (
        captured[
            "request"
        ].method
        == "POST"
    )
