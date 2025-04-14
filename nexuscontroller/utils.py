"""
Utility functions for Android MCP.
"""

import os
import re
import logging
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from .config import CONSTANTS, DEVICE_INFO_KEYS, BATTERY_STATUS_MAP

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("android_mcp")
logger.setLevel(logging.DEBUG)

# File handler
log_file = os.path.join(log_dir, f"android_mcp_{datetime.now().strftime('%Y%m%d')}.log")
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.WARNING)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def run_command(cmd: List[str], check: bool = False) -> Tuple[str, str, int]:
    """
    Run a command and return stdout, stderr, and return code.
    
    Args:
        cmd: Command to run as a list of strings
        check: Whether to raise an exception if the command fails
        
    Returns:
        Tuple of (stdout, stderr, return_code)
    """
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return result.stdout, result.stderr, result.returncode
    except subprocess.SubprocessError as e:
        logger.error(f"Error running command {' '.join(cmd)}: {str(e)}")
        if check:
            raise
        return "", str(e), 1

def generate_timestamp_filename(prefix: str, ext: str) -> str:
    """
    Generate a filename with a timestamp.
    
    Args:
        prefix: Prefix for the filename
        ext: File extension (without dot)
        
    Returns:
        Generated filename
    """
    timestamp = datetime.now().strftime(CONSTANTS['DATE_TIME_FORMAT'])
    return f"{prefix}_{timestamp}.{ext}"

def extract_regex_match(pattern: str, text: str, group: int = 1, default: str = "") -> str:
    """
    Extract a regex match from text.
    
    Args:
        pattern: Regex pattern
        text: Text to search in
        group: Group to extract (default: 1)
        default: Default value if no match is found
        
    Returns:
        Extracted text or default value
    """
    match = re.search(pattern, text)
    if match and len(match.groups()) >= group:
        return match.group(group)
    return default

def ensure_directory_exists(path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
    """
    os.makedirs(path, exist_ok=True)

def display_keycode_reference() -> None:
    """
    Display a reference of common Android keycodes.
    """
    from .config import KEYCODES
    
    print('\n=== Android Keycode Reference ===')
    print("These codes can be used with the 'Send keyevent' option:")
    for name, code in sorted(KEYCODES.items()):
        print(f"{code}: {name}")

def get_timestamp():
    """Get a formatted timestamp string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")
    return directory

# Android keycodes for reference
KEYCODES = {
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

def print_keycode_reference():
    """Print a reference of common Android keycodes."""
    print("\n=== Android Keycode Reference ===")
    print("These codes can be used with the 'Send keyevent' option:")
    for name, code in sorted(KEYCODES.items()):
        print(f"{code}: {name}") 