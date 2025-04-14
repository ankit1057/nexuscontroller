#!/usr/bin/env python3
"""
Android Mobile Control Panel (MCP) with Maestro Integration
A comprehensive Python script to control Android devices via ADB with Maestro UI automation.
"""

import os
import subprocess
import sys
import time
import re
import threading
import json
import yaml
from datetime import datetime
from pathlib import Path

class AndroidMCP:
    def __init__(self):
        self.check_adb_installed()
        self.check_maestro_installed()
        self.device_cache = {}
        self.maestro_flow_file = "maestro_flow.yaml"
        self.clear_maestro_flow()
        
    def check_adb_installed(self):
        """Check if ADB is installed and accessible."""
        try:
            result = subprocess.run(["adb", "version"], capture_output=True, text=True, check=True)
            print(f"✅ ADB is installed and accessible.\n{result.stdout.splitlines()[0]}")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("❌ ADB is not installed or not in PATH.")
            print("Please install ADB and make sure it's in your PATH.")
            sys.exit(1)
    
    def check_maestro_installed(self):
        """Check if Maestro is installed and accessible."""
        try:
            result = subprocess.run(["maestro", "--version"], capture_output=True, text=True, check=True)
            print(f"✅ Maestro is installed and accessible.\n{result.stdout.strip()}")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("⚠️ Maestro is not installed or not in PATH.")
            print("Some UI automation features will not be available.")
            print("To install Maestro, run: curl -Ls \"https://get.maestro.mobile.dev\" | bash")
            choice = input("Do you want to continue without Maestro? (y/n): ")
            if choice.lower() != 'y':
                sys.exit(1)
    
    def get_devices(self):
        """Get list of connected devices."""
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
        
        return devices
    
    def get_device_info(self, device_id, force_refresh=False):
        """Get comprehensive information about a device."""
        if device_id in self.device_cache and not force_refresh:
            return self.device_cache[device_id]
            
        info = {}
        
        # Get device model
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
            capture_output=True, text=True, check=False
        )
        info["model"] = result.stdout.strip()
        
        # Get device manufacturer
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.product.manufacturer"],
            capture_output=True, text=True, check=False
        )
        info["manufacturer"] = result.stdout.strip()
        
        # Get Android version
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.build.version.release"],
            capture_output=True, text=True, check=False
        )
        info["android_version"] = result.stdout.strip()
        
        # Get API level
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.build.version.sdk"],
            capture_output=True, text=True, check=False
        )
        info["api_level"] = result.stdout.strip()
        
        # Get battery level
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "dumpsys", "battery"],
            capture_output=True, text=True, check=False
        )
        battery_output = result.stdout
        
        # Extract battery level
        level_match = re.search(r'level: (\d+)', battery_output)
        info["battery_level"] = level_match.group(1) if level_match else "Unknown"
        
        # Extract battery status
        status_match = re.search(r'status: (\d+)', battery_output)
        status_code = int(status_match.group(1)) if status_match else -1
        status_map = {
            1: "Unknown",
            2: "Charging",
            3: "Discharging",
            4: "Not charging",
            5: "Full"
        }
        info["battery_status"] = status_map.get(status_code, "Unknown")
        
        # Get screen resolution
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "wm", "size"],
            capture_output=True, text=True, check=False
        )
        size_match = re.search(r'Physical size: (\d+x\d+)', result.stdout)
        info["screen_resolution"] = size_match.group(1) if size_match else "Unknown"
        
        # Get device IP address (if connected to WiFi)
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "ip", "addr", "show", "wlan0"],
            capture_output=True, text=True, check=False
        )
        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
        info["ip_address"] = ip_match.group(1) if ip_match else "Not connected to WiFi"
        
        # Cache the info
        self.device_cache[device_id] = info
        return info
    
    # Standard ADB functions
    
    def take_screenshot(self, device_id, output_path=None):
        """Take a screenshot on the device."""
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"screenshot_{device_id}_{timestamp}.png"
            
        print(f"📱 Taking screenshot on device {device_id}...")
        
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
        
        print(f"✅ Screenshot saved to {output_path}")
        return output_path
    
    def record_screen(self, device_id, duration=10, output_path=None):
        """Record the device screen for a specified duration (in seconds)."""
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"screenrecord_{device_id}_{timestamp}.mp4"
        
        print(f"🎥 Recording screen on device {device_id} for {duration} seconds...")
        
        # Start recording in a separate thread so we can time it
        def record():
            subprocess.run(
                ["adb", "-s", device_id, "shell", "screenrecord", "/sdcard/screenrecord.mp4"],
                check=False
            )
        
        record_thread = threading.Thread(target=record)
        record_thread.daemon = True
        record_thread.start()
        
        # Wait for specified duration
        for i in range(duration):
            sys.stdout.write(f"\rRecording: {i+1}/{duration} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        
        # Stop recording (by killing the screenrecord process)
        subprocess.run(
            ["adb", "-s", device_id, "shell", "killall", "screenrecord"],
            check=False
        )
        
        print("\nWaiting for recording to finalize...")
        time.sleep(2)  # Give it a moment to finish writing the file
        
        # Pull recording to computer
        subprocess.run(
            ["adb", "-s", device_id, "pull", "/sdcard/screenrecord.mp4", output_path],
            check=True
        )
        
        # Remove recording from device
        subprocess.run(
            ["adb", "-s", device_id, "shell", "rm", "/sdcard/screenrecord.mp4"],
            check=False
        )
        
        print(f"✅ Screen recording saved to {output_path}")
        return output_path
    
    def install_apk(self, device_id, apk_path):
        """Install an APK on the device."""
        if not os.path.exists(apk_path):
            print(f"❌ APK file not found: {apk_path}")
            return False
            
        print(f"📲 Installing APK on device {device_id}...")
        result = subprocess.run(
            ["adb", "-s", device_id, "install", "-r", apk_path],
            capture_output=True, text=True, check=False
        )
        
        if "Success" in result.stdout:
            print("✅ APK installed successfully")
            return True
        else:
            print(f"❌ Failed to install APK: {result.stderr}")
            return False
    
    def uninstall_app(self, device_id, package_name):
        """Uninstall an app from the device."""
        print(f"🗑️ Uninstalling {package_name} from device {device_id}...")
        result = subprocess.run(
            ["adb", "-s", device_id, "uninstall", package_name],
            capture_output=True, text=True, check=False
        )
        
        if "Success" in result.stdout:
            print("✅ App uninstalled successfully")
            return True
        else:
            print(f"❌ Failed to uninstall app: {result.stderr}")
            return False
    
    def list_packages(self, device_id, filter_str=None):
        """List installed packages on the device."""
        print(f"📋 Listing packages on device {device_id}...")
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "pm", "list", "packages"],
            capture_output=True, text=True, check=True
        )
        
        packages = []
        for line in result.stdout.strip().split('\n'):
            if line.startswith("package:"):
                package = line[8:]  # Remove "package:" prefix
                if not filter_str or filter_str.lower() in package.lower():
                    packages.append(package)
        
        return packages
    
    def get_app_info(self, device_id, package_name):
        """Get detailed information about an installed app."""
        print(f"ℹ️ Getting info for {package_name} on device {device_id}...")
        
        # Get app version
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "dumpsys", "package", package_name, "|", "grep", "versionName"],
            capture_output=True, text=True, shell=True, check=False
        )
        version_match = re.search(r'versionName=([^\s]+)', result.stdout)
        version = version_match.group(1) if version_match else "Unknown"
        
        # Get app path
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "pm", "path", package_name],
            capture_output=True, text=True, check=False
        )
        path_match = re.search(r'package:(.+)', result.stdout)
        path = path_match.group(1).strip() if path_match else "Unknown"
        
        # Get app permissions
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "dumpsys", "package", package_name, "|", "grep", "permission"],
            capture_output=True, text=True, shell=True, check=False
        )
        permissions = []
        for line in result.stdout.splitlines():
            perm_match = re.search(r'android\.permission\.([A-Z_]+)', line)
            if perm_match and perm_match.group(1) not in permissions:
                permissions.append(perm_match.group(1))
        
        return {
            "package": package_name,
            "version": version,
            "path": path,
            "permissions": sorted(permissions)
        }
    
    def clear_app_data(self, device_id, package_name):
        """Clear data for an app."""
        print(f"🧹 Clearing data for {package_name} on device {device_id}...")
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "pm", "clear", package_name],
            capture_output=True, text=True, check=False
        )
        
        if "Success" in result.stdout:
            print("✅ App data cleared successfully")
            return True
        else:
            print(f"❌ Failed to clear app data: {result.stderr}")
            return False
    
    def reboot_device(self, device_id, mode=None):
        """Reboot the device, optionally into a specific mode."""
        if mode:
            print(f"🔄 Rebooting device {device_id} into {mode} mode...")
            subprocess.run(
                ["adb", "-s", device_id, "reboot", mode],
                check=True
            )
        else:
            print(f"🔄 Rebooting device {device_id}...")
            subprocess.run(
                ["adb", "-s", device_id, "reboot"],
                check=True
            )
        print("✅ Reboot command sent")
    
    def send_text(self, device_id, text):
        """Send text input to the device."""
        print(f"⌨️ Sending text to device {device_id}...")
        # Replace spaces with %s for adb input
        text = text.replace(' ', '%s')
        subprocess.run(
            ["adb", "-s", device_id, "shell", "input", "text", text],
            check=True
        )
        print("✅ Text sent")
    
    def send_keyevent(self, device_id, keycode):
        """Send a keyevent to the device."""
        print(f"🔑 Sending keyevent {keycode} to device {device_id}...")
        subprocess.run(
            ["adb", "-s", device_id, "shell", "input", "keyevent", str(keycode)],
            check=True
        )
        print("✅ Keyevent sent")
    
    def tap_screen(self, device_id, x, y):
        """Tap the screen at the specified coordinates."""
        print(f"👆 Tapping at coordinates ({x}, {y}) on device {device_id}...")
        subprocess.run(
            ["adb", "-s", device_id, "shell", "input", "tap", str(x), str(y)],
            check=True
        )
        print("✅ Tap sent")
    
    def swipe_screen(self, device_id, x1, y1, x2, y2, duration=300):
        """Swipe the screen from (x1,y1) to (x2,y2) with the specified duration."""
        print(f"👆 Swiping from ({x1}, {y1}) to ({x2}, {y2}) on device {device_id}...")
        subprocess.run(
            ["adb", "-s", device_id, "shell", "input", "swipe", 
             str(x1), str(y1), str(x2), str(y2), str(duration)],
            check=True
        )
        print("✅ Swipe sent")
    
    def run_shell_command(self, device_id, command):
        """Run a shell command on the device."""
        print(f"🖥️ Running command on device {device_id}: {command}")
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", command],
            capture_output=True, text=True, check=False
        )
        
        print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Errors:\n{result.stderr}")
        
        return result.stdout
    
    def pull_file(self, device_id, device_path, local_path=None):
        """Pull a file from the device to the local machine."""
        if not local_path:
            local_path = os.path.basename(device_path)
            
        print(f"📥 Pulling file from device {device_id}: {device_path} -> {local_path}")
        result = subprocess.run(
            ["adb", "-s", device_id, "pull", device_path, local_path],
            capture_output=True, text=True, check=False
        )
        
        if "error" in result.stderr.lower():
            print(f"❌ Failed to pull file: {result.stderr}")
            return False
        else:
            print("✅ File pulled successfully")
            return True
    
    def push_file(self, device_id, local_path, device_path):
        """Push a file from the local machine to the device."""
        if not os.path.exists(local_path):
            print(f"❌ Local file not found: {local_path}")
            return False
            
        print(f"📤 Pushing file to device {device_id}: {local_path} -> {device_path}")
        result = subprocess.run(
            ["adb", "-s", device_id, "push", local_path, device_path],
            capture_output=True, text=True, check=False
        )
        
        if "error" in result.stderr.lower():
            print(f"❌ Failed to push file: {result.stderr}")
            return False
        else:
            print("✅ File pushed successfully")
            return True
    
    def get_logcat(self, device_id, filter_str=None, lines=50):
        """Get logcat output from the device."""
        if filter_str:
            print(f"📜 Getting logcat from device {device_id} with filter: {filter_str}...")
            result = subprocess.run(
                ["adb", "-s", device_id, "logcat", "-d", filter_str, f"-T", str(lines)],
                capture_output=True, text=True, check=True
            )
        else:
            print(f"📜 Getting logcat from device {device_id}...")
            result = subprocess.run(
                ["adb", "-s", device_id, "logcat", "-d", f"-T", str(lines)],
                capture_output=True, text=True, check=True
            )
        
        return result.stdout
    
    def start_logcat_capture(self, device_id, output_file=None):
        """Start capturing logcat to a file."""
        if not output_file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"logcat_{device_id}_{timestamp}.txt"
        
        print(f"📜 Starting logcat capture to {output_file}...")
        
        # Start logcat in a separate process
        logcat_process = subprocess.Popen(
            ["adb", "-s", device_id, "logcat"],
            stdout=open(output_file, "w"),
            stderr=subprocess.STDOUT
        )
        
        print(f"✅ Logcat capture started (PID: {logcat_process.pid})")
        return logcat_process.pid
    
    def stop_logcat_capture(self, pid):
        """Stop a running logcat capture process."""
        print(f"📜 Stopping logcat capture (PID: {pid})...")
        try:
            os.kill(pid, 15)  # SIGTERM
            print("✅ Logcat capture stopped")
            return True
        except OSError as e:
            print(f"❌ Failed to stop logcat capture: {e}")
            return False
    
    # Maestro Integration Functions
    
    def clear_maestro_flow(self):
        """Clear the Maestro flow file."""
        with open(self.maestro_flow_file, "w") as f:
            f.write("# Maestro Flow generated by Android MCP\n")
        print(f"✅ Cleared Maestro flow file: {self.maestro_flow_file}")
    
    def append_to_maestro_flow(self, yaml_snippet):
        """Append a YAML snippet to the Maestro flow file."""
        with open(self.maestro_flow_file, "a") as f:
            f.write(yaml_snippet + "\n")
    
    def maestro_launch_app(self, package_name):
        """Add a launchApp command to the Maestro flow."""
        yaml_snippet = f"""appId: {package_name}
---
- launchApp
"""
        self.append_to_maestro_flow(yaml_snippet)
        print(f"✅ Added 'launchApp' for {package_name} to Maestro flow")
    
    def maestro_tap(self, text=None, id=None, point=None):
        """Add a tap command to the Maestro flow."""
        yaml_snippet = "- tapOn:\n"
        
        if text:
            yaml_snippet += f"    text: \"{text}\"\n"
        elif id:
            yaml_snippet += f"    id: \"{id}\"\n"
        elif point:
            x, y = point.split(",")
            yaml_snippet += f"    point: \"{x.strip()},{y.strip()}\"\n"
        else:
            print("❌ Error: You must specify either text, id, or point for tap action")
            return False
        
        self.append_to_maestro_flow(yaml_snippet)
        
        if text:
            print(f"✅ Added 'tapOn' with text: \"{text}\" to Maestro flow")
        elif id:
            print(f"✅ Added 'tapOn' with id: \"{id}\" to Maestro flow")
        elif point:
            print(f"✅ Added 'tapOn' with point: \"{point}\" to Maestro flow")
        
        return True
    
    def maestro_input_text(self, text, id=None):
        """Add an inputText command to the Maestro flow."""
        yaml_snippet = "- inputText:\n"
        yaml_snippet += f"    text: \"{text}\"\n"
        
        if id:
            yaml_snippet += f"    id: \"{id}\"\n"
        
        self.append_to_maestro_flow(yaml_snippet)
        
        if id:
            print(f"✅ Added 'inputText' with text: \"{text}\" and id: \"{id}\" to Maestro flow")
        else:
            print(f"✅ Added 'inputText' with text: \"{text}\" to Maestro flow")
        
        return True
    
    def maestro_swipe(self, start, end):
        """Add a swipe command to the Maestro flow."""
        start_x, start_y = start.split(",")
        end_x, end_y = end.split(",")
        
        yaml_snippet = f"""- swipe:
    start: "{start_x.strip()},{start_y.strip()}"
    end: "{end_x.strip()},{end_y.strip()}"
"""
        
        self.append_to_maestro_flow(yaml_snippet)
        print(f"✅ Added 'swipe' from {start} to {end} to Maestro flow")
        return True
    
    def maestro_assert_visible(self, text=None, id=None):
        """Add an assertVisible command to the Maestro flow."""
        yaml_snippet = "- assertVisible:\n"
        
        if text:
            yaml_snippet += f"    text: \"{text}\"\n"
        elif id:
            yaml_snippet += f"    id: \"{id}\"\n"
        else:
            print("❌ Error: You must specify either text or id for assertVisible action")
            return False
        
        self.append_to_maestro_flow(yaml_snippet)
        
        if text:
            print(f"✅ Added 'assertVisible' with text: \"{text}\" to Maestro flow")
        elif id:
            print(f"✅ Added 'assertVisible' with id: \"{id}\" to Maestro flow")
        
        return True
    
    def maestro_wait(self, seconds):
        """Add a wait command to the Maestro flow."""
        yaml_snippet = f"""- wait: {seconds}
"""
        
        self.append_to_maestro_flow(yaml_snippet)
        print(f"✅ Added 'wait' for {seconds} seconds to Maestro flow")
        return True
    
    def maestro_back(self):
        """Add a pressBack command to the Maestro flow."""
        yaml_snippet = "- pressBack\n"
        
        self.append_to_maestro_flow(yaml_snippet)
        print("✅ Added 'pressBack' to Maestro flow")
        return True
    
    def maestro_run_flow(self, device_id=None):
        """Run the generated Maestro flow."""
        print(f"🚀 Running Maestro flow from {self.maestro_flow_file}...")
        
        command = ["maestro", "test", self.maestro_flow_file]
        if device_id:
            command.extend(["--device", device_id])
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("✅ Maestro flow executed successfully")
            print(f"Output:\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run Maestro flow: {e}")
            print(f"Error output:\n{e.stderr}")
            return False
    
    def maestro_record_flow(self, output_file=None):
        """Record a Maestro flow."""
        # Create a temporary flow file if not specified
        temp_flow_file = "temp_flow_to_record.yaml"
        
        # Create a minimal flow file for recording
        with open(temp_flow_file, "w") as f:
            f.write("# Temporary flow file for recording\n")
            f.write("appId: com.android.settings\n---\n")
        
        if not output_file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"recorded_flow_{timestamp}.yaml"
        
        print(f"🎥 Recording Maestro flow to {output_file}...")
        print("Interact with your device to record actions.")
        print("Press Ctrl+C to stop recording.")
        
        try:
            # Run maestro record with the temp flow file as input and --local flag
            if output_file:
                subprocess.run(["maestro", "record", "--local", temp_flow_file, output_file], check=True)
            else:
                subprocess.run(["maestro", "record", temp_flow_file], check=True)
                
            print(f"✅ Maestro flow recorded to {output_file}")
            
            # Clean up temp file
            try:
                os.remove(temp_flow_file)
            except:
                pass
                
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to record Maestro flow: {e}")
            return None
        except KeyboardInterrupt:
            print(f"\n✅ Maestro flow recording stopped and saved to {output_file}")
            return output_file
    
    def maestro_run_recorded_flow(self, flow_file, device_id=None):
        """Run a previously recorded Maestro flow."""
        if not os.path.exists(flow_file):
            print(f"❌ Flow file not found: {flow_file}")
            return False
            
        print(f"🚀 Running recorded Maestro flow from {flow_file}...")
        
        command = ["maestro", "test", flow_file]
        if device_id:
            command.extend(["--device", device_id])
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("✅ Recorded Maestro flow executed successfully")
            print(f"Output:\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run recorded Maestro flow: {e}")
            print(f"Error output:\n{e.stderr}")
            return False
    
    def maestro_studio(self):
        """Launch Maestro Studio for UI inspection."""
        print("🔍 Launching Maestro Studio...")
        
        try:
            subprocess.Popen(["maestro", "studio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ Maestro Studio launched")
            print("Use Maestro Studio to inspect UI elements and generate commands.")
            return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"❌ Failed to launch Maestro Studio: {e}")
            return False

