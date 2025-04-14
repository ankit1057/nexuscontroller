// Custom JavaScript for Maestro integration
// This script demonstrates how to use custom JavaScript with Maestro

function performCustomAction(device) {
  console.log("Executing custom JavaScript action");
  
  // Example: Get current activity
  const currentActivity = device.shell("dumpsys window windows | grep -E 'mCurrentFocus'");
  console.log("Current activity:", currentActivity);
  
  // Example: Get device properties
  const deviceModel = device.shell("getprop ro.product.model");
  const androidVersion = device.shell("getprop ro.build.version.release");
  console.log(`Device: ${deviceModel.trim()} (Android ${androidVersion.trim()})`);
  
  // Example: Custom UI interaction
  const screenWidth = parseInt(device.shell("wm size").match(/(\d+)x\d+/)[1]);
  const screenHeight = parseInt(device.shell("wm size").match(/\d+x(\d+)/)[1]);
  
  // Tap in the middle of the screen
  device.tap(screenWidth / 2, screenHeight / 2);
  
  // Return a value that can be used in the Maestro flow
  return {
    success: true,
    message: "Custom action completed successfully",
    screenDimensions: `${screenWidth}x${screenHeight}`
  };
}

// Execute the function and return the result
performCustomAction(device);