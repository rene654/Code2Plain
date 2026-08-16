# Code2Plain v1.1 — Secure Device Pairing

## Objective

Connect an authorized device without requiring a telephone number.

## Pairing flow

Authenticated learner
→ create pairing request
→ cryptographically random one-time token
→ device presents token
→ token validated
→ expiration validated
→ internal device_id created
→ pairing token marked used

## Security properties

Pairing tokens are:

- cryptographically random
- short lived
- one-time use
- stored only as hashes

## Device identity

Code2Plain uses internal device identifiers.

Example:

`device_abc123`

A telephone number is not required.

## Revocation

Devices can be revoked independently.

Future product controls should allow:

- disconnect this device
- disconnect all devices
- display active devices

## Separation of concerns

LearningProfile:

- pedagogical state

DeviceRegistry:

- authorized delivery endpoints

NotificationProvider:

- future push delivery

These systems remain separate.

## Source-code privacy

The DeviceRegistry does not store source code.
