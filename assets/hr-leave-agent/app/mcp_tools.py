"""MCP tools indirection layer.

This module is the owned indirection point for MCP tool loading.
Tests patch `mcp_tools.get_mcp_tools` — never the underlying implementation.

In production: delegates to the Agent Gateway (mcp_providers.agw).
In tests (IBD_TESTING=1): agw already returns mock tools from mcp-mock.json.
"""

from mcp_providers.agw import get_mcp_tools  # noqa: F401 — re-exported for patching

__all__ = ["get_mcp_tools"]
