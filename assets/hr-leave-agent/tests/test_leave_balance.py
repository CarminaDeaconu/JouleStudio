"""Unit tests for the leave balance tool (GET_rest_timemanagement_absence_v1_timeAccountBalances)."""
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def patch_mcp_tools(add_agent_to_path, mocker):
    """Patch MCP tools to return mock responses from mcp-mock.json."""
    import json
    from pathlib import Path

    mock_path = Path(__file__).parent.parent / "mcp-mock.json"
    mock_config = json.loads(mock_path.read_text())

    balances_tools = mock_config["servers"]["sap-sf-balances"]["tools"]

    def make_mock_tool(name, mock_resp):
        from langchain_core.tools import StructuredTool

        def fn(**kwargs):
            return mock_resp

        return StructuredTool.from_function(
            func=fn,
            name=name,
            description=f"Mock tool: {name}",
        )

    mock_tools = [
        make_mock_tool(name, tool["mock_response"])
        for name, tool in balances_tools.items()
    ]
    mocker.patch("mcp_tools.get_mcp_tools", return_value=mock_tools)
    return mock_tools


def test_leave_balance_tool_returns_results(patch_mcp_tools):
    """The mock balance tool should return a list of leave balance records."""
    tool = next(
        t for t in patch_mcp_tools
        if t.name == "GET_rest_timemanagement_absence_v1_timeAccountBalances"
    )
    result = tool.invoke({"userId": "EMP001"})
    assert "results" in result
    assert len(result["results"]) > 0
    first = result["results"][0]
    assert "timeTypeCode" in first
    assert "balance" in first


def test_leave_balance_tool_vacation_balance(patch_mcp_tools):
    """The mock balance should contain a vacation balance entry."""
    tool = next(
        t for t in patch_mcp_tools
        if t.name == "GET_rest_timemanagement_absence_v1_timeAccountBalances"
    )
    result = tool.invoke({"userId": "EMP001"})
    codes = [r["timeTypeCode"] for r in result["results"]]
    assert "VACATION" in codes
