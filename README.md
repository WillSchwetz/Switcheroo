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

Ensure you have Python 3.10+ installed. Then install the required packages:

```bash
pip install -r requirements.txt

[!NOTE]
Note: This utility is designed for Windows only.