# activity_tracker.py
from pynput import keyboard, mouse
from threading import Thread, Lock
import time

# Shared Activity Data
activity_data = {
    "keyboard_activity": "",
    "mouse_movement_distance": 0,
    "mouse_clicks": 0,
    "mouse_scrolls": 0,
}

last_mouse_position = None
lock = Lock()

# Mouse Handlers
def on_move(x, y):
    global last_mouse_position
    with lock:
        if last_mouse_position is not None:
            prev_x, prev_y = last_mouse_position
            distance = ((x - prev_x) ** 2 + (y - prev_y) ** 2) ** 0.5
            activity_data["mouse_movement_distance"] += distance
        last_mouse_position = (x, y)

def on_click(x, y, button, pressed):
    if pressed:
        with lock:
            activity_data["mouse_clicks"] += 1

def on_scroll(x, y, dx, dy):
    with lock:
        activity_data["mouse_scrolls"] += 1

# Keyboard Handler
def on_key_press(key):
    try:
        with lock:
            activity_data["keyboard_activity"] += key.char
    except AttributeError:
        pass

# Function to fetch and reset data
def get_activity_data():
    with lock:
        data_snapshot = activity_data.copy()
        # Reset all values after fetching
        activity_data["keyboard_activity"] = ""
        activity_data["mouse_movement_distance"] = 0
        activity_data["mouse_clicks"] = 0
        activity_data["mouse_scrolls"] = 0
        return data_snapshot

# Background Tracking
def start_tracking():
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)

    mouse_listener.start()
    keyboard_listener.start()

    mouse_listener.join()
    keyboard_listener.join()

# Run tracking in a background thread
tracking_thread = Thread(target=start_tracking, daemon=True)
tracking_thread.start()
