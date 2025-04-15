#!/bin/bash

# NexusController Launcher Script

# Script directory
SCRIPT_DIR="$(dirname "$0")"

# Check if dependencies are installed
check_dependencies() {
    # Check if we're in a virtual environment
    if [[ -z "$VIRTUAL_ENV" ]]; then
        # Try to activate the virtual environment
        if [[ -d "$SCRIPT_DIR/.venv" ]]; then
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
                # Windows
                source "$SCRIPT_DIR/.venv/Scripts/activate" 2>/dev/null
            else
                # Unix/macOS
                source "$SCRIPT_DIR/.venv/bin/activate" 2>/dev/null
            fi
        fi
    fi
    
    # Check if key packages are installed
    if ! python3 -c "import sys; sys.exit(0 if all(pkg in sys.modules or __import__(pkg, fromlist=['']) for pkg in ['subprocess', 'os', 'sys', 'time']) else 1)" 2>/dev/null; then
        return 1
    fi
    
    return 0
}

# Function to setup environment
setup_environment() {
    echo "Would you like to set up the environment now? (y/n)"
    read -p "> " setup_choice
    
    if [[ "$setup_choice" == "y" || "$setup_choice" == "Y" ]]; then
        echo "Setting up environment..."
        if [[ -f "$SCRIPT_DIR/setup_environment.sh" ]]; then
            bash "$SCRIPT_DIR/setup_environment.sh"
            if [ $? -eq 0 ]; then
                echo "Environment setup complete."
                return 0
            else
                echo "Environment setup failed."
                return 1
            fi
        else
            echo "❌ Setup script not found. Please ensure setup_environment.sh exists."
            return 1
        fi
    else
        echo "Skipping environment setup."
        return 1
    fi
}

# Check dependencies or offer to set them up
if ! check_dependencies; then
    echo "⚠️ Required dependencies are not installed or environment is not set up."
    if ! setup_environment; then
        echo "❌ Cannot continue without proper environment setup."
        exit 1
    fi
    # Try once more after setup
    if ! check_dependencies; then
        echo "❌ Still missing required dependencies. Please fix the environment manually."
        exit 1
    fi
fi

echo "====================================="
echo "      NexusController Platform       "
echo "====================================="
echo ""
echo "Please select a version to launch:"
echo "1. CLI Mode - Command Line Interface"
echo "2. MCP Server - Model Context Protocol server"
echo "3. Jupyter Integration"
echo "4. Setup/Update Environment"
echo "0. Exit"
echo ""

read -p "Enter your choice: " choice

case $choice in
    1)
        echo "Launching NexusController CLI Mode..."
        python3 "$SCRIPT_DIR/nexuscontroller_cli.py"
        ;;
    2)
        echo "Launching NexusController MCP Server..."
        python3 "$SCRIPT_DIR/start_mcp_server.py"
        ;;
    3)
        echo "Launching NexusController Jupyter Integration..."
        # Check if jupyter is installed
        if ! command -v jupyter &> /dev/null; then
            echo "❌ Jupyter not found. Installing..."
            pip install jupyter
        fi
        jupyter notebook "$SCRIPT_DIR/android_mcp_jupyter.ipynb"
        ;;
    4)
        echo "Setting up environment..."
        bash "$SCRIPT_DIR/setup_environment.sh"
        ;;
    0)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac 