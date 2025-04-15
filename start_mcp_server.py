#!/usr/bin/env python3
"""
NexusControl MCP Server Launcher
This script launches NexusControl in MCP server mode for IDE integrations.
"""

import os
import sys
import subprocess
import argparse

def main():
    """
    Main function to start the MCP server
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set environment variables
    env = os.environ.copy()
    env['NEXUSCONTROLLER_MCP_MODE'] = 'true'
    env['PYTHONPATH'] = script_dir
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Start NexusController MCP Server")
    # Remove host and port arguments as they're not supported
    # parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server to")
    # parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    args = parser.parse_args()
    
    # Path to the MCP server script
    mcp_server_script = os.path.join(script_dir, 'mcp_server.py')
    
    # Print debug info
    print(f"Starting NexusController MCP Server...", file=sys.stderr)
    print(f"Script directory: {script_dir}", file=sys.stderr)
    print(f"MCP Server script: {mcp_server_script}", file=sys.stderr)
    
    # Launch MCP Server without host/port arguments
    try:
        subprocess.run(
            [sys.executable, mcp_server_script],
            env=env,
            check=True
        )
    except KeyboardInterrupt:
        print("NexusController MCP Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Error launching NexusController MCP Server: {str(e)}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 