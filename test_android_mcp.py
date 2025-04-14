#!/usr/bin/env python3
"""
Test script for Android Mobile Control Platform (MCP)
This script performs basic tests to verify the functionality of Android MCP.
"""

import os
import sys
import time
from android_mcp import AndroidController
from android_mcp.utils import logger

def print_test(name, status):
    """Print a formatted test result."""
    if status:
        print(f"✅ {name}: PASSED")
    else:
        print(f"❌ {name}: FAILED")

def main():
    """Run basic tests for Android MCP."""
    print("Android MCP Test Script")
    print("======================\n")
    
    # Test 1: Initialize the controller
    print("Test 1: Initialize AndroidController")
    try:
        controller = AndroidController()
        print_test("Controller initialization", True)
    except Exception as e:
        print_test("Controller initialization", False)
        print(f"  Error: {str(e)}")
        return 1
    
    # Test 2: List devices
    print("\nTest 2: List connected devices")
    try:
        devices = controller.get_devices()
        print(f"  Found {len(devices)} device(s): {', '.join(devices) if devices else 'None'}")
        print_test("Get devices", True)
        
        if not devices:
            print("  Warning: No devices connected. Skipping device-specific tests.")
            return 0
    except Exception as e:
        print_test("Get devices", False)
        print(f"  Error: {str(e)}")
        return 1
    
    # Select first device for further tests
    device_id = devices[0]
    print(f"\nUsing device: {device_id} for further tests")
    
    # Test 3: Get device info
    print("\nTest 3: Get device information")
    try:
        info = controller.get_device_info(device_id)
        print(f"  Device model: {info.get('model', 'Unknown')}")
        print(f"  Android version: {info.get('android_version', 'Unknown')}")
        print(f"  Battery level: {info.get('battery_level', 'Unknown')}%")
        print_test("Get device info", True)
    except Exception as e:
        print_test("Get device info", False)
        print(f"  Error: {str(e)}")
    
    # Test 4: Take screenshot
    print("\nTest 4: Take screenshot")
    try:
        screenshot_path = controller.take_screenshot(device_id)
        if os.path.exists(screenshot_path):
            print(f"  Screenshot saved to: {screenshot_path}")
            print_test("Take screenshot", True)
        else:
            print(f"  Screenshot file not found: {screenshot_path}")
            print_test("Take screenshot", False)
    except Exception as e:
        print_test("Take screenshot", False)
        print(f"  Error: {str(e)}")
    
    # Test 5: Create Maestro flow (if Maestro is available)
    print("\nTest 5: Create Maestro flow")
    try:
        # Clear any existing flow
        controller.clear_maestro_flow()
        
        # Add launch app command
        controller.append_to_maestro_flow("appId: com.android.settings\n---\n- launchApp\n")
        
        # Add tap command
        controller.append_to_maestro_flow("- tapOn:\n    text: \"Network & internet\"\n")
        
        # Add wait command
        controller.append_to_maestro_flow("- wait: 2\n")
        
        # Add back command
        controller.append_to_maestro_flow("- pressBack\n")
        
        print("  Created basic Maestro flow")
        print_test("Create Maestro flow", True)
        
        # Ask if user wants to execute the flow
        run_flow = input("\nDo you want to run the Maestro flow? (y/n): ")
        if run_flow.lower() == 'y':
            print("  Running Maestro flow...")
            result = controller.maestro_run_flow(device_id)
            print_test("Run Maestro flow", result)
    except Exception as e:
        print_test("Create Maestro flow", False)
        print(f"  Error: {str(e)}")
    
    print("\nTest summary:")
    print("Android MCP basic functionality tests completed.")
    print("Check the test results above for details.")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        sys.exit(1) 