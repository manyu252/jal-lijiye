import os
import json
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "reminder_interval_minutes": 30,
    "snooze_duration_minutes": 10,
    "focus_mode": False,
    "asset_walk_gif": "assets/walk.gif",
    "asset_ask_gif": "assets/ask.gif",
    "asset_happy_gif": "assets/happy.gif",
    "asset_exit_gif": "assets/exit.gif",
    "asset_icon": "assets/icon.png",
}

class ConfigManager:
    def __init__(self, config_path: str = None) -> None:
        if config_path is None:
            config_dir = os.path.expanduser("~/.jal_lijiye")
            os.makedirs(config_dir, exist_ok=True)
            self.config_path = os.path.join(config_dir, "config.json")
        else:
            self.config_path = config_path
            
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        """Loads configuration from JSON file or initializes defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._config = {**DEFAULT_CONFIG, **loaded}
            except Exception as e:
                print(f"[ConfigManager] Error reading config, using defaults: {e}")
                self._config = DEFAULT_CONFIG.copy()
        else:
            self._config = DEFAULT_CONFIG.copy()
            self.save()
        return self._config

    def save(self) -> None:
        """Saves current configuration to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4)
        except Exception as e:
            print(f"[ConfigManager] Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value."""
        return self._config.get(key, default if default is not None else DEFAULT_CONFIG.get(key))

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration value and saves to disk."""
        self._config[key] = value
        self.save()

    def reset_defaults(self) -> None:
        """Resets configuration to default values."""
        self._config = DEFAULT_CONFIG.copy()
        self.save()
