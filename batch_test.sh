#!/bin/bash

# Batch Testing Script for NexusControl
# This script runs multiple Maestro flows in sequence or parallel

echo "====================================="
echo "    NexusControl Batch Testing      "
echo "====================================="

# Directory containing test flows
FLOW_DIR="$HOME/Desktop/NexusControl/flows"

# Create flows directory if it doesn't exist
mkdir -p "$FLOW_DIR"

# Function to run a single test
run_test() {
    local flow_file="$1"
    local device_id="$2"
    
    echo "Running test: $flow_file on device: $device_id"
    
    if [ -n "$device_id" ]; then
        maestro test --device "$device_id" "$flow_file"
    else
        maestro test "$flow_file"
    fi
    
    local result=$?
    if [ $result -eq 0 ]; then
        echo "✅ Test passed: $flow_file"
    else
        echo "❌ Test failed: $flow_file"
    fi
    
    return $result
}

# Function to run all tests in a directory
run_all_tests() {
    local device_id="$1"
    local failed_tests=()
    local passed_tests=()
    
    echo "Running all tests in $FLOW_DIR"
    
    for flow_file in "$FLOW_DIR"/*.yaml; do
        if [ -f "$flow_file" ]; then
            run_test "$flow_file" "$device_id"
            if [ $? -eq 0 ]; then
                passed_tests+=("$(basename "$flow_file")")
            else
                failed_tests+=("$(basename "$flow_file")")
            fi
            echo "-----------------------------------"
        fi
    done
    
    echo "====================================="
    echo "           Test Summary             "
    echo "====================================="
    echo "Passed: ${#passed_tests[@]} tests"
    echo "Failed: ${#failed_tests[@]} tests"
    
    if [ ${#passed_tests[@]} -gt 0 ]; then
        echo ""
        echo "Passed tests:"
        for test in "${passed_tests[@]}"; do
            echo "  ✅ $test"
        done
    fi
    
    if [ ${#failed_tests[@]} -gt 0 ]; then
        echo ""
        echo "Failed tests:"
        for test in "${failed_tests[@]}"; do
            echo "  ❌ $test"
        done
        return 1
    fi
    
    return 0
}

# Function to run tests in parallel
run_parallel_tests() {
    local num_devices="$1"
    
    echo "Running tests in parallel on $num_devices devices"
    
    # Get list of connected devices
    local devices=($(adb devices | grep -v "List" | grep "device$" | cut -f1))
    
    if [ ${#devices[@]} -lt $num_devices ]; then
        echo "Warning: Requested $num_devices devices but only ${#devices[@]} are connected"
        num_devices=${#devices[@]}
    fi
    
    if [ $num_devices -eq 0 ]; then
        echo "No devices connected. Exiting."
        exit 1
    fi
    
    # Run tests with concurrency
    maestro test -c $num_devices "$FLOW_DIR"/*.yaml
    
    local result=$?
    if [ $result -eq 0 ]; then
        echo "✅ All parallel tests passed"
    else
        echo "❌ Some parallel tests failed"
    fi
    
    return $result
}

# Main menu
while true; do
    echo ""
    echo "Select an option:"
    echo "1. Run a specific test"
    echo "2. Run all tests sequentially"
    echo "3. Run tests in parallel"
    echo "4. Create a new test flow"
    echo "0. Exit"
    echo ""
    
    read -p "Enter your choice: " choice
    
    case $choice in
        1)
            # List available tests
            echo "Available tests:"
            ls -1 "$FLOW_DIR"/*.yaml 2>/dev/null || echo "No test flows found in $FLOW_DIR"
            
            read -p "Enter test file path: " flow_file
            
            # Get list of connected devices
            devices=($(adb devices | grep -v "List" | grep "device$" | cut -f1))
            
            if [ ${#devices[@]} -gt 1 ]; then
                echo "Available devices:"
                for i in "${!devices[@]}"; do
                    echo "$((i+1)). ${devices[$i]}"
                done
                
                read -p "Select device number (or 0 for default): " device_num
                
                if [ "$device_num" -gt 0 ] && [ "$device_num" -le "${#devices[@]}" ]; then
                    device_id="${devices[$((device_num-1))]}"
                else
                    device_id=""
                fi
            else
                device_id=""
            fi
            
            run_test "$flow_file" "$device_id"
            ;;
        2)
            # Get list of connected devices
            devices=($(adb devices | grep -v "List" | grep "device$" | cut -f1))
            
            if [ ${#devices[@]} -gt 1 ]; then
                echo "Available devices:"
                for i in "${!devices[@]}"; do
                    echo "$((i+1)). ${devices[$i]}"
                done
                
                read -p "Select device number (or 0 for default): " device_num
                
                if [ "$device_num" -gt 0 ] && [ "$device_num" -le "${#devices[@]}" ]; then
                    device_id="${devices[$((device_num-1))]}"
                else
                    device_id=""
                fi
            else
                device_id=""
            fi
            
            run_all_tests "$device_id"
            ;;
        3)
            read -p "Enter number of devices to use for parallel testing: " num_devices
            run_parallel_tests "$num_devices"
            ;;
        4)
            read -p "Enter name for new test flow (without .yaml extension): " flow_name
            
            if [ -z "$flow_name" ]; then
                echo "Invalid name. Please try again."
                continue
            fi
            
            flow_file="$FLOW_DIR/${flow_name}.yaml"
            
            if [ -f "$flow_file" ]; then
                read -p "File already exists. Overwrite? (y/n): " overwrite
                if [ "$overwrite" != "y" ]; then
                    continue
                fi
            fi
            
            read -p "Enter app package ID: " app_id
            
            # Create basic flow template
            cat > "$flow_file" << EOL
# Maestro Flow: $flow_name
# Created: $(date)

appId: $app_id
---
- launchApp
- wait: 2

# Add your test steps here
# Example:
# - tapOn:
#     text: "Login"
# - inputText:
#     text: "username"
#     id: "username_field"
EOL
            
            echo "✅ Created new test flow: $flow_file"
            echo "Edit this file to add your test steps."
            ;;
        0)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done