from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from code2plain.service import Code2PlainService


mcp = FastMCP(
    "Code2Plain",
    stateless_http=True,
    json_response=True,
)

service = Code2PlainService()


@mcp.tool()
def explain_code(code: str) -> dict[str, Any]:
    """
    Explain source code using Code2Plain's visual-learning model.

    Returns:
    - script summary
    - numbered sections
    - color tags
    - what each section does
    - what the user should learn
    """
    return service.explain_code(code)


def main() -> None:
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
