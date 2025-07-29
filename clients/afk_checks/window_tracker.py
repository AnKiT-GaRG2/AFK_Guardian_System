import pyautogui
from pywinauto import Application
from time import sleep

def get_active_window():
    active_window = pyautogui.getActiveWindow()
    if active_window:
        return active_window.title
    else:
        print("No active window detected")
        return None
