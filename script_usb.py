import ctypes
import threading
import pystray
import pyautogui
import time
from PIL import Image, ImageDraw, ImageFont
import logging
import pywinusb.hid as hid

# Global variable to keep track of safe USB devices
safe_usb_devices = 1
DEFAULT_USB = 1

# Global variable to keep track of reload time in seconds
reload_time_in_seconds = 1

# Event to signal when the initial update is done
update_event = threading.Event()

# Flag to signal the thread to stop
stop_monitor_thread = threading.Event()

# Flag to control logging
enable_logging = False

# Set up logging if enabled
if enable_logging:
    logging.basicConfig(filename='error_usb.log', level=logging.ERROR)

def get_usb_device_count():
    try:
        all_devices = hid.HidDeviceFilter().get_devices()
        unique_device_ids = set()
        for device in all_devices:
            unique_device_ids.add((device.vendor_id, device.product_id))
        return len(unique_device_ids)
    except Exception as e:
        # Log the error
        logging.error(f"Error in get_usb_device_count(): {e}")
        return -1

def generate_usb_icon(num_devices):
    try:
        # Create a larger USB icon with the count displayed
        icon_size = (200, 100)  # Increase the size for a larger horizontal icon
        image = Image.new("RGB", icon_size, "white")
        draw = ImageDraw.Draw(image)
        
        # Set the background color based on the number of USB devices
        background_color = "red" if num_devices > safe_usb_devices else "white"
        
        # Draw USB pendrive-like shape
        body_width = 150  # Increase the width for a horizontal shape
        body_height = 60
        body_top_left = ((icon_size[0] - body_width) // 2, (icon_size[1] - body_height) // 2)
        
        # Draw left rectangle (body of USB pendrive) with thicker outline
        draw.rectangle([body_top_left, (body_top_left[0] + body_width, body_top_left[1] + body_height)],
                       outline="black", fill=background_color, width=7) 
        
        connector_width = 40  # Increase the width for a horizontal shape
        connector_height = 40
        connector_top_left = ((icon_size[0] + body_width) // 2, (icon_size[1] - connector_height) // 2)
        draw.rectangle([connector_top_left, (connector_top_left[0] + connector_width, connector_top_left[1] + connector_height)],
                       outline="black", fill="black")
        
        # Adjust font size dynamically based on icon size
        max_text_width = icon_size[0] - 10  # Leave some margin
        font_size = 24
        font = ImageFont.truetype("arial.ttf", font_size)
        while True:
            font = ImageFont.truetype("arial.ttf", font_size)
            text_width, text_height = draw.textlength(str(num_devices), font=font), font_size
            if text_width >= max_text_width or text_height >= icon_size[1]:
                break
            font_size += 1
    
        # Position the number inside the circle with a thinner, non-bold font
        text_position = ((icon_size[0] - text_width) / 2, (icon_size[1] - text_height) / 2)
        draw.text(text_position, str(num_devices), fill="black", font=font)
        
        return image
    except Exception as e:
        # Log the error
        logging.error(f"Error in generate_usb_icon(): {e}")
        return None
    


def update_usb_icon(icon):
    global safe_usb_devices, stop_monitor_thread, reload_time_in_seconds
    while not stop_monitor_thread.is_set():
        try:
            num_devices = get_usb_device_count()
    
            # Lock PC and show warning if a new USB device is connected
            if num_devices > safe_usb_devices:
                icon.title = f"USB Devices: {num_devices}" + "\n" + f"Default: {DEFAULT_USB}"
                icon.icon = generate_usb_icon(num_devices)
                ctypes.windll.user32.LockWorkStation()
                pyautogui.hotkey('win', 'd')
                result = ctypes.windll.user32.MessageBoxW(0, f"{num_devices} USB devices connected (default {DEFAULT_USB}). Do you want to add {safe_usb_devices+1}st/nd/rd/th USB devices to the safe list?", "Warning", 0x00000030 | 0x00000001)
                if result == 1:  # If "Yes" is clicked
                    safe_usb_devices += 1
                # Update icon after the dialog is closed
                icon.icon = generate_usb_icon(num_devices)
            elif num_devices < safe_usb_devices:
                icon.title = f"USB Devices: {num_devices}" + "\n" + f"Default: {DEFAULT_USB}"
                safe_usb_devices = num_devices
                icon.icon = generate_usb_icon(num_devices)
            elif not update_event.is_set():
                icon.title = f"USB Devices: {num_devices}" + "\n" + f"Default: {DEFAULT_USB}"
                icon.icon = generate_usb_icon(num_devices)
    
            # Signal that the initial update is done
            update_event.set()
    
            # Sleep for some time before checking again
            time.sleep(reload_time_in_seconds)  # Adjust as needed
        except Exception as e:
            # Log the error
            logging.error(f"Error in update_usb_icon(): {e}")

def main():
    global update_event

    # Create system tray icon
    usb_icon = pystray.Icon("USB Devices Counter")

    # Start thread to continuously update the icon
    usb_update_thread = threading.Thread(target=lambda: update_usb_icon(usb_icon))
    usb_update_thread.daemon = True
    usb_update_thread.start()

    # Wait for the initial update to finish
    update_event.wait()

    # Create menu
    usb_menu = (pystray.MenuItem("Exit", lambda: exit_application(usb_icon)),)
    
    # Set menu for icon
    usb_icon.menu = usb_menu

    # Run the icon in the system tray
    usb_icon.run()

def exit_application(icon):
    global stop_monitor_thread
    # Set the stop flag to stop the thread
    stop_monitor_thread.set()
    # Stop the icon
    icon.stop()

if __name__ == "__main__":
    main()
