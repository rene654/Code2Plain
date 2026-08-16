from code2plain.mcp.server import explain_code, mcp


def test_mcp_explain_code_contract():
    result = explain_code(
        """import pandas as pd

df = pd.read_excel("orders.xlsx")
"""
    )

    assert isinstance(result, dict)
    assert "summary" in result
    assert "sections" in result
    assert len(result["sections"]) == 2

    first = result["sections"][0]

    assert first["section_number"] == 1
    assert first["color_tag"]
    assert first["what_it_does"]
    assert first["what_to_learn"]


def test_mcp_is_configured_for_http():
    assert mcp.settings.stateless_http is True
    assert mcp.settings.json_response is True


def test_mcp_routes_to_requested_session(
    tmp_path,
    monkeypatch,
):
    import importlib

    from code2plain.live_store import (
        LiveExplanationStore,
    )

    server = importlib.import_module(
        "code2plain.mcp.server"
    )

    isolated_store = LiveExplanationStore(
        tmp_path / "mcp-live.db"
    )

    monkeypatch.setattr(
        server,
        "live_store",
        isolated_store,
    )

    result = server.explain_code(
        'late_orders = '
        'df[df["status"] == "Late"]',
        session_id="mcp-session",
        language="fr",
    )

    latest = isolated_store.latest(
        session_id="mcp-session"
    )

    assert (
        result["language"]
        == "fr"
    )

    assert latest is not None

    assert (
        latest["session_id"]
        == "mcp-session"
    )

    assert (
        latest["explanation"]["language"]
        == "fr"
    )
