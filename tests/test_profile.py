import os
import tempfile
import pytest
from src.config import ConfigManager
from src.db import DatabaseManager

def test_config_user_profiles():
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = ConfigManager(os.path.join(tmpdir, "config.json"))
        assert cfg.get_current_user() == "Default"
        
        cfg.set_current_user("Abhimanyu")
        assert cfg.get_current_user() == "Abhimanyu"
        
        # Test GIF resolution for user
        # Should fallback to assets/walk.gif if assets/abhimanyu_walk.gif does not exist
        walk_gif = cfg.get_user_gif("walk")
        assert walk_gif.endswith("walk.gif")

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
