"""
NexusController - Advanced Android Automation Platform

NexusController is a comprehensive and professional-grade Android device automation platform
that bridges the gap between manual testing and continuous integration. It provides a unified
solution for Android device control, UI automation, and test orchestration.

This package provides:
- Device management and control via ADB
- UI automation through Maestro integration
- Screen recording and screenshot capabilities
- App installation and management
- Interactive CLI and Jupyter notebook interfaces

Created and maintained by ankit1057 (github.com/ankit1057)
"""

__version__ = "1.0.0"
__author__ = "ankit1057"
__license__ = "MIT with Commercial Use Clause"

from .controller import AndroidController
from .config import CONSTANTS 