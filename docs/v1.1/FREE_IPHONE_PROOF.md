# Code2Plain v1.1 — Free iPhone Proof

## Objective

Validate the physical Code2Plain mobile learning experience
without activating the paid Apple Developer Program.

## Important architecture rule

ntfy is a temporary proof-of-delivery adapter.

It does not replace native Apple Push Notification service.

Native APNs support remains implemented in Code2Plain.

## Production path

NotificationDispatcher
→ APNsNotificationProvider
→ HTTP2APNsTransport
→ APNs
→ Code2Plain iOS Companion

## Free validation path

NotificationDispatcher
→ NtfyNotificationProvider
→ ntfy
→ iPhone ntfy app

## Why this is useful

This lets Code2Plain prove that a learning digest can travel
from the learning engine to a physical iPhone before paying
for Apple distribution infrastructure.

## Security

A ntfy topic acts like a temporary delivery secret.

Code2Plain generates high-entropy random topics.

Do not commit, publish, screenshot, or publicly share a live
topic.

The topic does not grant:

- Pro
- subscriptions
- account identity
- source code access

Commercial authorization remains inside EntitlementService.

## Physical test

1. Install the ntfy app on iPhone.
2. Run:

   python scripts/create_ntfy_iphone_topic.py

3. Subscribe in the ntfy app to the generated topic.
4. Run:

   python scripts/send_ntfy_iphone_test.py

5. Confirm the Code2Plain notification appears on the iPhone.

## Future activation

When Code2Plain is commercially ready, native APNs can be
activated without redesigning:

- learning sessions
- learning profiles
- adaptive digests
- entitlement logic
- notification dispatcher

## Unicode delivery decision

The ntfy proof adapter publishes using the JSON API rather
than Unicode metadata in HTTP headers.

This allows Code2Plain titles and pedagogical messages to
preserve accented and non-ASCII characters.

Request:

POST https://ntfy.sh/

JSON:

- topic
- title
- message
- priority
- tags

The physical proof therefore preserves localized Code2Plain
content without weakening the user-facing text.

## Full learning pipeline proof — Phase 10.7A.5

The physical proof is no longer limited to a hardcoded test
notification.

Code2Plain now validates the complete learning delivery path:

Learning observations
→ SessionLearningTracker
→ AdaptiveSessionDigestBuilder
→ EntitlementService
→ DeviceRegistry
→ NotificationDispatcher
→ NtfyNotificationProvider
→ physical iPhone

The ntfy adapter remains temporary.

The learning, entitlement, device, and dispatcher layers are
the same architectural layers intended for native APNs.

This proves the product behavior before paid Apple
distribution is activated.
