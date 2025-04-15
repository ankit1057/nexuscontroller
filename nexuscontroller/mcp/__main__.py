#!/usr/bin/env python3
"""
NexusController MCP Server - Entry Point Module

This module provides the entry point for running the NexusController MCP server
as a Python module using `python -m nexuscontroller.mcp`.
"""

import sys
from nexuscontroller.mcp.server import main

if __name__ == "__main__":
    sys.exit(main()) 