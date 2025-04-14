#!/usr/bin/env python3
"""
Setup script for Android MCP package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f.readlines() if not line.startswith("#")]

setup(
    name="android-mcp",
    version="0.2.0",
    author="ankit1057",
    author_email="ankit1057@users.noreply.github.com",
    description="Android Mobile Control Platform (MCP) with Maestro Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ankit1057/android-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "android-mcp=android_mcp_jupyter:run_ui_mode",
        ],
    },
    include_package_data=True,
) 