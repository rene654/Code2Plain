# Code2Plain v1.1 — Session Learning Architecture

## Product progression

EXPLAIN
→ REMEMBER
→ ADAPT
→ REINFORCE

Phase 10.0 implements REMEMBER.

## Pipeline

Explanation result
→ SessionLearningTracker
→ LearningSession
→ LearningProfile
→ SessionDigestBuilder

## Learning states

### new

First semantic exposure.

### practicing

Repeated exposure.

### familiar

Repeated exposure across use.

`familiar` does not mean mastered.

Future mastery signals may include:

- recall
- mistakes
- successful independent use
- quizzes
- repeated application over time

## Privacy

Persistent learning data should describe learning behavior,
not preserve source code whenever that source code is unnecessary.


## Phase 10.1 — Persistent learning memory

LearningProfile persistence uses a dedicated SQLite store.

Persisted data:

- learner_id
- concept
- total exposure count
- first seen timestamp
- last seen timestamp
- learning status

Session-only counters are intentionally not persisted.

The persistence layer does not require source-code storage.

A learner can therefore continue from prior learning state
after restarting Code2Plain.