def print_keycode_reference():
    """Print a reference of common Android keycodes."""
    keycodes = {
        "KEYCODE_HOME": 3,
        "KEYCODE_BACK": 4,
        "KEYCODE_DPAD_UP": 19,
        "KEYCODE_DPAD_DOWN": 20,
        "KEYCODE_DPAD_LEFT": 21,
        "KEYCODE_DPAD_RIGHT": 22,
        "KEYCODE_DPAD_CENTER": 23,
        "KEYCODE_VOLUME_UP": 24,
        "KEYCODE_VOLUME_DOWN": 25,
        "KEYCODE_POWER": 26,
        "KEYCODE_CAMERA": 27,
        "KEYCODE_MENU": 82,
        "KEYCODE_ENTER": 66,
        "KEYCODE_DEL": 67,
        "KEYCODE_TAB": 61,
        "KEYCODE_SPACE": 62,
        "KEYCODE_APP_SWITCH": 187
    }
    
    print("\n=== Android Keycode Reference ===")
    print("These codes can be used with the 'Send keyevent' option:")
    for name, code in sorted(keycodes.items()):
        print(f"{code}: {name}")

def main():
    mcp = AndroidMCP()
    
    while True:
        devices = mcp.get_devices()
        
        if not devices:
            print("❌ No devices connected. Please connect a device and try again.")
            choice = input("Try again? (y/n): ")
            if choice.lower() != 'y':
                break
            continue
        
        print("\n=== Android MCP with Maestro Integration ===")
        print(f"Found {len(devices)} connected device(s):")
        
        for i, device_id in enumerate(devices):
            info = mcp.get_device_info(device_id)
            print(f"{i+1}. {info['manufacturer']} {info['model']} (Android {info['android_version']}, API {info['api_level']})")
            print(f"   Battery: {info['battery_level']}% ({info['battery_status']}), Resolution: {info['screen_resolution']}")
            print(f"   IP: {info['ip_address']}")
            print(f"   ID: {device_id}")
        
        # Device selection
        if len(devices) == 1:
            selected_device = devices[0]
            print(f"\nAutomatically selected the only connected device: {selected_device}")
        else:
            while True:
                try:
                    device_num = int(input("\nSelect device number (or 0 to exit): "))
                    if device_num == 0:
                        return
                    if 1 <= device_num <= len(devices):
                        selected_device = devices[device_num - 1]
                        break
                    else:
                        print("Invalid device number. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        
        # Action menu
        while True:
            print("\n=== Main Menu ===")
            print("1. 📱 Device Information")
            print("2. 📸 Media Actions")
            print("3. 📦 App Management")
            print("4. 🔄 System Actions")
            print("5. 👆 Input Actions")
            print("6. 📂 File Operations")
            print("7. 📊 Monitoring & Logs")
            print("8. 🤖 Maestro UI Automation")
            print("9. 🔙 Select Different Device")
            print("0. 🚪 Exit")
            
            try:
                category = int(input("\nSelect category: "))
                
                if category == 0:
                    return
                elif category == 1:  # Device Information
                    print("\n=== Device Information ===")
                    print("1. View device details")
                    print("2. Export device information to JSON")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        info = mcp.get_device_info(selected_device, force_refresh=True)
                        print("\n=== Device Details ===")
                        for key, value in info.items():
                            print(f"{key}: {value}")
                    elif action == 2:
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        output_path = f"device_info_{selected_device}_{timestamp}.json"
                        
                        # Get basic device info
                        info = mcp.get_device_info(selected_device, force_refresh=True)
                        
                        # Get additional system properties
                        result = subprocess.run(
                            ["adb", "-s", selected_device, "shell", "getprop"],
                            capture_output=True, text=True, check=True
                        )
                        
                        # Parse properties
                        properties = {}
                        for line in result.stdout.splitlines():
                            match = re.match(r'\[([^\]]+)\]: \[([^\]]*)\]', line)
                            if match:
                                key, value = match.groups()
                                properties[key] = value
                        
                        # Get installed packages
                        packages = mcp.list_packages(selected_device)
                        
                        # Compile all information
                        export_data = {
                            "device_id": selected_device,
                            "export_time": datetime.now().isoformat(),
                            "basic_info": info,
                            "system_properties": properties,
                            "installed_packages_count": len(packages),
                            "installed_packages": packages
                        }
                        
                        # Write to file
                        with open(output_path, 'w') as f:
                            json.dump(export_data, f, indent=2)
                        
                        print(f"✅ Device information exported to {output_path}")
                
                elif category == 2:  # Media Actions
                    print("\n=== Media Actions ===")
                    print("1. Take screenshot")
                    print("2. Record screen")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        mcp.take_screenshot(selected_device)
                    elif action == 2:
                        try:
                            duration = int(input("Enter recording duration in seconds (default: 10): ") or "10")
                            mcp.record_screen(selected_device, duration)
                        except ValueError:
                            print("Invalid duration. Using default (10 seconds).")
                            mcp.record_screen(selected_device)
                
                elif category == 3:  # App Management
                    print("\n=== App Management ===")
                    print("1. List installed packages")
                    print("2. Install APK")
                    print("3. Uninstall app")
                    print("4. Get app info")
                    print("5. Clear app data")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        filter_str = input("Enter filter string (optional): ")
                        packages = mcp.list_packages(selected_device, filter_str)
                        print(f"\nFound {len(packages)} packages:")
                        for i, package in enumerate(sorted(packages)):
                            print(f"{i+1}. {package}")
                    elif action == 2:
                        apk_path = input("Enter APK file path: ")
                        mcp.install_apk(selected_device, apk_path)
                    elif action == 3:
                        package_name = input("Enter package name to uninstall: ")
                        mcp.uninstall_app(selected_device, package_name)
                    elif action == 4:
                        package_name = input("Enter package name: ")
                        app_info = mcp.get_app_info(selected_device, package_name)
                        print("\n=== App Information ===")
                        print(f"Package: {app_info['package']}")
                        print(f"Version: {app_info['version']}")
                        print(f"Path: {app_info['path']}")
                        print(f"Permissions ({len(app_info['permissions'])}):")
                        for perm in app_info['permissions']:
                            print(f"  - {perm}")
                    elif action == 5:
                        package_name = input("Enter package name to clear data: ")
                        mcp.clear_app_data(selected_device, package_name)
                
                elif category == 4:  # System Actions
                    print("\n=== System Actions ===")
                    print("1. Reboot device")
                    print("2. Reboot to recovery")
                    print("3. Reboot to bootloader")
                    print("4. Run shell command")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        confirm = input("Are you sure you want to reboot the device? (y/n): ")
                        if confirm.lower() == 'y':
                            mcp.reboot_device(selected_device)
                    elif action == 2:
                        confirm = input("Are you sure you want to reboot to recovery? (y/n): ")
                        if confirm.lower() == 'y':
                            mcp.reboot_device(selected_device, "recovery")
                    elif action == 3:
                        confirm = input("Are you sure you want to reboot to bootloader? (y/n): ")
                        if confirm.lower() == 'y':
                            mcp.reboot_device(selected_device, "bootloader")
                    elif action == 4:
                        command = input("Enter shell command: ")
                        mcp.run_shell_command(selected_device, command)
                
                elif category == 5:  # Input Actions
                    print("\n=== Input Actions ===")
                    print("1. Send text")
                    print("2. Send keyevent")
                    print("3. Tap screen")
                    print("4. Swipe screen")
                    print("5. Show keycode reference")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        text = input("Enter text to send: ")
                        mcp.send_text(selected_device, text)
                    elif action == 2:
                        try:
                            keycode = int(input("Enter keycode (see reference with option 5): "))
                            mcp.send_keyevent(selected_device, keycode)
                        except ValueError:
                            print("Invalid keycode. Please enter a number.")
                    elif action == 3:
                        try:
                            x = int(input("Enter X coordinate: "))
                            y = int(input("Enter Y coordinate: "))
                            mcp.tap_screen(selected_device, x, y)
                        except ValueError:
                            print("Invalid coordinates. Please enter numbers.")
                    elif action == 4:
                        try:
                            x1 = int(input("Enter start X coordinate: "))
                            y1 = int(input("Enter start Y coordinate: "))
                            x2 = int(input("Enter end X coordinate: "))
                            y2 = int(input("Enter end Y coordinate: "))
                            duration = int(input("Enter duration in ms (default: 300): ") or "300")
                            mcp.swipe_screen(selected_device, x1, y1, x2, y2, duration)
                        except ValueError:
                            print("Invalid input. Please enter numbers.")
                    elif action == 5:
                        print_keycode_reference()
                
                elif category == 6:  # File Operations
                    print("\n=== File Operations ===")
                    print("1. Pull file from device")
                    print("2. Push file to device")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        device_path = input("Enter file path on device: ")
                        local_path = input("Enter local destination path (optional): ")
                        mcp.pull_file(selected_device, device_path, local_path)
                    elif action == 2:
                        local_path = input("Enter local file path: ")
                        device_path = input("Enter destination path on device: ")
                        mcp.push_file(selected_device, local_path, device_path)
                
                elif category == 7:  # Monitoring & Logs
                    print("\n=== Monitoring & Logs ===")
                    print("1. View logcat")
                    print("2. Start logcat capture to file")
                    print("3. Stop logcat capture")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        filter_str = input("Enter logcat filter (optional): ")
                        try:
                            lines = int(input("Enter number of lines (default: 50): ") or "50")
                            logcat = mcp.get_logcat(selected_device, filter_str, lines)
                            print("\n=== Logcat Output ===")
                            print(logcat)
                        except ValueError:
                            print("Invalid number of lines. Using default (50).")
                            logcat = mcp.get_logcat(selected_device, filter_str)
                            print("\n=== Logcat Output ===")
                            print(logcat)
                    elif action == 2:
                        output_file = input("Enter output file path (optional): ")
                        pid = mcp.start_logcat_capture(selected_device, output_file)
                        print(f"To stop this capture later, use option 3 and enter PID: {pid}")
                    elif action == 3:
                        try:
                            pid = int(input("Enter PID of logcat process to stop: "))
                            mcp.stop_logcat_capture(pid)
                        except ValueError:
                            print("Invalid PID. Please enter a number.")
                
                elif category == 8:  # Maestro UI Automation
                    print("\n=== Maestro UI Automation ===")
                    print("1. Create new Maestro flow")
                    print("2. Add launch app to flow")
                    print("3. Add tap action to flow")
                    print("4. Add text input to flow")
                    print("5. Add swipe action to flow")
                    print("6. Add wait action to flow")
                    print("7. Add back button press to flow")
                    print("8. Add assertion to flow")
                    print("9. Run current Maestro flow")
                    print("10. Record new Maestro flow")
                    print("11. Run recorded Maestro flow")
                    print("12. Launch Maestro Studio")
                    print("0. Back to main menu")
                    
                    action = int(input("\nSelect action: "))
                    if action == 1:
                        mcp.clear_maestro_flow()
                    elif action == 2:
                        package_name = input("Enter package name to launch: ")
                        mcp.maestro_launch_app(package_name)
                    elif action == 3:
                        print("Select tap method:")
                        print("1. Tap by text")
                        print("2. Tap by ID")
                        print("3. Tap by coordinates")
                        tap_method = int(input("Enter method: "))
                        
                        if tap_method == 1:
                            text = input("Enter text to tap on: ")
                            mcp.maestro_tap(text=text)
                        elif tap_method == 2:
                            id_value = input("Enter element ID to tap on: ")
                            mcp.maestro_tap(id=id_value)
                        elif tap_method == 3:
                            point = input("Enter coordinates (x,y): ")
                            mcp.maestro_tap(point=point)
                        else:
                            print("Invalid method selected.")
                    elif action == 4:
                        text = input("Enter text to input: ")
                        id_value = input("Enter element ID (optional): ")
                        if id_value:
                            mcp.maestro_input_text(text, id=id_value)
                        else:
                            mcp.maestro_input_text(text)
                    elif action == 5:
                        start = input("Enter start coordinates (x,y): ")
                        end = input("Enter end coordinates (x,y): ")
                        mcp.maestro_swipe(start, end)
                    elif action == 6:
                        try:
                            seconds = float(input("Enter wait time in seconds: "))
                            mcp.maestro_wait(seconds)
                        except ValueError:
                            print("Invalid time. Please enter a number.")
                    elif action == 7:
                        mcp.maestro_back()
                    elif action == 8:
                        print("Select assertion method:")
                        print("1. Assert by text")
                        print("2. Assert by ID")
                        assert_method = int(input("Enter method: "))
                        
                        if assert_method == 1:
                            text = input("Enter text to assert visible: ")
                            mcp.maestro_assert_visible(text=text)
                        elif assert_method == 2:
                            id_value = input("Enter element ID to assert visible: ")
                            mcp.maestro_assert_visible(id=id_value)
                        else:
                            print("Invalid method selected.")
                    elif action == 9:
                        mcp.maestro_run_flow(selected_device)
                    elif action == 10:
                        output_file = input("Enter output file path (optional): ")
                        mcp.maestro_record_flow(output_file)
                    elif action == 11:
                        flow_file = input("Enter path to recorded flow file: ")
                        mcp.maestro_run_recorded_flow(flow_file, selected_device)
                    elif action == 12:
                        mcp.maestro_studio()
                
                elif category == 9:  # Select Different Device
                    break
                
                else:
                    print("Invalid category. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
            
            if category != 9:  # Don't prompt if changing device
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Android MCP...")
        sys.exit(0)