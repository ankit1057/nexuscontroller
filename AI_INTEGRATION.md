# NexusController AI Agent Integration Guide

NexusController is designed to work seamlessly with AI agents and copilots. This guide explains how to integrate NexusController with various AI platforms for automated mobile testing and device control.

## Table of Contents
- [Overview](#overview)
- [Integration with AI Assistants](#integration-with-ai-assistants)
- [MCP Configuration for AI Agents](#mcp-configuration-for-ai-agents)
- [Example: Claude Integration](#example-claude-integration)
- [Example: GPT Integration](#example-gpt-integration)
- [Contributing](#contributing)

## Overview

NexusController provides a Mobile Control Protocol (MCP) interface that allows AI agents to:

1. Discover connected Android devices
2. Take screenshots and analyze screen content
3. Control devices through taps, swipes, and text input
4. Execute automated test flows
5. Install, launch, and manage applications

## Integration with AI Assistants

AI assistants can be integrated with NexusController using the Mobile Control Protocol (MCP). This protocol allows the AI to interact with Android devices programmatically and perform actions based on user requests.

### Requirements

- NexusController installed and running
- A configuration file (mcp.json) for the AI platform
- The AI agent must have tool-calling capabilities

## MCP Configuration for AI Agents

To integrate an AI agent with NexusController, you'll need to create an MCP configuration. Below is a sample `mcp.json` configuration file:

```json
{
  "mcpServers": {
    "nexuscontroller": {
      "command": "python3",
      "args": ["/path/to/nexuscontroller/start_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/nexuscontroller"
      },
      "cwd": "/path/to/nexuscontroller",
      "transport": "stdio"
    }
  },
  "modelContext": {
    "version": "1.0",
    "protocols": {
      "mcp": {
        "tools": [
          {
            "name": "list_available_devices",
            "description": "List all available devices. This includes both physical devices and simulators.",
            "parameters": []
          },
          {
            "name": "use_device",
            "description": "Select a device to use for testing.",
            "parameters": [
              {
                "name": "device",
                "type": "string",
                "description": "The ID of the device to select"
              },
              {
                "name": "deviceType",
                "type": "string",
                "enum": ["android"],
                "description": "The type of device to select"
              }
            ]
          },
          {
            "name": "take_screenshot",
            "description": "Take a screenshot of the mobile device.",
            "parameters": []
          },
          // Add other tools as needed
        ]
      }
    }
  }
}
```

### Steps to Add MCP Configuration for AI Agents

1. **Create the MCP Configuration File**:
   - Create a file named `mcp.json` using the template above
   - Modify the paths to match your NexusController installation
   - Add or remove tools based on your requirements

2. **Configure the AI Platform**:
   - For Anthropic Claude: Upload the `mcp.json` file to the AI system settings
   - For OpenAI GPT: Include the MCP configuration in your API calls
   - For other platforms: Refer to the platform's documentation on tool integration

3. **Test the Integration**:
   - Ask the AI assistant to perform basic operations like listing devices
   - Verify that the assistant can take screenshots and control the device
   - Test more complex workflows like UI testing

## Example: Claude Integration

To integrate NexusController with Claude:

1. Upload your `mcp.json` to Claude's system settings
2. Grant Claude permissions to use the MCP interface
3. Ask Claude to perform mobile testing tasks, such as:
   - "List available Android devices"
   - "Take a screenshot of the connected device"
   - "Open the Settings app and navigate to Wi-Fi settings"

## Example: GPT Integration

To integrate NexusController with GPT:

1. Include the MCP configuration in your API calls
2. Set up the necessary environment for executing the MCP server
3. Create prompts that instruct GPT to use the MCP tools for mobile testing

## Contributing

We welcome contributions to enhance NexusController's AI integration capabilities. Here's how you can contribute:

1. **Add Support for New AI Platforms**:
   - Create MCP configurations for additional AI systems
   - Document the integration process

2. **Enhance Existing Integrations**:
   - Improve the MCP tool definitions
   - Add new capabilities or tools

3. **Share Your Use Cases**:
   - Document how you're using NexusController with AI agents
   - Provide feedback on the integration experience

To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/ai-integration`)
3. Commit your changes (`git commit -am 'Add support for new AI platform'`)
4. Push to the branch (`git push origin feature/ai-integration`)
5. Create a new Pull Request

---

If you have questions or need assistance with AI integration, please open an issue on our GitHub repository or contact us at github.com/ankit1057. 