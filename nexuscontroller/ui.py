"""
User Interface for Android MCP.
"""

import os
import sys
from typing import List, Dict, Any, Optional, Callable
from IPython.display import clear_output

from .controller import AndroidController
from .utils import display_keycode_reference, logger

class Menu:
    """
    Base menu class.
    """
    
    def __init__(self, title: str, options: List[Dict[str, Any]] = None):
        """
        Initialize a menu.
        
        Args:
            title: The menu title.
            options: List of menu options.
        """
        self.title = title
        self.options = options or []
    
    def add_option(self, key: str, label: str, action: Callable, description: str = ""):
        """
        Add an option to the menu.
        
        Args:
            key: The key to select this option (like "1" or "q").
            label: The displayed label for this option.
            action: The function to call when this option is selected.
            description: Optional description of the option.
        """
        self.options.append({
            "key": key,
            "label": label,
            "action": action,
            "description": description
        })
    
    def display(self):
        """
        Display the menu.
        """
        print(f"\n=== {self.title} ===")
        for option in self.options:
            print(f"{option['key']}. {option['label']}")
            if option['description']:
                print(f"   {option['description']}")
    
    def handle_input(self, user_input: str) -> bool:
        """
        Handle user input.
        
        Args:
            user_input: The user's input.
            
        Returns:
            True if the input was handled, False otherwise.
        """
        for option in self.options:
            if option['key'].lower() == user_input.lower():
                option['action']()
                return True
        
        print("Invalid selection. Please try again.")
        return False


class MainMenu(Menu):
    """
    Main menu for Android MCP.
    """
    
    def __init__(self, controller: AndroidController):
        """
        Initialize the main menu.
        
        Args:
            controller: The AndroidController instance.
        """
        super().__init__("Main Menu")
        self.controller = controller
        self.selected_device = None
        
        # Add options
        self.add_option("1", "📱 Device Information", self.show_device_info_menu)
        self.add_option("2", "📸 Media Actions", self.show_media_menu)
        self.add_option("3", "📦 App Management", self.show_app_menu)
        self.add_option("4", "🔄 System Actions", self.show_system_menu)
        self.add_option("5", "👆 Input Actions", self.show_input_menu)
        self.add_option("6", "📂 File Operations", self.show_file_menu)
        self.add_option("7", "📊 Monitoring & Logs", self.show_monitoring_menu)
        self.add_option("8", "🤖 Maestro UI Automation", self.show_maestro_menu)
        self.add_option("9", "💬 Send WhatsApp Message", self.send_whatsapp_message)
        self.add_option("0", "🚪 Exit", self.exit_program)
    
    def show_device_info_menu(self):
        """Show device information menu"""
        # Implementation would go here
        pass
    
    def show_media_menu(self):
        """Show media actions menu"""
        # Implementation would go here
        pass
    
    def show_app_menu(self):
        """Show app management menu"""
        # Implementation would go here
        pass
    
    def show_system_menu(self):
        """Show system actions menu"""
        # Implementation would go here
        pass
    
    def show_input_menu(self):
        """Show input actions menu"""
        # Implementation would go here
        pass
    
    def show_file_menu(self):
        """Show file operations menu"""
        # Implementation would go here
        pass
    
    def show_monitoring_menu(self):
        """Show monitoring & logs menu"""
        # Implementation would go here
        pass
    
    def show_maestro_menu(self):
        """Show Maestro UI automation menu"""
        menu = MaestroMenu(self.controller, self.selected_device)
        menu.run()
    
    def send_whatsapp_message(self):
        """Send a WhatsApp message"""
        # Implementation would go here
        pass
    
    def exit_program(self):
        """Exit the program"""
        print("Exiting Android MCP...")
        sys.exit(0)
    
    def select_device(self) -> bool:
        """
        Select a device to use.
        
        Returns:
            True if a device was selected, False otherwise.
        """
        devices = self.controller.get_devices()
        
        if not devices:
            print("❌ No devices connected. Please connect a device and try again.")
            input("Press Enter to continue...")
            return False
        
        # Display available devices
        print(f"\nFound {len(devices)} connected device(s):")
        for i, device_id in enumerate(devices):
            try:
                info = self.controller.get_device_info(device_id)
                print(f"{i + 1}. {info.get('manufacturer', 'Unknown')} {info.get('model', 'Unknown')} " + 
                      f"(Android {info.get('android_version', 'Unknown')}, API {info.get('api_level', 'Unknown')})")
                print(f"   Battery: {info.get('battery_level', 'Unknown')}% " + 
                      f"({info.get('battery_status', 'Unknown')}), Resolution: {info.get('screen_resolution', 'Unknown')}")
                print(f"   IP: {info.get('ip_address', 'Unknown')}")
                print(f"   ID: {device_id}")
            except Exception as e:
                logger.error(f"Error getting device info: {str(e)}")
                print(f"{i + 1}. Device ID: {device_id} (Error getting device info)")
        
        # Auto-select if only one device
        if len(devices) == 1:
            self.selected_device = devices[0]
            print(f"\nAutomatically selected the only connected device: {self.selected_device}")
            return True
        
        # Let user select a device
        try:
            device_num = int(input("\nSelect device number (or 0 to exit): "))
            if device_num == 0:
                return False
            
            if 1 <= device_num <= len(devices):
                self.selected_device = devices[device_num - 1]
                return True
            else:
                print("Invalid device number. Please try again.")
                return False
        except ValueError:
            print("Please enter a valid number.")
            return False
    
    def run(self):
        """
        Run the main menu loop.
        """
        while True:
            if not self.selected_device and not self.select_device():
                continue
            
            clear_output(wait=True)
            print(f"Current device: {self.selected_device}")
            
            self.display()
            
            user_input = input("\nSelect option: ")
            self.handle_input(user_input)
            
            # Let user see results before continuing
            input("\nPress Enter to continue...")


