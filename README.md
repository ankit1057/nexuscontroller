# Android Mobile Control Platform (MCP) with Maestro Integration

A comprehensive platform for controlling Android devices and automating UI interactions. This project provides an improved version of the Android MCP with a modular structure, better error handling, and enhanced Jupyter Notebook integration.

## Features

- **Device Control**: Connect to and control multiple Android devices via ADB
- **UI Automation**: Create and execute Maestro flows for automated UI testing
- **Jupyter Integration**: Use the platform directly from Jupyter notebooks with magic commands
- **Menu System**: Interactive menu-based UI for terminal usage
- **Modular Design**: Well-organized code structure with separated components

## Prerequisites

- Python 3.8+
- ADB (Android Debug Bridge) installed and in PATH
- Connected Android device with USB debugging enabled
- Maestro CLI (optional, for UI automation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/android-mcp.git
cd android-mcp
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Maestro CLI (optional, for UI automation):
```bash
curl -Ls "https://get.maestro.mobile.dev" | bash
```

## Usage

### Command Line Interface

Run the Android MCP in interactive menu mode:

```bash
python android_mcp_jupyter.py
```

This will start the menu-based UI allowing you to:
- Select a connected device
- View device information
- Take screenshots
- Record and replay UI interactions
- Manage apps
- Execute shell commands
- And more...

### Jupyter Notebook

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Open the demo notebook `android_mcp_demo.ipynb` or create a new notebook

3. Import the Android MCP module:
```python
import android_mcp_jupyter as amc
```

4. Use the magic commands:
```python
%android_devices  # List connected devices
%android_screenshot  # Take a screenshot
```

5. Or use the API directly:
```python
# List devices
devices = amc.get_devices()

# Select a device
device_id = amc.select_device()

# Take a screenshot
amc.take_screenshot(device_id)

# Create a Maestro flow
actions = [
    amc.create_maestro_tap(text="Network & internet"),
    amc.create_maestro_input(text="hello"),
    "- wait: 2\n"
]
flow = amc.create_complete_flow("com.android.settings", actions)

# Execute the flow
amc.execute_maestro_flow(device_id)
```

## Project Structure

- `android_mcp/` - Main package directory
  - `__init__.py` - Package initialization
  - `config.py` - Configuration constants
  - `controller.py` - Android device controller
  - `ui.py` - Menu-based user interface
  - `utils.py` - Utility functions
- `android_mcp_jupyter.py` - Jupyter integration
- `android_mcp_demo.ipynb` - Demo Jupyter notebook
- `maestro_flows/` - Directory for storing Maestro flows

## Advanced Features

### Creating Custom Maestro Flows

```python
# Create a custom flow
with open("maestro_flows/custom_flow.yaml", "w") as f:
    f.write("""appId: com.android.settings
---
- launchApp
- tapOn:
    text: "Network & internet"
- wait: 1
- tapOn:
    text: "Wi-Fi"
- wait: 2
- pressBack
- wait: 1
- pressBack
""")

# Execute the custom flow
amc.execute_maestro_flow(device_id, "maestro_flows/custom_flow.yaml")
```

### Recording Maestro Flows

To record a Maestro flow, use the menu system:
1. Run `python android_mcp_jupyter.py`
2. Select a device
3. Navigate to "Maestro UI Automation"
4. Choose "Record new Maestro flow"
5. Interact with your device to record actions
6. Press Ctrl+C to stop recording

## Extending the Platform

The modular design makes it easy to extend the platform:

1. Add new commands by extending the `AndroidController` class in `controller.py`
2. Add new menu options by modifying the menu classes in `ui.py`
3. Add new Jupyter magic commands in `android_mcp_jupyter.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Maestro](https://maestro.mobile.dev/) for their excellent UI automation tool
- Android Debug Bridge (ADB) for device communication