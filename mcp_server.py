#!/usr/bin/env python3
"""
FastMCP Server Implementation for NexusControl
This script implements a MCP (Mobile Control Protocol) server using the fastmcp library
to allow remote control of Android devices for testing mform_app.
"""

import os
import sys
import json
import base64
import logging
from typing import Dict, List, Any, Optional

# Import FastMCP library
try:
    from fastmcp import FastMCP
    from mcp import JSONRPCRequest, JSONRPCResponse, JSONRPCError
except ImportError:
    print("Error: fastmcp library not installed. Install it with: pip install fastmcp")
    sys.exit(1)

# Import NexusControl
from nexuscontrol_advanced import AndroidMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_server")

# Initialize NexusControl
android_mcp = AndroidMCP()
current_device = None

# Initialize FastMCP
mcp_server = FastMCP()

# Define tool functions for MCP methods

def list_available_devices():
    """List all available devices"""
    try:
        devices = android_mcp.get_devices()
        device_list = []
        
        for device_id in devices:
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
                logger.error(f"Error getting device info: {str(e)}")
                # Add basic info if we can't get detailed info
                device_list.append({
                    "id": device_id,
                    "name": "Android Device",
                    "type": "android"
                })
        
        return device_list
    except Exception as e:
        logger.error(f"Error listing devices: {str(e)}")
        raise Exception(f"Failed to list devices: {str(e)}")

def use_device(device: str, deviceType: str = "android"):
    """Select a device to use"""
    global current_device
    
    try:
        if not device:
            raise Exception("Missing required parameter: device")
        
        devices = android_mcp.get_devices()
        if device in devices:
            current_device = device
            return True
        else:
            raise Exception(f"Device {device} not found")
    except Exception as e:
        logger.error(f"Error selecting device: {str(e)}")
        raise Exception(f"Failed to use device: {str(e)}")

def take_screenshot():
    """Take a screenshot of the device"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        screenshot_path = android_mcp.take_screenshot(current_device)
        
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
            
            return image_b64
        else:
            raise Exception("Failed to capture screenshot")
    except Exception as e:
        logger.error(f"Error taking screenshot: {str(e)}")
        raise Exception(f"Failed to take screenshot: {str(e)}")

def list_apps():
    """List all installed apps on the device"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        packages = android_mcp.list_packages(current_device)
        return packages
    except Exception as e:
        logger.error(f"Error listing apps: {str(e)}")
        raise Exception(f"Failed to list apps: {str(e)}")

def launch_app(packageName: str):
    """Launch an app on the device"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        if not packageName:
            raise Exception("Missing required parameter: packageName")
        
        # Use monkey to launch app
        result = android_mcp.run_shell_command(
            current_device, 
            f"monkey -p {packageName} -c android.intent.category.LAUNCHER 1"
        )
        return True
    except Exception as e:
        logger.error(f"Error launching app: {str(e)}")
        raise Exception(f"Failed to launch app: {str(e)}")

def terminate_app(packageName: str):
    """Terminate an app on the device"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        if not packageName:
            raise Exception("Missing required parameter: packageName")
        
        result = android_mcp.run_shell_command(
            current_device, 
            f"am force-stop {packageName}"
        )
        return True
    except Exception as e:
        logger.error(f"Error terminating app: {str(e)}")
        raise Exception(f"Failed to terminate app: {str(e)}")

def get_screen_size():
    """Get the screen size of the device"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        # Get screen resolution from wm size
        result = android_mcp.run_shell_command(current_device, "wm size")
        
        # Parse result
        for line in result.split("\n"):
            if "Physical size" in line:
                # Format: Physical size: 1080x2340
                size = line.split(":")[1].strip()
                width, height = map(int, size.split("x"))
                return {"width": width, "height": height}
        
        raise Exception("Failed to get screen size")
    except Exception as e:
        logger.error(f"Error getting screen size: {str(e)}")
        raise Exception(f"Failed to get screen size: {str(e)}")

def click_on_screen_at_coordinates(x: int, y: int):
    """Click/tap on the screen at the given coordinates"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        if x is None or y is None:
            raise Exception("Missing required parameters: x and y")
        
        android_mcp.tap_screen(current_device, int(x), int(y))
        return True
    except Exception as e:
        logger.error(f"Error tapping screen: {str(e)}")
        raise Exception(f"Failed to tap screen: {str(e)}")

def swipe_on_screen(direction: str):
    """Swipe on the screen in the given direction"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        if not direction:
            raise Exception("Missing required parameter: direction")
        
        # Get screen size for calculating swipe coordinates
        result = android_mcp.run_shell_command(current_device, "wm size")
        
        width = 1080  # Default values
        height = 1920
        
        # Parse result to get actual screen size
        for line in result.split("\n"):
            if "Physical size" in line:
                size = line.split(":")[1].strip()
                width, height = map(int, size.split("x"))
        
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
            raise Exception("Invalid direction: must be 'up' or 'down'")
        
        # Perform the swipe
        android_mcp.swipe_screen(current_device, x1, y1, x2, y2, 300)
        return True
    except Exception as e:
        logger.error(f"Error swiping screen: {str(e)}")
        raise Exception(f"Failed to swipe screen: {str(e)}")

def type_keys(text: str, submit: bool = False):
    """Type text into the device"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        if not text:
            raise Exception("Missing required parameter: text")
        
        # Type the text
        android_mcp.send_text(current_device, text)
        
        # Send enter key if submit is true
        if submit:
            android_mcp.send_keyevent(current_device, 66)  # KEYCODE_ENTER
        
        return True
    except Exception as e:
        logger.error(f"Error typing text: {str(e)}")
        raise Exception(f"Failed to type text: {str(e)}")

