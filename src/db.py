import os
import sqlite3
from datetime import datetime, date
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            data_dir = os.path.expanduser("~/.jal_lijiye")
            os.makedirs(data_dir, exist_ok=True)
            self.db_path = os.path.join(data_dir, "hydration_tracker.db")
        else:
            self.db_path = db_path
            
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Water intake logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS water_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    date_str TEXT NOT NULL,
                    user_name TEXT DEFAULT 'Default',
                    volume_ml INTEGER DEFAULT 250
                )
            """)
            # Active application runtime session logs per day & user
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_logs (
                    user_date_key TEXT PRIMARY KEY,
                    user_name TEXT DEFAULT 'Default',
                    date_str TEXT NOT NULL,
                    active_seconds INTEGER DEFAULT 0
                )
            """)
            
            # Automatic schema migration for pre-existing SQLite databases
            cursor.execute("PRAGMA table_info(water_logs)")
            water_cols = [row["name"] for row in cursor.fetchall()]
            if "user_name" not in water_cols:
                cursor.execute("ALTER TABLE water_logs ADD COLUMN user_name TEXT DEFAULT 'Default'")
                
            cursor.execute("PRAGMA table_info(session_logs)")
            sess_cols = [row["name"] for row in cursor.fetchall()]
            if "user_name" not in sess_cols:
                cursor.execute("ALTER TABLE session_logs ADD COLUMN user_name TEXT DEFAULT 'Default'")
            if "user_date_key" not in sess_cols:
                cursor.execute("ALTER TABLE session_logs ADD COLUMN user_date_key TEXT")
                cursor.execute("UPDATE session_logs SET user_date_key = 'Default_' || date_str WHERE user_date_key IS NULL")

            conn.commit()

    def log_drink(self, user_name: str = "Default", timestamp: Optional[datetime] = None, volume_ml: int = 250) -> int:
        """Records a water drink event for a specific user."""
        if timestamp is None:
            timestamp = datetime.now()
            
        iso_str = timestamp.isoformat()
        date_str = timestamp.strftime("%Y-%m-%d")
        user = user_name.strip() if user_name else "Default"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO water_logs (timestamp, date_str, user_name, volume_ml) VALUES (?, ?, ?, ?)",
                (iso_str, date_str, user, volume_ml)
            )
            conn.commit()
            return cursor.lastrowid

    def add_session_time(self, seconds: int, user_name: str = "Default", target_date: Optional[date] = None) -> int:
        """Accumulates active app session time in seconds for a date and user."""
        if target_date is None:
            target_date = date.today()
        date_str = target_date.strftime("%Y-%m-%d")
        user = user_name.strip() if user_name else "Default"
        user_date_key = f"{user}_{date_str}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO session_logs (user_date_key, user_name, date_str, active_seconds)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_date_key) DO UPDATE SET active_seconds = active_seconds + ?
                """,
                (user_date_key, user, date_str, seconds, seconds)
            )
            conn.commit()
            
            cursor.execute("SELECT active_seconds FROM session_logs WHERE user_date_key = ?", (user_date_key,))
            row = cursor.fetchone()
            return row["active_seconds"] if row else 0

    def get_today_drink_count(self, user_name: Optional[str] = None) -> int:
        today_str = date.today().strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_name:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM water_logs WHERE date_str = ? AND user_name = ?",
                    (today_str, user_name)
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM water_logs WHERE date_str = ?",
                    (today_str,)
                )
            row = cursor.fetchone()
            return row["count"] if row else 0

    def get_today_active_hours(self, user_name: Optional[str] = None) -> float:
        today_str = date.today().strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_name:
                user_date_key = f"{user_name}_{today_str}"
                cursor.execute("SELECT active_seconds FROM session_logs WHERE user_date_key = ?", (user_date_key,))
            else:
                cursor.execute("SELECT SUM(active_seconds) as active_seconds FROM session_logs WHERE date_str = ?", (today_str,))
            row = cursor.fetchone()
            seconds = (row["active_seconds"] or 0) if row else 0
            return round(seconds / 3600.0, 2)

    def get_today_hydration_ratio(self, user_name: Optional[str] = None) -> float:
        """Returns drinks per active hour."""
        drinks = self.get_today_drink_count(user_name)
        hours = self.get_today_active_hours(user_name)
        if hours < 0.05:
            return float(drinks)
        return round(drinks / hours, 2)

    def get_daily_summary(self, limit_days: int = 7, user_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns historical daily summaries of drinks, active hours, and ratio."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_name:
                cursor.execute("""
                    SELECT 
                        COALESCE(s.date_str, w.date_str) as date_str,
                        COALESCE(w.drink_count, 0) as drinks,
                        COALESCE(s.active_seconds, 0) as active_seconds
                    FROM session_logs s
                    FULL OUTER JOIN (
                        SELECT date_str, COUNT(*) as drink_count 
                        FROM water_logs 
                        WHERE user_name = ?
                        GROUP BY date_str
                    ) w ON s.date_str = w.date_str
                    WHERE s.user_name = ? OR w.date_str IS NOT NULL
                    ORDER BY date_str DESC
                    LIMIT ?
                """, (user_name, user_name, limit_days))
            else:
                cursor.execute("""
                    SELECT 
                        COALESCE(s.date_str, w.date_str) as date_str,
                        COALESCE(w.drink_count, 0) as drinks,
                        COALESCE(s.active_seconds, 0) as active_seconds
                    FROM session_logs s
                    FULL OUTER JOIN (
                        SELECT date_str, COUNT(*) as drink_count 
                        FROM water_logs 
                        GROUP BY date_str
                    ) w ON s.date_str = w.date_str
                    ORDER BY date_str DESC
                    LIMIT ?
                """, (limit_days,))
            
            rows = cursor.fetchall()
            result = []
            for row in rows:
                date_str = row["date_str"]
                drinks = row["drinks"] or 0
                secs = row["active_seconds"] or 0
                hours = round(secs / 3600.0, 2)
                ratio = round(drinks / hours, 2) if hours >= 0.05 else float(drinks)
                result.append({
                    "date": date_str,
                    "drinks": drinks,
                    "active_hours": hours,
                    "hydration_ratio": ratio
                })
            return result

    def get_recent_logs(self, limit: int = 20, user_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns recent individual drink entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_name:
                cursor.execute(
                    "SELECT id, timestamp, user_name, volume_ml FROM water_logs WHERE user_name = ? ORDER BY timestamp DESC LIMIT ?",
                    (user_name, limit)
                )
            else:
                cursor.execute(
                    "SELECT id, timestamp, user_name, volume_ml FROM water_logs ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
            rows = cursor.fetchall()
            return [{"id": r["id"], "timestamp": r["timestamp"], "user_name": r["user_name"], "volume_ml": r["volume_ml"]} for r in rows]
