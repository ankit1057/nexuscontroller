#!/usr/bin/env python3
"""
Android Mobile Control Platform (MCP) with Maestro Integration in Jupyter Notebook

This module provides a detailed implementation of the Android MCP, integrating ADB for device control 
and Maestro for UI automation within a Jupyter Notebook environment.

Important Notes:
* This module assumes you have a connected Android device with Developer Options enabled and USB debugging authorized.
* Ensure ADB is installed and its path is added to your system's environment variables.
* Maestro CLI needs to be installed separately (curl -Ls "https://get.maestro.mobile.dev" | bash).
* This implementation provides comprehensive Maestro commands, but refer to Maestro's documentation for latest features.
"""

import os
import sys
import time
from android_mcp import AndroidController
from android_mcp.utils import logger, print_keycode_reference, ensure_dir

# Global controller instance
controller = AndroidController()

class Menu:
    """Base class for menu items."""
    def __init__(self, title, description=None):
        self.title = title
        self.description = description
    
    def display(self):
        """Display the menu item."""
        return self.title
    
    def execute(self):
        """Execute the menu action."""
        raise NotImplementedError("Subclasses must implement execute()")

class ActionMenu(Menu):
    """Menu item that executes a function."""
    def __init__(self, title, action, description=None):
        super().__init__(title, description)
        self.action = action
    
    def execute(self):
        """Execute the menu action."""
        return self.action()

