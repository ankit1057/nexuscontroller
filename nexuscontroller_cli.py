#!/usr/bin/env python3
"""
NexusController - Advanced Android Automation Platform

This module provides the main entry point for the NexusController platform, 
offering both CLI and Jupyter notebook interfaces for comprehensive Android
device automation and testing.

Key Features:
- Device management via ADB
- Screenshot and screen recording
- UI automation via Maestro
- Interactive menu system
- Jupyter notebook integration with magic commands

Created and maintained by ankit1057 (github.com/ankit1057)
"""

import os
import sys
import time
from nexuscontroller import AndroidController
from nexuscontroller.utils import logger, print_keycode_reference, ensure_dir

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

def record_screen(device_id=None, duration=10):
    """Record the screen on the selected device."""
    if not device_id:
        device_id = select_device()
    
    if device_id:
        try:
            print(f"📹 Recording screen for {duration} seconds...")
            video_path = controller.record_screen(device_id, duration)
            print(f"✅ Screen recording saved to {video_path}")
            return video_path
        except Exception as e:
            print(f"❌ Error recording screen: {str(e)}")
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
    try:
        controller.tap_screen(device_id, int(x), int(y))
        print(f"✅ Tapped at coordinates ({x}, {y}) on device {device_id}")
        return True
    except Exception as e:
        print(f"❌ Error tapping on screen: {str(e)}")
        return False

def input_text(device_id, text):
    """
    Input text on the device.
    
    Args:
        device_id: The device ID.
        text: Text to input.
    """
    try:
        controller.input_text(device_id, text)
        print(f"✅ Input text: '{text}' on device {device_id}")
        return True
    except Exception as e:
        print(f"❌ Error inputting text: {str(e)}")
        return False

def list_installed_apps(device_id=None):
    """List installed apps on the device."""
    if not device_id:
        device_id = select_device()
    
    if device_id:
        try:
            apps = controller.get_installed_packages(device_id)
            print(f"\nFound {len(apps)} installed apps on device {device_id}:")
            
            # Show first 10 apps
            for i, app in enumerate(apps[:10]):
                print(f"{i+1}. {app}")
            
            if len(apps) > 10:
                print(f"... and {len(apps)-10} more apps")
            
            return apps
        except Exception as e:
            print(f"❌ Error listing apps: {str(e)}")
            return None
    return None

def launch_app(device_id=None):
    """Launch an app on the device."""
    if not device_id:
        device_id = select_device()
    
    if device_id:
        package_name = input("Enter package name to launch: ")
        if package_name:
            try:
                controller.launch_app(device_id, package_name)
                print(f"✅ Launched app: {package_name} on device {device_id}")
                return True
            except Exception as e:
                print(f"❌ Error launching app: {str(e)}")
                return False
    return False

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
    """Run the UI mode of NexusController."""
    print("\n======================================")
    print("  NexusController - Android Automation")
    print("======================================\n")
    
    main_menu = build_main_menu()
    try:
        main_menu.execute()
    except KeyboardInterrupt:
        print("\nExiting NexusController...")
        sys.exit(0)

