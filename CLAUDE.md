# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DHV Session Timer is a PyQt6-based desktop application for dry herb vaporizer sessions (designed for the Arizer Solo 3). It provides timed temperature stage reminders with notifications and audio alerts to help users gradually increase heat during their sessions.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip3 install -r requirements.txt
```

### Running the Application
```bash
# From project root
cd src
python3 main.py
```

### Building
The project uses PyInstaller with a spec file located at `src/DHVSessionTimer.spec`.

**Linux:**
```bash
# Build only
./linux_build.sh

# Build and run (also copies to /usr/bin)
./linux_build_run.sh
```

**Mac:**
```bash
./mac_build.sh  # Creates DMG installer
```

**Windows:**
Windows builds are handled by GitHub Actions. To build locally:
```bash
cd src
python3 -m PyInstaller DHVSessionTimer.spec
```

### PyInstaller Command
```bash
# From src/ directory
python3 -m PyInstaller DHVSessionTimer.spec
```

## Architecture

### Application Structure

```
src/
├── main.py                    # Entry point, version checking, QSettings initialization
├── DHVSessionTimer.spec       # PyInstaller build configuration
├── UI/
│   ├── main_screen.py        # TimerApp class - main timer window and logic
│   ├── settings_screen.py    # SettingsWindow class - settings dialog
│   └── update_screen.py      # UpdateApp class - update notification dialog
├── utilities/
│   └── __init__.py           # resource_path() for PyInstaller, get_ding_resource()
└── asset/
    ├── ding.mp3              # Audio notification
    └── style.qss             # Qt stylesheet (Fusion style)
```

### Key Components

**main.py (src/main.py:1)**
- Application entry point
- Checks for updates via GitHub API on startup
- Initializes QSettings with organization "UnquenchedServant" and app "DHV-Session-Timer"
- Manages update skip logic (per-version and global)
- Current version tracked in `APP_VERSION` constant (src/main.py:16)

**TimerApp (src/UI/main_screen.py:30)**
- Main window with QTimer driving updates every second
- Three temperature stages with configurable times (default: 6, 8, 10 minutes)
- Mouse click actions configurable per button (left/middle/right)
- Spacebar shortcut for start/stop
- "Keep on top" window flag toggle
- Inverted time display mode (counts down instead of up)

**SettingsWindow (src/UI/settings_screen.py:9)**
- Temperature settings with F/C conversion
- Time intervals for each stage
- Notification and audio preferences
- Mouse button action bindings
- Platform-specific features (notification timeout not available on macOS)

### State Management

All settings are persisted using Qt's QSettings system:
- Organization: "UnquenchedServant"
- Application: "DHV-Session-Timer"
- Platform-specific storage (registry on Windows, plist on macOS, INI on Linux)

Key settings:
- `temp1/temp2/temp3`: Temperature values
- `temp_type`: "F" or "C"
- `time2/time3/time4`: Stage transition times in minutes
- `notifications`: Boolean for desktop notifications
- `almightyDing`: Boolean for audio alert
- `timeout`: Notification timeout in seconds
- `keep_active_default`: Default state for "keep on top"
- `inverted_time`: Toggle between elapsed/remaining time display
- `left_mouse_action/middle_mouse_action/right_mouse_action`: Mouse click behaviors
- `skip_{version}`: Per-version update skip flag
- `skip_all_updates`: Global update skip flag

### Timer Logic

The timer uses `DEBUG_TIME` multiplier (src/UI/main_screen.py:27) set to 60 for production (seconds per minute).

Stages are determined by elapsed time:
1. Stage 1: 0 to `time2 * DEBUG_TIME`
2. Stage 2: `time2 * DEBUG_TIME` to `time3 * DEBUG_TIME`
3. Stage 3: `time3 * DEBUG_TIME` to `time4 * DEBUG_TIME`
4. Complete: At `time4 * DEBUG_TIME`

### Waybar Integration

The app writes timer state to `~/dhv_timer.txt` as JSON for external tools like waybar:
```json
{
  "text": "4:32",
  "class": "yellow"  // green/yellow/red/white based on stage
}
```

Control files for waybar clicks:
- `~/dhv_timer_click1`: Detected every 10ms to toggle start/reset
- `~/dhv_timer_click2`: Detected every 10ms to invert time display

### Platform-Specific Behavior

**macOS:**
- Uses custom notification.py (root directory) instead of default plyer implementation
- Notification timeout not supported
- Notifications include default system sound
- Build script creates DMG installer

**Linux:**
- Recommended installation path: /usr/bin/
- Build scripts use `killall DHVSessionTimer` before copying

**Windows:**
- GitHub Actions handles builds automatically
- Path separators use backslashes in resource_path calls

### Notifications

Desktop notifications use the plyer library with platform-specific backends. The macOS implementation is customized (see notification.py in root) to work around plyer limitations with timeout and sound handling.

### Resource Management

The `resource_path()` utility function (src/utilities/__init__.py:13) handles paths for both development and PyInstaller bundled modes by checking for `sys._MEIPASS`.

## Temperature Constraints

Solo 3 valid ranges (enforced in settings):
- Fahrenheit: 122-428°F
- Celsius: 50-220°C

## Default Values

| Setting | Default |
|---------|---------|
| temp1 | 350°F |
| temp2 | 375°F |
| temp3 | 400°F |
| time2 | 6 min |
| time3 | 8 min |
| time4 | 10 min |
| notifications | True |
| almightyDing | True |
| timeout | 10 sec |
| keep_active_default | False |
| left_mouse_action | Invert Time |
| middle_mouse_action | Do Nothing |
| right_mouse_action | Start Timer |
