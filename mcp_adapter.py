#!/usr/bin/env python3
"""
MCP Adapter for NexusControl
This adapter enables NexusControl to be used as an MCP server.
"""

import os
import sys
import json
import time
import base64
import traceback
from typing import Dict, List, Any, Optional

# This will be imported from the main NexusControl script
android_mcp = None

class MCPAdapter:
    """Adapter to interface between NexusControl and MCP protocol"""
    
    def __init__(self):
        self.current_device = None
        self.devices = []
        self.initialize()
    
    def initialize(self):
        """Initialize the adapter with global NexusControl instance"""
        global android_mcp
        # This will be set by nexuscontrol_advanced.py
        if android_mcp is None:
            print("Error: NexusControl instance not available", file=sys.stderr)
            sys.exit(1)
        
        # Refresh devices list
        self.refresh_devices()
    
    def refresh_devices(self):
        """Refresh the list of connected devices"""
        try:
            self.devices = android_mcp.get_devices()
        except Exception as e:
            print(f"Error refreshing devices: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            self.devices = []
    
    def list_devices(self) -> List[Dict[str, str]]:
        """List all available devices in MCP format"""
        self.refresh_devices()
        
        device_list = []
        for device_id in self.devices:
            try:
                # Get device info
                info = android_mcp.get_device_info(device_id)
                
                # Format for MCP protocol
                device_info = {
                    "id": device_id,
                    "name": f"{info.get('model', 'Unknown')}",
                    "type": "android"
                }
                device_list.append(device_info)
            except Exception as e:
                print(f"Error getting device info: {str(e)}", file=sys.stderr)
                # Add basic info if we can't get detailed info
                device_list.append({
                    "id": device_id,
                    "name": "Android Device",
                    "type": "android"
                })
        
        return device_list
    
    def use_device(self, device_id: str, device_type: str) -> Dict[str, Any]:
        """Select a device to use"""
        if device_id in self.devices:
            self.current_device = device_id
            return {"success": True}
        else:
            self.refresh_devices()
            if device_id in self.devices:
                self.current_device = device_id
                return {"success": True}
            else:
                return {"success": False}
    
    def take_screenshot(self) -> Dict[str, Any]:
        """Take a screenshot on the current device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            screenshot_path = android_mcp.take_screenshot(self.current_device)
            
            # Check if file exists and read image data
            if os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as f:
                    image_data = f.read()
                
                # Base64 encode the image
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                
                # Delete the file after reading
                try:
                    os.remove(screenshot_path)
                except:
                    pass
                
                return {
                    "success": True,
                    "image": image_b64
                }
            else:
                return {"success": False}
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def list_apps(self) -> Dict[str, Any]:
        """List installed apps on the device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            packages = android_mcp.list_packages(self.current_device)
            return {
                "success": True,
                "packages": packages
            }
        except Exception as e:
            print(f"Error listing apps: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def launch_app(self, package_name: str) -> Dict[str, Any]:
        """Launch an app on the device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            # Use monkey to launch app
            result = android_mcp.run_shell_command(
                self.current_device, 
                f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
            )
            return {"success": True}
        except Exception as e:
            print(f"Error launching app: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def terminate_app(self, package_name: str) -> Dict[str, Any]:
        """Stop an app on the device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            result = android_mcp.run_shell_command(
                self.current_device, 
                f"am force-stop {package_name}"
            )
            return {"success": True}
        except Exception as e:
            print(f"Error terminating app: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def get_screen_size(self) -> Dict[str, Any]:
        """Get the screen size of the device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            # Get screen resolution from wm size
            result = android_mcp.run_shell_command(self.current_device, "wm size")
            
            # Parse result
            for line in result.split("\n"):
                if "Physical size" in line:
                    # Format: Physical size: 1080x2340
                    size = line.split(":")[1].strip()
                    width, height = map(int, size.split("x"))
                    return {
                        "success": True,
                        "width": width,
                        "height": height
                    }
            
            return {"success": False}
        except Exception as e:
            print(f"Error getting screen size: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def tap_screen(self, x: int, y: int) -> Dict[str, Any]:
        """Tap the screen at the given coordinates"""
        if not self.current_device:
            return {"success": False}
        
        try:
            android_mcp.tap_screen(self.current_device, x, y)
            return {"success": True}
        except Exception as e:
            print(f"Error tapping screen: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def swipe_screen(self, direction: str) -> Dict[str, Any]:
        """Swipe the screen in the given direction"""
        if not self.current_device:
            return {"success": False}
        
        try:
            # Get screen size for calculating swipe coordinates
            size_result = self.get_screen_size()
            if not size_result["success"]:
                return {"success": False}
            
            width = size_result["width"]
            height = size_result["height"]
            
            # Calculate swipe coordinates based on direction
            if direction.lower() == "up":
                x1 = width // 2
                y1 = height * 2 // 3
                x2 = width // 2
                y2 = height // 3
            elif direction.lower() == "down":
                x1 = width // 2
                y1 = height // 3
                x2 = width // 2
                y2 = height * 2 // 3
            else:
                return {"success": False}
            
            # Perform the swipe
            android_mcp.swipe_screen(self.current_device, x1, y1, x2, y2, 300)
            return {"success": True}
        except Exception as e:
            print(f"Error swiping screen: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def type_keys(self, text: str, submit: bool) -> Dict[str, Any]:
        """Type text into the device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            # Type the text
            android_mcp.send_text(self.current_device, text)
            
            # Send enter key if submit is true
            if submit:
                android_mcp.send_keyevent(self.current_device, 66)  # KEYCODE_ENTER
            
            return {"success": True}
        except Exception as e:
            print(f"Error typing text: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def press_button(self, button: str) -> Dict[str, Any]:
        """Press a button on the device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            button_map = {
                "BACK": 4,
                "HOME": 3,
                "VOLUME_UP": 24,
                "VOLUME_DOWN": 25,
                "ENTER": 66
            }
            
            if button.upper() not in button_map:
                return {"success": False}
            
            keycode = button_map[button.upper()]
            android_mcp.send_keyevent(self.current_device, keycode)
            
            return {"success": True}
        except Exception as e:
            print(f"Error pressing button: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def open_url(self, url: str) -> Dict[str, Any]:
        """Open a URL on the device"""
        if not self.current_device:
            return {"success": False}
        
        try:
            android_mcp.run_shell_command(
                self.current_device, 
                f"am start -a android.intent.action.VIEW -d {url}"
            )
            return {"success": True}
        except Exception as e:
            print(f"Error opening URL: {str(e)}", file=sys.stderr)
            return {"success": False}
    
    def list_elements_on_screen(self) -> Dict[str, Any]:
        """List UI elements on the screen"""
        if not self.current_device:
            return {"success": False}
        
        try:
            # We can use uiautomator dump to get UI elements
            dump_result = android_mcp.run_shell_command(
                self.current_device,
                "uiautomator dump /sdcard/window_dump.xml"
            )
            
            # Pull the XML file
            temp_xml = f"/tmp/window_dump_{int(time.time())}.xml"
            android_mcp.pull_file(self.current_device, "/sdcard/window_dump.xml", temp_xml)
            
            # Parse the XML (simplified for this adapter)
            elements = []
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(temp_xml)
                root = tree.getroot()
                
                # Extract basic info from nodes
                for node in root.findall(".//node"):
                    attrib = node.attrib
                    if attrib.get("clickable") == "true" or attrib.get("checkable") == "true" or attrib.get("focusable") == "true":
                        elements.append({
                            "text": attrib.get("text", ""),
                            "resourceId": attrib.get("resource-id", ""),
                            "class": attrib.get("class", ""),
                            "bounds": attrib.get("bounds", ""),
                            "clickable": attrib.get("clickable", "false") == "true"
                        })
            except Exception as xml_error:
                print(f"Error parsing XML: {str(xml_error)}", file=sys.stderr)
                return {"success": False}
            finally:
                # Clean up
                try:
                    os.remove(temp_xml)
                    android_mcp.run_shell_command(self.current_device, "rm /sdcard/window_dump.xml")
                except:
                    pass
            
            return {
                "success": True,
                "elements": elements
            }
        except Exception as e:
            print(f"Error listing elements: {str(e)}", file=sys.stderr)
            return {"success": False}

# Main MCP request handler
def handle_mcp_request(request_json):
    """Handle an MCP API request"""
    try:
        # Parse the request
        request = json.loads(request_json)
        id = request.get("id", 0)
        jsonrpc = request.get("jsonrpc", "2.0")
        method = request.get("method", "")
        params = request.get("params", {})
        
        # Initialize adapter if needed
        if not hasattr(handle_mcp_request, "adapter"):
            handle_mcp_request.adapter = MCPAdapter()
        
        adapter = handle_mcp_request.adapter
        
        # Standard response structure
        response = {
            "jsonrpc": "2.0",
            "id": id
        }
        
        # Route request to appropriate method
        try:
            if method == "mcp.mobile_list_available_devices":
                devices = adapter.list_devices()
                response["result"] = devices
            elif method == "mcp.mobile_use_device":
                device = params.get("device", "")
                device_type = params.get("deviceType", "android")
                result = adapter.use_device(device, device_type)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to use device"
                    }
            elif method == "mcp.mobile_take_screenshot":
                result = adapter.take_screenshot()
                if result.get("success", False):
                    response["result"] = result.get("image", "")
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to take screenshot"
                    }
            elif method == "mcp.mobile_list_apps":
                result = adapter.list_apps()
                if result.get("success", False):
                    response["result"] = result.get("packages", [])
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to list apps"
                    }
            elif method == "mcp.mobile_launch_app":
                package_name = params.get("packageName", "")
                result = adapter.launch_app(package_name)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to launch app"
                    }
            elif method == "mcp.mobile_terminate_app":
                package_name = params.get("packageName", "")
                result = adapter.terminate_app(package_name)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to terminate app"
                    }
            elif method == "mcp.mobile_get_screen_size":
                result = adapter.get_screen_size()
                if result.get("success", False):
                    response["result"] = {
                        "width": result.get("width", 0),
                        "height": result.get("height", 0)
                    }
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to get screen size"
                    }
            elif method == "mcp.mobile_click_on_screen_at_coordinates":
                x = params.get("x", 0)
                y = params.get("y", 0)
                result = adapter.tap_screen(x, y)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to tap screen"
                    }
            elif method == "mcp.swipe_on_screen":
                direction = params.get("direction", "")
                result = adapter.swipe_screen(direction)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to swipe screen"
                    }
            elif method == "mcp.mobile_type_keys":
                text = params.get("text", "")
                submit = params.get("submit", False)
                result = adapter.type_keys(text, submit)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to type text"
                    }
            elif method == "mcp.mobile_press_button":
                button = params.get("button", "")
                result = adapter.press_button(button)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to press button"
                    }
            elif method == "mcp.mobile_open_url":
                url = params.get("url", "")
                result = adapter.open_url(url)
                if result.get("success", False):
                    response["result"] = True
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to open URL"
                    }
            elif method == "mcp.mobile_list_elements_on_screen":
                result = adapter.list_elements_on_screen()
                if result.get("success", False):
                    response["result"] = result.get("elements", [])
                else:
                    response["error"] = {
                        "code": -32000,
                        "message": "Failed to list elements"
                    }
            else:
                response["error"] = {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
        except Exception as e:
            print(f"Method execution error: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            response["error"] = {
                "code": -32000,
                "message": f"Error: {str(e)}"
            }
            
        return response
            
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "jsonrpc": "2.0",
            "id": 0,
            "error": {
                "code": -32000,
                "message": f"Error handling request: {str(e)}"
            }
        }

# MCP server main loop
def run_mcp_server():
    """Run the MCP server loop"""
    print("NexusControl MCP Server started", file=sys.stderr)
    
    while True:
        try:
            # Read request line from stdin
            request_line = sys.stdin.readline().strip()
            if not request_line:
                continue
            
            # Parse and handle request
            response = handle_mcp_request(request_line)
            
            # Send response
            response_json = json.dumps(response)
            print(response_json, flush=True)
            
        except Exception as e:
            print(f"Error in MCP server: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            # Send error response in case of exception
            error_response = {
                "jsonrpc": "2.0",
                "id": 0,
                "error": {
                    "code": -32000,
                    "message": f"Server error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)

# This will be initialized by the main script
def initialize_mcp_adapter(mcp_instance):
    """Initialize the MCP adapter with the NexusControl instance"""
    global android_mcp
    android_mcp = mcp_instance
    
    # Start MCP server if we're in MCP mode
    if os.environ.get("NEXUSCONTROL_MCP_MODE") == "true":
        run_mcp_server()

if __name__ == "__main__":
    print("This module should be imported by NexusControl", file=sys.stderr) 