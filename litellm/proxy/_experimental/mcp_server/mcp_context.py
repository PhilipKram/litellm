"""
Shared ContextVars for the MCP server layer.

Lives in its own module to avoid circular imports between
mcp_server_manager.py and server.py.
"""

from contextvars import ContextVar
from typing import Any, Optional

# Set server-side in proxy_server.py route handlers when a request arrives via
# /toolset/{name}/mcp or the toolset fallback in dynamic_mcp_route.
# Never populated from client-supplied headers.
_mcp_active_toolset_id: ContextVar[Optional[str]] = ContextVar(
    "_mcp_active_toolset_id", default=None
)

# Per-request merged InitializeResult.instructions; set in MCP HTTP/SSE handlers.
_mcp_gateway_initialize_instructions: ContextVar[Optional[str]] = ContextVar(
    "_mcp_gateway_initialize_instructions", default=None
)

# Per-request litellm logging object set by mcp_server_tool_call before
# execute_mcp_tool fires, so post_mcp_call guardrails can write
# standard_logging_guardrail_information directly into
# litellm_logging_obj.model_call_details['metadata'] — that's the dict that
# async_success_handler uses to build the spend log payload. Without this
# bridge, guardrails would only see the synthetic data dict produced by
# _convert_mcp_to_llm_format, which is detached from the logging pipeline.
_mcp_active_litellm_logging_obj: ContextVar[Optional[Any]] = ContextVar(
    "_mcp_active_litellm_logging_obj", default=None
)
