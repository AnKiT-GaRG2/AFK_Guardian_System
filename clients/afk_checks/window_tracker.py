import subprocess
import shutil
import platform

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


def _get_macos_active_window_title():
    # Frontmost app name is generally available when Accessibility permissions are granted.
    app_name = _run_command([
        "osascript",
        "-e",
        'tell application "System Events" to get name of first application process whose frontmost is true',
    ])

    # Window title may fail for apps without standard windows; keep app name as fallback.
    window_title = _run_command([
        "osascript",
        "-e",
        'tell application "System Events" to tell (first application process whose frontmost is true) to get name of front window',
    ])

    if window_title and app_name and window_title != app_name:
        return f"{window_title} - {app_name}"
    if window_title:
        return window_title
    return app_name


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
    if platform.system() == "Darwin":
        mac_title = _get_macos_active_window_title()
        if mac_title:
            return mac_title

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
