import ctypes
import threading
import pystray
import pyautogui
import pyaudio
import time
from PIL import Image, ImageDraw, ImageFont
import logging

# Global variable to keep track of safe audio devices
safe_audio_devices = 4
DEFAULT_AUDIO = 4

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
    logging.basicConfig(filename='error_audio.log', level=logging.ERROR)

def get_audio_device_count():
    try:
        p = pyaudio.PyAudio()
        num_devices = p.get_host_api_info_by_index(0).get('deviceCount')
        p.terminate()
        return num_devices
    except Exception as e:
        # Log the error
        logging.error(f"Error in get_audio_device_count(): {e}")
        return -1

def generate_audio_icon(num_devices):
    try:
        # Create a larger audio play button-shaped icon
        icon_size = (128, 128)
        image = Image.new("RGB", icon_size, "white")
        draw = ImageDraw.Draw(image)
        
        # Set the background color based on the number of audio devices
        background_color = "red" if num_devices > safe_audio_devices else "white"
        
        # Define triangle dimensions
        triangle_width = 80
        triangle_height = 80
        
        # Calculate positions for two triangles
        first_triangle_x = (icon_size[0] - triangle_width * 2) // 3
        second_triangle_x = icon_size[0] - (icon_size[0] - triangle_width * 2) // 3  # Rightmost position
        triangle_y = (icon_size[1] - triangle_height) // 2
        
        # Draw the two triangles with bolder outlines
        draw.polygon([(first_triangle_x, triangle_y), 
                      (first_triangle_x + triangle_width, triangle_y + triangle_height // 2), 
                      (first_triangle_x, triangle_y + triangle_height)], 
                     outline="black", width=8, fill=background_color)
        
        draw.polygon([(second_triangle_x, triangle_y), 
                      (second_triangle_x - triangle_width, triangle_y + triangle_height // 2), 
                      (second_triangle_x, triangle_y + triangle_height)], 
                     outline="black", width=8, fill=background_color)  # Inverted right triangle
        
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
    
        # Position the number on top of the triangles with a thinner, non-bold font
        text_position = ((icon_size[0] - text_width) / 2, 0)
        draw.text(text_position, str(num_devices), fill="black", font=font)
        
        return image
    except Exception as e:
        # Log the error
        logging.error(f"Error in generate_audio_icon(): {e}")
        return None

def update_audio_icon(icon):
    global safe_audio_devices, stop_monitor_thread, reload_time_in_seconds
    while not stop_monitor_thread.is_set():
        try:
            num_devices = get_audio_device_count()
            
            # Lock PC and show warning if a new audio device is connected
            if num_devices > safe_audio_devices:
                icon.title = f"Audio Devices: {num_devices}" + "\n" + f"Default: {DEFAULT_AUDIO}"
                icon.icon = generate_audio_icon(num_devices)
                ctypes.windll.user32.LockWorkStation()
                pyautogui.hotkey('win', 'd')
                result = ctypes.windll.user32.MessageBoxW(0, f"{num_devices} audio devices connected (default {DEFAULT_AUDIO}). Do you want to add {num_devices-safe_audio_devices} audio devices to the safe list?", "Warning", 0x00000030 | 0x00000001)
                if result == 1:  # If "Yes" is clicked
                    safe_audio_devices = num_devices
                # Update icon after the dialog is closed
                icon.icon = generate_audio_icon(num_devices)
            elif num_devices < safe_audio_devices:
                icon.title = f"Audio Devices: {num_devices}" + "\n" + f"Default: {DEFAULT_AUDIO}"
                safe_audio_devices = num_devices
                icon.icon = generate_audio_icon(num_devices)
            elif not update_event.is_set():
                icon.title = f"Audio Devices: {num_devices}" + "\n" + f"Default: {DEFAULT_AUDIO}"
                icon.icon = generate_audio_icon(num_devices)
    
            # Signal that the initial update is done
            update_event.set()
    
            # Sleep for some time before checking again
            time.sleep(reload_time_in_seconds)  # Adjust as needed
        except Exception as e:
            # Log the error
            logging.error(f"Error in update_audio_icon(): {e}")

def main():
    global update_event

    # Create system tray icon
    audio_icon = pystray.Icon("Audio Devices Counter")

    # Start thread to continuously update the icon
    audio_update_thread = threading.Thread(target=lambda: update_audio_icon(audio_icon))
    audio_update_thread.daemon = True
    audio_update_thread.start()

    # Wait for the initial update to finish
    update_event.wait()

    # Create menu
    audio_menu = (pystray.MenuItem("Exit", lambda: exit_application(audio_icon)),)
    
    # Set menu for icon
    audio_icon.menu = audio_menu

    # Run the icon in the system tray
    audio_icon.run()

def exit_application(icon):
    global stop_monitor_thread
    # Set the stop flag to stop the thread
    stop_monitor_thread.set()
    # Stop the icon
    icon.stop()

if __name__ == "__main__":
    main()
