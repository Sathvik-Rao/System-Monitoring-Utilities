# System-Monitoring-Utilities

This repository contains a collection of Python scripts for monitoring various system resources and devices. These scripts utilize the PyStray library to provide a user-friendly interface via system tray icons. Currently, the repository includes the following monitoring utilities:

1. **Display Monitor Counter**: Monitors the number of connected display monitors and provides notifications when a new monitor is connected or disconnected.

2. **Audio Device Counter**: Monitors the number of connected audio devices and alerts the user when a new audio device is connected or disconnected.

3. **USB Device Counter**: Monitors the number of connected USB devices and notifies the user when a new USB device is connected or disconnected.

## System Protection Feature

The monitoring utilities in this application serve as a safeguard against unauthorized peripheral devices being connected to your system. Imagine you have a computer in a shared environment or a remote server located in a secure location. These utilities constantly keep an eye on your system's peripherals like display monitors, USB devices, and audio devices.

### How It Works

- **Automatic Locking**: If any peripheral device other than the default ones is connected to your system, the application takes immediate action to protect your privacy. It automatically locks your system to prevent unauthorized access.

- **Visual Warning Indicators**: After unlocking your system, you'll notice that the monitoring icons turn red. This visual change serves as a warning sign, indicating that an unauthorized peripheral device was detected.

- **Notification Prompt**: Additionally, a notification text box pops up to alert you about the detected peripheral device connection. This ensures that even if you miss the visual indicator, you'll still be informed about the potential security threat.

### Why It Matters

This feature is crucial for maintaining the security and integrity of your system, especially in shared or remote environments where unauthorized access could lead to data breaches or other security risks. By proactively monitoring peripheral devices and taking immediate action when unauthorized connections are detected, you can protect your system and sensitive information from potential threats.


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


Certainly! Here's how you can add a section for images demo:

## Images Demo

<img width="236" alt="Screenshot 2024-03-19 000546" src="https://github.com/Sathvik-Rao/System-Monitoring-Utilities/assets/36164509/04bbb169-98b3-430e-892f-271e1ce21c66">

![Screenshot 2024-03-19 000734](https://github.com/Sathvik-Rao/System-Monitoring-Utilities/assets/36164509/4171bf8e-49f0-4844-8dc6-af391b1889e5)

![Screenshot 2024-03-19 000804](https://github.com/Sathvik-Rao/System-Monitoring-Utilities/assets/36164509/6f433b8b-daa7-42d4-becc-ee6b9be42229)

![Screenshot 2024-03-19 000822](https://github.com/Sathvik-Rao/System-Monitoring-Utilities/assets/36164509/97145904-75fb-4dd6-8089-431fd54c9e9f)

![Screenshot 2024-03-19 000928](https://github.com/Sathvik-Rao/System-Monitoring-Utilities/assets/36164509/94ffe228-8bbf-4129-b03e-da78a08fbfa1)

