# Specification: Jal Lijiye (macOS Drinking Water Buddy)

## Objective
**Jal Lijiye** (Indian context friendly: "Water, please!") is a lightweight, team-friendly macOS desktop app that helps users stay hydrated. A customizable animated pixel-art character walks onto the bottom of the screen with a glass, prompts the user to drink water, celebrates on confirmation, snoozes when deferred, and maintains local hydration statistics over time.

### User Stories
1. **As a macOS user**, I want an animated pixel character to walk onto the bottom of my screen at scheduled intervals so that I am gently and visually reminded to drink water.
2. **As a user**, I want to click "Drink" (triggering a celebration GIF) or "Snooze" (sending the character away for 10 minutes) so that my workflow is respected.
3. **As a team member**, I want to easily run the app or build a `.app` bundle, select my own custom animated character GIFs (walk, ask, happy, exit), and configure intervals via a clean macOS Menu Bar (tray) icon.
4. **As a user**, I want to track my hydration history (total app active time, water drink count, and hydration ratio per day) stored locally in SQLite without sending data to external servers.

---

## Assumptions
1. Target OS is macOS (macOS 12+ recommended for PyQt6 transparent window handling).
2. Python 3.9+ environment with `PyQt6` and standard `sqlite3` libraries installed.
3. Character animations are provided as animated `.gif` files (with transparent backgrounds recommended) for four states: `walk.gif`, `ask.gif`, `happy.gif`, `exit.gif`.
4. Default placeholder pixel-art assets will be generated/provided so the app works immediately out of the box.

---

## Tech Stack
- **Language**: Python 3.9+
- **GUI Framework**: PyQt6 (`QApplication`, `QMainWindow`, `QSystemTrayIcon`, `QMovie`, `QPropertyAnimation`, `QGraphicsOpacityEffect`)
- **Database**: SQLite3 (built-in Python standard library `sqlite3`)
- **Packaging / Bundling**: PyInstaller (for generating standalone macOS `.app` bundle)
- **Testing**: `pytest`, `pytest-qt`

---

## Commands
```bash
# Environment Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run Application in Development
python3 main.py

# Run Tests
pytest

# Package into Standalone macOS App
pyinstaller JalLijiye.spec
```

---

## Project Structure
```
jal_lijiye/
├── assets/                  # Default pixel art GIF assets & icons
│   ├── icon.png             # Menu bar app icon
│   ├── walk.gif             # Character walking animation
│   ├── ask.gif              # Character holding glass asking question
│   ├── happy.gif            # Celebration animation
│   └── exit.gif             # Character walking away animation
├── src/
│   ├── __init__.py
│   ├── config.py            # App settings (intervals, asset paths, focus mode)
│   ├── db.py                # SQLite database manager (stats & logs)
│   ├── tray.py              # macOS Menu Bar tray icon & dropdown menu
│   ├── stats_dialog.py      # Hydration Stats & History dialog UI
│   ├── settings_dialog.py   # Settings & Custom GIF selector dialog UI
│   └── overlay.py           # Bottom-screen transparent animated overlay window
├── tests/
│   ├── test_db.py           # Unit tests for database metrics
│   ├── test_config.py       # Unit tests for config manager
│   └── test_overlay.py      # PyQt GUI component tests
├── docs/
│   └── spec.md              # Specification document
├── tasks/
│   ├── plan.md              # Implementation plan
│   └── todo.md              # Discrete task list
├── requirements.txt         # Python dependencies
├── main.py                  # Main entry point
└── README.md                # Installation and team distribution guide
```

---

## Code Style
- **PEP 8** standard Python code formatting.
- Type annotations on function signatures.
- Clean separation of concerns: GUI widgets (`overlay.py`, `tray.py`), data persistence (`db.py`), and configuration (`config.py`).

```python
# Example Code Style
from typing import Optional
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu

class WaterBuddyTray(QSystemTrayIcon):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._init_menu()

    def _init_menu(self) -> None:
        menu = QMenu()
        # Clean menu construction...
        self.setContextMenu(menu)
```

---

## Testing Strategy
- **Unit Tests (`pytest`)**:
  - Test SQLite database schema initialization, session time recording, drink logging, and hydration ratio calculation (`test_db.py`).
  - Test configuration saving/loading and default fallback values (`test_config.py`).
- **GUI Integration Tests (`pytest-qt`)**:
  - Test timer triggers, snooze 10-minute offset logic, and tray menu action handlers.

---

## Boundaries
- **Always do**:
  - Keep overlay windows frameless, transparent, always-on-top (`Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool`), positioned at the bottom of the active screen.
  - Automatically track session active time accurately even across app restarts.
  - Provide fallback default GIF assets if custom user GIFs are missing or corrupt.
- **Ask first**:
  - Adding external python packages beyond PyQt6, pytest, and PyInstaller.
  - Modifying SQLite database schema migrations.
- **Never do**:
  - Block the main Qt event loop with synchronous sleep calls (always use `QTimer`).
  - Transmit user activity or hydration data outside the local machine.
  - Allow overlay windows to obscure full screen without a clear dismiss option.

---

## Success Criteria
1. **Menu Bar Tray App**: Sits silently in macOS top menu bar with options for Settings, Hydration Stats, Pause (Focus Mode), Trigger Test Reminder, and Quit.
2. **Bottom Screen Animation**:
   - Character walks onto screen from edge to center-bottom playing `walk.gif`.
   - Switches to `ask.gif` with interactive "Drink" and "Snooze" buttons.
   - On "Drink": plays `happy.gif` celebration, records water entry in SQLite DB, then plays `exit.gif` walking off screen.
   - On "Snooze": plays `exit.gif` walking off screen, sets QTimer for 10 minutes.
3. **Hydration Stats Dialog**: Displays total active app hours, total water drinks logged, daily breakdown, and hydration efficiency ratio (drinks / active hour).
4. **Custom Assets & Configuration**: Users can select custom GIF paths for walk, ask, happy, and exit states, or revert to defaults.
5. **Team Distribution**: Includes clear installation instructions, `requirements.txt`, and PyInstaller build script for creating a macOS `.app` bundle.

---

## Open Questions
- None (All requirements clarified and confirmed during intent interview).
