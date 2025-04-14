# NexusController - Advanced Android Automation Platform

NexusController is a comprehensive and professional-grade Android device automation platform that bridges the gap between manual testing and continuous integration. Built for QA engineers, developers, and DevOps professionals, NexusController provides a unified solution for Android device control, UI automation, and test orchestration.

## Key Features

- **Universal Device Control**: Connect to and manage multiple Android devices simultaneously via ADB with robust error handling and device state management
- **Intelligent UI Automation**: Create, record, and execute Maestro flows for reliable UI testing that survives app updates and device variations
- **Jupyter Integration**: Leverage interactive Python notebooks for exploratory testing, automation script development, and results analysis
- **CI/CD Ready**: Integrate with your continuous integration pipeline through command-line tools and GitHub Actions workflows
- **Enterprise Scalability**: Extensible architecture designed for large-scale deployments across multiple testing environments
- **Comprehensive Reporting**: Generate detailed HTML reports with screenshots, error logs, and performance metrics

## Why NexusController?

- **Reliability**: Built with robust error detection, recovery mechanisms, and logging to handle real-world testing scenarios
- **Flexibility**: Works with any Android app or device without requiring code modifications or instrumentation
- **Productivity**: Interactive menus, intuitive Jupyter interface, and reusable components accelerate test development
- **Enterprise Ready**: Designed with security, scalability and commercial deployment requirements in mind
- **Developer-Focused**: Clear documentation, modular architecture, and extensible design make it easy to adapt to your needs

## Prerequisites

- Python 3.8+
- ADB (Android Debug Bridge) installed and in PATH
- Connected Android device with USB debugging enabled
- Maestro CLI (optional, for enhanced UI automation)

## Quick Start

1. **Installation**:
```bash
pip install nexuscontroller
```

2. **Basic Usage**:
```python
from nexuscontroller import NexusController

# Initialize controller
controller = NexusController()

# List connected devices
devices = controller.get_devices()

# Take a screenshot
controller.take_screenshot(devices[0])

# Run a UI test
controller.run_maestro_flow(devices[0], "flows/login_test.yaml")
```

3. **Interactive Mode**:
```bash
python -m nexuscontroller
```

## Commercial Use

NexusController is available under MIT license with special provisions for commercial use by large enterprises. See the [LICENSE](LICENSE) file for details.

## Documentation

For full documentation, examples, and API reference, visit our [documentation site](https://github.com/ankit1057/nexuscontroller).

## AI Integration

NexusController is designed to work seamlessly with AI assistants like Claude, GPT, and other AI agents. You can integrate NexusController with your AI tools to automate mobile testing and device control.

For integration details, see [AI_INTEGRATION.md](AI_INTEGRATION.md).

### Quick Integration Example

```json
// mcp.json configuration for AI assistants
{
  "mcpServers": {
    "nexuscontroller": {
      "command": "python3",
      "args": ["start_mcp_server.py"],
      "transport": "stdio"
    }
  }
}
```

## Contributing

We welcome contributions from the community! Here's how you can help:

1. **Code Contributions**:
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/amazing-feature`)
   - Commit your changes (`git commit -m 'Add amazing feature'`)
   - Push to the branch (`git push origin feature/amazing-feature`)
   - Open a Pull Request

2. **Bug Reports & Feature Requests**:
   - Use the GitHub issue tracker
   - Provide detailed information for bugs (steps to reproduce, logs, environment)
   - For feature requests, explain the use case and benefits

3. **Documentation**:
   - Help improve docs, examples, and tutorials
   - Submit corrections for typos or unclear instructions

4. **Share Your Experience**:
   - Write blog posts or tutorials about NexusController
   - Share your use cases and success stories

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ankit1057/nexuscontroller.git
cd nexuscontroller

# Set up development environment
pip install -e '.[dev]'

# Run tests
pytest
```

## Acknowledgments

- Created and maintained by [ankit1057](https://github.com/ankit1057)
- Powered by [Maestro](https://maestro.mobile.dev/) for UI automation
- Inspired by the mobile testing needs of enterprise app development teams
- Special thanks to all contributors who help make this project better