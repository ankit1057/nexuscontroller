#!/bin/bash

echo "====================================="
echo "  NexusController Git Setup Script   "
echo "====================================="
echo

# Configure Git
git config --local user.name "ankit1057"
git config --local user.email "ankit1057@github.com"
echo "✅ Git user configured as ankit1057"

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

# Create .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/

# Virtual environments
venv/
ENV/
.env/
.venv/
.env

# IDE files
.idea/
.vscode/
*.swp
*.swo
.project
.pydevproject
.settings/

# Generated files
logs/
screenshots/
*.log
*.pot
*.pyc

# OS-specific files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOL

echo "✅ .gitignore file created"

# Create sample Maestro flow directory
mkdir -p maestro_flows
cat > maestro_flows/sample_flow.yaml << EOL
# Sample Maestro Flow for NexusController
# This flow demonstrates basic Maestro commands for Android automation

# Specify the app to test
appId: com.android.settings
---
# Launch the app
- launchApp

# Wait for the app to load
- wait: 1

# Tap on Network & internet
- tapOn:
    text: "Network & internet"

# Wait for navigation
- wait: 0.5

# Verify the Wi-Fi option is visible
- assertVisible:
    text: "Wi-Fi"

# Tap on Wi-Fi
- tapOn:
    text: "Wi-Fi"

# Wait for Wi-Fi settings to load
- wait: 1

# Go back
- pressBack

# Wait for transition
- wait: 0.5

# Go back to main settings
- pressBack
EOL

echo "✅ Sample Maestro flow created"

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: NexusController - Advanced Android Automation Platform"
echo "✅ Initial commit created"

echo
echo "====================================="
echo "  Publishing Instructions            "
echo "====================================="
echo
echo "To publish this repository to GitHub:"
echo
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo
echo "2. Push to GitHub with the following commands:"
echo "   git remote add origin https://github.com/ankit1057/nexuscontroller.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo
echo "====================================="
echo

# Optionally push to GitHub
read -p "Would you like to push to GitHub now? (y/n): " push_choice
if [[ "$push_choice" == "y" || "$push_choice" == "Y" ]]; then
    read -p "Enter GitHub repository name (default: nexuscontroller): " repo_name
    repo_name=${repo_name:-nexuscontroller}
    
    echo "Setting up remote and pushing to GitHub..."
    git remote add origin "https://github.com/ankit1057/${repo_name}.git"
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub: https://github.com/ankit1057/${repo_name}"
    else
        echo "❌ Failed to push to GitHub. Please check your internet connection and GitHub access."
        echo "   You can push manually later using the commands above."
    fi
fi

# Make this script executable
chmod +x setup_git.sh 