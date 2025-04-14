#!/bin/bash

# NexusControl Environment Setup Script

echo "====================================="
echo "  NexusControl Environment Setup     "
echo "====================================="
echo ""

# Script directory
SCRIPT_DIR="$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

echo "✅ Python $(python3 --version) found"

# Function to install uv if not present
install_uv() {
    # Check if uv is available
    if command -v uv &> /dev/null; then
        echo "✅ uv is already installed"
        return 0
    else
        echo "🔄 Installing uv..."
        
        # Try to install using curl (preferred method)
        if command -v curl &> /dev/null; then
            echo "Installing uv using curl..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            
            # Update PATH to include uv
            if [ -f "$HOME/.cargo/env" ]; then
                source "$HOME/.cargo/env"
            fi
            
            # Add to PATH temporarily if uv is not in PATH but exists
            if [ -f "$HOME/.cargo/bin/uv" ] && ! command -v uv &> /dev/null; then
                export PATH="$HOME/.cargo/bin:$PATH"
            fi
        else
            # Fallback to pip if curl is not available
            if command -v pip3 &> /dev/null; then
                pip3 install -U uv
            elif command -v pip &> /dev/null; then
                pip install -U uv
            else
                echo "❌ Neither curl nor pip is available to install uv."
                return 1
            fi
        fi
    fi
    
    # Verify uv installation
    if command -v uv &> /dev/null; then
        echo "✅ uv $(uv --version) installed successfully"
        return 0
    else
        echo "❌ Failed to install uv"
        return 1
    fi
}

# Function to setup using modern uv approach (pyproject.toml)
setup_with_uv_modern() {
    echo "📦 Setting up project with uv and pyproject.toml (modern approach)..."
    
    # Check if we have pyproject.toml
    if [ ! -f "$SCRIPT_DIR/pyproject.toml" ]; then
        echo "❌ pyproject.toml not found, cannot use modern approach"
        return 1
    fi
    
    # Use uv to create project and install dependencies
    cd "$SCRIPT_DIR"
    
    # If venv already exists, use sync, otherwise do a full setup
    if [ -d "$SCRIPT_DIR/.venv" ]; then
        echo "🔄 Synchronizing existing environment with uv..."
        uv sync
    else
        echo "🔄 Setting up new environment with uv..."
        uv venv
        uv pip install -e .
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ Modern uv setup completed successfully!"
        return 0
    else
        echo "❌ Modern uv setup failed"
        return 1
    fi
}

# Function to setup using uv with requirements.txt (traditional approach)
setup_with_uv_traditional() {
    echo "📦 Setting up project with uv and requirements.txt (traditional approach)..."
    
    # Check if we have requirements.txt
    if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
        echo "❌ requirements.txt not found, cannot use traditional approach"
        return 1
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$SCRIPT_DIR/.venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv "$SCRIPT_DIR/.venv"
    fi
    
    # Use uv to install requirements
    cd "$SCRIPT_DIR"
    uv pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Traditional uv setup completed successfully!"
        return 0
    else
        echo "❌ Traditional uv setup failed"
        return 1
    fi
}

# Function to setup using pip (fallback)
setup_with_pip() {
    echo "📦 Setting up project with pip (fallback approach)..."
    
    # Check if we have requirements.txt
    if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
        echo "❌ requirements.txt not found, cannot use pip"
        return 1
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$SCRIPT_DIR/.venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv "$SCRIPT_DIR/.venv"
    fi
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source "$SCRIPT_DIR/.venv/Scripts/activate" 2>/dev/null
    else
        # Unix/macOS
        source "$SCRIPT_DIR/.venv/bin/activate" 2>/dev/null
    fi
    
    # Install requirements
    pip install -r "$SCRIPT_DIR/requirements.txt"
    
    if [ $? -eq 0 ]; then
        echo "✅ Pip setup completed successfully!"
        return 0
    else
        echo "❌ Pip setup failed"
        return 1
    fi
}

# Main installation logic
echo "Checking for UV package manager..."
install_uv

# Try different approaches in order of preference
if command -v uv &> /dev/null; then
    # If uv is available, try modern approach first
    setup_with_uv_modern || setup_with_uv_traditional || setup_with_pip
else
    # If uv is not available, fall back to pip
    setup_with_pip
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Environment setup complete!"
    echo "📱 You can now run NexusControl using:"
    echo "    ./launch_nexuscontrol.sh"
    echo ""
    exit 0
else
    echo ""
    echo "❌ Failed to set up environment using any method."
    echo "Please check the error messages above and try to resolve the issues manually."
    echo ""
    exit 1
fi 