class SubMenu(Menu):
    """Menu item that opens a submenu."""
    def __init__(self, title, items=None, description=None, back_option=True):
        super().__init__(title, description)
        self.items = items or []
        self.back_option = back_option
    
    def add_item(self, item):
        """Add an item to the submenu."""
        self.items.append(item)
    
    def execute(self):
        """Display and handle the submenu."""
        while True:
            print(f"\n=== {self.title} ===")
            if self.description:
                print(self.description)
            print()
            
            for i, item in enumerate(self.items):
                print(f"{i+1}. {item.display()}")
            
            if self.back_option:
                print("0. Back")
            
            try:
                choice = int(input("\nSelect option: "))
                if choice == 0 and self.back_option:
                    break
                elif 1 <= choice <= len(self.items):
                    self.items[choice-1].execute()
                else:
                    print("Invalid option. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                break
            
            if self.back_option:
                input("\nPress Enter to continue...")

def get_devices():
    """Get list of connected devices"""
    return controller.get_devices()

def select_device():
    """Select a device from connected devices."""
    devices = controller.get_devices()
    
    if not devices:
        print("❌ No devices connected. Please connect a device and try again.")
        return None
    
    print(f"\nFound {len(devices)} connected device(s):")
    
    for i, device_id in enumerate(devices):
        info = controller.get_device_info(device_id)
        print(f"{i+1}. {info['model']} (Android {info['android_version']}) - ID: {device_id}")
    
    # Device selection
    if len(devices) == 1:
        selected_device = devices[0]
        print(f"\nAutomatically selected the only connected device: {selected_device}")
        return selected_device
    else:
        while True:
            try:
                device_num = int(input("\nSelect device number (or 0 to cancel): "))
                if device_num == 0:
                    return None
                if 1 <= device_num <= len(devices):
                    return devices[device_num - 1]
                else:
                    print("Invalid device number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

def get_device_info(device_id):
    """
    Get detailed information about a device.
    
    Args:
        device_id: The device ID.
        
    Returns:
        Dictionary with device information.
    """
    return controller.get_device_info(device_id)

def take_screenshot(device_id=None):
    """Take a screenshot on the selected device."""
    if not device_id:
        device_id = select_device()
    
    if device_id:
        try:
            screenshot_path = controller.take_screenshot(device_id)
            print(f"✅ Screenshot saved to {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"❌ Error taking screenshot: {str(e)}")
            return None
    return None

def tap_on_screen(device_id, x, y):
    """
    Tap on the device screen at the specified coordinates.
    
    Args:
        device_id: The device ID.
        x: X coordinate.
        y: Y coordinate.
    """
    # You'll need to implement this method in the AndroidController class
    # controller.tap_screen(device_id, x, y)
    print(f"Tapping at coordinates ({x}, {y}) on device {device_id}")

def execute_maestro_flow(device_id=None, flow_file=None):
    """Execute a Maestro flow."""
    if not device_id:
        device_id = select_device()
    
    if not device_id:
        return False
    
    if flow_file:
        # Load flow from file
        with open(flow_file, 'r') as f:
            controller.clear_maestro_flow()
            controller.append_to_maestro_flow(f.read())
    
    result = controller.maestro_run_flow(device_id)
    if result:
        print("✅ Maestro flow executed successfully")
    else:
        print("❌ Failed to execute Maestro flow")
    
    return result

def add_to_maestro_flow(yaml_snippet):
    """
    Add a YAML snippet to the current Maestro flow.
    
    Args:
        yaml_snippet: The YAML snippet to add.
    """
    controller.append_to_maestro_flow(yaml_snippet)

def create_maestro_tap(text=None, id=None, point=None):
    """Create a Maestro tap action."""
    if text:
        return f"- tapOn:\n    text: \"{text}\"\n"
    elif id:
        return f"- tapOn:\n    id: \"{id}\"\n"
    elif point and len(point) == 2:
        return f"- tapOn:\n    point: [{point[0]}, {point[1]}]\n"
    else:
        raise ValueError("Must provide text, id, or point for tap action")

def create_maestro_input(text, id=None):
    """Create a Maestro input action."""
    if id:
        return f"- inputText:\n    id: \"{id}\"\n    text: \"{text}\"\n"
    else:
        return f"- inputText:\n    text: \"{text}\"\n"

def create_maestro_swipe(start, end):
    """
    Create a Maestro swipe command.
    
    Args:
        start: Start coordinates (format: "x,y").
        end: End coordinates (format: "x,y").
        
    Returns:
        YAML snippet for the swipe command.
    """
    start_x, start_y = start.split(',')
    end_x, end_y = end.split(',')
    
    yaml_content = '- swipe:\n'
    yaml_content += f'    start: "{start_x.strip()},{start_y.strip()}"\n'
    yaml_content += f'    end: "{end_x.strip()},{end_y.strip()}"\n'
    
    return yaml_content

def create_complete_flow(package_name, actions):
    """Create a complete Maestro flow from actions."""
    controller.clear_maestro_flow()
    
    # Add app package
    controller.append_to_maestro_flow(f"appId: {package_name}\n---\n")
    
    # Add launch command
    controller.append_to_maestro_flow("- launchApp\n")
    
    # Add all actions
    for action in actions:
        controller.append_to_maestro_flow(action)
    
    return controller.maestro_flow

def run_ui_mode():
    """Run the UI mode of Android MCP"""
    print("\n======================================")
    print("  Android Mobile Control Platform")
    print("======================================\n")
    
    main_menu = build_main_menu()
    try:
        main_menu.execute()
    except KeyboardInterrupt:
        print("\nExiting Android MCP...")
        sys.exit(0)

def build_main_menu():
    """Build the main menu structure."""
    main_menu = SubMenu("Android Mobile Control Platform", back_option=False)
    
    # Device submenu
    device_menu = SubMenu("Device Management")
    device_menu.add_item(ActionMenu("List connected devices", lambda: print(f"\nConnected devices: {get_devices()}")))
    device_menu.add_item(ActionMenu("Select device", select_device))
    device_menu.add_item(ActionMenu("View device info", lambda: print(f"\nDevice info: {controller.get_device_info(select_device(), force_refresh=True)}")))
    
    # Screenshot submenu
    screenshot_menu = SubMenu("Screenshot & Recording")
    screenshot_menu.add_item(ActionMenu("Take screenshot", lambda: take_screenshot(select_device())))
    
    # Maestro submenu
    maestro_menu = SubMenu("Maestro UI Automation")
    maestro_menu.add_item(ActionMenu("Run sample flow", lambda: run_sample_flow(select_device())))
    maestro_menu.add_item(ActionMenu("Load flow from file", load_flow_from_file))
    maestro_menu.add_item(ActionMenu("Execute loaded flow", lambda: execute_maestro_flow(select_device())))
    
    # Add submenus to main menu
    main_menu.add_item(device_menu)
    main_menu.add_item(screenshot_menu)
    main_menu.add_item(maestro_menu)
    main_menu.add_item(ActionMenu("Exit", sys.exit))
    
    return main_menu

def run_sample_flow(device_id):
    """Run the sample Maestro flow."""
    if device_id:
        try:
            # Check if sample flow exists
            sample_flow = "maestro_flows/sample.yaml"
            if os.path.exists(sample_flow):
                if controller.load_maestro_flow(sample_flow):
                    print(f"✅ Loaded sample flow from {sample_flow}")
                    return execute_maestro_flow(device_id)
                else:
                    print(f"❌ Failed to load sample flow from {sample_flow}")
                    return False
            else:
                print(f"❌ Sample flow file not found: {sample_flow}")
                print("Please create a sample flow file first.")
                return False
        except Exception as e:
            print(f"❌ Error running sample flow: {str(e)}")
            return False
    return False

def load_flow_from_file():
    """Load a Maestro flow from a file."""
    flow_file = input("Enter path to Maestro flow file: ")
    if os.path.exists(flow_file):
        if controller.load_maestro_flow(flow_file):
            print(f"✅ Loaded flow from {flow_file}")
            return True
        else:
            print(f"❌ Failed to load flow from {flow_file}")
            return False
    else:
        print(f"❌ Flow file not found: {flow_file}")
        return False

# Add IPython/Jupyter magic commands if in Jupyter environment
try:
    get_ipython
    
    # Jupyter environment detected
    from IPython.core.magic import register_line_magic
    
    @register_line_magic
    def android_devices(line):
        """List connected Android devices."""
        devices = get_devices()
        if devices:
            return devices
        else:
            return "No devices connected"
    
    @register_line_magic
    def android_screenshot(line):
        """Take a screenshot of the selected device."""
        return take_screenshot()
    
    print("Android MCP Jupyter magic commands loaded.")
    print("Available commands:")
    print("  %android_devices - List connected devices")
    print("  %android_screenshot - Take a screenshot")
    
except (NameError, ImportError):
    # Not in Jupyter
    pass

# For command-line usage
if __name__ == "__main__":
    run_ui_mode() 