# Product Requirements Document (PRD)

**Title:** HR Vacation & Sick Leave AI Agent
**Date:** 2026-10-22
**Solution Category:** AI Agent

## Product Purpose & Value Proposition

**Elevator Pitch:**
Employees waste time contacting HR for routine questions about vacation balances and sick leave policies. This AI agent answers those questions instantly via natural language, reducing HR workload and improving the employee experience.

**Business Need:**
HR teams receive a high volume of repetitive questions about leave entitlements and policies. An AI agent connected to SAP SuccessFactors can answer these instantly, freeing HR staff for higher-value work.

**Expected Value:**
- Employees get answers in under 10 seconds — no wait for an HR response.
- HR helpdesk volume for leave-related queries decreases significantly.

**Product Objectives:**
1. Answer employee leave questions accurately in ≤ 10 seconds.
2. Retrieve real-time leave data from SAP SuccessFactors.
3. Escalate complex or unresolvable queries to a human HR agent.

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Response time for leave-related questions | — | ≤ 10 seconds | — | Absence Management / Employee Self-Service | user |

## Requirements

### Must-Have Requirements

**REQ-01**: Answer leave balance questions

- **User Story**: As an employee, I need to ask how many vacation days I have left so that I can plan my time off.
- **Acceptance Criteria**: Given an authenticated employee asks about their leave balance, the agent retrieves the balance from SuccessFactors and returns it within 10 seconds.
- **Priority Rank**: 1

**REQ-02**: Explain leave policies

- **User Story**: As an employee, I need to ask about sick leave policies so that I understand my entitlements.
- **Acceptance Criteria**: Given an employee asks a policy question, the agent retrieves relevant instructional text from SuccessFactors and provides a clear plain-language answer.
- **Priority Rank**: 2

**REQ-03**: Show available leave types

- **User Story**: As an employee, I need to know what types of leave are available to me so that I select the correct type when submitting a request.
- **Acceptance Criteria**: The agent returns the list of available time types for the employee's context.
- **Priority Rank**: 3

**REQ-04**: View existing time-off records

- **User Story**: As an employee, I need to check my past and upcoming leave bookings so that I can manage my schedule.
- **Acceptance Criteria**: The agent retrieves and summarises existing time-off records from SAP SuccessFactors.
- **Priority Rank**: 4

**REQ-05**: Escalate unresolvable queries

- **User Story**: As an employee, I need the agent to tell me when it cannot answer my question so that I can reach an HR specialist.
- **Acceptance Criteria**: When the agent cannot confidently answer, it informs the employee and provides escalation guidance.
- **Priority Rank**: 5

## Solution Architecture

**Architecture Overview:**
A Python AI agent built on the A2A protocol, deployed on SAP BTP. It uses SAP SuccessFactors Time Off REST/OData APIs as custom tool integrations to retrieve real-time leave data and policies for the querying employee.

**Key Components:**
- Python AI Agent (A2A protocol): Core reasoning and conversation engine.
- SuccessFactors Time Off API tools: Balances, AvailableTimeTypes, ECTimeOff, InstructionalText.
- SAP Generative AI Hub: LLM runtime for natural-language understanding and response generation.

**Integration Points:**
- SAP SuccessFactors Employee Central: Read-only access to leave balances, time types, time-off records, and policy text.

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
- The agent exposes extension points to add new HR topic tools (e.g., payroll queries, onboarding information) without modifying core logic.
- Tool registration is modular — new SuccessFactors APIs can be added as additional tools.

**Business Step Instrumentation:**
All milestones must emit structured log statements following the pattern:
`[MILESTONE_ID].[achieved|missed]: [description]`

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent

**Actions the system performs without human approval:**
- Retrieve leave balances and time-off records for the authenticated employee.
- Retrieve available leave types and policy text.
- Formulate and return a natural-language answer.

**Actions that require human review or approval:**
- Submitting or modifying a leave request (out of scope for this version).

**Model or engine used:** SAP Generative AI Hub (LLM)

**Knowledge & data sources accessed:**
- SAP SuccessFactors Employee Central: leave balances, time types, time-off records, instructional/policy text.

**Tools or connectors invoked:**
- `Balances` API tool: retrieves employee leave balance (read-only).
- `AvailableTimeTypes` API tool: lists available leave types (read-only).
- `ECTimeOff` API tool: retrieves time-off records (read-only).
- `InstructionalText` API tool: retrieves policy/instructional text (read-only).

**Guardrails & fail-safes:**
- Agent never modifies leave records or submits requests autonomously.
- Confidence below threshold triggers escalation message to the employee.
- If SuccessFactors APIs are unavailable, the agent informs the employee and suggests contacting HR directly.

## Milestones

### M1: Question Received

- **Description**: Employee submits a natural-language question about vacation or sick leave.
- **Achieved when**: The agent successfully receives and parses the user's input.
- **Log on achievement**: `M1.achieved: employee question received and parsed`
- **Log on miss**: `M1.missed: failed to receive or parse employee question`

### M2: Policy or Data Lookup

- **Description**: Agent identifies the relevant SuccessFactors API and retrieves leave data or policy text.
- **Achieved when**: API call returns a successful response with relevant data.
- **Log on achievement**: `M2.achieved: leave data retrieved from SuccessFactors`
- **Log on miss**: `M2.missed: SuccessFactors API call failed or returned no data`

### M3: Answer Generated

- **Description**: Agent formulates a clear, accurate natural-language answer based on retrieved data.
- **Achieved when**: LLM produces a response grounded in the retrieved data.
- **Log on achievement**: `M3.achieved: answer generated from retrieved data`
- **Log on miss**: `M3.missed: answer generation failed or produced low-confidence response`

### M4: Response Delivered

- **Description**: Employee receives the answer within the target response time.
- **Achieved when**: Response is returned to the employee within ≤ 10 seconds end-to-end.
- **Log on achievement**: `M4.achieved: response delivered within target time`
- **Log on miss**: `M4.missed: response delivery exceeded 10-second target`

### M5: Escalation Triggered (if needed)

- **Description**: Complex or edge-case requests are escalated to a human HR agent.
- **Achieved when**: Agent detects it cannot answer and provides escalation guidance to the employee.
- **Log on achievement**: `M5.achieved: escalation guidance provided to employee`
- **Log on miss**: `M5.missed: escalation not triggered despite unresolvable query`
