# Task List: Jal Lijiye (macOS Drinking Water Buddy)

## Tasks

- [x] **Task 1: Environment & Default Pixel Assets Setup**
  - Acceptance: Project directory structure initialized, `requirements.txt` created, and default pixel GIF assets (`walk.gif`, `ask.gif`, `happy.gif`, `exit.gif`, `icon.png`) placed in `assets/`.
  - Verify: Directory exists and assets load properly.
  - Files: `requirements.txt`, `assets/*`

- [x] **Task 2: Configuration Manager (`src/config.py`)**
  - Acceptance: Configuration manager reads/writes JSON settings (reminder interval, snooze duration, focus mode state, custom asset paths) with sensible defaults.
  - Verify: Run `pytest tests/test_config.py`.
  - Files: `src/config.py`, `tests/test_config.py`

- [x] **Task 3: Database & Hydration Tracker Subsystem (`src/db.py`)**
  - Acceptance: SQLite database initializes tables, logs drinks, updates app session active time, and calculates hydration ratios.
  - Verify: Run `pytest tests/test_db.py`.
  - Files: `src/db.py`, `tests/test_db.py`

- [x] **Task 4: Transparent Animated Character Overlay Window (`src/overlay.py`)**
  - Acceptance: Frameless transparent always-on-top window positions itself at the bottom of the screen. Plays character walk-in animation, displays "Did you drink water?" prompt with "Drink" & "Snooze" buttons, plays happy celebration GIF on "Drink", and exits smoothly on completion or snooze.
  - Verify: Visual test of overlay animation state machine.
  - Files: `src/overlay.py`

- [x] **Task 5: macOS Menu Bar (Tray) & Reminder Scheduler (`src/tray.py`)**
  - Acceptance: Menu bar tray icon displays dropdown menu (Trigger Test, Pause/Focus Mode, Settings, Hydration Stats, Quit) and manages timer intervals and 10-minute snooze triggers.
  - Verify: Tray icon appears, menu clicks trigger overlay and toggle timers.
  - Files: `src/tray.py`

- [x] **Task 6: Hydration Stats & Settings Dialog UIs (`src/stats_dialog.py`, `src/settings_dialog.py`)**
  - Acceptance: Stats dialog displays daily drink counts, active hours, hydration ratio, and historical logs. Settings dialog allows configuring reminder frequency, snooze duration, and custom GIF asset paths.
  - Verify: Open dialogs from tray menu and verify interactions.
  - Files: `src/stats_dialog.py`, `src/settings_dialog.py`

- [x] **Task 7: Main Entry Point & Integration (`main.py`)**
  - Acceptance: `main.py` wires configuration, database, tray, overlay, and timers into a cohesive application lifecycle.
  - Verify: Launch app via `python3 main.py`, test full reminder flow and stats recording.
  - Files: `main.py`

- [x] **Task 8: Standalone Packaging & Documentation**
  - Acceptance: `JalLijiye.spec` for PyInstaller created and tested; `README.md` updated with team installation & customization instructions.
  - Verify: App bundle builds cleanly via PyInstaller or runs via single command script.
  - Files: `JalLijiye.spec`, `README.md`, `run.sh`
