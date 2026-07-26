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
                    volume_ml INTEGER DEFAULT 250
                )
            """)
            # Active application runtime session logs per day
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_logs (
                    date_str TEXT PRIMARY KEY,
                    active_seconds INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def log_drink(self, timestamp: Optional[datetime] = None, volume_ml: int = 250) -> int:
        """Records a water drink event."""
        if timestamp is None:
            timestamp = datetime.now()
            
        iso_str = timestamp.isoformat()
        date_str = timestamp.strftime("%Y-%m-%d")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO water_logs (timestamp, date_str, volume_ml) VALUES (?, ?, ?)",
                (iso_str, date_str, volume_ml)
            )
            conn.commit()
            return cursor.lastrowid

    def add_session_time(self, seconds: int, target_date: Optional[date] = None) -> int:
        """Accumulates active app session time in seconds for a date."""
        if target_date is None:
            target_date = date.today()
        date_str = target_date.strftime("%Y-%m-%d")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO session_logs (date_str, active_seconds)
                VALUES (?, ?)
                ON CONFLICT(date_str) DO UPDATE SET active_seconds = active_seconds + ?
                """,
                (date_str, seconds, seconds)
            )
            conn.commit()
            
            cursor.execute("SELECT active_seconds FROM session_logs WHERE date_str = ?", (date_str,))
            row = cursor.fetchone()
            return row["active_seconds"] if row else 0

    def get_today_drink_count(self) -> int:
        today_str = date.today().strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM water_logs WHERE date_str = ?", (today_str,))
            row = cursor.fetchone()
            return row["count"] if row else 0

    def get_today_active_hours(self) -> float:
        today_str = date.today().strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT active_seconds FROM session_logs WHERE date_str = ?", (today_str,))
            row = cursor.fetchone()
            seconds = row["active_seconds"] if row else 0
            return round(seconds / 3600.0, 2)

    def get_today_hydration_ratio(self) -> float:
        """Returns drinks per active hour."""
        drinks = self.get_today_drink_count()
        hours = self.get_today_active_hours()
        if hours < 0.05:
            # If less than 3 minutes of active time, return drink count directly as 1.0 multiplier ratio
            return float(drinks)
        return round(drinks / hours, 2)

    def get_daily_summary(self, limit_days: int = 7) -> List[Dict[str, Any]]:
        """Returns historical daily summaries of drinks, active hours, and ratio."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
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
                drinks = row["drinks"]
                secs = row["active_seconds"]
                hours = round(secs / 3600.0, 2)
                ratio = round(drinks / hours, 2) if hours >= 0.05 else float(drinks)
                result.append({
                    "date": date_str,
                    "drinks": drinks,
                    "active_hours": hours,
                    "hydration_ratio": ratio
                })
            return result

    def get_recent_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns recent individual drink entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, timestamp, volume_ml FROM water_logs ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            return [{"id": r["id"], "timestamp": r["timestamp"], "volume_ml": r["volume_ml"]} for r in rows]
