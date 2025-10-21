import threading
import pygetwindow as gw
import pywinauto
import keyboard
import pystray
from PIL import Image, ImageDraw
from functools import partial

# --- Globals ---
windows = []
selected_ids = set()   # store window HWNDs instead of titles
current_index = 0
running = True

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

# --- Tray icon creation ---
def create_icon_image():
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # car body (simple hatchback silhouette)
    body = [
        (8, 40),   # rear lower
        (8, 32),   # rear top
        (14, 26),  # rear slope
        (28, 20),  # roof rear
        (40, 18),  # roof front
        (50, 22),  # windshield/front slope
        (56, 30),  # front top
        (56, 36),  # front lower
        (8, 40)    # close
    ]
    draw.polygon(body, fill=(200, 25, 30, 255), outline=(120, 10, 12, 255))

    # windows (light gray/blue)
    windows = [(16, 30), (26, 22), (36, 20), (46, 24), (34, 24), (24, 28)]
    draw.polygon(windows, fill=(200, 220, 235, 220), outline=(120, 140, 150, 200))

    # door line / simple detailing
    draw.line([(32, 22), (32, 36)], fill=(110, 10, 12, 255), width=1)
    draw.line([(22, 34), (46, 34)], fill=(150, 20, 22, 200), width=1)

    # wheels
    left_center = (22, 46)
    right_center = (44, 46)
    for cx, cy in (left_center, right_center):
        draw.ellipse([cx-6, cy-6, cx+6, cy+6], fill=(20, 20, 20, 255))    # tyre
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(170, 170, 170, 255)) # hubcap

    # headlight (small yellow) and hint of grille
    draw.ellipse([50, 30, 54, 34], fill=(255, 220, 100, 220))
    draw.line([(52, 34), (52, 36)], fill=(120, 12, 15, 200), width=1)
    return img

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
    keyboard.add_hotkey('ctrl+alt+.', next_window)
    keyboard.add_hotkey('ctrl+alt+q', quit_program)
    print("Hotkeys:")
    print(" - Ctrl+Alt+.: Cycle selected windows")
    print(" - Ctrl+Alt+Q: Quit")
    keyboard.wait('ctrl+alt+q')

# --- Main ---
if __name__ == "__main__":
    threading.Thread(target=start_hotkeys, daemon=True).start()
    setup_tray()
