# HR Vacation & Sick Leave Agent

## Business challenge

Employees frequently contact HR to ask about vacation entitlements, leave balances, and sick leave policies. An AI agent should handle these questions conversationally, reducing HR helpdesk load and giving employees instant, accurate answers.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Response time for leave-related questions | — | ≤ 10 seconds | — | Absence Management / Employee Self-Service | user |

## Key Milestones

1. **Agent receives question** — Employee submits a natural-language question about vacation or sick leave.
2. **Policy lookup** — Agent retrieves relevant leave policy or balance data from SAP SuccessFactors.
3. **Answer generated** — Agent formulates a clear, accurate response based on retrieved data.
4. **Response delivered** — Employee receives the answer within the target response time.
5. **Handoff (if needed)** — Complex or edge-case requests are escalated to a human HR agent.

## Business Architecture (RBA)

### End-to-End Process

Recruit to Retire

### Process Hierarchy

```
Recruit to Retire (E2E)
└── Manage Workforce
    └── Manage Time and Attendance (BPS-393)
        └── Manage attendance and absence quotas
        └── Record absences
```

### Summary

The agent addresses the "Manage Time and Attendance" sub-process within the Recruit to Retire E2E, specifically covering absence quota management and absence recording for internal workforce.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|-------------------|-------------------|--------------------|----|---------------------|
| Query leave balances | SAP SuccessFactors Employee Central — Absence Management (SC4500) | `sap.sf:apiResource:Balances:v1` | — | — | — | — | No | No MCP server; API will be wrapped as a custom tool |
| Query available time/leave types | SAP SuccessFactors Employee Central | `sap.sf:apiResource:AvailableTimeTypes:v1` | — | — | — | — | No | No MCP server; API will be wrapped as a custom tool |
| View & manage time-off records | SAP SuccessFactors Employee Central | `sap.sf:apiResource:ECTimeOff:v1` | — | — | — | — | No | OData API; will be wrapped as a custom tool |
| Retrieve leave policy/instructional text | SAP SuccessFactors Employee Central | `sap.sf:apiResource:InstructionalText:v1` | — | — | — | — | No | REST API available |
| Natural-language Q&A interface | — | — | — | — | — | — | Yes | Requires custom AI agent implementation |

### Key findings

- SAP SuccessFactors Employee Central covers all absence management capabilities (mandatory).
- No pre-built MCP servers exist for the SuccessFactors Time Off APIs — they will be wrapped as custom tools within the agent.
- The FMLA Request API (`sap.sf:apiResource:FMLARequest:v1`) is not available in the current landscape and is excluded.
- A custom Python AI agent (A2A protocol) is the right fit for natural-language HR Q&A.
- The agent will call SuccessFactors REST/OData APIs for real-time leave data.

## Recommendations

### HR Vacation & Sick Leave AI Agent

#### Executive Summary

Python AI agent answering HR leave questions via SuccessFactors APIs.

#### Recommended Solution

A pro-code Python AI agent using the A2A protocol. It uses SAP SuccessFactors Time Off APIs (Balances, AvailableTimeTypes, ECTimeOff, InstructionalText) as custom tools to answer employee questions about vacation entitlements, leave balances, and sick leave policies in natural language.

#### Recommended solution category

AI Agent

#### Intent fit
90%
