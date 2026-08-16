# Code2Plain Cost Strategy

## Principle

Code2Plain should minimize external AI consumption.

The deterministic ExplanationEngine remains the first layer.

## Planned Routing

### Tier 0 — Local Engine

Use for syntax and concepts that can be explained reliably without an LLM.

Expected external AI cost: $0.

### Tier 1 — Efficient AI

Use a lower-cost OpenAI model for:

- contextual explanations;
- semantic interpretation;
- educational enrichment;
- complex library chains.

### Tier 2 — Advanced AI

Use stronger models only when:

- Tier 0 cannot explain the code confidently;
- Tier 1 produces insufficient context;
- the user explicitly asks for deeper analysis.

## Commercial Principle

Do not make one paid LLM call per source-code line.

Analyze the script locally first, group it into logical sections,
and send only the context necessary for AI enrichment.
