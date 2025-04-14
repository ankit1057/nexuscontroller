# Android MCP with Maestro Integration

This document explains how to use the Maestro integration features in the Android Mobile Control Panel (MCP).

## What is Maestro?

Maestro is a powerful UI testing framework for mobile apps that allows you to:
- Create and run UI tests with a simple YAML syntax
- Record UI interactions and replay them
- Run tests in parallel across multiple devices
- Inspect UI elements with Maestro Studio

## Installation

To use the Maestro integration features, you need to install Maestro:

```bash
# Install Maestro
curl -Ls "https://get.maestro.mobile.dev" | bash
```

After installation, make sure to add Maestro to your PATH.

## Features

The Android MCP with Maestro Integration provides the following UI automation features:

### 1. Creating and Running Maestro Flows

You can create Maestro flows by adding UI actions step by step:
- Launch an app
- Tap on elements (by text, ID, or coordinates)
- Input text
- Swipe
- Wait
- Press back button
- Assert elements are visible

Once you've created a flow, you can run it on your device.

### 2. Recording and Replaying

You can record your interactions with the device and save them as a Maestro flow:
- Record a new flow
- Run a previously recorded flow

### 3. UI Inspection

Launch Maestro Studio to inspect UI elements on your device and get their properties.

## Example Workflow

1. Connect your Android device
2. Launch the MCP with Maestro Integration
3. Create a new Maestro flow
4. Add actions to the flow (e.g., launch app, tap on elements, input text)
5. Run the flow on your device
6. Alternatively, record a flow and replay it later

## Maestro YAML Syntax

Maestro uses a simple YAML syntax for defining UI tests. Here are some examples:

### Launch an app
```yaml
appId: com.example.app
---
- launchApp
```

### Tap on an element by text
```yaml
- tapOn:
    text: "Login"
```

### Input text
```yaml
- inputText:
    text: "username"
    id: "username_field"
```

### Swipe
```yaml
- swipe:
    start: "500,1500"
    end: "500,500"
```

### Wait
```yaml
- wait: 2
```

### Assert element is visible
```yaml
- assertVisible:
    text: "Welcome"
```

## Troubleshooting

If you encounter issues with Maestro:

1. Make sure Maestro is installed and in your PATH
2. Check that your device is properly connected and authorized
3. Try running `maestro --version` to verify the installation
4. For more help, visit the [Maestro documentation](https://maestro.mobile.dev/)