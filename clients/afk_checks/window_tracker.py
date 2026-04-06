import subprocess
import shutil

try:
    import pyautogui
except ImportError:
    pyautogui = None


def _run_command(command):
    try:
        result = subprocess.check_output(command, stderr=subprocess.DEVNULL, text=True).strip()
        return result
    except Exception:
        return ""


def _get_linux_active_window_title():
    if shutil.which("xdotool"):
        title = _run_command(["xdotool", "getactivewindow", "getwindowname"])
        if title:
            return title

    if shutil.which("xprop"):
        active_window_info = _run_command(["xprop", "-root", "_NET_ACTIVE_WINDOW"])
        if "window id #" in active_window_info:
            window_id = active_window_info.split("window id #")[-1].strip()
            if window_id and window_id != "0x0":
                title_info = _run_command(["xprop", "-id", window_id, "WM_NAME"])
                if " = " in title_info:
                    title = title_info.split(" = ", 1)[-1].strip().strip('"')
                    if title:
                        return title

    return ""

def get_active_window():
    linux_title = _get_linux_active_window_title()
    if linux_title:
        return linux_title

    if pyautogui is None:
        return "Unknown Window"

    try:
        active_window = pyautogui.getActiveWindow()
        if active_window:
            return active_window.title
    except Exception:
        pass

    return "Unknown Window"
