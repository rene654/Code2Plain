# Code2Plain v1.1 — Notification Architecture

## Objective

Deliver learning reinforcement automatically without coupling
Code2Plain to one push provider.

## Pipeline

AdaptiveSessionDigest
→ NotificationDispatcher
→ NotificationProvider
→ delivery provider

## Provider abstraction

The core does not know whether delivery uses:

- APNs
- FCM
- Web Push
- ntfy
- another provider

## Device policy

Only active devices receive notifications.

Revoked devices are excluded automatically.

## Privacy

Notification delivery does not require:

- telephone number
- source code

The initial notification body uses a short pedagogical message.

## Automation

The user does not manually compose the notification.

Code2Plain creates the message automatically from the digest.
