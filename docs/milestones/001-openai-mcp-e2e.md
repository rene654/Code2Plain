# Milestone 001 — OpenAI → Remote MCP → Code2Plain

## Status

Completed.

## Result

Code2Plain successfully completed an end-to-end integration test using:

OpenAI Responses API
→ Remote MCP
→ Code2Plain MCP Server
→ explain_code
→ Code2PlainService
→ ExplanationEngine

## Verified MCP Events

The OpenAI response contained:

- mcp_list_tools
- mcp_call: explain_code
- status: completed
- final model message

## Remote Capability

The Code2Plain MCP server successfully exposed:

- Tool: explain_code
- Streamable HTTP transport
- Structured pedagogical response

## Pedagogical Contract

Each detected section currently returns:

- section_number
- start_line
- end_line
- code
- title
- category
- color_tag
- what_it_does
- what_to_learn

## Architecture Decision

Code2Plain remains provider-independent.

OpenAI is the first priority integration, but the core engine and
Code2PlainService must not depend on OpenAI-specific implementation details.

## Cost Strategy

Default behavior should prefer:

1. deterministic/local explanation when sufficient;
2. lower-cost AI model for enhanced explanations;
3. stronger model only for complex cases.

The API must not be required for every simple explanation.

## Next Product Milestone

Build the visual learning experience:

- numbered sections;
- synchronized section colors;
- code-focused interface;
- prominent but non-distracting explanations;
- "What it does";
- "What to learn";
- future learning-depth controls.
