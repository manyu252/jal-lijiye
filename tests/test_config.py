import os
import tempfile
import pytest
from src.config import ConfigManager, DEFAULT_CONFIG

def test_config_defaults():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        cfg = ConfigManager(config_path)
        assert cfg.get("reminder_interval_minutes") == 30
        assert cfg.get("snooze_duration_minutes") == 10
        assert cfg.get("focus_mode") is False

def test_config_set_and_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        cfg = ConfigManager(config_path)
        cfg.set("reminder_interval_minutes", 45)
        cfg.set("focus_mode", True)
        
        # Reload from disk
        cfg2 = ConfigManager(config_path)
        assert cfg2.get("reminder_interval_minutes") == 45
        assert cfg2.get("focus_mode") is True

def test_config_reset_defaults():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        cfg = ConfigManager(config_path)
        cfg.set("reminder_interval_minutes", 90)
        cfg.reset_defaults()
        assert cfg.get("reminder_interval_minutes") == 30
