# Specification: hr-leave-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` for full context.
- [x] Bootstrap agent code in `assets/hr-leave-agent/` using the sap-agent-bootstrap instructions.
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

- [x] Create `assets/hr-leave-agent/app/skills/hr-leave/SKILL.md` with HR leave Q&A instructions

---

## Project-Specific Tasks

### Leave Balance Questions

- [x] Configure the agent system prompt (`app/agent.py`)
- [x] Ensure the agent can handle: "How many vacation days do I have left?" via `Balances` MCP tool

### Available Leave Types

- [x] Ensure the agent can answer: "What types of leave can I take?" via `AvailableTimeTypes` MCP tool

### Leave Policy Questions

- [x] Ensure the agent can answer: "What is the sick leave policy?" via `InstructionalText` MCP tool

### Existing Time-Off Records

- [x] Ensure the agent can answer: "What leave do I have booked?" via `ECTimeOff` MCP tool

### Escalation

- [x] Implement escalation logic with M5 logging

---

## MCP Tool Integration

- [x] Invoke `mcp-translation-file` skill for all 4 API specs
- [x] Invoke `setup-solution` skill — `solution.yaml` and all `asset.yaml` files created
- [x] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from `mcp_tools` module
- [x] Add all 4 MCP server ORD IDs to `asset.yaml` under `requires`
- [x] Generate `mcp-mock.json` using the `mcp-mock-config` skill

---

## Business Instrumentation

- [x] M1: employee question received and parsed
- [x] M2: leave data retrieved from SuccessFactors
- [x] M3: answer generated from retrieved data
- [x] M4: response delivered within target time
- [x] M5: escalation guidance provided to employee
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## Testing

- [x] `conftest.py` sets only `IBD_TESTING=true`
- [x] Write unit tests — one per tool (Balances, AvailableTimeTypes, ECTimeOff, InstructionalText)
- [x] Write one integration test for end-to-end leave question flow
- [x] Run `pytest` — 114 passed, 75% coverage (above 70% threshold)
- [x] `test_report.json` exists in `assets/hr-leave-agent/`
