"""
Configuration constants for the Android MCP.
"""

import os

# Directory configuration
MAESTRO_FLOWS_DIR = 'maestro_flows'
CURRENT_MAESTRO_FLOW_FILE = os.path.join(MAESTRO_FLOWS_DIR, 'current_flow.yaml')

# Ensure Maestro flows directory exists
os.makedirs(MAESTRO_FLOWS_DIR, exist_ok=True)

# Command constants
CONSTANTS = {
    # ADB commands
    'ADB_COMMAND': 'adb',
    'DEVICE_FLAG': '--device',
    'SHELL_COMMAND': 'shell',
    'PULL_COMMAND': 'pull',
    'PUSH_COMMAND': 'push',
    'INSTALL_COMMAND': 'install',
    'UNINSTALL_COMMAND': 'uninstall',
    'LOGCAT_COMMAND': 'logcat',
    'VERSION_COMMAND': 'version',
    'REBOOT_COMMAND': 'reboot',
    
    # ADB shell commands
    'PACKAGE_MANAGER_COMMAND': 'pm',
    'LIST_COMMAND': 'list',
    'CLEAR_COMMAND': 'clear',
    'DUMPSYS_COMMAND': 'dumpsys',
    'INPUT_COMMAND': 'input',
    'SCREEN_CAPTURE_COMMAND': 'screencap',
    'SCREEN_RECORD_COMMAND': 'screenrecord',
    'KILLALL_COMMAND': 'killall',
    'GETPROP_COMMAND': 'getprop',
    'WM_SIZE_COMMAND': 'wm size',
    'BATTERY_INFO_COMMAND': 'battery',
    'PACKAGE_INFO_COMMAND': 'package',
    'PERMISSION_INFO_COMMAND': 'permission',
    
    # Maestro
    'MAESTRO_COMMAND': 'maestro',
    'TEST_COMMAND': 'test',
    'MAESTRO_STUDIO_COMMAND': 'studio',
    
    # Maestro actions
    'PRESS_BACK_COMMAND': 'pressBack',
    'WAIT_COMMAND': 'wait',
    'LONG_PRESS_COMMAND': 'longPressOn',
    'SCROLL_COMMAND': 'scroll',
    'ASSERT_NOT_VISIBLE_COMMAND': 'assertNotVisible',
    'RUN_SCRIPT_COMMAND': 'runScript',
    'ERASE_TEXT_COMMAND': 'eraseText',
    'CLIPBOARD_COPY_COMMAND': 'clipboardCopy',
    'CLIPBOARD_PASTE_COMMAND': 'clipboardPaste',
    'TAKE_SCREENSHOT_COMMAND': 'takeScreenshot',
    'ADB_SHELL_COMMAND': 'adbShell',
    'OPEN_LINK_COMMAND': 'openLink',
    'PRESS_KEY_COMMAND': 'pressKey',
    'SIMULATE_LOCATION_COMMAND': 'simulateLocation',
    'STOP_SIMULATE_LOCATION_COMMAND': 'stopSimulateLocation',
    'START_RECORDING_COMMAND': 'startRecording',
    'STOP_RECORDING_COMMAND': 'stopRecording',
    'RUN_FLOW_COMMAND': 'runFlow',
    'SET_PERSISTENT_VARIABLE_COMMAND': 'setPersistentVariable',
    'GET_PERSISTENT_VARIABLE_COMMAND': 'getPersistentVariable',
    'CLEAR_PERSISTENT_VARIABLE_COMMAND': 'clearPersistentVariable',
    'RUN_HTTP_COMMAND': 'runHttp',
    'ADB_REBOOT_COMMAND': 'adbReboot',
    'ADB_PULL_COMMAND': 'adbPull',
    'ADB_PUSH_COMMAND': 'adbPush',
    'ADB_INSTALL_COMMAND': 'adbInstall',
    'ADB_UNINSTALL_COMMAND': 'adbUninstall',
    
    # Other constants
    'ERROR_STRING': 'error',
    'SUCCESS_STRING': 'Success',
    'UNKNOWN_STRING': 'Unknown',
    'NEWLINE': '\n',
    'WRITE_MODE': 'w',
    'APPEND_MODE': 'a',
    'READ_MODE': 'r',
    'DEVICE_STATUS_DEVICE': 'device',
    'PACKAGE_PREFIX': 'package:',
    'DATE_TIME_FORMAT': '%Y%m%d_%H%M%S',
    
    # Regex patterns
    'VERSION_NAME_REGEX': r'versionName=([^\s]+)',
    'PACKAGE_PATH_REGEX': r'package:(.+)',
    'PERMISSION_REGEX': r'android\.permission\.([A-Z_]+)',
    'IP_ADDRESS_REGEX': r'inet (\d+\.\d+\.\d+\.\d+)',
    'SCREEN_SIZE_REGEX': r'Physical size: (\d+x\d+)',
    'BATTERY_LEVEL_REGEX': r'level: (\d+)',
    'BATTERY_STATUS_REGEX': r'status: (\d+)',
    
    # Network
    'WIFI_INTERFACE': 'wlan0',
    'IP_ADDR_COMMAND': 'ip addr show',
}

# Battery status mapping
BATTERY_STATUS_MAP = {
    1: CONSTANTS['UNKNOWN_STRING'],
    2: 'Charging',
    3: 'Discharging',
    4: 'Not charging',
    5: 'Full'
}

# Device info keys
DEVICE_INFO_KEYS = {
    'API_LEVEL_KEY': 'api_level',
    'ANDROID_VERSION_KEY': 'android_version',
    'MANUFACTURER_KEY': 'manufacturer',
    'MODEL_KEY': 'model',
    'BATTERY_LEVEL_KEY': 'battery_level',
    'BATTERY_STATUS_KEY': 'battery_status',
    'SCREEN_RESOLUTION_KEY': 'screen_resolution',
    'IP_ADDRESS_KEY': 'ip_address',
}

# Common Android keycodes
KEYCODES = {
    'KEYCODE_HOME': 3,
    'KEYCODE_BACK': 4,
    'KEYCODE_DPAD_UP': 19,
    'KEYCODE_DPAD_DOWN': 20,
    'KEYCODE_DPAD_LEFT': 21,
    'KEYCODE_DPAD_RIGHT': 22,
    'KEYCODE_DPAD_CENTER': 23,
    'KEYCODE_VOLUME_UP': 24,
    'KEYCODE_VOLUME_DOWN': 25,
    'KEYCODE_POWER': 26,
    'KEYCODE_CAMERA': 27,
    'KEYCODE_MENU': 82,
    'KEYCODE_ENTER': 66,
    'KEYCODE_DEL': 67,
    'KEYCODE_TAB': 61,
    'KEYCODE_SPACE': 62,
    'KEYCODE_APP_SWITCH': 187
} 