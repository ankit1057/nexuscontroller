#!/usr/bin/env python3
"""
NexusController MCP Server Launcher
This script launches NexusController in MCP server mode for IDE integrations.
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
    parser.add_argument("--install-deps", action="store_true", help="Install required dependencies before starting")
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("Installing MCP dependencies...", file=sys.stderr)
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "fastmcp==2.1.1"],
                check=True
            )
            print("Dependencies installed successfully", file=sys.stderr)
        except subprocess.CalledProcessError:
            print("Failed to install dependencies", file=sys.stderr)
            return 1
    
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
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            print("MCP Server exited with errors.", file=sys.stderr)
            print("You may need to install required dependencies with:", file=sys.stderr)
            print(f"  {sys.executable} {sys.argv[0]} --install-deps", file=sys.stderr)
        else:
            print(f"Error launching NexusController MCP Server: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error launching NexusController MCP Server: {str(e)}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 