def press_button(button: str):
    """Press a button on the device"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        if not button:
            raise Exception("Missing required parameter: button")
        
        # Map button names to keycodes
        button_map = {
            "BACK": 4,
            "HOME": 3,
            "VOLUME_UP": 24,
            "VOLUME_DOWN": 25,
            "ENTER": 66
        }
        
        if button not in button_map:
            raise Exception(f"Invalid button: {button}")
        
        android_mcp.send_keyevent(current_device, button_map[button])
        return True
    except Exception as e:
        logger.error(f"Error pressing button: {str(e)}")
        raise Exception(f"Failed to press button: {str(e)}")

def open_url(url: str):
    """Open a URL in the browser"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        if not url:
            raise Exception("Missing required parameter: url")
        
        # Use am to open URL
        result = android_mcp.run_shell_command(
            current_device, 
            f"am start -a android.intent.action.VIEW -d {url}"
        )
        
        return True
    except Exception as e:
        logger.error(f"Error opening URL: {str(e)}")
        raise Exception(f"Failed to open URL: {str(e)}")

def list_elements_on_screen():
    """List UI elements on the screen (using UI Automator)"""
    if not current_device:
        raise Exception("No device selected")
    
    try:
        # Use UI Automator to dump the UI hierarchy
        dump_file = "/sdcard/window_dump.xml"
        android_mcp.run_shell_command(current_device, f"uiautomator dump {dump_file}")
        
        # Pull the file
        local_dump = "window_dump.xml"
        android_mcp.pull_file(current_device, dump_file, local_dump)
        
        # Check if file exists
        if not os.path.exists(local_dump):
            raise Exception("Failed to get UI hierarchy")
        
        # Parse the XML and extract elements
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(local_dump)
            root = tree.getroot()
            
            elements = []
            for elem in root.findall(".//node"):
                attrs = elem.attrib
                
                # Get bounds
                bounds_str = attrs.get("bounds", "")
                bounds = []
                
                # Parse bounds (format is like "[0,0][1080,2340]")
                if bounds_str:
                    parts = bounds_str.strip("[]").split("][")
                    if len(parts) == 2:
                        try:
                            x1, y1 = map(int, parts[0].split(","))
                            x2, y2 = map(int, parts[1].split(","))
                            
                            # Calculate center point
                            center_x = (x1 + x2) // 2
                            center_y = (y1 + y2) // 2
                            
                            bounds = [center_x, center_y]
                        except:
                            bounds = []
                
                # Get text or description
                text = attrs.get("text", "")
                content_desc = attrs.get("content-desc", "")
                resource_id = attrs.get("resource-id", "")
                
                # Use content description if text is empty
                display_text = text if text else content_desc
                
                # Skip elements without text or bounds
                if (display_text or resource_id) and bounds:
                    elements.append({
                        "id": resource_id,
                        "text": display_text,
                        "bounds": bounds
                    })
            
            # Clean up
            try:
                os.remove(local_dump)
                android_mcp.run_shell_command(current_device, f"rm {dump_file}")
            except:
                pass
            
            return elements
        
        except ImportError:
            logger.error("ElementTree XML parser not available")
            raise Exception("XML parser not available")
        except Exception as e:
            logger.error(f"Error parsing UI hierarchy: {str(e)}")
            raise Exception(f"Failed to parse UI hierarchy: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error listing elements: {str(e)}")
        raise Exception(f"Failed to list elements: {str(e)}")

# ----- Register tools with FastMCP -----

# Add all the tools to the FastMCP server
mcp_server.add_tool(name="list_available_devices", fn=list_available_devices)
mcp_server.add_tool(name="use_device", fn=use_device)
mcp_server.add_tool(name="take_screenshot", fn=take_screenshot)
mcp_server.add_tool(name="list_apps", fn=list_apps)
mcp_server.add_tool(name="launch_app", fn=launch_app)
mcp_server.add_tool(name="terminate_app", fn=terminate_app)
mcp_server.add_tool(name="get_screen_size", fn=get_screen_size)
mcp_server.add_tool(name="click_on_screen_at_coordinates", fn=click_on_screen_at_coordinates)
mcp_server.add_tool(name="swipe_on_screen", fn=swipe_on_screen)
mcp_server.add_tool(name="type_keys", fn=type_keys)
mcp_server.add_tool(name="press_button", fn=press_button)
mcp_server.add_tool(name="open_url", fn=open_url)
mcp_server.add_tool(name="list_elements_on_screen", fn=list_elements_on_screen)

# ----- Main function -----

def main():
    """Main entry point to start the MCP server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FastMCP Server for NexusControl")
    # Comment out host and port arguments as they're not supported by FastMCP
    # parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server to")
    # parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    
    args = parser.parse_args()
    
    print(f"Starting FastMCP server")
    print("Press Ctrl+C to exit")
    
    try:
        # Call run() without arguments as FastMCP doesn't support host/port params
        mcp_server.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()