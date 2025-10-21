# Window Switcher Tray Utility

A lightweight Python utility for Windows that allows users to quickly cycle between selected open windows using global hotkeys. The application runs in the system tray and provides a simple interface to select which windows should be included in the cycle.

---

## Features

- **System Tray Icon:** Runs in the background with a tray icon for quick access.
- **Window Selection:** Right-click the tray icon to toggle which windows are included in the cycling.
- **Global Hotkeys:**
  - `Ctrl + Alt + .` — Cycle through selected windows.
  - `Ctrl + Alt + Q` — Quit the application.
- **Refresh Window List:** Update the list of open windows without restarting the program.
- **Lightweight & Reliable:** robust Windows window management without additional GUI dependencies.

---

## Installation

Coming soon

> [!CAUTION]
> Note: This utility is designed for Windows only.

---

## Usage
1. A tray icon (red car) will appear in your system tray.

2. Right-click the tray icon:

3. Toggle windows to include in cycling.

4. Refresh window list after opening/closing apps.

5. Quit the application.

6. Use the hotkeys:

7. Ctrl + Alt + . → Cycle through selected windows.

8. Ctrl + Alt + Q → Exit the program.

---

## Example Workflow

1. Launch the utility — tray icon appears.

2. Right-click → select your commonly used windows (e.g., Browser, IDE, Terminal).

3. Press Ctrl + Alt + Tab to switch between them without minimizing other applications.

4. Add or remove windows as needed via the tray menu.

---

## Limitations

- Only works on Windows.

- Only top-level windows with non-empty titles are included.

- Hotkeys require the script to have focus permissions and may not work if blocked by other security software.

---

## Future Improvements

- Persistence: Save selected windows between sessions (via JSON configuration).

- Per-Window Hotkeys: Assign custom hotkeys to specific windows.

- Auto-Start: Option to run the utility on Windows startup.

- Installer for ease of installation and use