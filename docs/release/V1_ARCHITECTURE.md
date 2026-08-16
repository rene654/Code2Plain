# Code2Plain v1 Architecture

## Purpose

Code2Plain is a visual learning layer for source code.

It is designed to help users understand AI-generated or shared
code without requiring repeated explanatory prompts.

## Pipeline

Source Code
→ ExplanationEngine
→ SemanticEnricher
→ Localization
→ LearningModeBuilder
→ QuickSummaryBuilder
→ API / MCP / Live Channel
→ Visual Learning UI

## Principles

### Code remains the protagonist
The interface explains code without replacing it with long prose.

### Deterministic first
Core explanations and quick summaries do not require an LLM call.

### Language-independent concepts
Internal semantic IDs remain stable:

IMPORT
LOAD DATA
FILTER
AGGREGATE
EXPORT
TRANSFORM
DECIDE
REPEAT
DEFINE
CALL
RETURN

Localization changes visible copy, not core logic.

### Session isolation
Every live explanation can be routed through a session_id.

### No code execution
Code2Plain parses and explains source text.
It does not run unknown user code.

## Current supported explanation languages

- Spanish
- English
- French

Spanish is the default language.

## Current primary integration

MCP + HTTP API + live visual web interface.

## Future productization

Production deployment should add:

- authentication
- authorization
- encrypted persistent accounts
- retention controls
- billing
- analytics
- rate limiting
- production observability
