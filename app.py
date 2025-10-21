import threading
import pygetwindow as gw
import pywinauto
import keyboard
import pystray
from PIL import Image, ImageDraw

# --- Globals ---
windows = []
selected_titles = set()
current_index = 0
running = True

# --- Window management ---
def refresh_windows():
    global windows
    
    windows = [w for w in gw.getWindowsWithTitle('') if w.title.strip()]
    print(f"Found {len(windows)} windows.")
    rebuild_tray_menu()

def toggle_window_selection(title):
    if title in selected_titles:
        selected_titles.remove(title)
    else:
        selected_titles.add(title)
    rebuild_tray_menu()
    print("Selected windows:", selected_titles)

def next_window():
    global current_index
    if not selected_titles:
        print("No windows selected. Use tray menu to select some.")
        return
    selected = [w for w in windows if w.title in selected_titles]
    if not selected:
        print("No valid selected windows.")
        return
    current_index = (current_index + 1) % len(selected)
    try:
        handle = selected[current_index]._hWnd
        app = pywinauto.Application().connect(handle=handle)
        app.top_window().set_focus()
        print(f"Switched to: {selected[current_index].title}")
    except Exception as e:
        print("Error switching window:", e)

# --- Tray icon creation ---
def create_icon_image():
    img = Image.new('RGB', (64, 64), (70, 130, 250))
    draw = ImageDraw.Draw(img)
    draw.rectangle([12, 12, 52, 52], fill=(0, 0, 180))
    return img

def rebuild_tray_menu():
    global tray_icon
    items = []

    # Add windows as toggles
    for w in windows:
        title = w.title[:50] or "<Untitled>"
        checked = title in selected_titles
        items.append(
            pystray.MenuItem(
                f"{'✔ ' if checked else ''}{title}",
                lambda _, t=title: toggle_window_selection(t),
                checked=lambda item, t=title: t in selected_titles
            )
        )

    # Add separators and commands
    items += [
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
    tray_icon = pystray.Icon(
        "WindowSwitcher",
        create_icon_image(),
        "Window Switcher",
        menu=pystray.Menu(
            pystray.MenuItem("Loading windows...", lambda: None)
        )
    )
    refresh_windows()
    tray_icon.run()

# --- Hotkey thread ---
def start_hotkeys():
    keyboard.add_hotkey('ctrl+alt+tab', next_window)
    keyboard.add_hotkey('ctrl+alt+q', quit_program)
    print("Hotkeys:")
    print(" - Ctrl+Alt+Tab: Cycle selected windows")
    print(" - Ctrl+Alt+Q: Quit")
    keyboard.wait('ctrl+alt+q')

# --- Main ---
if __name__ == "__main__":
    threading.Thread(target=start_hotkeys, daemon=True).start()
    setup_tray()