class MaestroMenu(Menu):
    """
    Menu for Maestro UI automation.
    """
    
    def __init__(self, controller: AndroidController, device_id: str):
        """
        Initialize the Maestro menu.
        
        Args:
            controller: The AndroidController instance.
            device_id: The selected device ID.
        """
        super().__init__("Maestro UI Automation")
        self.controller = controller
        self.device_id = device_id
        
        # Build the menu
        self._build_menu()
    
    def _build_menu(self):
        """
        Build the Maestro menu options.
        """
        self.add_option("1", "Create new Maestro flow", self.create_new_flow)
        self.add_option("2", "Add launch app to flow", self.add_launch_app)
        self.add_option("3", "Add tap action to flow", self.add_tap_action)
        self.add_option("4", "Add text input to flow", self.add_text_input)
        self.add_option("5", "Add swipe action to flow", self.add_swipe_action)
        self.add_option("6", "Add wait action to flow", self.add_wait_action)
        self.add_option("7", "Add back button press to flow", self.add_back_press)
        # Add more Maestro options here
        self.add_option("34", "Run current Maestro flow", self.run_flow)
        self.add_option("35", "Record new Maestro flow", self.record_flow)
        self.add_option("36", "List recorded Maestro flows", self.list_flows)
        self.add_option("37", "Run recorded Maestro flow", self.run_recorded_flow)
        self.add_option("0", "Back to main menu", self.back_to_main)
    
    def create_new_flow(self):
        """Create a new Maestro flow"""
        self.controller.clear_maestro_flow()
    
    def add_launch_app(self):
        """Add launch app command to flow"""
        package_name = input("Enter package name to launch: ")
        self.controller.append_to_maestro_flow(f"appId: {package_name}\n---\n- launchApp\n")
        print(f"✅ Added 'launchApp' for {package_name} to current Maestro flow")
    
    def add_tap_action(self):
        """Add tap action to flow"""
        print("Select tap method:")
        print("1. Tap by text")
        print("2. Tap by ID")
        print("3. Tap by coordinates")
        
        tap_method = input("Enter method: ")
        
        if tap_method == "1":
            text = input("Enter text to tap on: ")
            yaml_content = f'- tapOn:\n    text: "{text}"\n'
            self.controller.append_to_maestro_flow(yaml_content)
            print(f"✅ Added 'tapOn' with text: \"{text}\" to current Maestro flow")
        elif tap_method == "2":
            element_id = input("Enter element ID to tap on: ")
            yaml_content = f'- tapOn:\n    id: "{element_id}"\n'
            self.controller.append_to_maestro_flow(yaml_content)
            print(f"✅ Added 'tapOn' with id: \"{element_id}\" to current Maestro flow")
        elif tap_method == "3":
            coordinates = input("Enter coordinates (x,y): ")
            x, y = coordinates.split(',')
            yaml_content = f'- tapOn:\n    point: "{x.strip()},{y.strip()}"\n'
            self.controller.append_to_maestro_flow(yaml_content)
            print(f"✅ Added 'tapOn' with point: \"{coordinates}\" to current Maestro flow")
        else:
            print("Invalid method selected.")
    
    def add_text_input(self):
        """Add text input to flow"""
        text_to_input = input("Enter text to input: ")
        element_id = input("Enter element ID (optional): ")
        
        yaml_content = '- inputText:\n'
        yaml_content += f'    text: "{text_to_input}"\n'
        
        if element_id:
            yaml_content += f'    id: "{element_id}"\n'
        
        self.controller.append_to_maestro_flow(yaml_content)
        print(f"✅ Added 'inputText' to current Maestro flow")
    
    def add_swipe_action(self):
        """Add swipe action to flow"""
        start_coords = input("Enter start coordinates (x,y): ")
        end_coords = input("Enter end coordinates (x,y): ")
        
        start_x, start_y = start_coords.split(',')
        end_x, end_y = end_coords.split(',')
        
        yaml_content = '- swipe:\n'
        yaml_content += f'    start: "{start_x.strip()},{start_y.strip()}"\n'
        yaml_content += f'    end: "{end_x.strip()},{end_y.strip()}"\n'
        
        self.controller.append_to_maestro_flow(yaml_content)
        print(f"✅ Added 'swipe' from {start_coords} to {end_coords} to current Maestro flow")
    
    def add_wait_action(self):
        """Add wait action to flow"""
        try:
            wait_time = float(input("Enter wait time in seconds: "))
            yaml_content = f'- wait: {wait_time}\n'
            self.controller.append_to_maestro_flow(yaml_content)
            print(f"✅ Added 'wait' for {wait_time} seconds to current Maestro flow")
        except ValueError:
            print("Invalid time. Please enter a number.")
    
    def add_back_press(self):
        """Add back button press to flow"""
        yaml_content = '- pressBack\n'
        self.controller.append_to_maestro_flow(yaml_content)
        print(f"✅ Added 'pressBack' to current Maestro flow")
    
    def run_flow(self):
        """Run the current Maestro flow"""
        self.controller.maestro_run_flow(self.device_id)
    
    def record_flow(self):
        """Record a new Maestro flow"""
        # Implementation would go here
        pass
    
    def list_flows(self):
        """List recorded Maestro flows"""
        # Implementation would go here
        pass
    
    def run_recorded_flow(self):
        """Run a recorded Maestro flow"""
        # Implementation would go here
        pass
    
    def back_to_main(self):
        """Go back to the main menu"""
        # This just needs to exit this menu's loop
        pass
    
    def run(self):
        """
        Run the Maestro menu loop.
        """
        running = True
        while running:
            clear_output(wait=True)
            print(f"Current device: {self.device_id}")
            
            self.display()
            
            user_input = input("\nSelect option: ")
            if user_input == "0":
                running = False
            else:
                self.handle_input(user_input)
                
                # Let user see results before continuing
                input("\nPress Enter to continue...")


def main():
    """
    Main entry point for the Android MCP UI.
    """
    try:
        controller = AndroidController()
        menu = MainMenu(controller)
        menu.run()
    except KeyboardInterrupt:
        print("\nExiting Android MCP...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1) 