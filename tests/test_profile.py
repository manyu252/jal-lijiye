import os
import tempfile
import pytest
from src.config import ConfigManager
from src.db import DatabaseManager

def test_config_user_profiles():
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        assert cfg.get_user_name() in ["Default", "Abhimanyu"]
        
        cfg.set_user_name("Shreya")
        assert cfg.get_user_name() == "Shreya"
        
        # Test GIF resolution for user-configured GIF
        walk_gif = cfg.get_user_gif("walk")
        assert walk_gif.endswith("walk.gif")
        
        exit_gif = cfg.get_user_gif("exit")
        assert exit_gif.endswith("exit.gif")

def test_db_multi_user_isolation():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = DatabaseManager(os.path.join(tmpdir, "test.db"))
        
        # Log drinks for User1 and User2
        db.log_drink(user_name="Abhimanyu")
        db.log_drink(user_name="Abhimanyu")
        db.log_drink(user_name="Friend")
        
        assert db.get_today_drink_count("Abhimanyu") == 2
        assert db.get_today_drink_count("Friend") == 1
        assert db.get_today_drink_count() == 3  # Total count across all users
