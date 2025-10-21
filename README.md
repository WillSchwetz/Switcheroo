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

> [!NOTE]
> Note: This utility is designed for Windows only.

---

## Usage
A tray icon (blue square) will appear in your system tray.

Right-click the tray icon:

Toggle windows to include in cycling.

Refresh window list after opening/closing apps.

Quit the application.

Use the hotkeys:

Ctrl + Alt + . → Cycle through selected windows.

Ctrl + Alt + Q → Exit the program.

## Example Workflow

Launch the utility — tray icon appears.

Right-click → select your commonly used windows (e.g., Browser, IDE, Terminal).

Press Ctrl + Alt + Tab to switch between them without minimizing other applications.

Add or remove windows as needed via the tray menu.

## Limitations

Only works on Windows.

Only top-level windows with non-empty titles are included.

Hotkeys require the script to have focus permissions and may not work if blocked by other security software.

## Future Improvements

Persistence: Save selected windows between sessions (via JSON configuration).

Per-Window Hotkeys: Assign custom hotkeys to specific windows.

Auto-Start: Option to run the utility on Windows startup.