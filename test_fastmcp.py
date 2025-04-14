#!/usr/bin/env python3
"""
Test script for fastmcp library
This script verifies that the fastmcp library is properly installed and can be imported
"""

import sys
import inspect

# Test import of fastmcp
try:
    from fastmcp import FastMCP
    print("✅ fastmcp library imported successfully!")
    
    # Try to initialize the FastMCP server
    mcp_server = FastMCP()
    print("✅ FastMCP server instance created successfully!")
    
    # Print info about FastMCP class
    methods = [m for m in dir(mcp_server) if not m.startswith('_')]
    print(f"  - FastMCP available methods: {len(methods)}")
    print(f"  - Available methods: {', '.join(methods)}")
    
    # Test method decorator access
    print(f"  - FastMCP has method decorator: {hasattr(mcp_server, 'method')}")
    print(f"  - FastMCP has register_methods: {hasattr(mcp_server, 'register_methods')}")
    
    # Import MCP classes for JSON RPC
    from mcp import JSONRPCRequest, JSONRPCResponse, JSONRPCError
    print("✅ JsonRpc classes imported from mcp!")
    
    print("\nAll tests passed - fastmcp is properly installed.")
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Please ensure fastmcp is installed with: pip install fastmcp")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error initializing FastMCP: {e}")
    sys.exit(1) 