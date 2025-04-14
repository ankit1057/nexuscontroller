#!/bin/bash

echo "====================================="
echo "  Android MCP Git Setup Script       "
echo "====================================="
echo ""

# Set Git username and email
git config --local user.name "ankit1057"
git config --local user.email "ankit1057@users.noreply.github.com"
echo "✅ Git user configured as ankit1057"

# Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

# Create .gitignore file
cat > .gitignore << EOL
# Python bytecode
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Virtual environments
.env
.venv
env/
venv/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# IDE files
.idea/
.vscode/

# Generated files
screenshots_*/
*.log
maestro_flows/*.yaml
!maestro_flows/sample_flow.yaml

# macOS
.DS_Store
EOL
echo "✅ .gitignore file created"

# Create sample Maestro flow
mkdir -p maestro_flows
cat > maestro_flows/sample_flow.yaml << EOL
# Sample Maestro Flow for Android MCP
# This flow demonstrates basic Maestro commands

# Specify the app to test
appId: com.android.settings
---
# Launch the app
- launchApp

# Wait for 1 second
- wait: 1

# Tap on "Network & internet"
- tapOn:
    text: "Network & internet"

# Wait for 0.5 seconds
- wait: 0.5

# Tap on "Wi-Fi"
- tapOn:
    text: "Wi-Fi"

# Wait for 1 second
- wait: 1

# Go back
- pressBack

# Wait for 0.5 seconds
- wait: 0.5

# Go back again to return to the main settings
- pressBack
EOL
echo "✅ Sample Maestro flow created"

# Add files to Git
git add .
echo "✅ Files added to Git"

# Create initial commit
git commit -m "Initial commit: Android Mobile Control Platform (MCP) with Maestro Integration"
echo "✅ Initial commit created"

# Instructions for publishing
echo ""
echo "====================================="
echo "  Publishing Instructions            "
echo "====================================="
echo ""
echo "To publish this repository to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Push to GitHub with the following commands:"
echo "   git remote add origin https://github.com/ankit1057/android-mcp.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "====================================="

# Make the script executable
chmod +x setup_git.sh 