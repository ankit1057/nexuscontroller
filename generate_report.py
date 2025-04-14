#!/usr/bin/env python3
"""
Maestro Test Report Generator
This script generates HTML reports from Maestro test results
"""

import os
import sys
import json
import glob
import time
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

def run_maestro_test(flow_file, device_id=None):
    """Run a Maestro test and capture the output"""
    print(f"Running test: {flow_file}")
    
    cmd = ["maestro", "test", flow_file]
    if device_id:
        cmd.extend(["--device", device_id])
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end_time = time.time()
    
    return {
        "flow_file": flow_file,
        "success": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr,
        "duration": end_time - start_time
    }

def parse_test_results(test_results):
    """Parse test results to extract key information"""
    parsed_results = []
    
    for result in test_results:
        # Extract screenshots
        screenshots = []
        for line in result["output"].splitlines():
            if "Screenshot saved to" in line:
                screenshot_path = line.split("Screenshot saved to")[-1].strip()
                if os.path.exists(screenshot_path):
                    screenshots.append(screenshot_path)
        
        # Extract errors
        errors = []
        if not result["success"]:
            for line in result["error"].splitlines():
                if "Error:" in line or "Failed:" in line:
                    errors.append(line.strip())
        
        # Extract app package
        app_package = "Unknown"
        for line in result["output"].splitlines():
            if "appId:" in line:
                app_package = line.split("appId:")[-1].strip()
                break
        
        parsed_results.append({
            "flow_file": result["flow_file"],
            "app_package": app_package,
            "success": result["success"],
            "duration": result["duration"],
            "screenshots": screenshots,
            "errors": errors
        })
    
    return parsed_results

def generate_html_report(parsed_results, output_dir):
    """Generate an HTML report from parsed test results"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_file = os.path.join(output_dir, f"report_{int(time.time())}.html")
    
    # Copy screenshots to report directory
    screenshot_dir = os.path.join(output_dir, "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    for result in parsed_results:
        for i, screenshot in enumerate(result["screenshots"]):
            test_name = os.path.basename(result["flow_file"]).replace(".yaml", "")
            new_screenshot = os.path.join(
                screenshot_dir, 
                f"{test_name}_screenshot_{i+1}.png"
            )
            try:
                with open(screenshot, "rb") as src, open(new_screenshot, "wb") as dst:
                    dst.write(src.read())
                # Update path in results
                result["screenshots"][i] = os.path.relpath(new_screenshot, output_dir)
            except Exception as e:
                print(f"Error copying screenshot: {e}")
    
    # Calculate summary statistics
    total_tests = len(parsed_results)
    passed_tests = sum(1 for r in parsed_results if r["success"])
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    total_duration = sum(r["duration"] for r in parsed_results)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexusControl - Maestro Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .header {{
            background-color: #3498db;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .summary {{
            display: flex;
            justify-content: space-between;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .summary-item {{
            text-align: center;
        }}
        .summary-value {{
            font-size: 24px;
            font-weight: bold;
        }}
        .test-card {{
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .test-title {{
            font-size: 18px;
            font-weight: bold;
        }}
        .success {{
            color: #27ae60;
        }}
        .failure {{
            color: #e74c3c;
        }}
        .screenshots {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}
        .screenshot {{
            max-width: 200px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }}
        .error-list {{
            background-color: #ffecec;
            border-left: 4px solid #e74c3c;
            padding: 10px;
            margin-top: 10px;
        }}
        .progress-bar {{
            height: 20px;
            background-color: #ecf0f1;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .progress {{
            height: 100%;
            background-color: #27ae60;
            border-radius: 10px;
            width: {success_rate}%;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>NexusControl - Maestro Test Report</h1>
        <p>Generated on: {report_time}</p>
    </div>
    
    <div class="progress-bar">
        <div class="progress"></div>
    </div>
    
    <div class="summary">
        <div class="summary-item">
            <div class="summary-value">{total_tests}</div>
            <div>Total Tests</div>
        </div>
        <div class="summary-item">
            <div class="summary-value success">{passed_tests}</div>
            <div>Passed</div>
        </div>
        <div class="summary-item">
            <div class="summary-value failure">{failed_tests}</div>
            <div>Failed</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">{success_rate:.1f}%</div>
            <div>Success Rate</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">{total_duration:.1f}s</div>
            <div>Total Duration</div>
        </div>
    </div>
    
    <h2>Test Results</h2>
"""
    
    # Add test results
    for result in parsed_results:
        test_name = os.path.basename(result["flow_file"]).replace(".yaml", "")
        status_class = "success" if result["success"] else "failure"
        status_text = "PASSED" if result["success"] else "FAILED"
        
        html += f"""
    <div class="test-card">
        <div class="test-header">
            <div class="test-title">{test_name}</div>
            <div class="{status_class}">{status_text}</div>
        </div>
        <div>
            <strong>App Package:</strong> {result["app_package"]}
        </div>
        <div>
            <strong>Duration:</strong> {result["duration"]:.2f} seconds
        </div>
"""
        
        if result["screenshots"]:
            html += f"""
        <div>
            <strong>Screenshots:</strong>
            <div class="screenshots">
"""
            for screenshot in result["screenshots"]:
                html += f"""
                <img src="{screenshot}" class="screenshot" alt="Test Screenshot">
"""
            html += """
            </div>
        </div>
"""
        
        if result["errors"]:
            html += f"""
        <div>
            <strong>Errors:</strong>
            <div class="error-list">
                <ul>
"""
            for error in result["errors"]:
                html += f"""
                    <li>{error}</li>
"""
            html += """
                </ul>
            </div>
        </div>
"""
        
        html += """
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    with open(report_file, "w") as f:
        f.write(html)
    
    print(f"Report generated: {report_file}")
    return report_file

def main():
    parser = argparse.ArgumentParser(description="Generate HTML reports from Maestro test results")
    parser.add_argument("--flows", "-f", help="Directory containing Maestro flow files", default="flows")
    parser.add_argument("--output", "-o", help="Output directory for reports", default="reports")
    parser.add_argument("--device", "-d", help="Specific device ID to test on")
    parser.add_argument("--run", "-r", action="store_true", help="Run tests before generating report")
    
    args = parser.parse_args()
    
    # Ensure flows directory exists
    if not os.path.exists(args.flows):
        print(f"Error: Flows directory '{args.flows}' not found")
        return 1
    
    # Get flow files
    flow_files = glob.glob(os.path.join(args.flows, "*.yaml"))
    if not flow_files:
        print(f"Error: No flow files found in '{args.flows}'")
        return 1
    
    test_results = []
    
    if args.run:
        # Run tests
        for flow_file in flow_files:
            result = run_maestro_test(flow_file, args.device)
            test_results.append(result)
    else:
        # Simulate test results for demonstration
        for flow_file in flow_files:
            test_results.append({
                "flow_file": flow_file,
                "success": True,
                "output": f"Running flow: {flow_file}\nappId: com.example.app\nScreenshot saved to /tmp/screenshot.png",
                "error": "",
                "duration": 5.0
            })
    
    # Parse results
    parsed_results = parse_test_results(test_results)
    
    # Generate report
    report_file = generate_html_report(parsed_results, args.output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())