#!/bin/bash

echo "====================================="
echo "  Android MCP Installation Script    "
echo "====================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

python_version=$(python3 --version)
echo "✅ Found $python_version"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip and try again."
    exit 1
fi

pip_version=$(pip3 --version)
echo "✅ Found $pip_version"

# Check if virtualenv is available
create_venv=false
if ! command -v virtualenv &> /dev/null; then
    echo "⚠️ virtualenv is not installed. Installing virtualenv..."
    pip3 install virtualenv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install virtualenv. Continuing without virtual environment."
    else
        create_venv=true
        echo "✅ virtualenv installed"
    fi
else
    create_venv=true
    echo "✅ Found virtualenv"
fi

# Create and activate virtual environment
if [ "$create_venv" = true ]; then
    echo "Creating virtual environment..."
    virtualenv venv
    
    # Activate virtual environment
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Failed to activate virtual environment. Continuing without it."
    else
        echo "✅ Virtual environment created and activated"
    fi
fi

# Install required packages
echo "Installing required packages..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install some packages. Please check the error messages above."
    exit 1
fi
echo "✅ Required packages installed"

# Check if ADB is installed
if ! command -v adb &> /dev/null; then
    echo "⚠️ ADB is not installed or not in PATH."
    echo "Android MCP requires ADB to interact with Android devices."
    echo "Please install Android SDK Platform Tools and make sure adb is in your PATH."
    echo "You can download it from: https://developer.android.com/studio/releases/platform-tools"
else
    adb_version=$(adb version | head -n 1)
    echo "✅ Found $adb_version"
fi

# Install the Android MCP package in development mode
echo "Installing Android MCP in development mode..."
pip3 install -e .
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Android MCP package. Please check the error messages above."
    exit 1
fi
echo "✅ Android MCP installed in development mode"

# Check for Maestro
if ! command -v maestro &> /dev/null; then
    echo "⚠️ Maestro CLI is not installed or not in PATH."
    echo "Some UI automation features will not be available."
    echo "To install Maestro CLI, run:"
    echo "curl -Ls \"https://get.maestro.mobile.dev\" | bash"
else
    maestro_version=$(maestro --version)
    echo "✅ Found Maestro CLI $maestro_version"
fi

# Create necessary directories
mkdir -p maestro_flows
echo "✅ Created maestro_flows directory"

echo ""
echo "====================================="
echo "  Installation Complete              "
echo "====================================="
echo ""
echo "You can now use Android MCP:"
echo ""
echo "1. Run the test script to verify installation:"
echo "   python3 test_android_mcp.py"
echo ""
echo "2. Run the UI mode:"
echo "   python3 android_mcp_jupyter.py"
echo ""
echo "3. Start Jupyter Notebook for interactive usage:"
echo "   jupyter notebook android_mcp_demo.ipynb"
echo ""
echo "====================================="

# Make the script executable
chmod +x install.sh 