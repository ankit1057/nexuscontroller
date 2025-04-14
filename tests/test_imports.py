#!/usr/bin/env python3
"""
Basic import tests for Android MCP
These tests don't require a connected device.
"""

import os
import sys
import unittest

class TestImports(unittest.TestCase):
    """Test basic imports of the Android MCP package."""
    
    def test_import_android_mcp(self):
        """Test importing the main package."""
        try:
            import android_mcp
            self.assertTrue(True)
        except ImportError:
            self.fail("Failed to import android_mcp package")
    
    def test_import_controller(self):
        """Test importing the controller module."""
        try:
            from android_mcp import AndroidController
            self.assertTrue(True)
        except ImportError:
            self.fail("Failed to import AndroidController")
    
    def test_import_utils(self):
        """Test importing the utils module."""
        try:
            from android_mcp import utils
            self.assertTrue(True)
        except ImportError:
            self.fail("Failed to import utils module")

if __name__ == "__main__":
    unittest.main() 