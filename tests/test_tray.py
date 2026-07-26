import os
import tempfile
import pytest
from src.config import ConfigManager
from src.db import DatabaseManager
from src.tray import WaterBuddyTray
from src.stats_dialog import StatsDialog
from src.settings_dialog import SettingsDialog

def test_tray_initialization(qtbot):
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        db = DatabaseManager(os.path.join(tmpdir, "test.db"))
        tray = WaterBuddyTray(cfg, db)
        
        assert tray is not None
        assert tray.contextMenu() is not None

def test_stats_dialog(qtbot):
    with tempfile.TemporaryDirectory() as tmpdir:
        db = DatabaseManager(os.path.join(tmpdir, "test.db"))
        db.log_drink()
        dialog = StatsDialog(db)
        qtbot.addWidget(dialog)
        assert dialog.table.rowCount() >= 1

def test_settings_dialog(qtbot):
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        dialog = SettingsDialog(cfg)
        qtbot.addWidget(dialog)
        
        dialog.spin_interval.setValue(45)
        dialog._save_settings()
        assert cfg.get("reminder_interval_minutes") == 45
