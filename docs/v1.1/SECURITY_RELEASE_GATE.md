# Code2Plain v1.1
# Security / Privacy / Release Gate

## Release classification

Code2Plain v1.1 is being evaluated for:

**PERSONAL BETA**

This gate does not certify the product as production-secure
for public commercial deployment.

---

## Personal Beta — required

### PASS requirements

- No Apple `.p8` private key tracked by Git.
- No runtime device SQLite database tracked by Git.
- Pairing tokens use high-entropy one-time credentials.
- Pairing token persistence uses a hash rather than the raw
  pairing credential.
- Learning profiles do not contain phone numbers.
- Learning profiles do not contain APNs tokens.
- Learning profiles do not contain ntfy topics.
- Learning profiles do not contain source code.
- Unknown user code is not executed by the learning engine.
- Device delivery remains separate from commercial
  entitlements.
- Revocable device records exist.
- Adaptive learning digest has been physically delivered to
  an iPhone.

---

## Current physical proof

Validated pipeline:

Learning observation
→ SessionLearningTracker
→ AdaptiveSessionDigestBuilder
→ EntitlementService
→ DeviceRegistry
→ NotificationDispatcher
→ NtfyNotificationProvider
→ physical iPhone

This is a real delivery proof.

ntfy remains a temporary validation transport.

Native APNs remains the intended Apple production channel.

---

## Known security debt

The following items intentionally block a claim of
production/commercial security.

### 1. APNs token encryption at rest

ApplePushRegistry currently persists the APNs device token.

Before public deployment:

- encrypt token material at rest
- establish key management
- implement token rotation handling
- define deletion/revocation behavior

### 2. ntfy topic storage

The temporary ntfy topic behaves like a delivery capability.

Before any public use of this transport:

- use authenticated/private topics, or
- self-host the transport, or
- encrypt capability material at rest

ntfy is currently a Personal Beta proof adapter.

### 3. Production account authentication

The current pairing flow proves possession of a one-time
pairing credential.

Before public deployment, registration endpoints must also
be bound to authenticated account authorization.

### 4. Concurrent pairing redemption

One-time token redemption should be hardened with an atomic
transaction or equivalent concurrency-safe mechanism before
public deployment.

### 5. Durable commercial entitlement source

EntitlementService currently provides the authorization
boundary used by the product architecture.

Before commercial release:

- subscription state must be server-authoritative
- plan state must be durable
- usage counters must be durable
- billing provider state must be reconciled server-side

### 6. Existing application data retention

The broader Code2Plain application may persist code and
explanations in SQLite.

Before public deployment:

- define retention periods
- implement deletion
- expose privacy controls
- document storage scope

### 7. Public backend hardening

Before Internet-facing public deployment:

- authenticated API access
- rate limiting
- request size limits
- structured security logging
- secret management
- HTTPS-only deployment
- database backup policy
- dependency vulnerability scanning

---

## Release decision

### Personal Beta

Eligible after:

- full automated regression passes
- security release gate passes
- physical iPhone learning delivery remains validated

### Public Beta

**BLOCKED**

until the production-security items above are implemented.

### Commercial Release

**BLOCKED**

until public security, identity, durable entitlement state,
billing integration, privacy controls and operational
monitoring are implemented.

---

## Product rule

QR or pairing authorizes a device.

The account authorizes the user.

The subscription determines available features and limits.

Device authorization must never grant subscription state.
