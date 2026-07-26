# Implementation Plan: Jal Lijiye (macOS Drinking Water Buddy)

## Architectural Overview
The application consists of five core modular layers:
1. **Config Layer (`src/config.py`)**: Persistent JSON configuration for reminder intervals, snooze duration, focus mode state, and custom GIF asset paths.
2. **Database Layer (`src/db.py`)**: SQLite storage for tracking daily session active time, water intake timestamps, and calculating hydration ratios.
3. **Animated Overlay Layer (`src/overlay.py`)**: A transparent, frameless, always-on-top PyQt6 window positioned at the bottom of the screen. Controls animation state machine (`WALK_IN` -> `ASK` -> `HAPPY` -> `WALK_OUT`) and user action prompts ("Drink", "Snooze").
4. **Tray System Layer (`src/tray.py`)**: macOS Menu Bar app icon, context menu, timer loop scheduler, and dialog triggers.
5. **Dialog Windows (`src/stats_dialog.py`, `src/settings_dialog.py`)**: User interface for viewing hydration metrics and customizing GIF assets / timer intervals.

---

## Phase Breakdown & Order

### Phase 1: Core Setup & Asset Preparation
- Project directory structure & `requirements.txt`.
- Creation/generation of default pixel art GIF assets (`walk.gif`, `ask.gif`, `happy.gif`, `exit.gif`, `icon.png`).
- Configuration manager (`src/config.py`).

### Phase 2: Database & Statistics Subsystem
- SQLite schema design (`water_logs`, `session_logs`).
- Database manager (`src/db.py`) methods: `log_drink()`, `update_session_time()`, `get_daily_stats()`, `get_hydration_ratio()`.
- Unit tests (`tests/test_db.py`).

### Phase 3: Animated Overlay & Window State Machine
- PyQt6 transparent frameless overlay window (`src/overlay.py`).
- Screen bottom-edge geometry calculation (`QGuiApplication.primaryScreen().availableGeometry()`).
- Animation pipeline using `QMovie` for GIFs and `QPropertyAnimation` for horizontal/vertical slide-in/slide-out movement.
- Interactive prompt card overlaying character ("Did you drink water?", "Drink" button, "Snooze" button).

### Phase 4: Menu Bar (Tray) & Timer Scheduler
- macOS `QSystemTrayIcon` (`src/tray.py`) with custom icon.
- Background `QTimer` handling scheduled reminders, 10-minute snooze timers, and focus mode pausing.
- Instant "Test Reminder" trigger.

### Phase 5: Settings & Stats Dialogs
- Hydration Stats Dialog (`src/stats_dialog.py`) displaying summary metrics (Today's Drinks, Active Time, Hydration Ratio, History list).
- Settings Dialog (`src/settings_dialog.py`) allowing custom GIF selection, interval sliders, and reset to defaults.

### Phase 6: Bundling, Packaging & Documentation
- `main.py` entry point connecting all modules.
- `PyInstaller` `.spec` file configuration for macOS `.app` bundle creation.
- `README.md` with team setup & usage instructions.

---

## Risk & Mitigation Strategies
- **macOS Window Transparency & Floating Level**:
  - *Risk*: Frameless window might flicker or appear behind fullscreen app windows on macOS.
  - *Mitigation*: Use `Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool` and set `setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)`.
- **GIF Animation Scaling & Performance**:
  - *Risk*: High CPU usage from smooth GIF rendering on high-DPI Mac Retina displays.
  - *Mitigation*: Use `QMovie` with fixed bounding rects and smooth transformation scaling.

---

## Verification Checkpoints
- **Checkpoint 1**: Database unit tests pass cleanly (`pytest tests/test_db.py`).
- **Checkpoint 2**: Overlay window moves smoothly across screen bottom, renders GIFs, and reacts to button clicks without freezing.
- **Checkpoint 3**: Menu bar icon successfully schedules timers, pauses during focus mode, and opens stats/settings.
- **Checkpoint 4**: Standalone `.app` bundle builds cleanly via PyInstaller.
