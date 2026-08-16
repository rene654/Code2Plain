# Code2Plain v1.1 — Entitlements and Monetization

## Core commercial rule

Pairing identifies a device.

Pairing does not grant premium access.

## Separation

Account
→ SubscriptionPlan
→ EntitlementService
→ feature decision

Learner
→ DeviceRegistry
→ paired device

The systems remain separate.

## Initial plans

### Free

Initial product policy:

- basic adaptive learning available
- limited mobile digests
- multiple devices restricted

### Pro

Initial product policy:

- unrestricted mobile digest entitlement
- advanced feature entitlement path
- multi-device capability

The exact commercial packaging may change later without
rewriting the feature consumers.

## Mobile digest

Before sending a learning digest:

1. identify the account
2. evaluate mobile_digest entitlement
3. find active paired devices
4. send the digest
5. consume Free usage only after successful delivery

## Upgrade behavior

Upgrading Free → Pro does not require pairing the device again.

Device identity and commercial entitlement are separate.

## Future billing integration

A billing provider should update the account subscription
state.

The delivery layer should continue asking EntitlementService
for authorization rather than reading billing-provider state
directly.

## Security

Premium state must never be trusted from:

- QR payload
- browser/client flags
- device metadata
- push payload

Feature authorization remains server-side.
