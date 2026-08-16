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

## Real APNs Transport — Phase 10.7A.2

The provider transport uses Apple's HTTP/2 provider API.

Development endpoint:

api.sandbox.push.apple.com

Production endpoint:

api.push.apple.com

Each notification is sent to:

/3/device/{device_token}

Token-based authentication uses a signed ES256 JWT.

The JWT includes:

- issuer: Apple Team ID
- issued-at timestamp
- key identifier in JWT header

The request includes:

- authorization bearer token
- apns-topic = application bundle ID
- apns-push-type = alert
- apns-priority = 10

Apple credentials are not committed to the repository.

The `.p8` signing key must be injected through a protected
runtime secret or mounted secret file in production.

The APNs transport reports Apple response reason and APNs
request ID without logging provider credentials.
