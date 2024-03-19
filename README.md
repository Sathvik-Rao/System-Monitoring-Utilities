# System-Monitoring-Utilities

This repository contains a collection of Python scripts for monitoring various system resources and devices. These scripts utilize the PyStray library to provide a user-friendly interface via system tray icons. Currently, the repository includes the following monitoring utilities:

1. **Display Monitor Counter**: Monitors the number of connected display monitors and provides notifications when a new monitor is connected or disconnected.

2. **Audio Device Counter**: Monitors the number of connected audio devices and alerts the user when a new audio device is connected or disconnected.

3. **USB Device Counter**: Monitors the number of connected USB devices and notifies the user when a new USB device is connected or disconnected.

## Installation

Here are the additional instructions you can add to your README.md file:

## Additional Setup Instructions

### 1) DumpEDID Setup

1. **Place DumpEDID Folder**: Copy the DumpEDID folder to any directory on your system where the file path does not contain white spaces.

2. **Add to Environment Variables**:
   - Open the Control Panel and navigate to System and Security > System > Advanced system settings.
   - In the System Properties window, click on the "Environment Variables" button.
   - Under "System variables," find the "Path" variable and click on "Edit."
   - Add the path to the DumpEDID folder to the list of paths. For example, if the folder is located at `C:\DumpEDID`, add `C:\DumpEDID` to the end of the list.
   - Click "OK" to save the changes.

3. **Verify Installation**: Open a command prompt and type `DumpEDID -a` to verify that DumpEDID is correctly installed and accessible.

### 2) Startup Setup

1. **Place Executable File**: Copy the `.exe` file generated from the Python scripts to any directory on your system.

2. **Add to Startup**:
   - Press `Win + R` to open the Run dialog.
   - Type `shell:startup` and press Enter to open the Startup folder.
   - Copy the `.exe` file into this folder.
   - Restart your computer to ensure that the monitoring utility starts automatically with the system.

### 2a) Generating Executable from Python Scripts

Refer to the instructions provided in the `generate_exe/create.txt` file to generate an executable (`.exe`) file from the Python scripts.


