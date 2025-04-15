#!/usr/bin/env python3
"""
NexusController MCP Server Launcher

This script provides a convenient way to launch the NexusController MCP server.
It supports the same command-line arguments as the module.

Usage:
  python start_mcp_server.py [options]

Options:
  --install-deps  Install required dependencies
  --debug         Enable debug logging
"""

import sys
from nexuscontroller.mcp.server import main

if __name__ == "__main__":
    sys.exit(main()) 