def build_main_menu():
    """Build the main menu structure."""
    main_menu = SubMenu("NexusController - Android Automation Platform", back_option=False)
    
    # Device submenu
    device_menu = SubMenu("📱 Device Management")
    device_menu.add_item(ActionMenu("List connected devices", lambda: print(f"\nConnected devices: {get_devices()}")))
    device_menu.add_item(ActionMenu("Select device", select_device))
    device_menu.add_item(ActionMenu("View device info", lambda: print(f"\nDevice info: {controller.get_device_info(select_device(), force_refresh=True)}")))
    
    # Screenshot submenu
    media_menu = SubMenu("📸 Media Actions")
    media_menu.add_item(ActionMenu("Take screenshot", lambda: take_screenshot(select_device())))
    media_menu.add_item(ActionMenu("Record screen", lambda: record_screen(select_device(), int(input("Enter duration in seconds: ")))))
    
    # App management submenu
    app_menu = SubMenu("📦 App Management")
    app_menu.add_item(ActionMenu("List installed apps", lambda: list_installed_apps(select_device())))
    app_menu.add_item(ActionMenu("Launch app", lambda: launch_app(select_device())))
    app_menu.add_item(ActionMenu("Force stop app", lambda: controller.force_stop_app(select_device(), input("Enter package name to stop: "))))
    app_menu.add_item(ActionMenu("Clear app data", lambda: controller.clear_app_data(select_device(), input("Enter package name to clear data: "))))
    
    # System actions submenu
    system_menu = SubMenu("🔄 System Actions")
    system_menu.add_item(ActionMenu("Reboot device", lambda: controller.reboot_device(select_device())))
    system_menu.add_item(ActionMenu("Get device properties", lambda: print(f"\nDevice properties: {controller.get_device_properties(select_device())}")))
    
    # Input actions submenu
    input_menu = SubMenu("👆 Input Actions")
    input_menu.add_item(ActionMenu("Tap on screen", lambda: tap_on_screen(select_device(), 
                                                                        input("Enter X coordinate: "), 
                                                                        input("Enter Y coordinate: "))))
    input_menu.add_item(ActionMenu("Input text", lambda: input_text(select_device(), input("Enter text to input: "))))
    input_menu.add_item(ActionMenu("Press key", lambda: controller.press_key(select_device(), input("Enter key code (e.g., HOME, BACK): "))))
    input_menu.add_item(ActionMenu("Show keycode reference", print_keycode_reference))
    
    # Maestro submenu
    maestro_menu = SubMenu("🤖 Maestro UI Automation")
    maestro_menu.add_item(ActionMenu("Run sample flow", lambda: run_sample_flow(select_device())))
    maestro_menu.add_item(ActionMenu("Load flow from file", load_flow_from_file))
    maestro_menu.add_item(ActionMenu("Execute loaded flow", lambda: execute_maestro_flow(select_device())))
    maestro_menu.add_item(ActionMenu("Create and save flow", create_and_save_flow))
    
    # Add submenus to main menu
    main_menu.add_item(device_menu)
    main_menu.add_item(media_menu)
    main_menu.add_item(app_menu)
    main_menu.add_item(system_menu)
    main_menu.add_item(input_menu)
    main_menu.add_item(maestro_menu)
    main_menu.add_item(ActionMenu("Exit", sys.exit))
    
    return main_menu

def create_and_save_flow():
    """Create and save a Maestro flow interactively."""
    device_id = select_device()
    if not device_id:
        return False
    
    package_name = input("Enter package name to automate: ")
    if not package_name:
        print("❌ Package name is required.")
        return False
    
    controller.clear_maestro_flow()
    controller.append_to_maestro_flow(f"appId: {package_name}\n---\n")
    controller.append_to_maestro_flow("- launchApp\n")
    
    print("\nBuilding Maestro flow. Select actions to add:")
    
    while True:
        print("\n--- Available Actions ---")
        print("1. Tap on text")
        print("2. Tap on element by ID")
        print("3. Tap on coordinates")
        print("4. Input text")
        print("5. Swipe")
        print("6. Wait")
        print("7. Press back button")
        print("8. Save and exit")
        print("0. Cancel")
        
        try:
            action = int(input("\nSelect action: "))
            
            if action == 0:
                print("❌ Flow creation cancelled.")
                return False
            
            elif action == 1:
                text = input("Enter text to tap on: ")
                controller.append_to_maestro_flow(create_maestro_tap(text=text))
            
            elif action == 2:
                element_id = input("Enter element ID to tap on: ")
                controller.append_to_maestro_flow(create_maestro_tap(id=element_id))
            
            elif action == 3:
                x = input("Enter X coordinate: ")
                y = input("Enter Y coordinate: ")
                controller.append_to_maestro_flow(create_maestro_tap(point=[x, y]))
            
            elif action == 4:
                text = input("Enter text to input: ")
                controller.append_to_maestro_flow(create_maestro_input(text))
            
            elif action == 5:
                start = input("Enter start coordinates (x,y): ")
                end = input("Enter end coordinates (x,y): ")
                controller.append_to_maestro_flow(create_maestro_swipe(start, end))
            
            elif action == 6:
                seconds = input("Enter seconds to wait: ")
                controller.append_to_maestro_flow(f"- wait: {seconds}\n")
            
            elif action == 7:
                controller.append_to_maestro_flow("- back\n")
            
            elif action == 8:
                # Save flow
                flow_file = input("Enter file path to save flow: ")
                if not flow_file:
                    flow_file = f"maestro_flows/{package_name}_flow.yaml"
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(flow_file), exist_ok=True)
                
                # Save to file
                with open(flow_file, 'w') as f:
                    f.write(controller.maestro_flow)
                
                print(f"✅ Flow saved to {flow_file}")
                return True
            
            else:
                print("Invalid option. Please try again.")
        
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nFlow creation cancelled.")
            return False

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
    
    print("NexusController Jupyter integration loaded.")
    print("Available commands:")
    print("  %android_devices - List connected devices")
    print("  %android_screenshot - Take a screenshot")
    
except (NameError, ImportError):
    # Not in Jupyter
    pass

if __name__ == "__main__":
    run_ui_mode() 