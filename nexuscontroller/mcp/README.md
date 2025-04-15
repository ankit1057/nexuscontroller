# NexusController MCP Server

The Model Context Protocol (MCP) server component of NexusController allows you to control Android devices using AI assistants and other tools that support the MCP protocol.

## Installation

To use the MCP server, install NexusController with the MCP extras:

```bash
pip install 'nexuscontroller[mcp]'
```

## Running the MCP Server

You can run the MCP server in several ways:

### 1. Using the module directly:

```bash
python -m nexuscontroller.mcp
```

### 2. Using the command-line script:

After installation, the `nexus-mcp` command will be available:

```bash
nexus-mcp
```

### 3. Using the starter script:

If you've cloned the repository, you can use the included starter script:

```bash
./start_mcp_server.py
```

### Command-line options

All methods support the following options:

- `--install-deps`: Install required dependencies
- `--debug`: Enable debug logging

## Integration with AI Tools

To use NexusController with AI assistants, configure your MCP client to use the NexusController server:

```json
{
  "mcpServers": {
    "nexuscontroller": {
      "command": "python3",
      "args": ["-m", "nexuscontroller.mcp"],
      "transport": "stdio"
    }
  }
}
```

## Available Tools

The MCP server provides the following tools:

- `list_available_devices`: List all connected Android devices
- `use_device`: Select a device to use
- `take_screenshot`: Take a screenshot of the current device
- `list_apps`: List all installed apps on the device
- `launch_app`: Launch an app on the device
- `terminate_app`: Terminate an app on the device
- `get_screen_size`: Get the screen dimensions of the device
- `click_on_screen_at_coordinates`: Tap at specific coordinates
- `swipe_on_screen`: Swipe in a specified direction
- `type_keys`: Type text into the device
- `press_button`: Press a hardware or system button
- `open_url`: Open a URL in the default browser
- `list_elements_on_screen`: List UI elements visible on screen

## Troubleshooting

If you encounter issues:

1. Make sure ADB is installed and in your PATH
2. Ensure your device is connected and authorized for debugging
3. Try running with `--debug` for more detailed logs
4. If dependencies are missing, run with `--install-deps` 