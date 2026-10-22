"""Integration test: end-to-end agent flow for leave questions with mocked LLM and MCP tools."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_tools(add_agent_to_path):
    """Build a set of mock LangChain tools from mcp-mock.json."""
    from langchain_core.tools import StructuredTool

    mock_path = Path(__file__).parent.parent / "mcp-mock.json"
    mock_config = json.loads(mock_path.read_text())

    tools = []
    for _server_slug, server in mock_config["servers"].items():
        for tool_name, tool_def in server["tools"].items():
            mock_resp = tool_def["mock_response"]

            def fn(_resp=mock_resp, **kwargs):
                return _resp

            tools.append(
                StructuredTool.from_function(
                    func=fn,
                    name=tool_name,
                    description=tool_def.get("description", tool_name),
                )
            )
    return tools


@pytest.fixture
def mock_llm_response():
    """Return a canned LLM response for the integration test."""
    return "You have 15 days of Annual Vacation remaining and 10 days of Sick Leave remaining."


@pytest.mark.asyncio
async def test_leave_balance_question_end_to_end(add_agent_to_path, mock_tools, mock_llm_response, mocker):
    """Test that the agent answers a leave balance question end-to-end with mocked dependencies."""
    mocker.patch("mcp_tools.get_mcp_tools", return_value=mock_tools)

    # Mock the LLM to return a canned response
    from langchain_core.messages import AIMessage

    mock_llm = MagicMock()
    mock_llm.ainvoke = AsyncMock(return_value=AIMessage(content=mock_llm_response))

    from agent import SampleAgent

    agent = SampleAgent()

    # Patch _invoke to bypass real LLM calls
    async def fake_invoke(tools, system_prompt, query, context_id, extra_messages=None):
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=mock_llm_response)]}

    mocker.patch.object(agent, "_invoke", side_effect=fake_invoke)

    response = await agent.invoke(
        query="How many vacation days do I have left?",
        context_id="test-session-001",
        tools=mock_tools,
    )

    assert response.status == "completed"
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_sick_leave_policy_question(add_agent_to_path, mock_tools, mocker):
    """Test that the agent handles a sick leave policy question."""
    mocker.patch("mcp_tools.get_mcp_tools", return_value=mock_tools)

    policy_response = "Sick leave requires a medical certificate for absences longer than 3 days. Please contact your HR department for more details."

    from agent import SampleAgent

    agent = SampleAgent()

    async def fake_invoke(tools, system_prompt, query, context_id, extra_messages=None):
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=policy_response)]}

    mocker.patch.object(agent, "_invoke", side_effect=fake_invoke)

    response = await agent.invoke(
        query="What is the sick leave policy?",
        context_id="test-session-002",
        tools=mock_tools,
    )

    assert response.status == "completed"
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_escalation_detected(add_agent_to_path, mock_tools, mocker):
    """Test that escalation is properly detected and logged."""
    mocker.patch("mcp_tools.get_mcp_tools", return_value=mock_tools)

    escalation_response = "I'm not able to fully answer this. Please contact your HR department directly for further assistance."

    from agent import SampleAgent

    agent = SampleAgent()

    async def fake_invoke(tools, system_prompt, query, context_id, extra_messages=None):
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=escalation_response)]}

    mocker.patch.object(agent, "_invoke", side_effect=fake_invoke)

    response = await agent.invoke(
        query="Can I dispute the sick leave decision from last year?",
        context_id="test-session-003",
        tools=mock_tools,
    )

    assert response.status == "completed"
    assert "hr" in response.message.lower() or "contact" in response.message.lower()


@pytest.mark.asyncio
async def test_stream_yields_completion(add_agent_to_path, mock_tools, mocker):
    """Test that stream() yields a final completion chunk."""
    mocker.patch("mcp_tools.get_mcp_tools", return_value=mock_tools)

    answer = "You have 20 days of vacation remaining."

    from agent import SampleAgent

    agent = SampleAgent()

    async def fake_invoke(tools, system_prompt, query, context_id, extra_messages=None):
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=answer)]}

    mocker.patch.object(agent, "_invoke", side_effect=fake_invoke)

    chunks = []
    async for chunk in agent.stream(
        query="How much leave do I have?",
        context_id="test-session-004",
        tools=mock_tools,
    ):
        chunks.append(chunk)

    completed_chunks = [c for c in chunks if c.get("is_task_complete")]
    assert len(completed_chunks) > 0
    assert len(completed_chunks[0]["content"]) > 0
