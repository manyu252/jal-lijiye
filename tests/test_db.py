import os
import tempfile
from datetime import datetime, timedelta
from src.db import DatabaseManager

def test_db_init_and_log_drink():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = DatabaseManager(db_path)
        
        assert db.get_today_drink_count() == 0
        db.log_drink()
        assert db.get_today_drink_count() == 1
        db.log_drink()
        assert db.get_today_drink_count() == 2

def test_db_session_time_and_ratio():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = DatabaseManager(db_path)
        
        # Add 3600 seconds (1 hour) of active app time
        db.add_session_time(3600)
        assert db.get_today_active_hours() == 1.0
        
        # Log 2 drinks
        db.log_drink()
        db.log_drink()
        
        assert db.get_today_hydration_ratio() == 2.0

def test_db_summary_history():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = DatabaseManager(db_path)
        
        db.log_drink()
        db.add_session_time(1800)
        
        summary = db.get_daily_summary(7)
        assert len(summary) >= 1
        latest = summary[0]
        assert latest["drinks"] == 1
        assert latest["active_hours"] == 0.5

def test_db_recent_logs():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = DatabaseManager(db_path)
        
        id1 = db.log_drink(volume_ml=250)
        id2 = db.log_drink(volume_ml=300)
        
        logs = db.get_recent_logs(10)
        assert len(logs) == 2
        assert logs[0]["volume_ml"] == 300
        assert logs[1]["volume_ml"] == 250

def test_legacy_session_logs_migration():
    import sqlite3
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "legacy.db")
        # Manually create legacy table with date_str as PRIMARY KEY
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE session_logs (date_str TEXT PRIMARY KEY, active_seconds INTEGER)")
        cursor.execute("INSERT INTO session_logs VALUES ('2026-07-27', 1200)")
        conn.commit()
        conn.close()

        # Instantiate DatabaseManager (should trigger migration automatically)
        db = DatabaseManager(db_path)
        
        # Multiple users should now log session time for the same date without UNIQUE constraint error
        sec1 = db.add_session_time(60, user_name="Abhimanyu")
        sec2 = db.add_session_time(60, user_name="Shreya")
        assert sec1 > 0
        assert sec2 == 60
