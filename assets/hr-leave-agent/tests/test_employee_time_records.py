"""Unit tests for the EmployeeTime OData tools (leave records)."""
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def patch_mcp_tools(add_agent_to_path, mocker):
    """Patch MCP tools to return mock responses from mcp-mock.json."""
    import json
    from pathlib import Path

    mock_path = Path(__file__).parent.parent / "mcp-mock.json"
    mock_config = json.loads(mock_path.read_text())

    odata_tools = mock_config["servers"]["sap-sf-ectimeoff"]["tools"]

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
        for name, tool in odata_tools.items()
    ]
    mocker.patch("mcp_tools.get_mcp_tools", return_value=mock_tools)
    return mock_tools


def test_list_employeetime_returns_records(patch_mcp_tools):
    """list_employeetime should return a results list of time records."""
    tool = next(t for t in patch_mcp_tools if t.name == "list_employeetime_for_sfodata")
    result = tool.invoke({})
    assert "results" in result
    assert len(result["results"]) > 0


def test_get_employeetime_by_key(patch_mcp_tools):
    """get_employeetime should return a single record."""
    tool = next(t for t in patch_mcp_tools if t.name == "get_employeetime_for_sfodata")
    result = tool.invoke({"externalCode": "EMP001-LEAVE-001"})
    assert "externalCode" in result
    assert result["userId"] == "EMP001"


def test_list_timeaccount_returns_records(patch_mcp_tools):
    """list_timeaccount should return a results list of time accounts."""
    tool = next(t for t in patch_mcp_tools if t.name == "list_timeaccount_for_sfodata")
    result = tool.invoke({})
    assert "results" in result
    assert len(result["results"]) > 0
    first = result["results"][0]
    assert "accountType" in first


def test_list_availabletimetype_odata(patch_mcp_tools):
    """list_availabletimetype should return time types via OData tool."""
    tool = next(t for t in patch_mcp_tools if t.name == "list_availabletimetype_for_sfodata")
    result = tool.invoke({})
    assert "results" in result
    assert len(result["results"]) > 0
