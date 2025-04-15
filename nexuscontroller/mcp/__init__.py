"""
MCP (Model Context Protocol) Server for NexusController

Provides fastmcp integration for controlling Android devices via AI assistants
and interfaces that implement the Model Context Protocol.

This module includes:
- MCP Server implementation
- Tool functions for device control
- Server startup utilities
"""

__all__ = ["server", "start_server", "run"]

from .server import main as start_server, run 