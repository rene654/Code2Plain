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
