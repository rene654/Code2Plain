# Code2Plain v1.1 — Learning Session Privacy

## Core rule

The learning engine does not require a telephone number.

## Learning profile stores

- learner_id
- semantic concepts
- exposure counts
- first seen timestamp
- last seen timestamp
- learning status

## Learning profile does not store

- telephone number
- mobile number
- push token
- device token
- source code

## Future mobile architecture

Account
→ Device Registry
→ provider-issued push token
→ push provider
→ authorized device

Telephone numbers are outside the default architecture.

## Notification policy

Source code must not be included in mobile push payloads by default.

Preferred push:

`Your Code2Plain learning summary is ready.`

The authenticated client can then retrieve the pedagogical digest.
