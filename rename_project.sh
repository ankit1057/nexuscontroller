#!/bin/bash
# Rename script for NexusController project
# This script renames the project from android_mcp to nexuscontroller

echo "=================================="
echo "  NexusController Rename Utility  "
echo "=================================="
echo

# Create new package directory
mkdir -p nexuscontroller

# Copy files from old to new package
echo "Copying module files..."
cp -r android_mcp/* nexuscontroller/

# Update imports in Python files
echo "Updating imports in Python files..."
find . -name "*.py" -type f -exec sed -i 's/from android_mcp/from nexuscontroller/g' {} \;
find . -name "*.py" -type f -exec sed -i 's/import android_mcp/import nexuscontroller/g' {} \;

# Rename main entry point
echo "Renaming main entry point..."
cp android_mcp_jupyter.py nexuscontroller_cli.py
sed -i 's/from android_mcp/from nexuscontroller/g' nexuscontroller_cli.py

# Update setup.py
echo "Updating setup.py..."
sed -i 's/android_mcp_jupyter:run_ui_mode/nexuscontroller_cli:run_ui_mode/g' setup.py

# Update tests
echo "Updating tests..."
find tests -name "*.py" -type f -exec sed -i 's/import android_mcp/import nexuscontroller/g' {} \;
find tests -name "*.py" -type f -exec sed -i 's/from android_mcp/from nexuscontroller/g' {} \;

echo "✅ Project successfully renamed!"
echo "You can now run 'pip install -e .' to install the renamed package."
echo
echo "NOTE: You may still need to manually review some files for remaining references."
echo "      After testing, you can safely remove the android_mcp directory."

# Make script executable
chmod +x rename_project.sh 