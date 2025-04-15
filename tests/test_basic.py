#!/usr/bin/env python3
"""
Basic tests for the NexusController package.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nexuscontroller import AndroidController
from nexuscontroller.utils import generate_timestamp_filename, extract_regex_match

class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality of the NexusController package."""
    
    def test_imports(self):
        """Test that the package can be imported."""
        self.assertIsNotNone(AndroidController)
        
    def test_controller_init(self):
        """Test that the controller can be initialized."""
        with patch('nexuscontroller.controller.subprocess.run') as mock_run:
            # Mock the ADB check
            mock_process = MagicMock()
            mock_process.stdout = "Android Debug Bridge version 1.0.41"
            mock_process.returncode = 0
            mock_run.return_value = mock_process
            
            controller = AndroidController()
            self.assertIsNotNone(controller)
            
    def test_utils(self):
        """Test utility functions."""
        # Test timestamp filename generation
        filename = generate_timestamp_filename("test", "txt")
        self.assertIn("test_", filename)
        self.assertIn(".txt", filename)
        
        # Test regex extraction
        text = "Version: 1.2.3"
        version = extract_regex_match(r"Version: ([\d\.]+)", text)
        self.assertEqual(version, "1.2.3")

if __name__ == '__main__':
    unittest.main() 