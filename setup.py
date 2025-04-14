#!/usr/bin/env python3
"""
Setup script for NexusController
"""

import os
from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nexuscontroller",
    version="1.0.0",
    author="ankit1057",
    author_email="ankit1057@github.com",
    description="Advanced Android automation platform for testing and device control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ankit1057/nexuscontroller",
    project_urls={
        "Bug Tracker": "https://github.com/ankit1057/nexuscontroller/issues",
        "Documentation": "https://github.com/ankit1057/nexuscontroller",
        "Source Code": "https://github.com/ankit1057/nexuscontroller",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nexuscontroller=nexuscontroller_cli:run_ui_mode",
        ],
    },
    include_package_data=True,
) 