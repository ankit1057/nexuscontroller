#!/usr/bin/env python3
"""
Android Mobile Control Panel (MCP)
A simple Python script to control Android devices via ADB.
"""

import os
import subprocess
import sys
import time

class AndroidMCP:
    def __init__(self):
        self.check_adb_installed()
        
    def check_adb_installed(self):
        """Check if ADB is installed and accessible."""
        try:
            subprocess.run(["adb", "version"], capture_output=True, text=True, check=True)
            print("✅ ADB is installed and accessible.")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("❌ ADB is not installed or not in PATH.")
            print("Please install ADB and make sure it's in your PATH.")
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
    
    def get_device_info(self, device_id):
        """Get basic information about a device."""
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
            info["battery"] = result.stdout.strip().split(": ")[1]
        except (IndexError, ValueError):
            info["battery"] = "Unknown"
            
        return info
    
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
    
    def list_packages(self, device_id):
        """List installed packages on the device."""
        print(f"📋 Listing packages on device {device_id}...")
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "pm", "list", "packages"],
            capture_output=True, text=True, check=True
        )
        
        packages = []
        for line in result.stdout.strip().split('\n'):
            if line.startswith("package:"):
                packages.append(line[8:])  # Remove "package:" prefix
        
        return packages
    
    def reboot_device(self, device_id):
        """Reboot the device."""
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
        
        print("\n=== Android Mobile Control Panel ===")
        print(f"Found {len(devices)} connected device(s):")
        
        for i, device_id in enumerate(devices):
            info = mcp.get_device_info(device_id)
            print(f"{i+1}. {info['model']} (Android {info['android_version']}) - Battery: {info['battery']}% - ID: {device_id}")
        
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
            print("\n=== Device Actions ===")
            print("1. Take screenshot")
            print("2. Install APK")
            print("3. Uninstall app")
            print("4. List installed packages")
            print("5. Reboot device")
            print("6. Send text input")
            print("7. Run shell command")
            print("8. Select different device")
            print("0. Exit")
            
            try:
                action = int(input("\nSelect action: "))
                
                if action == 0:
                    return
                elif action == 1:
                    mcp.take_screenshot(selected_device)
                elif action == 2:
                    apk_path = input("Enter APK file path: ")
                    mcp.install_apk(selected_device, apk_path)
                elif action == 3:
                    package_name = input("Enter package name to uninstall: ")
                    mcp.uninstall_app(selected_device, package_name)
                elif action == 4:
                    packages = mcp.list_packages(selected_device)
                    print("\nInstalled packages:")
                    for i, package in enumerate(sorted(packages)):
                        print(f"{i+1}. {package}")
                elif action == 5:
                    confirm = input("Are you sure you want to reboot the device? (y/n): ")
                    if confirm.lower() == 'y':
                        mcp.reboot_device(selected_device)
                elif action == 6:
                    text = input("Enter text to send: ")
                    mcp.send_text(selected_device, text)
                elif action == 7:
                    command = input("Enter shell command: ")
                    mcp.run_shell_command(selected_device, command)
                elif action == 8:
                    break
                else:
                    print("Invalid action. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Android MCP...")
        sys.exit(0)