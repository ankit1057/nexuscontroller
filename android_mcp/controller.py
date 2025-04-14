"""
Android Controller Module
Provides the main controller class for interacting with Android devices.
"""

import os
import subprocess
import sys
import time
import re
import json
import base64
import threading
import traceback
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from pathlib import Path

from .config import CONSTANTS, DEVICE_INFO_KEYS, BATTERY_STATUS_MAP, MAESTRO_FLOWS_DIR, CURRENT_MAESTRO_FLOW_FILE
from .utils import run_command, generate_timestamp_filename, extract_regex_match, ensure_directory_exists, logger

class AndroidController:
    """
    Main controller class for Android device interaction.
    Provides methods for device control, app management, and UI automation.
    """
    
    def __init__(self):
        """Initialize the controller and check for ADB."""
        self.check_adb_installed()
        self.device_cache = {}
        self.maestro_flow = ""
        logger.info("AndroidController initialized")
        self.current_maestro_flow_file = CURRENT_MAESTRO_FLOW_FILE
        ensure_directory_exists(MAESTRO_FLOWS_DIR)
        self.clear_maestro_flow()
    
    def check_adb_installed(self):
        """Check if ADB is installed and accessible."""
        try:
            result = subprocess.run(["adb", "version"], capture_output=True, text=True, check=True)
            logger.info(f"ADB is installed: {result.stdout.splitlines()[0]}")
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error("ADB is not installed or not in PATH")
            print("❌ ADB is not installed or not in PATH.")
            print("Please install ADB and make sure it's in your PATH.")
            return False
    
    def get_devices(self):
        """Get list of connected devices."""
        logger.info("Getting connected devices")
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip the first line (header)
        
        devices = []
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    device_id = parts[0].strip()
                    status = parts[1].strip()
                    if status == "device":  # Only include authorized devices
                        devices.append(device_id)
        
        logger.info(f"Found {len(devices)} device(s): {devices}")
        return devices
    
    def get_device_info(self, device_id, force_refresh=False):
        """Get comprehensive information about a device."""
        logger.info(f"Getting device info for {device_id}")
        
        if device_id in self.device_cache and not force_refresh:
            return self.device_cache[device_id]
            
        info = {}
        
        # Get device model
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
            capture_output=True, text=True, check=False
        )
        info["model"] = result.stdout.strip()
        
        # Get Android version
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.build.version.release"],
            capture_output=True, text=True, check=False
        )
        info["android_version"] = result.stdout.strip()
        
        # Get battery level
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "dumpsys", "battery", "|", "grep", "level"],
            capture_output=True, text=True, shell=True, check=False
        )
        try:
            info["battery_level"] = result.stdout.strip().split(": ")[1]
        except (IndexError, ValueError):
            info["battery_level"] = "Unknown"
        
        # Cache the info
        self.device_cache[device_id] = info
        return info
    
    def take_screenshot(self, device_id, output_path=None):
        """Take a screenshot on the device."""
        logger.info(f"Taking screenshot on device {device_id}")
        
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"screenshot_{device_id}_{timestamp}.png"
            
        # Take screenshot on device
        subprocess.run(
            ["adb", "-s", device_id, "shell", "screencap", "-p", "/sdcard/screenshot.png"],
            check=True
        )
        
        # Pull screenshot to computer
        subprocess.run(
            ["adb", "-s", device_id, "pull", "/sdcard/screenshot.png", output_path],
            check=True
        )
        
        # Remove screenshot from device
        subprocess.run(
            ["adb", "-s", device_id, "shell", "rm", "/sdcard/screenshot.png"],
            check=True
        )
        
        logger.info(f"Screenshot saved to {output_path}")
        return output_path
    
    # Maestro integration methods
    def clear_maestro_flow(self):
        """Clear the current Maestro flow."""
        self.maestro_flow = ""
        logger.info("Maestro flow cleared")
        try:
            with open(self.current_maestro_flow_file, CONSTANTS['WRITE_MODE']) as f:
                f.write('# Maestro Flow generated by Android MCP\n')
            print(f"✅ Cleared current Maestro flow file: {self.current_maestro_flow_file}")
        except Exception as e:
            logger.error(f"Error clearing Maestro flow: {str(e)}")
            print(f"❌ Failed to clear Maestro flow: {str(e)}")
    
    def append_to_maestro_flow(self, yaml_snippet):
        """Append to the current Maestro flow."""
        self.maestro_flow += yaml_snippet
        logger.info(f"Added to Maestro flow: {yaml_snippet.strip()}")
    
    def maestro_run_flow(self, device_id=None):
        """Run the current Maestro flow."""
        if not self.maestro_flow:
            logger.error("No Maestro flow to run")
            return False
            
        # Save flow to temporary file
        flow_file = "maestro_flows/temp_flow.yaml"
        os.makedirs(os.path.dirname(flow_file), exist_ok=True)
        
        with open(flow_file, "w") as f:
            f.write(self.maestro_flow)
        
        # Run Maestro test
        cmd = ["maestro", "test", flow_file]
        if device_id:
            cmd.extend(["--device", device_id])
        
        logger.info(f"Running Maestro flow: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Maestro flow ran successfully")
                return True
            else:
                logger.error(f"Maestro flow failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error running Maestro flow: {str(e)}")
            return False

    # Add remaining methods from the original AndroidController here
    # including record_screen, install_apk, uninstall_app, list_packages, etc.
    
    def check_maestro_installed(self) -> None:
        """
        Check if Maestro is installed and accessible.
        
        If Maestro is not installed, the user is prompted to continue without
        Maestro or exit.
        """
        try:
            stdout, stderr, return_code = run_command(
                [CONSTANTS['MAESTRO_COMMAND'], '--version']
            )
            
            if return_code == 0:
                logger.info(f"Maestro is installed and accessible: {stdout.strip()}")
            else:
                self._handle_maestro_not_installed()
        except Exception as e:
            logger.error(f"Error checking Maestro installation: {str(e)}")
            self._handle_maestro_not_installed()
    
    def _handle_maestro_not_installed(self) -> None:
        """
        Handle the case when Maestro is not installed.
        
        Prompts the user to continue without Maestro or exit.
        """
        print('⚠️ Maestro is not installed or not in PATH.')
        print('Some UI automation features will not be available.')
        print('To install Maestro, run: curl -Ls "https://get.maestro.mobile.dev" | bash')
        
        continue_without_maestro = input('Do you want to continue without Maestro? (y/n): ')
        if continue_without_maestro.lower() != 'y':
            sys.exit(1)

    def _get_device_property(self, device_id: str, property_name: str) -> str:
        """
        Get a specific property from the device.
        
        Args:
            device_id: The device ID/serial.
            property_name: The name of the property to get.
            
        Returns:
            The property value as a string.
        """
        stdout, stderr, return_code = run_command([
            CONSTANTS['ADB_COMMAND'], 
            CONSTANTS['DEVICE_FLAG'], 
            device_id, 
            CONSTANTS['SHELL_COMMAND'], 
            CONSTANTS['GETPROP_COMMAND'], 
            property_name
        ])
        
        return stdout.strip()
    
    def _run_adb_shell_command(self, device_id: str, command: str) -> str:
        """
        Run an ADB shell command on the device.
        
        Args:
            device_id: The device ID/serial.
            command: The shell command to run.
            
        Returns:
            The command output as a string.
        """
        stdout, stderr, return_code = run_command([
            CONSTANTS['ADB_COMMAND'], 
            CONSTANTS['DEVICE_FLAG'], 
            device_id, 
            CONSTANTS['SHELL_COMMAND'], 
            command
        ])
        
        return stdout
    
    def record_screen(self, device_id: str, output_path: Optional[str] = None) -> str:
        """
        Record a screen video of the device.
        
        Args:
            device_id: The device ID/serial.
            output_path: The path to save the video to.
            
        Returns:
            The path to the saved video.
        """
        remote_path = '/sdcard/screen_record.mp4'
        
        if not output_path:
            output_path = generate_timestamp_filename(f"screen_record_{device_id}", "mp4")
        
        print(f"📹 Recording screen on device {device_id}...")
        
        try:
            # Record screen
            run_command([
                CONSTANTS['ADB_COMMAND'], 
                CONSTANTS['DEVICE_FLAG'], 
                device_id, 
                CONSTANTS['SHELL_COMMAND'], 
                CONSTANTS['SCREEN_RECORD_COMMAND'], 
                '-p', 
                remote_path
            ], check=True)
            
            # Pull to local machine
            run_command([
                CONSTANTS['ADB_COMMAND'], 
                CONSTANTS['DEVICE_FLAG'], 
                device_id, 
                CONSTANTS['PULL_COMMAND'], 
                remote_path, 
                output_path
            ], check=True)
            
            # Clean up
            run_command([
                CONSTANTS['ADB_COMMAND'], 
                CONSTANTS['DEVICE_FLAG'], 
                device_id, 
                CONSTANTS['SHELL_COMMAND'], 
                'rm', 
                remote_path
            ])
            
            print(f"✅ Screen recording saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error recording screen: {str(e)}")
            print(f"❌ Failed to record screen: {str(e)}")
            return ""

    # Add more Maestro-related methods here 