import threading
import pygetwindow as gw
import pywinauto
import keyboard
import pystray
from PIL import Image, ImageDraw
from functools import partial
import requests
from pystray import Icon as icon, Menu as menu, MenuItem as item
# --- Globals ---
windows = []
selected_ids = set()   # store window HWNDs instead of titles
current_index = 0
running = True
current_version = "v0.0.1"
update_available = False

# --- Window management ---
def refresh_windows():
    global windows
    windows = [w for w in gw.getAllWindows() if getattr(w, 'title', '').strip()]
    for w in windows:
        print(f"Window: {w.title} (HWND={getattr(w, '_hWnd', None)})")
    print(f"Found {len(windows)} windows.")
    rebuild_tray_menu()

def toggle_window_selection(hwnd, *args):
    # accept extra args because pystray may pass (icon, item) or item
    if hwnd in selected_ids:
        selected_ids.remove(hwnd)
    else:
        selected_ids.add(hwnd)
    rebuild_tray_menu()
    print("Selected window HWNDs:", selected_ids)

def next_window():
    global current_index
    if not selected_ids:
        print("No windows selected. Use tray menu to select some.")
        return
    selected = [w for w in windows if getattr(w, '_hWnd', None) in selected_ids]
    if not selected:
        print("No valid selected windows.")
        return
    current_index = (current_index + 1) % len(selected)
    try:
        handle = selected[current_index]._hWnd
        app = pywinauto.Application().connect(handle=handle)
        app.top_window().set_focus()
        print(f"Switched to: {selected[current_index].title} (HWND={handle})")
    except Exception as e:
        print("Error switching window:", e)

def rebuild_tray_menu():
    global tray_icon
    items = []

    



    # helper for checked callback
    def _is_selected(hwnd, item=None):
        return hwnd in selected_ids

    # Add windows as toggles (show title, toggle by hwnd)
    for w in windows:
        title = (w.title[:50] or "<Untitled>")
        hwnd = getattr(w, '_hWnd', None)
        checked = hwnd in selected_ids
        action = partial(toggle_window_selection, hwnd)        # bind HWND explicitly
        checked_cb = partial(_is_selected, hwnd)               # bind HWND for checked state
        items.append(
            pystray.MenuItem(
                f"{title}",
                action,
                checked=checked_cb
            )
        )

    # Add separators and commands
    items += [
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(f"{'❗' if update_available else ''} Update App", lambda:None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Refresh Windows", lambda: threading.Thread(target=refresh_windows).start()),
        pystray.MenuItem("Quit", quit_program)
    ]

    tray_icon.menu = pystray.Menu(*items)

def quit_program(icon=None, item=None):
    global running
    running = False
    if icon:
        icon.stop()
    print("Exiting...")

def setup_tray():
    global tray_icon
    image = Image.open("icons/switcheroo.ico")
    tray_icon = pystray.Icon(
        "WindowSwitcher",
        image,
        "Window Switcher",
        menu=pystray.Menu(
            pystray.MenuItem("Loading windows...", lambda: None)
        )
    )
    refresh_windows()
    tray_icon.run()

# --- Hotkey thread ---
def start_hotkeys():
    keyboard.add_hotkey('ctrl+alt+.', next_window)
    keyboard.add_hotkey('ctrl+alt+q', quit_program)
    print("Hotkeys:")
    print(" - Ctrl+Alt+.: Cycle selected windows")
    keyboard.wait('ctrl+alt+q')

def check_for_updates():
    repo = "WillSchwetz/task_switch"
    response = requests.get(f"https://api.github.com/repos/{repo}/releases/latest").json()
    latest_version = response.get("tag_name", "")
    if latest_version and latest_version != current_version:
        update_available = True

# --- Main ---
if __name__ == "__main__":
    threading.Thread(target=start_hotkeys, daemon=True).start()
    setup_tray()
