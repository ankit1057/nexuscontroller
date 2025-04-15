# NexusController Cleanup Plan

## Redundant Files to Remove

The following files are redundant and should be removed as part of the cleanup process:

### Legacy Controller Files
- `/home/ankit/Desktop/NexusControl/nexuscontrol_basic.py`
- `/home/ankit/Desktop/NexusControl/nexuscontrol_advanced.py`
- `/home/ankit/Desktop/NexusControl/nexuscontrol_maestro.py`

These have been replaced by the `nexuscontroller` module with `controller.py`.

### Duplicate MCP Files
- `/home/ankit/Desktop/NexusControl/mcp_adapter.py`

This functionality has been integrated into `mcp_server.py`.

### Outdated Script References
- `/home/ankit/Desktop/NexusControl/launch_nexuscontrol.sh` (should be replaced with `launch_nexuscontroller.sh`)
- `/home/ankit/Desktop/NexusControl/android_mcp_demo.ipynb` (needs to be updated for new API)

### Renaming Script
- `/home/ankit/Desktop/NexusControl/rename_project.sh` (no longer needed after project renaming)

## Files to Update

The following files should be updated to use the new module name:

1. `/home/ankit/Desktop/NexusControl/nexuscontroller_cli.py`
   - Update imports to use `from nexuscontroller import AndroidController`

2. `/home/ankit/Desktop/NexusControl/android_mcp_jupyter.py`
   - Update imports to use `from nexuscontroller import AndroidController`

3. Any test files referencing the old module names

## New Launch Script

Create a new launch script `launch_nexuscontroller.sh` that references the new module name.

## Cleanup Process

1. First, ensure all necessary functionality is correctly implemented in the `nexuscontroller` module
2. Create proper tests to verify the functionality works after removing legacy files
3. Gradually remove redundant files one by one, testing after each removal
4. Update references in remaining files to point to the new module
5. Finally, update documentation to reflect the new structure

## Benefits of Cleanup

- Simpler codebase structure
- Eliminated redundancy and duplication
- Clearer API surface
- More maintainable code
- Smaller package size
- Consistent naming across the project 