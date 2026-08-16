# Code2Plain v1.1 — Apple Push Architecture

## Objective

Deliver Code2Plain learning digests to an authorized iPhone
through Apple Push Notification service.

## Flow

Code2Plain device pairing
→ internal device_id
→ iOS app registers with APNs
→ iOS receives APNs device token
→ token is sent securely to Code2Plain backend
→ ApplePushRegistry associates token with device_id
→ NotificationDispatcher
→ APNsNotificationProvider
→ APNs
→ iPhone

## Separation

QR pairing answers:

Which Code2Plain device is authorized?

APNs registration answers:

Where should Apple deliver the notification?

EntitlementService answers:

Is the account allowed to use mobile digest?

These remain separate.

## Security

The APNs device token is not a subscription credential.

The push token must never grant Pro access.

The entitlement decision remains account-scoped.

## Payload

Initial push payload should contain only a short pedagogical
message and optionally a digest identifier.

Source code should not be included in the push payload.

## Production follow-up

Real APNs delivery requires:

- Apple App ID / bundle ID
- Push Notifications capability
- APNs authentication credentials
- signed iOS companion app
- HTTP/2 APNs transport
- secure token storage
- token rotation handling
