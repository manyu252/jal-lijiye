import sys
from pathlib import Path
from typing import Optional
from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

from src.config import resolve_asset_path
from src.overlay import CharacterOverlayWindow
from src.stats_dialog import StatsDialog
from src.settings_dialog import SettingsDialog
from src.profile_dialog import ProfileDialog

class WaterBuddyTray(QSystemTrayIcon):
    def __init__(self, config_manager, db_manager, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.config = config_manager
        self.db = db_manager
        
        # Load tray icon via resolve_asset_path with OS-specific default icon
        is_windows = sys.platform == 'win32'
        default_icon = "assets/icon.ico" if is_windows else "assets/icon.png"
        icon_path = Path(resolve_asset_path(self.config.get("asset_icon", default_icon)))
        if icon_path.exists():
            self.setIcon(QIcon(str(icon_path)))
        else:
            self.setIcon(QIcon.fromTheme("system-help"))
            
        self.setToolTip("Jal Lijiye - Drinking Water Companion")
        
        # Instantiate overlay window
        self.overlay = CharacterOverlayWindow(self.config)
        self.overlay.drink_confirmed.connect(self._on_drink_confirmed)
        self.overlay.snooze_requested.connect(self._on_snooze_requested)
        
        # Timers
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.trigger_reminder)
        
        self.session_timer = QTimer(self)
        self.session_timer.timeout.connect(self._on_session_tick)
        self.session_timer.start(60000) # Every 60 seconds
        
        self._init_menu()
        self._update_reminder_timer()

    def _init_menu(self) -> None:
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #1a242b;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3498db;
            }
        """)

        # 1. Trigger Test Reminder
        act_test = QAction("Trigger Test Reminder", self)
        act_test.triggered.connect(self.trigger_reminder)
        menu.addAction(act_test)

        menu.addSeparator()

        # 2. Hydration Stats
        act_stats = QAction("Hydration Stats", self)
        act_stats.triggered.connect(self.show_stats_dialog)
        menu.addAction(act_stats)

        # 3. Focus Mode Toggle
        self.act_focus = QAction("Pause Reminders (Focus Mode)", self)
        self.act_focus.setCheckable(True)
        self.act_focus.setChecked(self.config.get("focus_mode", False))
        self.act_focus.toggled.connect(self._on_focus_toggled)
        menu.addAction(self.act_focus)

        # 4. Settings
        act_settings = QAction("Settings", self)
        act_settings.triggered.connect(self.show_settings_dialog)
        menu.addAction(act_settings)

        # 5. Profile / Switch User (placed below Settings)
        current_user = self.config.get_current_user()
        self.act_profile = QAction(f"Switch User ({current_user})", self)
        self.act_profile.triggered.connect(self.show_profile_dialog)
        menu.addAction(self.act_profile)

        menu.addSeparator()

        # 6. Quit
        act_quit = QAction("Quit Jal Lijiye", self)
        act_quit.triggered.connect(QApplication.instance().quit)
        menu.addAction(act_quit)

        self.setContextMenu(menu)

    def _update_reminder_timer(self) -> None:
        if self.config.get("focus_mode", False):
            self.reminder_timer.stop()
            return
            
        interval_ms = self.config.get("reminder_interval_minutes", 30) * 60 * 1000
        self.reminder_timer.start(interval_ms)

    def trigger_reminder(self) -> None:
        """Manually triggers character walk-in overlay."""
        try:
            self.overlay.show_reminder()
        except Exception as e:
            print(f"[WaterBuddyTray] Error in trigger_reminder: {e}")

    def _on_drink_confirmed(self) -> None:
        """Callback when user confirms drinking water."""
        try:
            user_name = self.config.get_current_user()
            self.db.log_drink(user_name=user_name)
            self._update_reminder_timer()
        except Exception as e:
            print(f"[WaterBuddyTray] Error logging drink: {e}")

    def _on_snooze_requested(self) -> None:
        """Callback when user clicks 'Snooze'."""
        try:
            snooze_ms = self.config.get("snooze_duration_minutes", 10) * 60 * 1000
            self.reminder_timer.start(snooze_ms)
        except Exception as e:
            print(f"[WaterBuddyTray] Error in snooze: {e}")

    def _on_focus_toggled(self, checked: bool) -> None:
        try:
            self.config.set("focus_mode", checked)
            self._update_reminder_timer()
        except Exception as e:
            print(f"[WaterBuddyTray] Error in focus toggled: {e}")

    def _on_session_tick(self) -> None:
        """Increments active laptop session time by 60 seconds in SQLite for active user."""
        try:
            user_name = self.config.get_current_user()
            self.db.add_session_time(60, user_name=user_name)
        except Exception as e:
            print(f"[WaterBuddyTray] Error in session tick: {e}")

    def show_profile_dialog(self) -> None:
        dialog = ProfileDialog(self.config)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        QApplication.setActiveWindow(dialog)
        if dialog.exec() == ProfileDialog.DialogCode.Accepted:
            current_user = self.config.get_current_user()
            self.act_profile.setText(f"Switch User ({current_user})")

    def show_stats_dialog(self) -> None:
        user_name = self.config.get_current_user()
        dialog = StatsDialog(self.db, user_name=user_name)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        QApplication.setActiveWindow(dialog)
        dialog.exec()

    def show_settings_dialog(self) -> None:
        dialog = SettingsDialog(self.config)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        QApplication.setActiveWindow(dialog)
        if dialog.exec() == SettingsDialog.DialogCode.Accepted:
            self._update_reminder_timer()
            current_user = self.config.get_current_user()
            self.act_profile.setText(f"Switch User ({current_user})")
