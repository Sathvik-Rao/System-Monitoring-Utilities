import ctypes
import time
import threading
import pystray
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import logging
import wexpect

# Define necessary constants
SM_CMONITORS = 80

# Global variable to keep track of safe monitors
safe_monitors = 0
safe_monitor_name = "ParsecVDA"
DEFAULT_MONITOR = 0

# Global variable to keep track of reload time in seconds
reload_time_in_seconds = 1

# Event to signal when the initial update is done
update_monitor_event = threading.Event()

# Flag to signal the thread to stop
stop_monitor_thread = threading.Event()

# Flag to control logging
enable_logging = False

# Set up logging if enabled
if enable_logging:
    logging.basicConfig(filename='error_monitor.log', level=logging.ERROR)

def get_display_count(safe_monitor_name):
    try:
        child = wexpect.spawn("dumpedid -a")
        child.expect(wexpect.EOF)
        output = child.before
        child.close()
        
        monitor_names = [line.split(':')[-1].strip() for line in output.split('\n') if 'Monitor Name' in line]
        if safe_monitor_name in monitor_names:
            return len(monitor_names) - 1
        return len(monitor_names)
    except Exception as e:
        # Log the error
        logging.error(f"Error in get_display_count(): {e}")
        return -1

def generate_monitor_icon(num_displays):
    try:
        # Create a monitor-shaped icon
        icon_size = (64, 64)
        image = Image.new("RGB", icon_size, "white")
        draw = ImageDraw.Draw(image)
        
        # Set the background color based on the number of monitors
        background_color = "red" if num_displays > safe_monitors else "white"
        
        # Draw the monitor shape
        monitor_width = icon_size[0] - 10
        monitor_height = icon_size[1] - 15
        monitor_border = 5
        draw.rectangle([(monitor_border, monitor_border), (monitor_width, monitor_height)], outline="black", width=3, fill=background_color)
        draw.rectangle([(monitor_border+2, monitor_border+2), (monitor_width-2, monitor_height-2)], outline="black", width=1)
        
        # Draw the monitor stand
        stand_width = 10
        stand_height = 6
        stand_left = (icon_size[0] - stand_width) / 2
        stand_top = icon_size[1] - stand_height - 2
        draw.rectangle([(stand_left, stand_top), (stand_left + stand_width, stand_top + stand_height)], fill="black")

        # Adjust font size dynamically based on icon size
        font_size = 1
        font = None
        while True:
            font = ImageFont.truetype("arial.ttf", font_size)
            text_width, text_height = draw.textlength(str(num_displays), font=font), font_size
            if text_width >= monitor_width or text_height >= monitor_height:
                break
            font_size += 1

        # Center the text within the monitor
        text_position = ((icon_size[0] - text_width) / 2, (icon_size[1] - text_height) / 2)
        draw.text(text_position, str(num_displays), fill="black", font=font)
        
        return image
    except Exception as e:
        # Log the error
        logging.error(f"Error in generate_monitor_icon(): {e}")
        return None

def update_monitor_icon(icon):
    global safe_monitors, stop_monitor_thread, reload_time_in_seconds, safe_monitor_name
    while not stop_monitor_thread.is_set():
        try:
            num_displays = get_display_count(safe_monitor_name)
            
            # Lock PC and show warning if a new monitor is connected
            if num_displays > safe_monitors:
                icon.title = f"Monitors: {num_displays}" + "\n" + f"Default: {DEFAULT_MONITOR}"
                icon.icon = generate_monitor_icon(num_displays)
                ctypes.windll.user32.LockWorkStation()
                pyautogui.hotkey('win', 'd')
                result = ctypes.windll.user32.MessageBoxW(0, f"{num_displays} monitors connected (default {DEFAULT_MONITOR}). Do you want to add the {safe_monitors+1}st/nd/rd/th monitor to the safe list?", "Warning", 0x00000030 | 0x00000001)
                if result == 1:  # If "Yes" is clicked
                    safe_monitors += 1
                # Update icon after the dialog is closed
                icon.icon = generate_monitor_icon(num_displays)
            elif num_displays < safe_monitors:
                icon.title = f"Monitors: {num_displays}" + "\n" + f"Default: {DEFAULT_MONITOR}"
                safe_monitors = num_displays
                icon.icon = generate_monitor_icon(num_displays)
            elif not update_monitor_event.is_set():
                icon.title = f"Monitors: {num_displays}" + "\n" + f"Default: {DEFAULT_MONITOR}"
                icon.icon = generate_monitor_icon(num_displays)

            # Signal that the initial update is done
            update_monitor_event.set()

            # Sleep for some time before checking again
            time.sleep(reload_time_in_seconds)  # Adjust as needed
        except Exception as e:
            # Log the error
            logging.error(f"Error in update_monitor_icon(): {e}")
            

def main():
    global update_monitor_event

    # Create system tray icon
    monitor_icon = pystray.Icon("Displays Counter")

    # Start thread to continuously update the icon
    monitor_update_thread = threading.Thread(target=lambda: update_monitor_icon(monitor_icon))
    monitor_update_thread.daemon = True
    monitor_update_thread.start()

    # Signal that the initial update is done
    update_monitor_event.wait()

    # Create menu
    monitor_menu = (pystray.MenuItem("Exit", lambda: exit_application(monitor_icon)),)
    
    # Set menu for icon
    monitor_icon.menu = monitor_menu

    # Run the icon in the system tray
    monitor_icon.run()

def exit_application(icon):
    global stop_monitor_thread
    # Set the stop flag to stop the thread
    stop_monitor_thread.set()
    # Stop the icon
    icon.stop()

if __name__ == "__main__":
    main()
